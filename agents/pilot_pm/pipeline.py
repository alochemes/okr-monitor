"""Pilot-PM pipeline. One run = one pilot_milestone_review proposal."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import run_proposal

_AGENT = "pilot_pm"
_KIND = "pilot_milestone_review"
_PROMPT = (Path(__file__).parent / "prompts" / "pilot_milestone_review.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "No pilot list yet (we have 0 pilots — first design partners targeted by 2026-05-19). "
        "Draft a TEMPLATE review for an empty pilot list, defining the verdict criteria the agent "
        "will apply each week once pilots exist. Reply with ONLY the JSON object specified."
    )


def _format_body_md(parsed: dict[str, Any], raw_text: str) -> str:
    if not parsed:
        return f"_(unparsed)_\n\n```\n{raw_text}\n```"
    lines = [f"# {parsed.get('title', '(no title)')}", "",
             parsed.get("summary", "").strip(), ""]
    for label, key in [("On track", "pilots_on_track"),
                       ("At risk", "pilots_at_risk"),
                       ("Dormant", "pilots_dormant"),
                       ("Converting", "pilots_converting")]:
        items = parsed.get(key) or []
        if not items:
            continue
        lines.append(f"## {label} ({len(items)})")
        for p in items:
            if key == "pilots_at_risk":
                lines.append(f"- **{p.get('name')}** — {p.get('reason')}\n  _Intervention:_ {p.get('intervention')}")
            elif key == "pilots_dormant":
                lines.append(f"- **{p.get('name')}** — silent {p.get('days_silent')}d\n  _Breakup:_ {p.get('breakup_email_subject')}")
            else:
                lines.append(f"- **{p.get('name')}** — {p.get('milestone_hit') or p.get('next_step', '')}")
        lines.append("")
    if decs := parsed.get("decisions_needed_from_operator"):
        lines.append("## Decisions needed from operator")
        lines.extend(f"- [ ] {d}" for d in decs)
        lines.append("")
    if (conf := parsed.get("confidence")) is not None:
        lines.append(f"_Confidence: {conf:.2f}_")
    if parsed.get("reasoning"):
        lines.append(f"_Reasoning: {parsed['reasoning']}_")
    return "\n".join(lines)


def run(*, today: date | None = None) -> dict[str, Any]:
    return run_proposal(
        agent=_AGENT, kind=_KIND, prompt=_PROMPT,
        user_message_fn=_user_message,
        body_md_fn=_format_body_md,
        today=today,
    )
