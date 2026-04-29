"""Sunday-evening planning pass: run the strategy pod, then write each proposal
as a markdown file under `proposals/YYYY-MM-DD/` plus a one-page MONDAY_BRIEF.md
summary the operator (or a remote routine) reads first thing Monday.

This wrapper is **git-agnostic**. It only writes files. The caller (local cron,
the remote Sunday routine, or the operator running it by hand) is responsible
for committing and pushing.

Behavior on missing API key
---------------------------
If `ANTHROPIC_API_KEY` is empty AND `OKR_MONITOR_DRY_RUN` is unset, this script
flips dry-run on for the duration of this run and adds a clear banner to
MONDAY_BRIEF.md so the operator can see at a glance that the proposals are
stubs. This makes the wrapper safe to run in environments (like a remote
sandbox) where the secret may not be available — it never silently bills 0
calls and it never crashes for a missing key.

Usage
-----
  python scripts/sunday_evening.py
  python scripts/sunday_evening.py --date 2026-05-03   # backfill / dry runs
  OKR_MONITOR_DRY_RUN=true python scripts/sunday_evening.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass

from agents.ceo import pipeline as ceo_pipe  # noqa: E402
from agents.cpo import pipeline as cpo_pipe  # noqa: E402
from agents.cto import pipeline as cto_pipe  # noqa: E402
from agents.cfo import pipeline as cfo_pipe  # noqa: E402
from agents.okr_mapper import pipeline as mapper_pipe  # noqa: E402
from agents.narrative import pipeline as narrative_pipe  # noqa: E402
from agents.signals_analyst import pipeline as signals_pipe  # noqa: E402
from agents.forecasting import pipeline as forecasting_pipe  # noqa: E402
from core import dogfood, store  # noqa: E402


_AGENTS = [
    ("ceo", ceo_pipe),
    ("cpo", cpo_pipe),
    ("cto", cto_pipe),
    ("cfo", cfo_pipe),
]


def _force_dry_run_if_no_key() -> bool:
    """Returns True iff this run forced dry-run because no API key was
    available. Caller uses this to add a banner to the brief."""
    if os.environ.get("OKR_MONITOR_DRY_RUN", "").lower() in ("true", "false"):
        return False
    if os.environ.get("ANTHROPIC_API_KEY"):
        return False
    os.environ["OKR_MONITOR_DRY_RUN"] = "true"
    return True


def _run_pod(today: date) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for name, mod in _AGENTS:
        try:
            stats = mod.run(today=today)
            results.append({"agent": name, "ok": True, "stats": stats})
        except Exception as exc:
            results.append({
                "agent": name, "ok": False,
                "error": str(exc), "trace": traceback.format_exc(),
            })
    return results


def _fetch_proposal_for_run(run_id: str) -> dict[str, Any] | None:
    with store.connect() as conn:
        row = conn.execute(
            "SELECT id, agent, kind, title, summary, body_md, confidence, model"
            " FROM proposals WHERE run_id = ? ORDER BY created_at DESC LIMIT 1",
            (run_id,),
        ).fetchone()
    return dict(row) if row else None


def _write_proposal_files(out_dir: Path, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """For each successful agent, fetch its proposal from the DB and write
    `<agent>_<kind>.md`. Returns the list of {row, path} dicts in the order
    agents ran."""
    written: list[dict[str, Any]] = []
    for r in results:
        if not r.get("ok"):
            continue
        run_id = r["stats"].get("run_id")
        if not run_id:
            continue
        row = _fetch_proposal_for_run(run_id)
        if not row:
            continue
        path = out_dir / f"{row['agent']}_{row['kind']}.md"
        path.write_text(row["body_md"], encoding="utf-8")
        written.append({"row": row, "path": path})
    return written


def _run_dogfood_loop(
    *, today: date, results: list[dict[str, Any]],
) -> dict[str, Any]:
    """After the strategy pod runs, ingest each new proposal as a work_event,
    map every unmapped event to KRs, and generate the weekly company
    narrative. Returns a summary dict so the brief can mention it."""
    out: dict[str, Any] = {
        "ingested_events": 0, "ingested_new": 0,
        "mapper_run_id": None, "mapper_events_processed": 0,
        "mapper_mappings_written": 0, "mapper_cost_usd": 0.0,
        "narrative_id": None, "narrative_title": None,
        "narrative_cost_usd": 0.0, "narrative_mappings_in_window": 0,
        "errors": [],
    }

    # 1. Ingest fresh proposals as work_events (idempotent on proposal_id).
    try:
        ingested = dogfood.ingest_recent_proposals(limit=20)
        out["ingested_events"] = len(ingested)
        out["ingested_new"] = sum(1 for r in ingested if r["was_new"])
    except Exception as exc:
        out["errors"].append({"step": "ingest", "error": str(exc)})
        return out

    # 2. Sweep all unmapped events through the OKR-Mapper.
    try:
        mapper_stats = mapper_pipe.run_all_unmapped(limit=100)
        out["mapper_run_id"] = mapper_stats.get("run_id")
        out["mapper_events_processed"] = mapper_stats.get("events_processed", 0)
        out["mapper_mappings_written"] = mapper_stats.get("mappings_written", 0)
        out["mapper_cost_usd"] = mapper_stats.get("total_cost_usd", 0.0) or 0.0
    except Exception as exc:
        out["errors"].append({"step": "okr_mapper", "error": str(exc)})

    # 2a. Compute kr_signals (counts) — pure compute, no LLM cost.
    try:
        sig_stats = signals_pipe.run()
        out["signals_krs_processed"] = sig_stats.get("krs_processed", 0)
    except Exception as exc:
        out["errors"].append({"step": "signals_analyst", "error": str(exc)})

    # 2b. Forecast verdicts — pure compute, no LLM cost.
    try:
        fc_stats = forecasting_pipe.run(today=today)
        out["forecast_by_verdict"] = fc_stats.get("by_verdict", {})
    except Exception as exc:
        out["errors"].append({"step": "forecasting", "error": str(exc)})

    # 3. Generate weekly narrative covering trailing 7 days ending today.
    try:
        narr_stats = narrative_pipe.run(period_end=today, period_days=7)
        out["narrative_id"] = narr_stats.get("narrative_id")
        out["narrative_title"] = narr_stats.get("title")
        out["narrative_cost_usd"] = narr_stats.get("cost_usd", 0.0) or 0.0
        out["narrative_mappings_in_window"] = narr_stats.get("mappings_in_window", 0)
    except Exception as exc:
        out["errors"].append({"step": "narrative", "error": str(exc)})

    return out


def _write_narrative_file(out_dir: Path, narrative_id: str | None) -> Path | None:
    """Pull the narrative we just wrote out of the DB and dump it as a
    standalone markdown file alongside the proposals, so a reader of the
    proposals/ directory has the whole package together."""
    if not narrative_id:
        return None
    with store.connect() as conn:
        row = conn.execute(
            "SELECT title, body_md FROM narratives WHERE id = ?", (narrative_id,),
        ).fetchone()
    if not row:
        return None
    path = out_dir / "weekly_narrative.md"
    path.write_text(row["body_md"], encoding="utf-8")
    return path


def _build_monday_brief(
    *,
    today: date,
    written: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    forced_dry_run: bool,
    dogfood_summary: dict[str, Any] | None = None,
    narrative_path: Path | None = None,
) -> str:
    lines: list[str] = [
        f"# Monday Brief — week starting {today.isoformat()}",
        "",
        f"_Generated by the strategy pod on {today.isoformat()}._",
        "",
    ]
    if forced_dry_run:
        lines.extend([
            "> ⚠️ **Dry-run mode** — `ANTHROPIC_API_KEY` was not available in this environment.",
            "> The proposals below are stubs from `core/llm._default_mock()`, not real model output.",
            "> Surface this to the routine config so the next Sunday brief is real.",
            "",
        ])
    lines.extend([
        f"**{len(written)} proposal(s)** are in the queue. "
        f"Review locally with: `python -m cli.review --all`.",
        "",
        "## This week's proposals",
        "",
    ])
    for item in written:
        row, path = item["row"], item["path"]
        conf = row["confidence"]
        conf_s = f"{conf:.2f}" if conf is not None else "—"
        rel = path.relative_to(ROOT).as_posix()
        lines.append(f"### {row['agent'].upper()} · {row['kind']}  ·  confidence {conf_s}")
        lines.append(f"**{row['title']}**")
        lines.append("")
        lines.append((row["summary"] or "").strip())
        lines.append("")
        lines.append(f"_Full proposal:_ [`{rel}`](../{path.parent.name}/{path.name})")
        lines.append("")

    if failures:
        lines.append("## Agents that failed this run")
        lines.append("")
        for f in failures:
            lines.append(f"- **{f['agent']}**: `{f.get('error', 'unknown error')}`")
        lines.append("")
        lines.append("_See `data/audit/<today>.jsonl` for full traces._")
        lines.append("")

    if dogfood_summary:
        d = dogfood_summary
        lines.append("## Dogfood loop")
        lines.append(
            f"- Ingested **{d.get('ingested_new', 0)} new** proposals as work_events "
            f"(of {d.get('ingested_events', 0)} considered)."
        )
        lines.append(
            f"- OKR-Mapper processed **{d.get('mapper_events_processed', 0)} events**, "
            f"wrote **{d.get('mapper_mappings_written', 0)} mappings** "
            f"(cost ${d.get('mapper_cost_usd', 0.0):.4f})."
        )
        if d.get("signals_krs_processed") is not None:
            verdicts = d.get("forecast_by_verdict") or {}
            verdicts_s = ", ".join(f"{k}={v}" for k, v in sorted(verdicts.items())) or "—"
            lines.append(
                f"- KR signals + forecast: **{d['signals_krs_processed']} KRs** processed. "
                f"Verdicts: {verdicts_s}."
            )
        if narrative_path is not None:
            lines.append(
                f"- Weekly narrative: `{narrative_path.name}` covering "
                f"{d.get('narrative_mappings_in_window', 0)} mapped event(s) "
                f"(cost ${d.get('narrative_cost_usd', 0.0):.4f})."
            )
            lines.append(
                f"  → [`weekly_narrative.md`](./{narrative_path.name})"
            )
        elif d.get("narrative_title"):
            lines.append(f"- Weekly narrative: \"{d['narrative_title']}\"")
        for err in d.get("errors", []):
            lines.append(f"- ⚠️ Dogfood step `{err['step']}` failed: `{err['error']}`")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## What to do Monday morning",
        "",
        "1. `python -m cli.review --all` — walk the queue, decide on each proposal.",
        "2. Update `TRACKER.md` §6 (Sprint Log) and §7 (Decision Log) with anything you accept.",
        "3. If any proposal called for a TRACKER.md change, edit and commit.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        type=date.fromisoformat,
        default=None,
        help="Override 'today' for backfill or testing. ISO format YYYY-MM-DD.",
    )
    args = parser.parse_args()
    today = args.date or date.today()

    forced_dry_run = _force_dry_run_if_no_key()

    out_dir = ROOT / "proposals" / today.isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)

    store.init_db()
    results = _run_pod(today)
    written = _write_proposal_files(out_dir, results)
    failures = [r for r in results if not r.get("ok")]

    # Run the dogfood loop AFTER the pod so it sees today's fresh proposals.
    dogfood_summary = _run_dogfood_loop(today=today, results=results)
    narrative_path = _write_narrative_file(out_dir, dogfood_summary.get("narrative_id"))

    brief_md = _build_monday_brief(
        today=today, written=written, failures=failures,
        forced_dry_run=forced_dry_run,
        dogfood_summary=dogfood_summary,
        narrative_path=narrative_path,
    )
    brief_path = out_dir / "MONDAY_BRIEF.md"
    brief_path.write_text(brief_md, encoding="utf-8")

    summary = {
        "today": today.isoformat(),
        "out_dir": out_dir.relative_to(ROOT).as_posix(),
        "brief_path": brief_path.relative_to(ROOT).as_posix(),
        "proposals_written": [
            {"agent": w["row"]["agent"],
             "kind": w["row"]["kind"],
             "path": w["path"].relative_to(ROOT).as_posix(),
             "confidence": w["row"]["confidence"]}
            for w in written
        ],
        "dogfood": dogfood_summary,
        "narrative_path": narrative_path.relative_to(ROOT).as_posix() if narrative_path else None,
        "failures": [{"agent": f["agent"], "error": f.get("error")} for f in failures],
        "forced_dry_run": forced_dry_run,
    }
    print(json.dumps(summary, indent=2, default=str))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
