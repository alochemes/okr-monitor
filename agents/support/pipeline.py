"""Support pipeline. One run = one ticket_triage proposal."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import render_dict_as_markdown, run_proposal

_AGENT = "support"
_KIND = "ticket_triage"
_PROMPT = (Path(__file__).parent / "prompts" / "ticket_triage.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "No live ticket queue yet (pre-launch). Draft a TRIAGE TEMPLATE that defines the rubric "
        "the agent will apply once tickets exist (per the YAML output_quality_bar). "
        "Reply with ONLY the JSON object specified in the schema."
    )


def run(*, today: date | None = None) -> dict[str, Any]:
    return run_proposal(
        agent=_AGENT, kind=_KIND, prompt=_PROMPT,
        user_message_fn=_user_message,
        body_md_fn=lambda p, t: render_dict_as_markdown(
            p, t, list_keys=("tickets", "escalations"),
        ),
        today=today,
    )
