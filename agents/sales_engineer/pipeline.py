"""Sales-Engineer pipeline. One run = one demo_script proposal."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import render_dict_as_markdown, run_proposal

_AGENT = "sales_engineer"
_KIND = "demo_script"
_PROMPT = (Path(__file__).parent / "prompts" / "demo_script.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Draft a 25-min demo script for the standard ICP archetype (Chief of Staff at Series B SaaS, "
        "200 employees, Notion-OKRs + GitHub + Linear + Slack). "
        "Reply with ONLY the JSON object specified in the schema."
    )


def run(*, today: date | None = None) -> dict[str, Any]:
    return run_proposal(
        agent=_AGENT, kind=_KIND, prompt=_PROMPT,
        user_message_fn=_user_message,
        body_md_fn=lambda p, t: render_dict_as_markdown(
            p, t, list_keys=("slots", "expected_questions"),
        ),
        today=today,
    )
