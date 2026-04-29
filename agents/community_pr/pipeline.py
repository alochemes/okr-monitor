"""Community-PR pipeline. One run = one pr_pitches proposal (5 pitches)."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import render_dict_as_markdown, run_proposal

_AGENT = "community_pr"
_KIND = "pr_pitches"
_PROMPT = (Path(__file__).parent / "prompts" / "pr_pitches.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Propose 5 PR/community pitches for this week. Each must name a real venue, host/editor, "
        "and a tailored angle. Reply with ONLY the JSON object specified in the schema."
    )


def run(*, today: date | None = None) -> dict[str, Any]:
    return run_proposal(
        agent=_AGENT, kind=_KIND, prompt=_PROMPT,
        user_message_fn=_user_message,
        body_md_fn=lambda p, t: render_dict_as_markdown(p, t, list_keys=("pitches",)),
        today=today,
    )
