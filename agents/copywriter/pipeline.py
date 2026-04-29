"""Copywriter pipeline. One run = one copy_draft proposal (3 variants)."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import run_proposal

_AGENT = "copywriter"
_KIND = "copy_draft"
_PROMPT = (Path(__file__).parent / "prompts" / "copy_draft.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Draft 3 variants for the **landing page H1 headline**. Slot constraint: ≤80 chars. "
        "Voice rules in `company.yaml` are non-negotiable. Reply with ONLY the JSON object specified."
    )


def _format_body_md(parsed: dict[str, Any], raw_text: str) -> str:
    if not parsed:
        return f"_(unparsed)_\n\n```\n{raw_text}\n```"
    lines = [f"# {parsed.get('title', '(no title)')}", "",
             parsed.get("summary", "").strip(), ""]
    for v in parsed.get("variants", []) or []:
        lines.append(
            f"### Variant {v.get('id', '?')} — _{v.get('angle', '?')}_\n"
            f"> {v.get('text', '')}\n\n"
            f"_Rationale:_ {v.get('rationale', '')}"
        )
        lines.append("")
    if pick := parsed.get("operator_pick_recommended"):
        lines.append(f"**Recommended pick:** {pick}")
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
