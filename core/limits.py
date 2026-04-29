"""Daily LLM cost circuit breaker.

Reads/writes today's running LLM spend in `kpi_daily['llm_cost_usd_today']`.
Refuses new model calls once today's accumulated spend exceeds the cap.

Default caps (operator-approved 2026-04-29):
  - $50.00/day during Sprint 0–1 (through 2026-05-26)
  - $100.00/day from Sprint 2 onward (2026-05-27+)

Override either via env var `OKR_MONITOR_DAILY_LLM_CAP_USD` (a float).

Semantics: we check *before* the call against the running total. If that
total is already at or above the cap, the call is refused. We do not try to
predict the unknown cost of the impending call — that would over-throttle.
A single in-flight call is allowed to push the day slightly over the cap;
the next call will then be blocked. This is intentional: a circuit breaker
trips after the burst, not in anticipation of one.

In dry-run mode (OKR_MONITOR_DRY_RUN=true), no spend is recorded and the
breaker never fires.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone

from core import store


class CircuitBreakerOpen(RuntimeError):
    """Raised when today's LLM spend has reached the daily cap."""


_DEFAULT_CAP_USD = 50.0
_SPRINT_2_PLUS_CAP_USD = 100.0
_SPRINT_2_START_DATE = "2026-05-27"


def _today_iso() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def daily_cap_usd() -> float:
    """Resolve today's hard cap. Env var override wins."""
    override = os.environ.get("OKR_MONITOR_DAILY_LLM_CAP_USD")
    if override:
        try:
            return float(override)
        except ValueError:
            pass
    return _DEFAULT_CAP_USD if _today_iso() < _SPRINT_2_START_DATE else _SPRINT_2_PLUS_CAP_USD


def spent_today() -> float:
    """Sum of LLM cost recorded today via `record_spend`."""
    today = _today_iso()
    with store.connect() as conn:
        row = conn.execute(
            "SELECT value FROM kpi_daily WHERE day = ? AND metric = 'llm_cost_usd_today'",
            (today,),
        ).fetchone()
    return float(row["value"]) if row else 0.0


def check_or_raise() -> None:
    """Raise CircuitBreakerOpen if today's recorded spend is at or above the cap.

    Called at the top of `core.llm.complete()`. Skipped in dry-run mode by the
    caller. Returns silently when within budget.
    """
    cap = daily_cap_usd()
    spent = spent_today()
    if spent >= cap:
        raise CircuitBreakerOpen(
            f"Daily LLM cap ${cap:.2f} reached "
            f"(spent ${spent:.4f} today). Refusing further calls. "
            "Override with OKR_MONITOR_DAILY_LLM_CAP_USD=<n> if intentional."
        )


def record_spend(cost_usd: float) -> None:
    """Add to today's running total atomically (UPSERT with += semantics)."""
    if cost_usd <= 0:
        return
    today = _today_iso()
    with store.connect() as conn:
        conn.execute(
            "INSERT INTO kpi_daily(day, metric, value) VALUES(?, 'llm_cost_usd_today', ?)"
            " ON CONFLICT(day, metric) DO UPDATE SET value = value + excluded.value",
            (today, float(cost_usd)),
        )


def reset_today() -> None:
    """Reset today's running total to zero. Operator-only escape hatch — used
    by tests and by the daily KPI rollup if it wants to recompute from rows."""
    today = _today_iso()
    with store.connect() as conn:
        conn.execute(
            "DELETE FROM kpi_daily WHERE day = ? AND metric = 'llm_cost_usd_today'",
            (today,),
        )
