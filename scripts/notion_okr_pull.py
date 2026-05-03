"""Pull OKRs from Notion → cache + regenerate TRACKER.md §2.

Run after every meaningful edit in Notion, or let the daily evening cron
do it for you (`scripts/daily_evening.py` calls into this code path).

Usage:
  # Pull using NOTION_OKR_DATABASE_ID from env (or notion.json cache)
  python scripts/notion_okr_pull.py

  # Override the database id from the CLI
  python scripts/notion_okr_pull.py --database-id <id>

  # Pull but don't touch TRACKER.md (just refresh the JSON cache)
  python scripts/notion_okr_pull.py --no-tracker
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Windows console can't print non-cp1252 chars in OKR text. Force UTF-8 so
# the JSON output isn't truncated. No effect on the Notion API path.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):    # pragma: no cover
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass

from core import notion_okr, workspace  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-id", default=None,
                        help="Override NOTION_OKR_DATABASE_ID env / "
                             "data/workspaces/.../notion.json.")
    parser.add_argument("--no-tracker", action="store_true",
                        help="Skip TRACKER.md §2 regeneration (cache only).")
    args = parser.parse_args()

    workspace.assert_internal()

    res = notion_okr.pull_and_update(
        database_id=args.database_id,
        update_tracker=not args.no_tracker,
    )
    print(json.dumps(res, indent=2))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
