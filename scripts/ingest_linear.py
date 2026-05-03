"""Manual Linear ingestion CLI.

Usage:
    # Workspace-wide, last 7 days
    python scripts/ingest_linear.py

    # Just one team, longer window
    python scripts/ingest_linear.py --team ENG --since-days 30

Auth: set `LINEAR_API_KEY` in `.env` (personal API key from
https://linear.app/<workspace>/settings/api). Without it, this script no-ops
with a clear error.

Idempotency: schema-level `UNIQUE(source, source_event_id)` plus a state-aware
event id (e.g. `ENG-42@issue_completed`) — rerunning the script never creates
duplicates, but a state transition (opened → completed) does land as a new
event so the mapper can credit progress.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass

from core import linear_ingest, store  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--team", default=None,
                        help="Linear team key (e.g. ENG). Omit for workspace-wide.")
    parser.add_argument("--since-days", type=int, default=7)
    parser.add_argument("--page-cap", type=int, default=5,
                        help="Max GraphQL pages (50 issues/page).")
    args = parser.parse_args()

    store.init_db()

    if not linear_ingest.is_configured():
        print("[err] LINEAR_API_KEY not set in .env — nothing to do.",
              file=sys.stderr)
        return 2

    try:
        res = linear_ingest.poll_workspace(
            since_days=args.since_days,
            team_key=args.team,
            page_cap=args.page_cap,
        )
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        return 1

    print(json.dumps({"ok": True, **res}, indent=2))
    return 0 if not res.get("errors") else 1


if __name__ == "__main__":
    sys.exit(main())
