"""Platform pipeline. One run = one infra_review."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import render_dict_as_markdown, run_proposal

_AGENT = "platform"
_KIND = "infra_review"
_PROMPT = (Path(__file__).parent / "prompts" / "infra_review.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Do this week's infra review. Cite TRACKER.md §3 Engineering KRs and §9 risks. "
        "Reply with ONLY the JSON object specified in the schema."
    )


def run(*, today: date | None = None) -> dict[str, Any]:
    return run_proposal(
        agent=_AGENT, kind=_KIND, prompt=_PROMPT,
        user_message_fn=_user_message,
        body_md_fn=lambda p, t: render_dict_as_markdown(
            p, t, list_keys=("components", "single_points_of_failure", "observability_gaps"),
        ),
        today=today,
    )
