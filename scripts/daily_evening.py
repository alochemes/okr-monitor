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

_AGENT_LABEL = {
    "ceo": "CEO synopsis — today vs expected",
    "cpo": "Product roadmap",
    "cfo": "Cost & token projection (next 14 days)",
    "analytics_ops": "Growth metrics",
}


def _fetch_proposal_body(proposal_id: str | None) -> str:
    if not proposal_id:
        return "_(no proposal — agent failed; see daily_evening output for trace)_"
    with store.connect() as conn:
        row = conn.execute(
            "SELECT body_md FROM proposals WHERE id = ?", (proposal_id,),
        ).fetchone()
    return row["body_md"] if row else "_(proposal id not found in DB)_"


def _is_dry_run_body(body: str) -> bool:
    return "DRY_RUN" in body[:500] or "_Confidence: 0.10_" in body


def _agent_headline(body: str) -> str:
    """One-line summary pulled from the agent body — first H1, or first
    non-blank prose line. Used in the TL;DR section instead of the full body."""
    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# "):
            return line[2:].strip()
        if line.startswith(("##", "**", "_", "-", "|")):
            continue
        return line[:140]
    return "_(empty)_"


def _kr_rollup() -> tuple[dict[str, int], list[dict[str, Any]]]:
    """Return (counts by verdict, list of stale/off KRs needing attention)."""
    rows = store.latest_kr_signals()
    counts: dict[str, int] = {}
    attention: list[dict[str, Any]] = []
    for r in rows:
        v = r["forecast_verdict"] or "qualitative"
        counts[v] = counts.get(v, 0) + 1
        if v in ("stale", "drifting", "off"):
            attention.append(dict(r))
    return counts, attention


def _kpi_alerts() -> list[dict[str, Any]]:
    """KPIs that aren't green — what the operator should look at first."""
    return [k for k in kpi_status.all_kpis() if k["status"] != "green"]


def _build_tldr(
    *, today: date, activity: dict[str, Any],
    kr_counts: dict[str, int], kpi_rows: list[dict[str, Any]],
    dry_run_count: int, total_agents: int,
) -> str:
    kpi_summary = kpi_status.summary_line()
    kr_parts = [f"{n} {v}" for v, n in sorted(kr_counts.items(), key=lambda kv: -kv[1])]
    kr_summary = " · ".join(kr_parts) if kr_parts else "no signals computed"
    kr_total = sum(kr_counts.values())

    cap_row = next((k for k in kpi_rows if k["id"] == "K1"), None)
    cap_value = cap_row["value"] if cap_row else f"${activity['spend_today_usd']:.4f}"

    lines = [
        "## TL;DR",
        "",
        f"- **KRs ({kr_total}):** {kr_summary}",
        f"- **Today:** {activity['events_today']} events · "
        f"{activity['mappings_today']} mappings · "
        f"{activity['proposals_today']} proposals",
        f"- **Spend:** {cap_value}",
        f"- **KPIs:** {kpi_summary}",
    ]
    if dry_run_count:
        lines.append(
            f"- **⚠️ Agent output: {dry_run_count}/{total_agents} stub (DRY_RUN)** — "
            "see warning below"
        )
    return "\n".join(lines)


def _build_dry_run_banner(dry_run_count: int, total_agents: int) -> str:
    if not dry_run_count:
        return ""
    if dry_run_count == total_agents:
        msg = "All agents fell through to stub responses."
    else:
        msg = f"{dry_run_count} of {total_agents} agents fell through to stub responses."
    return (
        "> ⚠️ **DRY_RUN — no live agent output.** " + msg + " "
        "Set `ANTHROPIC_API_KEY` in repo secrets to enable real synopsis: "
        "https://github.com/alochemes/okr-monitor/settings/secrets/actions"
    )


def _build_alerts_section(
    kpi_rows: list[dict[str, Any]],
    attention_krs: list[dict[str, Any]],
) -> str:
    if not kpi_rows and not attention_krs:
        return "## Alerts\n\n_All KPIs green and no KRs in attention zone._"

    glyph = {"yellow": "🟡", "red": "🔴", "unknown": "❓"}
    lines = ["## Alerts & action items", ""]
    for k in kpi_rows:
        lines.append(
            f"- {glyph.get(k['status'], '·')} **{k['id']}** {k['label']} — _{k['value']}_"
        )
    if attention_krs:
        lines.append("")
        lines.append("**KRs needing attention** (stale / drifting / off):")
        for r in attention_krs[:8]:
            v = r["forecast_verdict"]
            tgt = r["target_numeric"]
            cur = r["current_numeric"]
            req = r["pace_required"]
            days = r["days_remaining"]
            tgt_s = f"target {tgt:g}" if tgt is not None else ""
            cur_s = f"current {cur:g}" if cur is not None else "current 0"
            req_s = f"need {req:.2f}/d" if req is not None else ""
            days_s = f"{days}d left" if days is not None else ""
            tail = " · ".join(p for p in (tgt_s, cur_s, days_s, req_s) if p)
            lines.append(
                f"- {glyph.get('yellow', '·')} **KR {r['kr_id']}** ({v}) — {tail}"
            )
        if len(attention_krs) > 8:
            lines.append(f"- _…and {len(attention_krs) - 8} more (see Details)_")
    return "\n".join(lines)


