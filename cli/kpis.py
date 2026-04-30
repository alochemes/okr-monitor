"""Operator KPI dashboard — live status of K1–K10.

Usage:
  python -m cli.kpis              # full status table
  python -m cli.kpis --summary    # one-line summary
  python -m cli.kpis --json       # machine-readable
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402

from core import kpi_status  # noqa: E402

_GLYPH = {
    "green":   "[green]ok[/green]",
    "yellow":  "[yellow]warn[/yellow]",
    "red":     "[red]ALERT[/red]",
    "unknown": "[dim]?[/dim]",
}


def _table() -> int:
    rows = kpi_status.all_kpis()
    t = Table(title=f"KPI status: {kpi_status.summary_line()}",
              show_lines=False, box=None)
    t.add_column("ID", no_wrap=True)
    t.add_column("Status", no_wrap=True)
    t.add_column("KPI")
    t.add_column("Value")
    t.add_column("Target")
    for r in rows:
        t.add_row(
            r["id"],
            _GLYPH.get(r["status"], "?"),
            r["label"][:40],
            r["value"][:50],
            r["target"][:30],
        )
    Console().print(t)
    return 0


def _summary() -> int:
    print(kpi_status.summary_line())
    return 0


def _dump_json() -> int:
    print(json.dumps(kpi_status.all_kpis(), indent=2, default=str))
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--summary", action="store_true", help="One-line summary.")
    p.add_argument("--json", action="store_true", help="Machine-readable.")
    args = p.parse_args()
    if args.json:
        return _dump_json()
    if args.summary:
        return _summary()
    return _table()


if __name__ == "__main__":
    sys.exit(main())
