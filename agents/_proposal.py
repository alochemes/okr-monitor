"""Shared run helper for "single LLM call → one structured proposal" agents.

Used by every Product/Design, GTM, and Customer/Ops agent that follows the
same shape as the strategy pod: cached system prompt (role + company.yaml +
TRACKER.md) + per-call user message → JSON proposal → markdown body for
operator review.

Each calling agent provides:
  - its name, kind, prompt markdown, model config (yaml-loaded)
  - a `user_message_fn(today)` that returns the per-call user prompt
  - a `body_md_fn(parsed, raw_text)` that turns the parsed JSON into the
    operator-facing markdown
"""

from __future__ import annotations

from datetime import date
from typing import Any, Callable

from agents import _base
from core import audit, config, llm, store


def run_proposal(
    *,
    agent: str,
    kind: str,
    prompt: str,
    user_message_fn: Callable[[date], str],
    body_md_fn: Callable[[dict[str, Any], str], str],
    today: date | None = None,
    default_temperature: float = 0.4,
    default_max_tokens: int = 2048,
) -> dict[str, Any]:
    """Run one LLM call, write one proposal, end the run. Idempotent only at
    the proposal-write level — multiple calls on the same day produce
    multiple proposal rows (intentional; lets the operator compare model
    drafts of the same kind)."""
    today = today or date.today()
    store.init_db()
    run_id = store.start_run(agent=agent, kind=kind)
    cfg = config.agent(agent)
    stats: dict[str, Any] = {"run_id": run_id, "today": today.isoformat()}

    try:
        snap_id, was_new = _base.snapshot_tracker(run_id=run_id, agent=agent)
        stats["tracker_snapshot_id"] = snap_id
        stats["tracker_changed_since_last"] = was_new

        result = llm.complete(
            system=_base.build_system_prompt(agent_prompt_md=prompt),
            user=user_message_fn(today),
            model=cfg["model"],
            max_tokens=cfg.get("max_tokens", default_max_tokens),
            temperature=cfg.get("temperature", default_temperature),
            run_id=run_id, agent=agent, action=f"{agent}.{kind}",
        )

        parsed = result.parse_json()
        body_md = body_md_fn(parsed, result.text)

        pid = store.write_proposal(
            run_id=run_id, agent=agent, kind=kind,
            title=parsed.get("title") or f"{kind} — {today.isoformat()}",
            summary=parsed.get("summary") or result.text[:300],
            body_md=body_md,
            evidence={"raw_parsed": parsed, "model": result.model,
                      "today": today.isoformat()},
            confidence=parsed.get("confidence"),
            model=result.model,
            tokens_in=result.tokens_in,
            tokens_out=result.tokens_out,
            cost_usd=result.cost_usd,
        )
        stats.update({
            "proposal_id": pid,
            "cost_usd": result.cost_usd,
            "tokens_in": result.tokens_in,
            "tokens_out": result.tokens_out,
            "cache_read_tokens": result.cache_read_tokens,
            "parsed_ok": bool(parsed),
        })
        audit.emit(
            run_id=run_id, agent=agent, action=f"{kind}.proposal_written",
            subject_type="proposal", subject_id=pid,
            payload={"title": parsed.get("title"),
                     "confidence": parsed.get("confidence")},
        )
        store.end_run(run_id, status="ok", stats=stats)
        return stats

    except Exception as exc:
        store.end_run(run_id, status="error", stats=stats, error=str(exc))
        audit.emit(
            run_id=run_id, agent=agent, action=f"{kind}.exception",
            severity="error", payload={"error": str(exc)},
        )
        raise


def render_dict_as_markdown(parsed: dict[str, Any], raw_text: str,
                            *, list_keys: tuple[str, ...] = ()) -> str:
    """Generic body_md formatter for agents that don't need a custom layout.
    Renders the title, summary, list-of-things keys (in order given), and
    confidence/reasoning footer. Used as a default by simple agents."""
    if not parsed:
        return f"_(model output did not parse as JSON; raw below)_\n\n```\n{raw_text}\n```"

    lines: list[str] = []
    if parsed.get("title"):
        lines.append(f"# {parsed['title']}")
        lines.append("")
    if parsed.get("summary"):
        lines.append(parsed["summary"].strip())
        lines.append("")

    for key in list_keys:
        items = parsed.get(key) or []
        if not items:
            continue
        lines.append(f"## {key.replace('_', ' ').title()}")
        for item in items:
            if isinstance(item, str):
                lines.append(f"- {item}")
            elif isinstance(item, dict):
                # Render as bullet with key lines
                first_key = next(iter(item))
                lines.append(f"- **{item.get(first_key)}**")
                for k, v in item.items():
                    if k == first_key:
                        continue
                    lines.append(f"  - _{k}:_ {v}")
            else:
                lines.append(f"- {item}")
        lines.append("")

    if (conf := parsed.get("confidence")) is not None:
        try:
            lines.append(f"_Confidence: {float(conf):.2f}_")
        except (TypeError, ValueError):
            pass
    if parsed.get("reasoning"):
        lines.append(f"_Reasoning: {parsed['reasoning']}_")
    return "\n".join(lines)
