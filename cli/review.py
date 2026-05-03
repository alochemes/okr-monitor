"""Operator review CLI for pending agent proposals.

Usage:
  python -m cli.review            # interactive review of the oldest pending
  python -m cli.review --list     # list all pending proposals (no action)
  python -m cli.review --all      # review every pending proposal in order

Decisions: approve | edit | reject | defer
- approve: take the proposal as-is. Recorded with edit_distance = 0.
- edit:    operator edits the markdown in $EDITOR (or notepad on Windows). The
           edited final_text is stored; edit_distance is computed.
- reject:  proposal is filed but not actioned.
- defer:   leave it in the queue for now (no review row written).
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich.console import Console  # noqa: E402
from rich.markdown import Markdown  # noqa: E402
from rich.panel import Panel  # noqa: E402
from rich.table import Table  # noqa: E402

from core import store  # noqa: E402

_OPERATOR = os.environ.get("OPERATOR_EMAIL", "alochemes@gmail.com")
_console = Console()


def _editor() -> str:
    return os.environ.get("EDITOR") or ("notepad" if os.name == "nt" else "nano")


def _open_in_editor(text: str) -> str:
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
        path = f.name
    try:
        subprocess.call([_editor(), path])
        return Path(path).read_text(encoding="utf-8")
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def _edit_distance(a: str, b: str) -> float:
    """Cheap normalized distance: 1 - (longest common subsequence ratio).
    Avoids a Levenshtein dependency. Good enough as a "did this change a lot?"
    signal for operator-trust telemetry."""
    if a == b:
        return 0.0
    if not a:
        return 1.0
    # Use difflib's ratio (Python stdlib); 1 - ratio is a normalized distance.
    from difflib import SequenceMatcher
    return round(1.0 - SequenceMatcher(None, a, b).ratio(), 4)


def _list(rows: list) -> None:
    if not rows:
        _console.print("[dim]No pending proposals.[/dim]")
        return
    t = Table(title="Pending proposals", show_lines=False)
    t.add_column("#", justify="right")
    t.add_column("Agent")
    t.add_column("Kind")
    t.add_column("Title")
    t.add_column("Conf", justify="right")
    t.add_column("Created")
    for i, r in enumerate(rows, 1):
        conf = r["confidence"]
        conf_s = f"{conf:.2f}" if conf is not None else "—"
        t.add_row(
            str(i),
            r["agent"],
            r["kind"],
            (r["title"] or "")[:80],
            conf_s,
            (r["created_at"] or "")[:19],
        )
    _console.print(t)


def _review_one(row) -> bool:
    """Return True if a review row was written (approve/edit/reject), False on
    defer or skip."""
    _console.rule(f"[bold]{row['agent']} · {row['kind']}[/bold]")
    _console.print(Panel.fit(
        f"[dim]proposal_id:[/dim] {row['proposal_id']}\n"
        f"[dim]model:[/dim] {row['model']}\n"
        f"[dim]created:[/dim] {row['created_at']}\n"
        f"[dim]confidence:[/dim] {row['confidence']}",
    ))
    _console.print(Markdown(row["body_md"]))
    _console.print()
    started = time.monotonic()
    while True:
        choice = _console.input(
            "[bold]Decision[/bold] (a)pprove · (e)dit · (r)eject · (d)efer · (s)kip · (q)uit > "
        ).strip().lower()
        if choice in ("a", "approve"):
            store.write_proposal_review(
                proposal_id=row["proposal_id"], decision="approve",
                final_text=None, edit_distance=0.0,
                time_to_review_s=int(time.monotonic() - started),
                reviewed_by=_OPERATOR, notes=None,
            )
            _console.print("[green]Approved.[/green]")
            return True
        if choice in ("e", "edit"):
            edited = _open_in_editor(row["body_md"])
            ed = _edit_distance(row["body_md"], edited)
            store.write_proposal_review(
                proposal_id=row["proposal_id"], decision="edit",
                final_text=edited, edit_distance=ed,
                time_to_review_s=int(time.monotonic() - started),
                reviewed_by=_OPERATOR, notes=None,
            )
            _console.print(f"[green]Edit recorded.[/green] [dim](edit_distance={ed})[/dim]")
            return True
        if choice in ("r", "reject"):
            note = _console.input("Reason (optional): ").strip() or None
            store.write_proposal_review(
                proposal_id=row["proposal_id"], decision="reject",
                final_text=None, edit_distance=None,
                time_to_review_s=int(time.monotonic() - started),
                reviewed_by=_OPERATOR, notes=note,
            )
            _console.print("[yellow]Rejected.[/yellow]")
            return True
        if choice in ("d", "defer"):
            _console.print("[dim]Deferred — left in queue.[/dim]")
            return False
        if choice in ("s", "skip"):
            return False
        if choice in ("q", "quit"):
            raise SystemExit(0)
        _console.print("[red]Unknown choice. Try again.[/red]")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--list", action="store_true", help="List pending proposals and exit.")
    p.add_argument("--all", action="store_true", help="Review every pending proposal in order.")
    args = p.parse_args()

    rows = store.list_pending_proposals(limit=200)
    if args.list:
        _list(rows)
        return 0
    if not rows:
        _console.print("[dim]No pending proposals.[/dim]")
        return 0
    if args.all:
        for r in rows:
            _review_one(r)
        return 0
    _review_one(rows[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
