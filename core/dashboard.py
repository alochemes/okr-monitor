"""Render the KR scoreboard as markdown for inclusion in reports / emails.

This is the "real-time KPI dashboard" the operator sees at the top of the
daily 7pm OWNER/FINANCE email and at the top of any report we publish.
"""

from __future__ import annotations

from core import store


_VERDICT_GLYPH = {
    "on_track":    "🟢 on_track",
    "active":      "🟢 active",
    "drifting":    "🟡 drifting",
    "stale":       "🟡 stale",
    "off":         "🔴 off",
    "qualitative": "— qual",
}


def render_kpi_dashboard_md() -> str:
    """Markdown table of the latest signal per KR. One row per KR."""
    rows = store.latest_kr_signals()
    if not rows:
        return ("_No KR signals computed yet. Run "
                "`python scripts/run_signals_analyst.py` and "
                "`python scripts/run_forecasting.py` to populate._")

    lines = [
        "| KR | Verdict | 7d | 30d | All | Days left | Target | Current | Req/d |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        verdict = r["forecast_verdict"] or "qualitative"
        days = r["days_remaining"]
        days_s = "—" if days is None else str(days)
        tgt = r["target_numeric"]
        cur = r["current_numeric"]
        req = r["pace_required"]
        lines.append(
            f"| {r['kr_id']} | {_VERDICT_GLYPH.get(verdict, verdict)} | "
            f"{r['events_7d']} | {r['events_30d']} | {r['events_total']} | "
            f"{days_s} | "
            f"{'—' if tgt is None else f'{tgt:g}'} | "
            f"{'—' if cur is None else f'{cur:g}'} | "
            f"{'—' if req is None else f'{req:.2f}'} |"
        )
    return "\n".join(lines)


def render_kpi_summary_line() -> str:
    """One-line scoreboard summary for an email subject or short heading.

    Example: '17 KRs · 6 stale · 1 active · 10 qualitative'
    """
    rows = store.latest_kr_signals()
    if not rows:
        return "0 KRs computed"
    by_verdict: dict[str, int] = {}
    for r in rows:
        v = r["forecast_verdict"] or "qualitative"
        by_verdict[v] = by_verdict.get(v, 0) + 1
    parts = [f"{len(rows)} KRs"] + [f"{n} {v}" for v, n in sorted(by_verdict.items())]
    return " · ".join(parts)
