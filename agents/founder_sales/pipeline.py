"""Founder-Sales pipeline. One run = one outreach_drafts proposal (5 drafts)."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import run_proposal

_AGENT = "founder_sales"
_KIND = "outreach_drafts"
_PROMPT = (Path(__file__).parent / "prompts" / "outreach_drafts.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "No specific account list passed yet. Draft 5 GENERIC TEMPLATES for the segment "
        "'Chief of Staff at Series B SaaS, 100-300 employees' that the operator will personalize "
        "against named accounts. Each template must include placeholder text in `{curly_braces}` "
        "for the public artifact hook. Reply with ONLY the JSON object specified."
    )


def _format_body_md(parsed: dict[str, Any], raw_text: str) -> str:
    if not parsed:
        return f"_(unparsed)_\n\n```\n{raw_text}\n```"
    lines = [f"# {parsed.get('title', '(no title)')}", "",
             parsed.get("summary", "").strip(), ""]
    for i, d in enumerate(parsed.get("drafts", []) or [], 1):
        lines.append(
            f"### Draft {i} — {d.get('persona', '?')}\n"
            f"_Hook:_ {d.get('artifact_hook', '?')}\n\n"
            f"**Subject:** {d.get('subject', '')}\n\n"
            f"{d.get('body', '')}\n\n"
            f"_Rationale:_ {d.get('rationale', '')}"
        )
        lines.append("")
    if cad := parsed.get("follow_up_cadence_suggested"):
        lines.append(f"**Follow-up cadence:** {cad}")
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
