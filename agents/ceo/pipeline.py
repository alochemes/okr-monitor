"""CEO-Agent pipeline. One run = one weekly_priorities proposal.

run() = build cached system prompt → call Sonnet → parse JSON → format
body markdown → write proposal to DB. The operator reviews via cli/review.py.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents import _base
from core import audit, config, llm, store


_AGENT = "ceo"
_KIND = "weekly_priorities"
_PROMPT = (Path(__file__).parent / "prompts" / "weekly_priorities.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Produce the weekly priorities proposal for the operator. "
        "Use the OKRs, risks, milestones, and decision log in TRACKER.md as your evidence base. "
        "Reply with ONLY the JSON object specified in the schema."
    )


def _format_body_md(parsed: dict[str, Any], raw_text: str) -> str:
    """Render the parsed JSON as a reviewable markdown brief. Falls back to
    the raw model text if parsing failed."""
    if not parsed:
        return f"_(model output did not parse as JSON; raw below)_\n\n```\n{raw_text}\n```"

    lines: list[str] = []
    lines.append(f"# {parsed.get('title', '(no title)')}")
    lines.append("")
    lines.append(parsed.get("summary", "").strip())
    lines.append("")
    lines.append("## Priorities")
    for p in parsed.get("priorities", []):
        lines.append(
            f"{p.get('rank', '?')}. **{p.get('what', '')}**  \n"
            f"   Owner: `{p.get('owner_pod', '?')}` · KR `{p.get('kr', '?')}` · "
            f"Due `{p.get('deadline', '?')}`  \n"
            f"   _Why:_ {p.get('why', '')}"
        )
    lines.append("")
    risks = parsed.get("risks_to_watch") or []
    if risks:
        lines.append("## Risks to watch")
        lines.extend(f"- {r}" for r in risks)
        lines.append("")
    decisions = parsed.get("decisions_needed_from_operator") or []
    if decisions:
        lines.append("## Decisions needed from operator")
        lines.extend(f"- [ ] {d}" for d in decisions)
        lines.append("")
    conf = parsed.get("confidence")
    if conf is not None:
        lines.append(f"_Confidence: {conf:.2f}_")
    if parsed.get("reasoning"):
        lines.append(f"_Reasoning: {parsed['reasoning']}_")
    return "\n".join(lines)


def run(*, today: date | None = None) -> dict[str, Any]:
    """Run one CEO planning pass. Returns a stats dict (proposal_id, cost,
    tokens). Safe to call repeatedly — each call writes a new proposal row."""
    today = today or date.today()
    store.init_db()
    run_id = store.start_run(agent=_AGENT, kind=_KIND)
    cfg = config.agent(_AGENT)
    stats: dict[str, Any] = {"run_id": run_id, "today": today.isoformat()}

    try:
        snap_id, was_new = _base.snapshot_tracker(run_id=run_id, agent=_AGENT)
        stats["tracker_snapshot_id"] = snap_id
        stats["tracker_changed_since_last"] = was_new

        system = _base.build_system_prompt(agent_prompt_md=_PROMPT)
        user = _user_message(today)

        result = llm.complete(
            system=system,
            user=user,
            model=cfg["model"],
            max_tokens=cfg.get("max_tokens", 2048),
            temperature=cfg.get("temperature", 0.3),
            run_id=run_id,
            agent=_AGENT,
            action=f"{_AGENT}.{_KIND}",
        )

        parsed = result.parse_json()
        body_md = _format_body_md(parsed, result.text)

        pid = store.write_proposal(
            run_id=run_id,
            agent=_AGENT,
            kind=_KIND,
            title=parsed.get("title") or f"Weekly priorities — {today.isoformat()}",
            summary=parsed.get("summary") or result.text[:300],
            body_md=body_md,
            evidence={"raw_parsed": parsed, "model": result.model, "today": today.isoformat()},
            confidence=parsed.get("confidence"),
            model=result.model,
            tokens_in=result.tokens_in,
            tokens_out=result.tokens_out,
            cost_usd=result.cost_usd,
        )
        stats["proposal_id"] = pid
        stats["cost_usd"] = result.cost_usd
        stats["tokens_in"] = result.tokens_in
        stats["tokens_out"] = result.tokens_out
        stats["cache_read_tokens"] = result.cache_read_tokens
        stats["parsed_ok"] = bool(parsed)

        audit.emit(
            run_id=run_id, agent=_AGENT, action=f"{_KIND}.proposal_written",
            subject_type="proposal", subject_id=pid,
            payload={"title": parsed.get("title"), "confidence": parsed.get("confidence")},
        )
        store.end_run(run_id, status="ok", stats=stats)
        return stats

    except Exception as exc:  # pragma: no cover
        store.end_run(run_id, status="error", stats=stats, error=str(exc))
        audit.emit(
            run_id=run_id, agent=_AGENT, action=f"{_KIND}.exception",
            severity="error", payload={"error": str(exc)},
        )
        raise
