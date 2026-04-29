"""PM agent pipeline. One run = one user_stories proposal."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import render_dict_as_markdown, run_proposal

_AGENT = "pm"
_KIND = "user_stories"
_PROMPT = (Path(__file__).parent / "prompts" / "user_stories.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Propose 5 user stories for the next sprint. Each story must cite a specific KR by ID. "
        "Reply with ONLY the JSON object specified in the schema."
    )


def _format_body_md(parsed: dict[str, Any], raw_text: str) -> str:
    if not parsed:
        return f"_(unparsed model output)_\n\n```\n{raw_text}\n```"
    lines: list[str] = [f"# {parsed.get('title', '(no title)')}", "",
                        parsed.get("summary", "").strip(), ""]
    for s in parsed.get("stories", []) or []:
        lines.append(
            f"### Story (KR `{s.get('kr', '?')}`)\n"
            f"**As a** {s.get('as_a', '?')}, **I want** {s.get('i_want', '?')}, "
            f"**so that** {s.get('so_that', '?')}.\n\n"
            f"_Acceptance:_\n" + "\n".join(f"  - {c}" for c in s.get('acceptance', []) or [])
        )
        lines.append("")
    if cuts := parsed.get("stories_cut"):
        lines.append("## Cut from this sprint")
        lines.extend(f"- {c}" for c in cuts)
        lines.append("")
    if decs := parsed.get("decisions_needed_from_operator"):
        lines.append("## Decisions needed from operator")
        lines.extend(f"- [ ] {d}" for d in decs)
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
