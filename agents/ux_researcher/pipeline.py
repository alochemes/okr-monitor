"""UX-Researcher pipeline. One run = one discovery_synthesis proposal."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import run_proposal

_AGENT = "ux_researcher"
_KIND = "discovery_synthesis"
_PROMPT = (Path(__file__).parent / "prompts" / "discovery_synthesis.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "No call notes are passed yet (KR1.4 calls not started). "
        "For now, draft a synthesis TEMPLATE — what JTBD clusters we'd EXPECT given our ICP, "
        "to be revised against real notes after the first 5 calls land. Mark every cluster with "
        "`(synthetic, replace with real evidence)` so the operator never confuses this with a real synthesis. "
        "Reply with ONLY the JSON object specified in the schema."
    )


def _format_body_md(parsed: dict[str, Any], raw_text: str) -> str:
    if not parsed:
        return f"_(unparsed)_\n\n```\n{raw_text}\n```"
    lines = [f"# {parsed.get('title', '(no title)')}", "",
             parsed.get("summary", "").strip(), ""]
    if clusters := parsed.get("jtbd_clusters"):
        lines.append("## JTBD clusters")
        for c in clusters:
            lines.append(
                f"### {c.get('job', '?')}\n"
                f"_Frequency:_ {c.get('frequency', '?')} · _Intensity:_ {c.get('intensity', '?')}\n"
            )
            for ev in c.get("evidence", []) or []:
                lines.append(f"  - {ev}")
            lines.append("")
    if anti := parsed.get("anti_signals"):
        lines.append("## Anti-signals (wrong-fit)")
        lines.extend(f"- {a}" for a in anti)
        lines.append("")
    if refs := parsed.get("icp_refinements"):
        lines.append("## ICP refinements")
        lines.extend(f"- {r}" for r in refs)
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
