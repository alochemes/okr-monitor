"""Growth-Hacker pipeline. One run = one experiment_proposal (3 experiments)."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import render_dict_as_markdown, run_proposal

_AGENT = "growth_hacker"
_KIND = "experiment_proposal"
_PROMPT = (Path(__file__).parent / "prompts" / "experiment_proposal.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Propose 3 growth experiments for the coming sprint. Each must have a falsifiable hypothesis, "
        "a metric, sample size / runtime, and kill criteria. "
        "Reply with ONLY the JSON object specified in the schema."
    )


def run(*, today: date | None = None) -> dict[str, Any]:
    return run_proposal(
        agent=_AGENT, kind=_KIND, prompt=_PROMPT,
        user_message_fn=_user_message,
        body_md_fn=lambda p, t: render_dict_as_markdown(p, t, list_keys=("experiments",)),
        today=today,
    )
