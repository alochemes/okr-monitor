"""Daily 7pm OWNER/FINANCE status report.

Orchestrator for the daily report:
  1. Refresh kr_signals + forecast (no LLM cost).
  2. Gather today's activity (events, mappings, proposals, spend).
  3. Run 4 reporter agents:
       CEO            → daily_status synopsis (today vs expected)
       CPO            → product_roadmap_report (current state + 2-week roadmap)
       CFO            → cost_projection (14-day spend forecast)
       analytics_ops  → growth_metrics (pilots, CAC, growth spend)
  4. Render the KPI dashboard as a markdown table.
  5. Assemble the OWNER/FINANCE report email body.
  6. Send via SMTP if configured, else write to reports/daily/YYYY-MM-DD/ only.
  7. Write the report to disk regardless of email status.

Usage:
  python scripts/daily_evening.py
  OKR_MONITOR_DRY_RUN=true python scripts/daily_evening.py    # safe / no API
  python scripts/daily_evening.py --date 2026-05-03           # backfill
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from datetime import date, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass

from agents.ceo import pipeline as ceo_pipe  # noqa: E402
from agents.cpo import pipeline as cpo_pipe  # noqa: E402
from agents.cfo import pipeline as cfo_pipe  # noqa: E402
from agents.analytics_ops import pipeline as analytics_pipe  # noqa: E402
from agents.signals_analyst import pipeline as signals_pipe  # noqa: E402
from agents.forecasting import pipeline as forecasting_pipe  # noqa: E402
from core import dashboard, kpi_status, mailer, store  # noqa: E402


# --------------------------------------------------------------------------
# Data gathering (all SQL — cheap, no LLM)

def _utc_window(d: date) -> tuple[str, str]:
    return (f"{d.isoformat()}T00:00:00+00:00", f"{d.isoformat()}T23:59:59.999999+00:00")


def _gather_today_activity(today: date) -> dict[str, Any]:
    start, end = _utc_window(today)
    with store.connect() as conn:
        events = conn.execute(
            "SELECT id, title, source FROM work_events"
            " WHERE occurred_at >= ? AND occurred_at <= ?"
            " ORDER BY occurred_at DESC LIMIT 50",
            (start, end),
        ).fetchall()
        mappings = conn.execute(
            "SELECT COUNT(*) AS n FROM event_kr_mappings WHERE created_at >= ?",
            (start,),
        ).fetchone()["n"]
        proposals = conn.execute(
            "SELECT id, agent, kind, title FROM proposals"
            " WHERE created_at >= ? AND created_at <= ?"
            " ORDER BY created_at DESC",
            (start, end),
        ).fetchall()
        spent_row = conn.execute(
            "SELECT value FROM kpi_daily WHERE day = ? AND metric = 'llm_cost_usd_today'",
            (today.isoformat(),),
        ).fetchone()
    return {
        "today": today.isoformat(),
        "events_today": len(events),
        "mappings_today": mappings,
        "proposals_today": len(proposals),
        "spend_today_usd": float(spent_row["value"]) if spent_row else 0.0,
        "event_titles": [e["title"][:80] for e in events[:10]],
        "proposal_titles": [
            f"{p['agent']}/{p['kind']}: {p['title'][:60]}" for p in proposals[:10]
        ],
    }


def _gather_cost_history(today: date, *, days: int = 14) -> dict[str, Any]:
    cutoff_day = (today - timedelta(days=days)).isoformat()
    cutoff_iso = f"{cutoff_day}T00:00:00+00:00"
    with store.connect() as conn:
        daily_rows = conn.execute(
            "SELECT day, value FROM kpi_daily"
            " WHERE metric = 'llm_cost_usd_today' AND day >= ?"
            " ORDER BY day",
            (cutoff_day,),
        ).fetchall()
        agent_rows = conn.execute(
            "SELECT agent, COUNT(*) AS calls,"
            " COALESCE(SUM(cost_usd), 0) AS total_usd"
            " FROM proposals WHERE created_at >= ?"
            " GROUP BY agent ORDER BY total_usd DESC",
            (cutoff_iso,),
        ).fetchall()
    return {
        "daily_spend": [{"day": r["day"], "usd": float(r["value"])} for r in daily_rows],
        "by_agent": [
            {"agent": r["agent"], "calls": r["calls"],
             "total_usd": float(r["total_usd"])}
            for r in agent_rows
        ],
    }


def _gather_growth_data(today: date) -> dict[str, Any]:
    """Pre-launch placeholder. Once a `pilots` table exists, query it."""
    return {
        "pilots_total": 0, "pilots_active": 0,
        "pilots_new_today": 0, "pilots_converting": 0,
        "growth_spend_ytd_usd": 0.0, "growth_spend_today_usd": 0.0,
        "outreach_today": {"emails_sent": 0, "linkedin_touches": 0,
                            "replies": 0, "meetings_booked": 0},
    }


# --------------------------------------------------------------------------
# Run reporters

def _safe_run(name: str, fn, **kwargs) -> dict[str, Any]:
    try:
        return {"name": name, "ok": True, "stats": fn(**kwargs)}
    except Exception as exc:
        return {"name": name, "ok": False, "error": str(exc),
                "trace": traceback.format_exc()}


# --------------------------------------------------------------------------
# Assemble report body

_VERDICT_HEADER_GLYPH = {"on_track": "🟢", "drifting": "🟡", "off": "🔴"}


def _fetch_proposal_body(proposal_id: str | None) -> str:
    if not proposal_id:
        return "_(no proposal — agent failed; see daily_evening output for trace)_"
    with store.connect() as conn:
        row = conn.execute(
            "SELECT body_md FROM proposals WHERE id = ?", (proposal_id,),
        ).fetchone()
    return row["body_md"] if row else "_(proposal id not found in DB)_"


def _build_report_body(
    *, today: date, activity: dict[str, Any],
    dashboard_md: str, results: dict[str, dict[str, Any]],
) -> str:
    def section(title: str, key: str) -> str:
        r = results.get(key, {})
        if not r.get("ok"):
            return (f"## {title}\n\n_⚠️ Agent failed:_ "
                    f"`{r.get('error', 'unknown')}`\n")
        body = _fetch_proposal_body(r["stats"].get("proposal_id"))
        return f"## {title}\n\n{body}\n"

    return "\n".join([
        f"# OKR Monitor — Daily OWNER/FINANCE — {today.isoformat()}",
        "",
        f"_Generated automatically at the daily 7pm cutover. "
        f"Activity today: {activity['events_today']} events · "
        f"{activity['mappings_today']} mappings · "
        f"{activity['proposals_today']} proposals · "
        f"spend ${activity['spend_today_usd']:.4f}._",
        "",
        "## Operational KPIs",
        "",
        f"_{kpi_status.summary_line()}_",
        "",
        kpi_status.render_md(),
        "",
        "## KR Dashboard (real-time)",
        "",
        dashboard_md,
        "",
        "---",
        "",
        section("CEO synopsis — today vs expected", "ceo"),
        "---",
        "",
        section("Product roadmap report", "cpo"),
        "---",
        "",
        section("Cost & token projection (next 14 days)", "cfo"),
        "---",
        "",
        section("Growth metrics", "analytics_ops"),
        "---",
        "",
        "_Repo: https://github.com/alochemes/okr-monitor_",
        f"_Today's audit log: data/audit/{today.isoformat()}.jsonl_",
        "_This is an automated report. Reply to andrew@skinmap.com._",
    ])


# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=date.fromisoformat, default=None,
                        help="Override 'today' for backfill.")
    parser.add_argument("--no-email", action="store_true",
                        help="Skip SMTP send even if configured.")
    args = parser.parse_args()
    today = args.date or date.today()

    out_dir = ROOT / "reports" / "daily" / today.isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)

    store.init_db()

    # Refresh signals + forecast so the dashboard reflects today's reality.
    try:
        signals_pipe.run()
        forecasting_pipe.run(today=today)
    except Exception as exc:    # pragma: no cover
        print(f"[warn] signals/forecast refresh failed: {exc}", file=sys.stderr)

    activity = _gather_today_activity(today)
    cost_history = _gather_cost_history(today)
    growth_data = _gather_growth_data(today)

    results = {
        "ceo": _safe_run("ceo", ceo_pipe.run_daily_status,
                         today=today, today_activity=activity),
        "cpo": _safe_run("cpo", cpo_pipe.run_product_roadmap_report,
                         today=today, activity=activity),
        "cfo": _safe_run("cfo", cfo_pipe.run_cost_projection,
                         today=today, cost_history=cost_history),
        "analytics_ops": _safe_run("analytics_ops", analytics_pipe.run,
                                   today=today, growth_data=growth_data),
    }

    dashboard_md = dashboard.render_kpi_dashboard_md()
    body = _build_report_body(
        today=today, activity=activity,
        dashboard_md=dashboard_md, results=results,
    )

    report_path = out_dir / "OWNER_FINANCE_REPORT.md"
    report_path.write_text(body, encoding="utf-8")

    if args.no_email:
        email_status: dict[str, Any] = {"sent": False, "reason": "--no-email flag set"}
    else:
        email_status = mailer.send_report_email(
            subject=(f"OKR Monitor — Daily OWNER/FINANCE — {today.isoformat()} · "
                     f"{dashboard.render_kpi_summary_line()}"),
            body_md=body,
        )

    summary = {
        "today": today.isoformat(),
        "report_path": report_path.relative_to(ROOT).as_posix(),
        "kpi_summary": dashboard.render_kpi_summary_line(),
        "activity": {
            "events": activity["events_today"],
            "mappings": activity["mappings_today"],
            "proposals": activity["proposals_today"],
            "spend_usd": activity["spend_today_usd"],
        },
        "agents": {
            k: {"ok": v["ok"], "proposal_id": v.get("stats", {}).get("proposal_id"),
                "error": v.get("error")}
            for k, v in results.items()
        },
        "email": email_status,
    }
    print(json.dumps(summary, indent=2, default=str))
    return 0 if all(r["ok"] for r in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
