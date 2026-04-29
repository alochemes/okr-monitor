"""Onboarding pipeline. One run = one onboarding_playbook proposal."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import run_proposal

_AGENT = "onboarding"
_KIND = "onboarding_playbook"
_PROMPT = (Path(__file__).parent / "prompts" / "onboarding_playbook.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "No specific pilot context passed yet. Draft a GENERIC v1 playbook for our default ICP "
        "(Chief of Staff at a 200-person Series B with Notion-OKRs + GitHub + Linear + Slack). "
        "This becomes the starting template the operator customizes per pilot. "
        "Reply with ONLY the JSON object specified in the schema."
    )


def _format_body_md(parsed: dict[str, Any], raw_text: str) -> str:
    if not parsed:
        return f"_(unparsed)_\n\n```\n{raw_text}\n```"
    lines = [f"# {parsed.get('title', '(no title)')}", "",
             parsed.get("summary", "").strip(), ""]
    if ctx := parsed.get("pilot_context"):
        lines.append(f"_Context:_ {ctx.get('company')} · {ctx.get('size')} · "
                     f"OKRs in {ctx.get('okr_tool')} · integrations: {', '.join(ctx.get('integrations') or [])}")
        lines.append("")
    if fv := parsed.get("first_value_moment"):
        lines.append(f"## First-value moment\n{fv}")
        lines.append("")
    if agenda := parsed.get("kickoff_agenda"):
        lines.append("## Kickoff agenda (45 min)")
        for item in agenda:
            decision = f" — _decision:_ {item['decision_point']}" if item.get("decision_point") else ""
            lines.append(f"- `{item.get('window', '?')}` — {item.get('topic', '')}{decision}")
        lines.append("")
    if ms := parsed.get("first_week_milestones"):
        lines.append("## First-week milestones")
        for m in ms:
            lines.append(f"- **{m.get('day', '?')}:** {m.get('milestone', '')}\n  _Signal:_ {m.get('observable_signal', '')}")
        lines.append("")
    if d30 := parsed.get("day_30_check_in"):
        lines.append("## Day-30 check-in")
        lines.append("_Agenda:_ " + "; ".join(d30.get("agenda", []) or []))
        lines.append("_Success criteria:_ " + "; ".join(d30.get("success_criteria", []) or []))
        lines.append("")
    if d60 := parsed.get("day_60_decision"):
        lines.append(f"## Day-60 decision\n_Options:_ {', '.join(d60.get('options', []) or [])}\n_Criteria:_ {d60.get('criteria', '')}")
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
