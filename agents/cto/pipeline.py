"""CTO-Agent pipeline. One run = one architecture_review proposal."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents import _base
from core import audit, config, llm, store


_AGENT = "cto"
_KIND = "architecture_review"
_PROMPT = (Path(__file__).parent / "prompts" / "architecture_review.md").read_text(encoding="utf-8")


def _user_message(today: date) -> str:
    return (
        f"Today is {today.isoformat()}.\n\n"
        "Review the current architecture and engineering choices visible in TRACKER.md "
        "(§3 Engineering pod KRs, §7 Decision Log, §9 Risks). "
        "Flag concrete risks with concrete mitigations. "
        "Reply with ONLY the JSON object specified in the schema."
    )


def _format_body_md(parsed: dict[str, Any], raw_text: str) -> str:
    if not parsed:
        return f"_(model output did not parse as JSON; raw below)_\n\n```\n{raw_text}\n```"
    lines = [f"# {parsed.get('title', '(no title)')}", "", parsed.get("summary", "").strip(), ""]
    risks = parsed.get("risks") or []
    if risks:
        lines.append("## Risks")
        for r in risks:
            sev = r.get("severity", "?").upper()
            lines.append(
                f"- **[{sev}]** `{r.get('area', '?')}` — {r.get('risk', '')}  \n"
                f"  → _Mitigation:_ {r.get('mitigation', '')} (`{r.get('effort', '?')}`)"
            )
        lines.append("")
    decisions = parsed.get("decisions_needed_from_operator") or []
    if decisions:
        lines.append("## Decisions needed from operator")
        lines.extend(f"- [ ] {d}" for d in decisions)
        lines.append("")
    if (conf := parsed.get("confidence")) is not None:
        lines.append(f"_Confidence: {conf:.2f}_")
    if parsed.get("reasoning"):
        lines.append(f"_Reasoning: {parsed['reasoning']}_")
    return "\n".join(lines)


def run(*, today: date | None = None) -> dict[str, Any]:
    today = today or date.today()
    store.init_db()
    run_id = store.start_run(agent=_AGENT, kind=_KIND)
    cfg = config.agent(_AGENT)
    stats: dict[str, Any] = {"run_id": run_id, "today": today.isoformat()}

    try:
        snap_id, was_new = _base.snapshot_tracker(run_id=run_id, agent=_AGENT)
        stats["tracker_snapshot_id"] = snap_id
        stats["tracker_changed_since_last"] = was_new

        result = llm.complete(
            system=_base.build_system_prompt(agent_prompt_md=_PROMPT),
            user=_user_message(today),
            model=cfg["model"],
            max_tokens=cfg.get("max_tokens", 2048),
            temperature=cfg.get("temperature", 0.2),
            run_id=run_id, agent=_AGENT, action=f"{_AGENT}.{_KIND}",
        )

        parsed = result.parse_json()
        body_md = _format_body_md(parsed, result.text)

        pid = store.write_proposal(
            run_id=run_id, agent=_AGENT, kind=_KIND,
            title=parsed.get("title") or f"Architecture review — {today.isoformat()}",
            summary=parsed.get("summary") or result.text[:300],
            body_md=body_md,
            evidence={"raw_parsed": parsed, "model": result.model, "today": today.isoformat()},
            confidence=parsed.get("confidence"),
            model=result.model, tokens_in=result.tokens_in,
            tokens_out=result.tokens_out, cost_usd=result.cost_usd,
        )
        stats.update({
            "proposal_id": pid, "cost_usd": result.cost_usd,
            "tokens_in": result.tokens_in, "tokens_out": result.tokens_out,
            "cache_read_tokens": result.cache_read_tokens, "parsed_ok": bool(parsed),
        })
        audit.emit(
            run_id=run_id, agent=_AGENT, action=f"{_KIND}.proposal_written",
            subject_type="proposal", subject_id=pid,
            payload={"title": parsed.get("title"), "confidence": parsed.get("confidence")},
        )
        store.end_run(run_id, status="ok", stats=stats)
        return stats

    except Exception as exc:
        store.end_run(run_id, status="error", stats=stats, error=str(exc))
        audit.emit(run_id=run_id, agent=_AGENT, action=f"{_KIND}.exception",
                   severity="error", payload={"error": str(exc)})
        raise
