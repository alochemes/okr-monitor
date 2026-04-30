"""Generate an OKR Health Check from a customer's intake YAML.

Operator-triggered (Stage 0) — this is the lead-magnet artifact promised on
the landing page CTA. Run after a prospect submits the pilot intake
questionnaire; review output before sending.

Usage:
  python scripts/run_okr_health_check.py --intake data/health_checks/example_acme/intake.yaml
  OKR_MONITOR_DRY_RUN=false python scripts/run_okr_health_check.py --intake <path>

Output:
  data/health_checks/<slug>/HEALTH_CHECK.md   (operator-reviewable brief)
  data/health_checks/<slug>/HEALTH_CHECK.json (structured for downstream tooling)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass

from agents import _base  # noqa: E402
from core import audit, config, llm, store  # noqa: E402

_AGENT = "onboarding"
_KIND = "okr_health_check"
_PROMPT = (ROOT / "agents" / "onboarding" / "prompts" / "okr_health_check.md").read_text(encoding="utf-8")


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "unnamed"


def _user_message(intake: dict[str, Any]) -> str:
    today = date.today().isoformat()
    return (
        f"Today is {today}.\n\n"
        f"## Customer intake (verbatim)\n\n"
        f"```yaml\n{yaml.safe_dump(intake, sort_keys=False, allow_unicode=True)}```\n\n"
        "Generate the OKR Health Check. Reply with ONLY the JSON object specified in the schema."
    )


def _format_md(parsed: dict[str, Any], intake: dict[str, Any], raw_text: str) -> str:
    if not parsed:
        return f"_(model output did not parse as JSON; raw below)_\n\n```\n{raw_text}\n```"

    company = (intake.get("company") or {}).get("name", "Customer")
    today = date.today().isoformat()

    lines: list[str] = [
        f"# OKR Health Check — {company}",
        "",
        f"_Prepared {today} by OKR Monitor for review at pilot kickoff._",
        "",
        "## 01 / Verdict",
        "",
        parsed.get("verdict_summary", "").strip() or "_(no verdict produced)_",
        "",
    ]

    fvm = parsed.get("first_value_moment_for_this_pilot")
    if fvm:
        lines.extend([
            "**First-value moment we'll engineer for this pilot:** " + fvm.strip(),
            "",
        ])

    # KR review
    kr_rows = parsed.get("kr_review") or []
    if kr_rows:
        lines.append("## 02 / KR review")
        lines.append("")
        for r in kr_rows:
            score = (r.get("score") or "?").lower()
            badge = {"pass": "🟢 PASS", "needs_cleanup": "🟡 CLEANUP", "rewrite": "🔴 REWRITE"}.get(
                score, score.upper()
            )
            lines.append(f"### {badge} — `{r.get('kr_id', '?')}`")
            lines.append(f"_As written:_ {r.get('kr_text_as_written', '')}")
            for v in r.get("rule_violations") or []:
                lines.append(f"- ✗ {v}")
            if (rw := r.get("proposed_rewrite")):
                lines.append("")
                lines.append(f"**Proposed rewrite:** `{rw}`")
            lines.append("")

    # Sample brief
    if (sb := parsed.get("sample_friday_brief_markdown")):
        lines.append("## 03 / Sample Friday brief — populated against your recent work")
        lines.append("")
        lines.append("> _The cell below is a styled mockup of what your Friday brief would look like, generated against the work summary you provided. The first real brief will be richer because the OKR-Mapper will have seen 30 days of commits + tickets + threads._")
        lines.append("")
        lines.append(sb.strip())
        lines.append("")

    # Cleanup actions
    cleanups = parsed.get("cleanup_actions") or []
    if cleanups:
        lines.append("## 04 / Cleanup actions before pilot day 7")
        lines.append("")
        lines.append("| # | Action | Owner | Deadline |")
        lines.append("|---|---|---|---|")
        for c in cleanups:
            lines.append(
                f"| {c.get('priority', '?')} | {c.get('action', '')} | "
                f"{c.get('owner', '?')} | {c.get('deadline', '?')} |"
            )
        lines.append("")

    # Kickoff agenda
    agenda = parsed.get("kickoff_agenda_45min") or []
    if agenda:
        lines.append("## 05 / Customized kickoff agenda (45 min)")
        lines.append("")
        for slot in agenda:
            decision = slot.get("decision_point")
            decision_s = f" — **decision:** {decision}" if decision else ""
            lines.append(
                f"- `{slot.get('window', '?')}` — {slot.get('topic', '?')}{decision_s}"
            )
        lines.append("")

    # Operator notes
    if (notes := parsed.get("operator_notes")):
        lines.append("## 06 / Notes for the operator (do not send to customer)")
        lines.append("")
        lines.append(notes.strip())
        lines.append("")

    if (conf := parsed.get("confidence")) is not None:
        lines.append(f"_Confidence: {conf:.2f}_")
    if (reason := parsed.get("reasoning")):
        lines.append(f"_Reasoning: {reason}_")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True, help="Path to intake.yaml")
    parser.add_argument("--out-dir", default=None, help="Override output directory.")
    args = parser.parse_args()

    intake_path = Path(args.intake).resolve()
    if not intake_path.exists():
        print(f"Error: intake file not found: {intake_path}", file=sys.stderr)
        return 1

    with intake_path.open("r", encoding="utf-8") as f:
        intake = yaml.safe_load(f) or {}

    company_name = (intake.get("company") or {}).get("name", "unknown")
    out_dir = Path(args.out_dir) if args.out_dir else (intake_path.parent)
    out_dir.mkdir(parents=True, exist_ok=True)

    store.init_db()
    run_id = store.start_run(agent=_AGENT, kind=_KIND)
    cfg = config.agent(_AGENT)

    try:
        _base.snapshot_tracker(run_id=run_id, agent=_AGENT)
        result = llm.complete(
            system=_base.build_system_prompt(agent_prompt_md=_PROMPT),
            user=_user_message(intake),
            model=cfg.get("model", "claude-sonnet-4-6"),
            max_tokens=4096,
            temperature=0.35,
            run_id=run_id, agent=_AGENT, action=f"{_AGENT}.{_KIND}",
        )
        parsed = result.parse_json()
        body_md = _format_md(parsed, intake, result.text)

        md_path = out_dir / "HEALTH_CHECK.md"
        md_path.write_text(body_md, encoding="utf-8")

        json_path = out_dir / "HEALTH_CHECK.json"
        json_path.write_text(
            json.dumps(
                {
                    "company": company_name,
                    "generated_at": date.today().isoformat(),
                    "run_id": run_id,
                    "model": result.model,
                    "cost_usd": result.cost_usd,
                    "parsed": parsed,
                },
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

        # Also store as a regular proposal so it shows in the operator queue.
        pid = store.write_proposal(
            run_id=run_id, agent=_AGENT, kind=_KIND,
            title=parsed.get("title") or f"OKR Health Check — {company_name}",
            summary=parsed.get("verdict_summary") or result.text[:300],
            body_md=body_md,
            evidence={"intake_path": str(intake_path), "raw_parsed": parsed},
            confidence=parsed.get("confidence"),
            model=result.model,
            tokens_in=result.tokens_in,
            tokens_out=result.tokens_out,
            cost_usd=result.cost_usd,
        )

        audit.emit(
            run_id=run_id, agent=_AGENT, action=f"{_KIND}.complete",
            subject_type="proposal", subject_id=pid,
            payload={
                "company": company_name,
                "intake_path": str(intake_path.relative_to(ROOT)).replace("\\", "/"),
                "md_path": str(md_path.relative_to(ROOT)).replace("\\", "/"),
            },
        )
        store.end_run(run_id, status="ok", stats={"company": company_name, "proposal_id": pid})

        print(json.dumps({
            "company": company_name,
            "md_path": str(md_path.relative_to(ROOT)).replace("\\", "/"),
            "json_path": str(json_path.relative_to(ROOT)).replace("\\", "/"),
            "proposal_id": pid,
            "cost_usd": result.cost_usd,
            "tokens_in": result.tokens_in,
            "tokens_out": result.tokens_out,
            "parsed_ok": bool(parsed),
        }, indent=2, default=str))
        return 0

    except Exception as exc:
        store.end_run(run_id, status="error", stats={}, error=str(exc))
        audit.emit(run_id=run_id, agent=_AGENT, action=f"{_KIND}.exception",
                   severity="error", payload={"error": str(exc)})
        print(f"Failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
