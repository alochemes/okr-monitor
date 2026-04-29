"""Narrative pipeline. One run = one weekly_narrative covering [start, end].

Default window is the trailing 7 days ending today. Operator can override
for backfill or to generate ad-hoc summaries (e.g. for a board prep)."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from agents import _base
from core import audit, config, llm, store


_AGENT = "narrative"
_KIND = "weekly_narrative"
_PROMPT = (Path(__file__).parent / "prompts" / "weekly_narrative.md").read_text(encoding="utf-8")


def _format_mappings_for_user(mappings: list[dict[str, Any]]) -> str:
    """Group mappings by KR and produce a compact text block for the user
    message. Keeping this small matters for cost; the system block carries
    the company identity + TRACKER.md."""
    by_kr: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for m in mappings:
        by_kr[str(m["kr_id"])].append(m)

    lines: list[str] = []
    for kr_id in sorted(by_kr.keys()):
        rows = by_kr[kr_id]
        lines.append(f"### KR {kr_id} — {len(rows)} mapped event(s)")
        for r in rows:
            lines.append(
                f"- [{r['source']}/{r.get('kind') or 'unknown'} by "
                f"{r.get('actor') or '?'} @ {r['occurred_at'][:10]}] "
                f"\"{r['title']}\"  "
                f"(conf {r['confidence']:.2f}; {r.get('reasoning') or 'no reasoning'})"
            )
        lines.append("")

    return "\n".join(lines) if lines else "(no mapped events in this window)"


def _user_message(period_start: date, period_end: date, mappings: list[dict[str, Any]]) -> str:
    return (
        f"Generate the weekly narrative for {period_start.isoformat()} → {period_end.isoformat()}.\n\n"
        f"Total mapped events this period: {len(mappings)}.\n"
        f"Distinct KRs touched: {len({str(m['kr_id']) for m in mappings})}.\n\n"
        "Mappings (grouped by KR):\n\n"
        f"{_format_mappings_for_user(mappings)}\n\n"
        "Reply with ONLY the JSON object specified in the schema."
    )


def _format_body_md(parsed: dict[str, Any], raw_text: str,
                    period_start: date, period_end: date,
                    events_count: int) -> str:
    if not parsed:
        return f"_(model output did not parse as JSON; raw below)_\n\n```\n{raw_text}\n```"
    lines = [
        f"# {parsed.get('title', '(no title)')}",
        "",
        f"_Period: {period_start.isoformat()} → {period_end.isoformat()} · "
        f"{events_count} mapped event(s)_",
        "",
        "## Verdict",
        parsed.get("verdict_summary", "").strip(),
        "",
    ]
    verdicts = parsed.get("kr_verdicts") or []
    if verdicts:
        lines.append("## KR-by-KR")
        for v in verdicts:
            verdict_label = {
                "on_track": "🟢 On track",
                "drifting": "🟡 Drifting",
                "off": "🔴 Off",
            }.get(v.get("verdict", ""), v.get("verdict", "?"))
            lines.append(
                f"### KR {v.get('kr_id', '?')} — **{verdict_label}**  "
                f"_({v.get('events_count', 0)} events)_"
            )
            lines.append(v.get("narrative", "").strip())
            lines.append("")
    align_pct = parsed.get("alignment_score_pct")
    if align_pct is not None:
        lines.append(f"## Attention alignment: **{align_pct}%**")
        if parsed.get("alignment_commentary"):
            lines.append(parsed["alignment_commentary"])
        lines.append("")
    if parsed.get("what_to_do_next_week"):
        lines.append("## What to do next week")
        lines.append(parsed["what_to_do_next_week"])
        lines.append("")
    if (conf := parsed.get("confidence")) is not None:
        lines.append(f"_Confidence: {conf:.2f}_")
    if parsed.get("reasoning"):
        lines.append(f"_Reasoning: {parsed['reasoning']}_")
    return "\n".join(lines)


def run(*, period_end: date | None = None, period_days: int = 7) -> dict[str, Any]:
    period_end = period_end or date.today()
    period_start = period_end - timedelta(days=period_days - 1)
    store.init_db()
    run_id = store.start_run(agent=_AGENT, kind=_KIND)
    cfg = config.agent(_AGENT)
    stats: dict[str, Any] = {
        "run_id": run_id,
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
    }

    try:
        _base.snapshot_tracker(run_id=run_id, agent=_AGENT)

        # Window is inclusive on both ends; broaden to UTC-day boundaries.
        start_iso = f"{period_start.isoformat()}T00:00:00+00:00"
        end_iso = f"{period_end.isoformat()}T23:59:59.999999+00:00"
        mapping_rows = store.list_mappings_in_window(start_iso=start_iso, end_iso=end_iso)
        mappings = [dict(r) for r in mapping_rows]
        stats["mappings_in_window"] = len(mappings)
        stats["distinct_krs_touched"] = len({str(m["kr_id"]) for m in mappings})

        result = llm.complete(
            system=_base.build_system_prompt(agent_prompt_md=_PROMPT),
            user=_user_message(period_start, period_end, mappings),
            model=cfg["model"],
            max_tokens=cfg.get("max_tokens", 3072),
            temperature=cfg.get("temperature", 0.5),
            run_id=run_id, agent=_AGENT, action=f"{_AGENT}.{_KIND}",
        )
        parsed = result.parse_json()

        title = parsed.get("title") or f"Weekly narrative — {period_end.isoformat()}"
        body_md = _format_body_md(
            parsed, result.text, period_start, period_end, len(mappings),
        )
        evidence = {
            "mappings_count": len(mappings),
            "distinct_krs_touched": stats["distinct_krs_touched"],
            "alignment_score_pct": parsed.get("alignment_score_pct"),
            "raw_parsed": parsed,
        }

        nid = store.write_narrative(
            run_id=run_id,
            period_start=period_start.isoformat(),
            period_end=period_end.isoformat(),
            title=title, body_md=body_md, evidence=evidence,
            model=result.model, tokens_in=result.tokens_in,
            tokens_out=result.tokens_out, cost_usd=result.cost_usd,
        )

        stats.update({
            "narrative_id": nid, "title": title,
            "cost_usd": result.cost_usd,
            "tokens_in": result.tokens_in, "tokens_out": result.tokens_out,
            "cache_read_tokens": result.cache_read_tokens,
            "parsed_ok": bool(parsed),
        })
        audit.emit(
            run_id=run_id, agent=_AGENT, action=f"{_KIND}.written",
            subject_type="narrative", subject_id=nid,
            payload={"title": title, "events_count": len(mappings)},
        )
        store.end_run(run_id, status="ok", stats=stats)
        return stats

    except Exception as exc:
        store.end_run(run_id, status="error", stats=stats, error=str(exc))
        audit.emit(run_id=run_id, agent=_AGENT, action=f"{_KIND}.exception",
                   severity="error", payload={"error": str(exc)})
        raise
