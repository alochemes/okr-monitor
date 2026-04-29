"""AI-Engineer pipeline. One run = one eval_proposal."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import render_dict_as_markdown, run_proposal

_AGENT = "ai_engineer"
_KIND = "eval_proposal"
_PROMPT = (Path(__file__).parent / "prompts" / "eval_proposal.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Propose one improvement to the OKR-Mapper eval/prompt setup that moves us toward KR1.3 "
        "(precision ≥85% @ recall ≥70% on the 200-event labeled set). "
        "Reply with ONLY the JSON object specified in the schema."
    )


def run(*, today: date | None = None) -> dict[str, Any]:
    return run_proposal(
        agent=_AGENT, kind=_KIND, prompt=_PROMPT,
        user_message_fn=_user_message,
        body_md_fn=lambda p, t: render_dict_as_markdown(p, t),
        today=today,
    )
