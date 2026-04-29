"""Demand-Gen pipeline. One run = one cold_sequence proposal."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import run_proposal

_AGENT = "demand_gen"
_KIND = "cold_sequence"
_PROMPT = (Path(__file__).parent / "prompts" / "cold_sequence.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Design a 5-touch sequence for the segment: Series A RevOps leaders, 50-150 employees, "
        "raised in last 12 months. Reply with ONLY the JSON object specified in the schema."
    )


def _format_body_md(parsed: dict[str, Any], raw_text: str) -> str:
    if not parsed:
        return f"_(unparsed)_\n\n```\n{raw_text}\n```"
    lines = [f"# {parsed.get('title', '(no title)')}", "",
             parsed.get("summary", "").strip(), ""]
    if seg := parsed.get("segment"):
        lines.append(f"**Segment:** {seg.get('persona')} · {seg.get('company_archetype')} · trigger: {seg.get('trigger_event')}")
        lines.append("")
    for t in parsed.get("touches", []) or []:
        lines.append(
            f"### Touch {t.get('n')} — Day {t.get('day')} · `{t.get('channel', '?')}`\n"
            f"**{t.get('subject_or_opening', '')}**\n\n"
            f"{t.get('body', '')}\n\n"
            f"_Thesis:_ {t.get('thesis', '')}"
        )
        lines.append("")
    if rate := parsed.get("expected_reply_rate_pct"):
        lines.append(f"**Expected reply rate:** {rate}%")
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
