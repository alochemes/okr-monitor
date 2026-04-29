"""Signals-Analyst pipeline. Pure compute, no LLM.

Reads `event_kr_mappings` joined to `work_events`, writes one `kr_signals`
row per KR per run covering rolling 7d / 30d / all-time counts. Forecast
columns are left NULL — the forecasting agent fills them in a separate pass
so signals_analyst stays cheap and side-effect-free."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from core import audit, store, tracker


_AGENT = "signals_analyst"
_KIND = "kr_signals_snapshot"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def _compute_for_kr(kr_id: str, *, now: datetime) -> dict[str, Any]:
    """Return a metrics dict for one KR. Cheap SQL only — no joins outside
    what's already indexed."""
    rows = store.list_mappings_for_kr(kr_id)
    events_total = len(rows)
    cutoff_7d = now - timedelta(days=7)
    cutoff_30d = now - timedelta(days=30)

    events_7d = 0
    events_30d = 0
    confidences: list[float] = []
    actors: set[str] = set()
    last_event_at: str | None = None
    for r in rows:
        try:
            ts = datetime.fromisoformat(r["occurred_at"])
        except (TypeError, ValueError):
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if last_event_at is None or ts.isoformat() > last_event_at:
            last_event_at = ts.isoformat()
        if ts >= cutoff_7d:
            events_7d += 1
        if ts >= cutoff_30d:
            events_30d += 1
        if r["confidence"] is not None:
            confidences.append(float(r["confidence"]))
        if r["actor"]:
            actors.add(r["actor"])

    mean_conf = round(sum(confidences) / len(confidences), 4) if confidences else None
    return {
        "events_total": events_total,
        "events_7d": events_7d,
        "events_30d": events_30d,
        "distinct_actors": len(actors),
        "last_event_at": last_event_at,
        "mean_confidence": mean_conf,
    }


def run() -> dict[str, Any]:
    """Compute signals for every KR present in TRACKER.md §2. Returns a
    stats dict including per-KR counts."""
    store.init_db()
    run_id = store.start_run(agent=_AGENT, kind=_KIND)
    now = _utcnow()
    stats: dict[str, Any] = {
        "run_id": run_id, "computed_at": _iso(now),
        "krs_processed": 0, "signals_written": 0, "per_kr": [],
    }
    try:
        objectives = tracker.extract_okrs()
        kr_ids: list[str] = [kr["id"] for obj in objectives for kr in obj["krs"]]

        for kr_id in kr_ids:
            metrics = _compute_for_kr(kr_id, now=now)
            sid = store.write_kr_signal(
                run_id=run_id, kr_id=kr_id, computed_at=_iso(now),
                events_total=metrics["events_total"],
                events_7d=metrics["events_7d"],
                events_30d=metrics["events_30d"],
                distinct_actors=metrics["distinct_actors"],
                last_event_at=metrics["last_event_at"],
                mean_confidence=metrics["mean_confidence"],
            )
            stats["krs_processed"] += 1
            stats["signals_written"] += 1
            stats["per_kr"].append({
                "kr_id": kr_id, "signal_id": sid,
                "events_total": metrics["events_total"],
                "events_7d": metrics["events_7d"],
                "events_30d": metrics["events_30d"],
            })

        audit.emit(
            run_id=run_id, agent=_AGENT, action=f"{_KIND}.complete",
            payload={"krs_processed": stats["krs_processed"],
                     "total_events_30d": sum(p["events_30d"] for p in stats["per_kr"])},
        )
        store.end_run(run_id, status="ok", stats=stats)
        return stats

    except Exception as exc:
        store.end_run(run_id, status="error", stats=stats, error=str(exc))
        audit.emit(run_id=run_id, agent=_AGENT, action=f"{_KIND}.exception",
                   severity="error", payload={"error": str(exc)})
        raise
