"""Content pipeline. One run = one blog_post_draft proposal (~900 words)."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import run_proposal

_AGENT = "content"
_KIND = "blog_post_draft"
_PROMPT = (Path(__file__).parent / "prompts" / "blog_post_draft.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Pick the topic that most supports our wedge (TRACKER.md §1) and draft one long-form "
        "post (800-1,200 words). Reply with ONLY the JSON object specified in the schema."
    )


def _format_body_md(parsed: dict[str, Any], raw_text: str) -> str:
    if not parsed:
        return f"_(unparsed)_\n\n```\n{raw_text}\n```"
    lines = [f"# {parsed.get('title', '(no title)')}", "",
             parsed.get("summary", "").strip(), ""]
    if outline := parsed.get("outline"):
        lines.append("## Outline")
        lines.extend(f"{i}. {s}" for i, s in enumerate(outline, 1))
        lines.append("")
    if draft := parsed.get("first_draft_md"):
        wc = parsed.get("actual_word_count", "?")
        lines.append(f"## Draft ({wc} words)")
        lines.append(draft)
        lines.append("")
    if stat := parsed.get("anchor_stat"):
        lines.append(f"**Anchor stat:** {stat}")
    if anti := parsed.get("named_anti_pattern"):
        lines.append(f"**Anti-pattern:** {anti}")
    if frame := parsed.get("proprietary_frame"):
        lines.append(f"**Frame:** {frame}")
    lines.append("")
    if quote := parsed.get("social_pull_quote"):
        lines.append(f"> {quote}")
        lines.append("")
    if kw := parsed.get("seo_keywords"):
        lines.append(f"_SEO keywords:_ {', '.join(kw)}")
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
