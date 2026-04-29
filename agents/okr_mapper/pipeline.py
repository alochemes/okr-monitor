"""OKR-Mapper pipeline. One run = map one work_event to N KRs.

The mapper is the load-bearing IP for OKR Monitor (KR1.3). Cost-sensitive
because it scales linearly with event volume — see TRACKER.md §3 AI/Data pod
for the cost model. This pipeline supports two entry points:

  run(event_id=...)    — map one specific event
  run_all_unmapped()   — sweep every event without an event_kr_mappings row
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agents import _base
from core import audit, config, llm, store


_AGENT = "okr_mapper"
_KIND = "map_event"
_PROMPT = (Path(__file__).parent / "prompts" / "map_event.md").read_text(encoding="utf-8")


def _user_message(event: dict[str, Any]) -> str:
    return (
        "Map this work event to KR(s). Reply with ONLY the JSON object specified in the schema.\n\n"
        f"Event source: {event.get('source')}\n"
        f"Event kind: {event.get('kind')}\n"
        f"Actor: {event.get('actor')}\n"
        f"Occurred at: {event.get('occurred_at')}\n"
        f"Title: {event.get('title')}\n\n"
        "Body:\n"
        f"{event.get('body') or '(no body)'}"
    )


def _map_one(event: dict[str, Any], *, run_id: str, system: str) -> dict[str, Any]:
    cfg = config.agent(_AGENT)
    result = llm.complete(
        system=system,
        user=_user_message(event),
        model=cfg["model"],
        max_tokens=cfg.get("max_tokens", 1024),
        temperature=cfg.get("temperature", 0.1),
        run_id=run_id,
        agent=_AGENT,
        action=f"{_AGENT}.{_KIND}",
    )
    parsed = result.parse_json()
    raw_mappings = parsed.get("mappings") or []

    # Defensive filter: drop any mapping with bad shape or low confidence.
    cleaned: list[dict[str, Any]] = []
    for m in raw_mappings:
        try:
            kr_id = str(m["kr_id"]).strip()
            conf = float(m["confidence"])
        except (KeyError, TypeError, ValueError):
            continue
        if not kr_id or conf < 0.5:
            continue
        cleaned.append({
            "kr_id": kr_id, "confidence": conf,
            "reasoning": (m.get("reasoning") or "").strip() or None,
        })

    mapping_ids = store.write_event_kr_mappings(
        event_id=event["id"], run_id=run_id, mappings=cleaned,
        model=result.model, tokens_in=result.tokens_in,
        tokens_out=result.tokens_out, cost_usd=result.cost_usd,
    )

    audit.emit(
        run_id=run_id, agent=_AGENT, action=f"{_KIND}.complete",
        subject_type="work_event", subject_id=event["id"],
        payload={
            "kr_count": len(cleaned),
            "krs": [m["kr_id"] for m in cleaned],
            "mean_confidence": (
                round(sum(m["confidence"] for m in cleaned) / len(cleaned), 3)
                if cleaned else None
            ),
            "no_mapping_reason": parsed.get("no_mapping_reason"),
        },
        model=result.model, tokens_in=result.tokens_in,
        tokens_out=result.tokens_out, cost_usd=result.cost_usd,
    )
    return {
        "event_id": event["id"], "mapping_ids": mapping_ids,
        "mappings": cleaned, "cost_usd": result.cost_usd,
    }


def _build_system_once() -> str:
    """Build the cacheable system block once per pipeline invocation. The
    KR catalog (TRACKER.md §2) is the most important part — it's what the
    mapper picks from."""
    return _base.build_system_prompt(agent_prompt_md=_PROMPT)


def run(*, event_id: str) -> dict[str, Any]:
    """Map one specific work_event."""
    store.init_db()
    run_id = store.start_run(agent=_AGENT, kind=_KIND)
    stats: dict[str, Any] = {"run_id": run_id, "event_id": event_id}
    try:
        with store.connect() as conn:
            row = conn.execute(
                "SELECT * FROM work_events WHERE id = ?", (event_id,),
            ).fetchone()
        if not row:
            raise ValueError(f"work_event {event_id} not found")
        _base.snapshot_tracker(run_id=run_id, agent=_AGENT)
        result = _map_one(dict(row), run_id=run_id, system=_build_system_once())
        stats.update({
            "mappings_count": len(result["mappings"]),
            "krs": [m["kr_id"] for m in result["mappings"]],
            "cost_usd": result["cost_usd"],
        })
        store.end_run(run_id, status="ok", stats=stats)
        return stats
    except Exception as exc:
        store.end_run(run_id, status="error", stats=stats, error=str(exc))
        audit.emit(run_id=run_id, agent=_AGENT, action=f"{_KIND}.exception",
                   severity="error", payload={"error": str(exc)})
        raise


def run_all_unmapped(*, limit: int = 100) -> dict[str, Any]:
    """Sweep every work_event with no mappings yet. Builds the system prompt
    once and reuses it across calls so the prompt cache pays off across the
    batch."""
    store.init_db()
    run_id = store.start_run(agent=_AGENT, kind=f"{_KIND}.sweep")
    stats: dict[str, Any] = {
        "run_id": run_id, "events_processed": 0, "mappings_written": 0,
        "events_with_no_mappings": 0, "total_cost_usd": 0.0, "per_event": [],
    }
    try:
        events = store.list_unmapped_events(limit=limit)
        if not events:
            store.end_run(run_id, status="ok", stats=stats)
            return stats

        _base.snapshot_tracker(run_id=run_id, agent=_AGENT)
        system = _build_system_once()
        for r in events:
            evt = dict(r)
            try:
                result = _map_one(evt, run_id=run_id, system=system)
            except Exception as exc:
                audit.emit(run_id=run_id, agent=_AGENT,
                           action=f"{_KIND}.event_failed", severity="warn",
                           subject_type="work_event", subject_id=evt["id"],
                           payload={"error": str(exc)})
                continue
            stats["events_processed"] += 1
            n = len(result["mappings"])
            stats["mappings_written"] += n
            if n == 0:
                stats["events_with_no_mappings"] += 1
            stats["total_cost_usd"] += result["cost_usd"] or 0.0
            stats["per_event"].append({
                "event_id": evt["id"], "title": evt["title"][:80],
                "krs": [m["kr_id"] for m in result["mappings"]],
            })
        stats["total_cost_usd"] = round(stats["total_cost_usd"], 4)
        store.end_run(run_id, status="ok", stats=stats)
        return stats
    except Exception as exc:
        store.end_run(run_id, status="error", stats=stats, error=str(exc))
        audit.emit(run_id=run_id, agent=_AGENT, action=f"{_KIND}.sweep.exception",
                   severity="error", payload={"error": str(exc)})
        raise
