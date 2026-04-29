"""A/B experiment report for the marketing landing page.

Pulls PostHog event data for the configured experiments, computes
exposures/conversions/lift per variant + a two-proportion z-test for
significance, and writes a markdown report at reports/ab/YYYY-MM-DD.md.

Same dry-run-first ethos as the rest of the system: if `POSTHOG_API_KEY`
isn't set, the script falls back to a stub report explaining how to
enable it. The cron / GitHub Actions workflow still fires; the operator
just sees "not configured" instead of a crash.

Usage:
  python scripts/run_ab_report.py                # last 14 days
  python scripts/run_ab_report.py --days 30
  python scripts/run_ab_report.py --json         # machine-readable
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass


# Experiment registry — keep in sync with web/components/Hero.tsx.
EXPERIMENTS: list[dict[str, Any]] = [
    {
        "key": "hero_headline",
        "title": "Hero Headline",
        "variants": ["control", "variant_a", "variant_b"],
        "control": "control",
        "conversion_event": "waitlist_signup",
    },
    {
        "key": "hero_cta",
        "title": "Hero CTA",
        "variants": ["control", "variant_a", "variant_b"],
        "control": "control",
        "conversion_event": "waitlist_signup",
    },
]


# ---------------------------------------------------------------------------
# PostHog HogQL client (no SDK — stdlib urllib so this script has no deps)


def _ph_query(host: str, project_id: str, api_key: str, hogql: str) -> list[list[Any]]:
    """Run a HogQL query and return the rows. Raises on HTTP error."""
    url = f"{host.rstrip('/')}/api/projects/{project_id}/query/"
    body = json.dumps({"query": {"kind": "HogQLQuery", "query": hogql}}).encode("utf-8")
    req = Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    with urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload.get("results", []) or []


def _exposures_hogql(flag_key: str, days: int) -> str:
    return f"""
        SELECT properties.$feature_flag_response AS variant,
               count(DISTINCT distinct_id) AS n
        FROM events
        WHERE event = '$experiment_started'
          AND properties.$feature_flag = '{flag_key}'
          AND timestamp >= now() - INTERVAL {days} DAY
        GROUP BY variant
        ORDER BY variant
    """


def _conversions_hogql(flag_key: str, conv_event: str, days: int) -> str:
    # Attribute each converter to the variant they saw on $experiment_started.
    return f"""
        SELECT properties.$feature_flag_response AS variant,
               count(DISTINCT distinct_id) AS n
        FROM events
        WHERE event = '$experiment_started'
          AND properties.$feature_flag = '{flag_key}'
          AND timestamp >= now() - INTERVAL {days} DAY
          AND distinct_id IN (
            SELECT DISTINCT distinct_id FROM events
            WHERE event = '{conv_event}'
              AND timestamp >= now() - INTERVAL {days} DAY
          )
        GROUP BY variant
        ORDER BY variant
    """


# ---------------------------------------------------------------------------
# Stats — two-proportion z-test, stdlib only


def _two_prop_z(c_a: int, n_a: int, c_b: int, n_b: int) -> float:
    if n_a == 0 or n_b == 0:
        return float("nan")
    p_a = c_a / n_a
    p_b = c_b / n_b
    p = (c_a + c_b) / (n_a + n_b)
    se = math.sqrt(p * (1 - p) * (1 / n_a + 1 / n_b))
    if se == 0:
        return float("nan")
    return (p_b - p_a) / se


def _two_tailed_p(z: float) -> float:
    """Two-tailed p-value. Uses math.erfc; no scipy dependency."""
    if math.isnan(z):
        return float("nan")
    return math.erfc(abs(z) / math.sqrt(2))


def _significance_label(p: float) -> str:
    if math.isnan(p):
        return "n/a"
    if p < 0.01:
        return "** highly significant (p<0.01)"
    if p < 0.05:
        return "*  significant (p<0.05)"
    if p < 0.10:
        return ".  trending (p<0.10)"
    return "   not significant"


# ---------------------------------------------------------------------------
# Data collection


def _collect_one(
    *,
    exp: dict[str, Any],
    days: int,
    host: str,
    project_id: str,
    api_key: str,
) -> dict[str, Any]:
    exposures: dict[str, int] = {}
    conversions: dict[str, int] = {}

    try:
        for variant, n in _ph_query(
            host, project_id, api_key, _exposures_hogql(exp["key"], days)
        ):
            if variant:
                exposures[str(variant)] = int(n or 0)
        for variant, n in _ph_query(
            host, project_id, api_key, _conversions_hogql(
                exp["key"], exp["conversion_event"], days
            )
        ):
            if variant:
                conversions[str(variant)] = int(n or 0)
    except (HTTPError, URLError, json.JSONDecodeError) as err:
        return {
            "key": exp["key"],
            "error": f"PostHog query failed: {err}",
            "exposures": {},
            "conversions": {},
        }

    # Compute per-variant rate + lift vs control.
    control = exp["control"]
    c_n = exposures.get(control, 0)
    c_c = conversions.get(control, 0)
    c_rate = (c_c / c_n) if c_n else 0.0

    rows = []
    for variant in exp["variants"]:
        n = exposures.get(variant, 0)
        c = conversions.get(variant, 0)
        rate = (c / n) if n else 0.0
        if variant == control or c_n == 0:
            lift = None
            z = float("nan")
            p = float("nan")
        else:
            lift = (rate - c_rate) / c_rate if c_rate else None
            z = _two_prop_z(c_c, c_n, c, n)
            p = _two_tailed_p(z)
        rows.append({
            "variant": variant, "is_control": variant == control,
            "exposures": n, "conversions": c, "rate": rate,
            "lift_vs_control": lift,
            "z": z, "p": p,
            "significance": _significance_label(p),
        })

    # Pick a winner (highest rate among variants with n >= min_n AND p < 0.05).
    MIN_N = 100
    qualifiers = [r for r in rows if r["exposures"] >= MIN_N]
    sig_winners = [r for r in qualifiers if not r["is_control"] and (
        not math.isnan(r["p"]) and r["p"] < 0.05 and r["rate"] > c_rate
    )]
    winner = max(sig_winners, key=lambda r: r["rate"]) if sig_winners else None

    return {
        "key": exp["key"], "title": exp["title"],
        "conversion_event": exp["conversion_event"],
        "rows": rows,
        "control_rate": c_rate,
        "winner": winner["variant"] if winner else None,
        "min_n_per_variant": MIN_N,
    }


# ---------------------------------------------------------------------------
# Markdown rendering


def _pct(x: float | None) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    return f"{x * 100:.2f}%"


def _signed_pct(x: float | None) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    return f"{x * 100:+.1f}%"


def _render_md(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# A/B Report — {report['today']} (last {report['days']} days)")
    lines.append("")
    if report.get("not_configured"):
        lines.append(report["not_configured_message"])
        lines.append("")
        return "\n".join(lines)

    lines.append(
        f"_Source: {report['host']} · project `{report['project_id']}` · "
        f"window: trailing {report['days']} days._"
    )
    lines.append("")

    for r in report["experiments"]:
        lines.append(f"## {r['title']} (`{r['key']}`)")
        lines.append("")
        if r.get("error"):
            lines.append(f"> ⚠️ {r['error']}")
            lines.append("")
            continue
        lines.append("| Variant | Exposures | Conversions | Rate | Lift | p-value | Significance |")
        lines.append("|---|---:|---:|---:|---:|---:|---|")
        for row in r["rows"]:
            tag = " (control)" if row["is_control"] else ""
            lines.append(
                f"| {row['variant']}{tag} | {row['exposures']} | {row['conversions']} | "
                f"{_pct(row['rate'])} | "
                f"{_signed_pct(row['lift_vs_control']) if not row['is_control'] else '—'} | "
                f"{_pct(row['p']) if not math.isnan(row['p']) else '—'} | "
                f"{row['significance']} |"
            )
        lines.append("")
        if r["winner"]:
            lines.append(f"**Winner:** `{r['winner']}` — significant lift, sample sufficient.")
        else:
            lines.append(
                f"_No significant winner yet. Min sample needed per variant: "
                f"{r['min_n_per_variant']} exposures + p<0.05._"
            )
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("_Significance levels: `**` p<0.01 · `*` p<0.05 · `.` p<0.10._")
    lines.append("_Two-proportion z-test, two-tailed. Conversion event: distinct visitor signed up to the waitlist._")
    return "\n".join(lines)


# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=14, help="Lookback window in days.")
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout instead of writing markdown.")
    args = parser.parse_args()

    today = date.today()
    api_key = os.environ.get("POSTHOG_API_KEY", "").strip()
    project_id = os.environ.get("POSTHOG_PROJECT_ID", "").strip()
    host = os.environ.get("POSTHOG_HOST", "https://us.i.posthog.com").strip()

    out_dir = ROOT / "reports" / "ab"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{today.isoformat()}.md"

    if not api_key or not project_id:
        report = {
            "today": today.isoformat(),
            "days": args.days,
            "not_configured": True,
            "not_configured_message": (
                "**A/B reporting is not configured yet.** To enable:\n\n"
                "1. Create a PostHog account (or use existing).\n"
                "2. In PostHog → Project settings → API keys, create a "
                "**Personal API key** with `query:read` scope.\n"
                "3. Add to local `.env`:\n"
                "   ```\n"
                "   POSTHOG_API_KEY=phx_...        # personal API key\n"
                "   POSTHOG_PROJECT_ID=12345       # numeric project id\n"
                "   POSTHOG_HOST=https://us.i.posthog.com   # or eu.i.posthog.com\n"
                "   ```\n"
                "4. Add `NEXT_PUBLIC_POSTHOG_KEY=phc_...` (the project key, not personal) "
                "to `web/.env.local` so the landing page actually emits events.\n"
                "5. In PostHog → Feature flags, create:\n"
                "   - `hero_headline` with variants `control` / `variant_a` / `variant_b`, equal split.\n"
                "   - `hero_cta` with variants `control` / `variant_a` / `variant_b`, equal split.\n"
                "6. Re-run this script. First report shows up after ~100 exposures per variant.\n"
            ),
        }
    else:
        per_exp = []
        for exp in EXPERIMENTS:
            per_exp.append(_collect_one(
                exp=exp, days=args.days,
                host=host, project_id=project_id, api_key=api_key,
            ))
        report = {
            "today": today.isoformat(),
            "days": args.days,
            "host": host,
            "project_id": project_id,
            "experiments": per_exp,
        }

    if args.json:
        print(json.dumps(report, indent=2, default=str))
        return 0

    md = _render_md(report)
    out_path.write_text(md, encoding="utf-8")
    print(json.dumps({
        "today": today.isoformat(),
        "report_path": str(out_path.relative_to(ROOT)).replace("\\", "/"),
        "configured": not report.get("not_configured"),
        "experiments": [r.get("key") for r in report.get("experiments", [])] if not report.get("not_configured") else [],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