def _build_agent_headlines(results: dict[str, dict[str, Any]]) -> str:
    """One-line headline per agent — shows the highest-signal sentence,
    not the full body. Full bodies live under Details."""
    lines = ["## Pod headlines", ""]
    for key, label in _AGENT_LABEL.items():
        r = results.get(key, {})
        if not r.get("ok"):
            lines.append(f"- **{label}** — ⚠️ failed: `{r.get('error', 'unknown')}`")
            continue
        body = _fetch_proposal_body(r["stats"].get("proposal_id"))
        if _is_dry_run_body(body):
            lines.append(f"- **{label}** — _(DRY_RUN stub — see banner above)_")
        else:
            lines.append(f"- **{label}** — {_agent_headline(body)}")
    return "\n".join(lines)


def _build_details_section(
    *, dashboard_md: str, results: dict[str, dict[str, Any]],
    show_agent_bodies: bool,
) -> str:
    parts: list[str] = ["## Details", "", "### Operational KPIs", "",
                        kpi_status.render_md(), "",
                        "### KR Dashboard (real-time)", "",
                        dashboard_md, ""]
    if show_agent_bodies:
        for key, label in _AGENT_LABEL.items():
            r = results.get(key, {})
            parts.append("---")
            parts.append("")
            parts.append(f"### {label}")
            parts.append("")
            if not r.get("ok"):
                parts.append(f"_⚠️ Agent failed:_ `{r.get('error', 'unknown')}`")
            else:
                parts.append(_fetch_proposal_body(r["stats"].get("proposal_id")))
            parts.append("")
    return "\n".join(parts)


def _build_report_body(
    *, today: date, activity: dict[str, Any],
    dashboard_md: str, results: dict[str, dict[str, Any]],
) -> str:
    # DRY_RUN detection — count how many agents fell through to stubs.
    dry_run_count = 0
    total_agents = 0
    for r in results.values():
        if r.get("ok") and r["stats"].get("proposal_id"):
            total_agents += 1
            body = _fetch_proposal_body(r["stats"]["proposal_id"])
            if _is_dry_run_body(body):
                dry_run_count += 1

    kr_counts, attention_krs = _kr_rollup()
    kpi_alerts = _kpi_alerts()
    all_dry = dry_run_count == total_agents and total_agents > 0

    sections: list[str] = [
        f"# OKR Monitor — Daily OWNER/FINANCE — {today.isoformat()}",
        "",
        f"_7pm cutover · spend ${activity['spend_today_usd']:.4f} · "
        f"{kpi_status.summary_line()} · {kr_counts.get('on_track', 0)}/"
        f"{sum(kr_counts.values())} KRs on track_",
        "",
    ]

    banner = _build_dry_run_banner(dry_run_count, total_agents)
    if banner:
        sections += [banner, ""]

    sections += [
        _build_tldr(today=today, activity=activity, kr_counts=kr_counts,
                    kpi_rows=kpi_alerts, dry_run_count=dry_run_count,
                    total_agents=total_agents),
        "",
        _build_alerts_section(kpi_alerts, attention_krs),
        "",
    ]

    # When everything is DRY_RUN the agent bodies add nothing. Show only the
    # headline list, hide the stub bodies entirely.
    sections += [_build_agent_headlines(results), ""]

    sections += [
        "---",
        "",
        _build_details_section(dashboard_md=dashboard_md, results=results,
                               show_agent_bodies=not all_dry),
        "",
        "---",
        "",
        f"_Full report file: reports/daily/{today.isoformat()}/OWNER_FINANCE_REPORT.md_",
        "_Repo: https://github.com/alochemes/okr-monitor_",
        f"_Today's audit log: data/audit/{today.isoformat()}.jsonl_",
        "_Reply to alochemes@gmail.com._",
    ]
    return "\n".join(sections)


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
