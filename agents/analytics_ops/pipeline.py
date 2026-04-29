"""Analytics-Ops pipeline. Daily growth_metrics report.

Reads pilot/customer/spend data passed in by the orchestrator (no pilots
table exists yet — pre-launch state returns 'no customers' verdict)."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from agents._proposal import run_proposal

_AGENT = "analytics_ops"
_KIND = "growth_metrics"
_PROMPT = (Path(__file__).parent / "prompts" / "growth_metrics.md").read_text(encoding="utf-8")


def _user_message(today: date, *, growth_data: dict[str, Any] | None = None) -> str:
    growth_data = growth_data or {}
    return (
        f"Today is {today.isoformat()}.\n\n"
        f"## Growth data (live data)\n"
        f"- Pilots total: {growth_data.get('pilots_total', 0)}\n"
        f"- Pilots active: {growth_data.get('pilots_active', 0)}\n"
        f"- New pilots today: {growth_data.get('pilots_new_today', 0)}\n"
        f"- Growth spend YTD: ${growth_data.get('growth_spend_ytd_usd', 0.0):.2f}\n"
        f"- Growth spend today: ${growth_data.get('growth_spend_today_usd', 0.0):.2f}\n"
        f"- Outreach today: {growth_data.get('outreach_today', {})}\n\n"
        "Reply with ONLY the JSON object specified in the schema."
    )


def _format_body_md(parsed: dict[str, Any], raw_text: str) -> str:
    if not parsed:
        return f"_(unparsed)_\n\n```\n{raw_text}\n```"
    lines = [f"# {parsed.get('title', '(no title)')}", "",
             parsed.get("summary", "").strip(), ""]
    lines.append(f"**Stage:** {parsed.get('stage', 'unknown')}")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Pilots total | {parsed.get('pilots_total', 0)} |")
    lines.append(f"| Pilots active | {parsed.get('pilots_active', 0)} |")
    lines.append(f"| Pilots new today | {parsed.get('pilots_new_today', 0)} |")
    lines.append(f"| Pilots converting | {parsed.get('pilots_converting', 0)} |")
    lines.append(f"| Growth spend YTD | ${parsed.get('growth_spend_ytd_usd', 0.0):.2f} |")
    lines.append(f"| Growth spend today | ${parsed.get('growth_spend_today_usd', 0.0):.2f} |")
    cac = parsed.get("cac_blended_usd")
    lines.append(f"| Blended CAC | {'n/a' if cac is None else f'${cac:.2f}'} |")
    lines.append("")
    if cac_chan := parsed.get("cac_by_channel"):
        lines.append("## CAC by channel")
        lines.append("| Channel | Spend | Pilots | CAC |")
        lines.append("|---|---:|---:|---:|")
        for c in cac_chan:
            cac_v = c.get("cac_usd")
            lines.append(f"| {c.get('channel', '?')} | ${c.get('spend_usd', 0):.2f} | "
                         f"{c.get('pilots', 0)} | {'n/a' if cac_v is None else f'${cac_v:.2f}'} |")
        lines.append("")
    if outreach := parsed.get("outreach_today"):
        lines.append("## Outreach today")
        for k, v in outreach.items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    if issues := parsed.get("flagged_issues"):
        lines.append("## Flagged issues")
        lines.extend(f"- {i}" for i in issues)
        lines.append("")
    if action := parsed.get("recommended_action"):
        lines.append(f"**Recommended action:** {action}")
        lines.append("")
    if (conf := parsed.get("confidence")) is not None:
        lines.append(f"_Confidence: {conf:.2f}_")
    if parsed.get("reasoning"):
        lines.append(f"_Reasoning: {parsed['reasoning']}_")
    return "\n".join(lines)


def run(*, today: date | None = None,
        growth_data: dict[str, Any] | None = None) -> dict[str, Any]:
    return run_proposal(
        agent=_AGENT, kind=_KIND, prompt=_PROMPT,
        user_message_fn=lambda t: _user_message(t, growth_data=growth_data),
        body_md_fn=_format_body_md,
        today=today,
    )
