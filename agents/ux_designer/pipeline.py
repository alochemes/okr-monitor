"""UX-Designer pipeline. One run = one design_brief proposal."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import render_dict_as_markdown, run_proposal

_AGENT = "ux_designer"
_KIND = "design_brief"
_PROMPT = (Path(__file__).parent / "prompts" / "design_brief.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Pick the highest-leverage MVP feature (per TRACKER.md §1 wedge) and draft its design brief. "
        "Reply with ONLY the JSON object specified in the schema."
    )


def run(*, today: date | None = None) -> dict[str, Any]:
    return run_proposal(
        agent=_AGENT, kind=_KIND, prompt=_PROMPT,
        user_message_fn=_user_message,
        body_md_fn=lambda p, t: render_dict_as_markdown(
            p, t, list_keys=("user_flow", "screens", "tradeoffs_considered", "open_questions"),
        ),
        today=today,
    )
