"""Operator KR scoreboard. Reads the latest kr_signals row per KR and prints
a compact dashboard. No LLM, no API.

Usage:
  python -m cli.status
  python -m cli.status --kr 1.3      # detail for one KR (recent mappings)
  python -m cli.status --json        # machine-readable
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402

from core import store  # noqa: E402

_VERDICT_DISPLAY = {
    "on_track":    "[green]on_track[/green]",
    "active":      "[green]active[/green]",
    "drifting":    "[yellow]drifting[/yellow]",
    "stale":       "[yellow]stale[/yellow]",
    "off":         "[red]off[/red]",
    "qualitative": "[dim]qual[/dim]",
}
_DASH = "-"   # ASCII-safe placeholder; Windows cmd defaults to cp1252 and chokes on em-dash


def _scoreboard() -> int:
    rows = store.latest_kr_signals()
    if not rows:
        Console().print("[dim]No kr_signals yet. Run scripts/run_signals_analyst.py and scripts/run_forecasting.py.[/dim]")
        return 0

    t = Table(title="KR scoreboard (latest signals)", show_lines=False, box=None)
    t.add_column("KR")
    t.add_column("Verdict", no_wrap=True)
    t.add_column("7d", justify="right")
    t.add_column("30d", justify="right")
    t.add_column("All", justify="right")
    t.add_column("Act", justify="right")
    t.add_column("Days", justify="right")
    t.add_column("Target", justify="right")
    t.add_column("Curr", justify="right")
    t.add_column("Req/d", justify="right")

    for r in rows:
        verdict = r["forecast_verdict"] or "qualitative"
        days = r["days_remaining"]
        days_s = _DASH if days is None else (str(days) if days >= 0 else f"[red]{days}[/red]")
        tgt = r["target_numeric"]
        cur = r["current_numeric"]
        req = r["pace_required"]
        t.add_row(
            r["kr_id"],
            _VERDICT_DISPLAY.get(verdict, verdict),
            str(r["events_7d"]),
            str(r["events_30d"]),
            str(r["events_total"]),
            str(r["distinct_actors"]),
            days_s,
            _DASH if tgt is None else f"{tgt:g}",
            _DASH if cur is None else f"{cur:g}",
            _DASH if req is None else f"{req:.2f}",
        )
    Console().print(t)
    return 0


def _kr_detail(kr_id: str) -> int:
    console = Console()
    rows = store.latest_kr_signals()
    sig = next((dict(r) for r in rows if r["kr_id"] == kr_id), None)
    if sig is None:
        console.print(f"[red]No signal yet for KR {kr_id}.[/red]")
        return 1

    console.print(f"[bold]KR {kr_id}[/bold] — verdict: "
                  f"{_VERDICT_DISPLAY.get(sig['forecast_verdict'] or 'qualitative', '?')}")
    console.print(
        f"  events: total={sig['events_total']}  7d={sig['events_7d']}  30d={sig['events_30d']}\n"
        f"  target={sig['target_numeric']}  current={sig['current_numeric']}  "
        f"due={sig['due_date']}  days_remaining={sig['days_remaining']}\n"
        f"  pace_required={sig['pace_required']}  pace_per_day={sig['pace_per_day']}"
    )
    console.print()
    mappings = store.list_mappings_for_kr(kr_id)
    if not mappings:
        console.print("[dim]No mappings yet.[/dim]")
        return 0
    console.print(f"[bold]Recent mappings ({len(mappings)} total):[/bold]")
    for m in mappings[:15]:
        console.print(
            f"  · [{m['source']}/{m['kind'] or '?'}] "
            f"{m['title'][:80]}  [dim]conf={m['confidence']:.2f}  by {m['actor'] or '?'}  "
            f"@ {m['occurred_at'][:19]}[/dim]"
        )
    if len(mappings) > 15:
        console.print(f"  ... +{len(mappings) - 15} older")
    return 0


def _json_dump() -> int:
    rows = store.latest_kr_signals()
    out = [dict(r) for r in rows]
    print(json.dumps(out, indent=2, default=str))
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--kr", type=str, default=None, help="Show detail for one KR.")
    p.add_argument("--json", action="store_true", help="Machine-readable output.")
    args = p.parse_args()
    if args.json:
        return _json_dump()
    if args.kr:
        return _kr_detail(args.kr)
    return _scoreboard()


if __name__ == "__main__":
    sys.exit(main())
