"""Forecasting pipeline. Pure compute, no LLM.

For each KR, reads the latest signals_analyst row, reads TRACKER.md §2 for
target/current/due_date, writes a NEW kr_signals row with the forecast
columns populated.

V0 verdict logic (no probability model — just heuristics):
  on_track    — gap (target - current) ≤ 0  (KR already met)
  off         — due_date < today AND gap > 0
  drifting    — due_date within 14 days AND events_7d == 0
  active      — numeric KR, events_7d > 0, days_remaining > 0
  stale       — numeric KR, events_7d == 0, days_remaining > 0
  qualitative — target or current not parseable as a number

This intentionally does NOT try to compute P(hit). Events count ≠ target
unit for most KRs (a commit isn't a pilot). Adding a real probability model
needs per-KR conversion factors — defer to v1 when we have real data to
calibrate against.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from typing import Any

from core import audit, config, store, tracker


_AGENT = "forecasting"
_KIND = "kr_forecast_snapshot"

_NUMBER_RE = re.compile(r"(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)")
_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _parse_numeric(raw: str | None) -> float | None:
    """Extract the first number from a target/current cell. Handles
    comma-grouped numbers ('5,000'), percentages ('≥60%' → 60), and
    fractions ('30/30' → 30). Returns None if no number found."""
    if not raw:
        return None
    m = _NUMBER_RE.search(raw)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None


def _parse_iso_date(raw: str | None) -> date | None:
    if not raw:
        return None
    m = _DATE_RE.search(raw)
    if not m:
        return None
    try:
        return date.fromisoformat(m.group(1))
    except ValueError:
        return None


def _verdict(
    *,
    target: float | None,
    current: float | None,
    due_date: date | None,
    today: date,
    events_7d: int,
) -> tuple[str, int | None, float | None, float | None]:
    """Return (verdict, days_remaining, pace_required, pace_per_day_proxy)."""
    if target is None or current is None or due_date is None:
        return "qualitative", None, None, None

    gap = target - current
    days_remaining = (due_date - today).days

    if gap <= 0:
        return "on_track", days_remaining, 0.0, None

    if days_remaining < 0:
        return "off", days_remaining, None, None

    pace_required = gap / max(days_remaining, 1)
    if days_remaining <= 14 and events_7d == 0:
        return "drifting", days_remaining, pace_required, None
    if events_7d > 0:
        return "active", days_remaining, pace_required, events_7d / 7.0
    return "stale", days_remaining, pace_required, 0.0


def run(*, today: date | None = None) -> dict[str, Any]:
    today = today or date.today()
    store.init_db()
    run_id = store.start_run(agent=_AGENT, kind=_KIND)
    cfg = config.agent(_AGENT)
    stats: dict[str, Any] = {
        "run_id": run_id, "today": today.isoformat(),
        "krs_processed": 0, "by_verdict": {}, "per_kr": [],
    }

    try:
        # 1. Pull the latest signals_analyst snapshot per KR.
        latest = {row["kr_id"]: dict(row) for row in store.latest_kr_signals()}
        # 2. Pull TRACKER.md §2 for target/current/due_date per KR.
        objectives = tracker.extract_okrs()
        kr_meta: dict[str, dict[str, str]] = {}
        for obj in objectives:
            for kr in obj["krs"]:
                kr_meta[kr["id"]] = kr

        now_iso = datetime.now(timezone.utc).isoformat()
        by_verdict: dict[str, int] = {}

        for kr_id, meta in kr_meta.items():
            sig = latest.get(kr_id)
            if not sig:
                continue   # signals_analyst hasn't seen this KR yet — skip
            target_raw = meta.get("target")
            current_raw = meta.get("current")
            target_num = _parse_numeric(target_raw)
            current_num = _parse_numeric(current_raw)
            due_date = _parse_iso_date(meta.get("due"))
            verdict, days_remaining, pace_required, pace_per_day = _verdict(
                target=target_num, current=current_num,
                due_date=due_date, today=today,
                events_7d=int(sig["events_7d"]),
            )

            store.write_kr_signal(
                run_id=run_id, kr_id=kr_id, computed_at=now_iso,
                events_total=int(sig["events_total"]),
                events_7d=int(sig["events_7d"]),
                events_30d=int(sig["events_30d"]),
                distinct_actors=int(sig["distinct_actors"]),
                last_event_at=sig.get("last_event_at"),
                mean_confidence=sig.get("mean_confidence"),
                target_raw=target_raw, target_numeric=target_num,
                current_numeric=current_num,
                due_date=due_date.isoformat() if due_date else None,
                days_remaining=days_remaining,
                pace_per_day=pace_per_day,
                pace_required=pace_required,
                forecast_verdict=verdict,
                forecast_p_hit=None,    # deferred to v1
            )
            stats["krs_processed"] += 1
            by_verdict[verdict] = by_verdict.get(verdict, 0) + 1
            stats["per_kr"].append({
                "kr_id": kr_id, "verdict": verdict,
                "days_remaining": days_remaining,
                "events_7d": int(sig["events_7d"]),
                "target": target_num, "current": current_num,
            })

        stats["by_verdict"] = by_verdict
        audit.emit(
            run_id=run_id, agent=_AGENT, action=f"{_KIND}.complete",
            payload={"krs_processed": stats["krs_processed"], "by_verdict": by_verdict},
        )
        store.end_run(run_id, status="ok", stats=stats)
        return stats

    except Exception as exc:
        store.end_run(run_id, status="error", stats=stats, error=str(exc))
        audit.emit(run_id=run_id, agent=_AGENT, action=f"{_KIND}.exception",
                   severity="error", payload={"error": str(exc)})
        raise
