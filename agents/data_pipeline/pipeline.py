"""Data-Pipeline pipeline. One run = one pipeline_design proposal."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import render_dict_as_markdown, run_proposal

_AGENT = "data_pipeline"
_KIND = "pipeline_design"
_PROMPT = (Path(__file__).parent / "prompts" / "pipeline_design.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Spec the GitHub-events pipeline — source shape (webhook payload), sink shape "
        "(work_events row), normalization rules, late-arrival handling, backfill. "
        "Reply with ONLY the JSON object specified in the schema."
    )


def run(*, today: date | None = None) -> dict[str, Any]:
    return run_proposal(
        agent=_AGENT, kind=_KIND, prompt=_PROMPT,
        user_message_fn=_user_message,
        body_md_fn=lambda p, t: render_dict_as_markdown(p, t, list_keys=("normalization_rules",)),
        today=today,
    )
