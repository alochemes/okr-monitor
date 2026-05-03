"""One-time seed: push the OKRs from TRACKER.md §2 into a fresh Notion
database under a parent page you control.

Run this exactly once after setting up the Notion integration. After
seeding, edit OKRs in Notion (not TRACKER.md). The daily pull will keep
TRACKER.md §2 in sync.

Required env (in `.env`):
  NOTION_API_KEY      — internal integration token
  NOTION_PARENT_PAGE_ID — the Notion page hosting the OKR DB; the
                          integration must be granted access

Usage:
  # Dry-run — print what would be created
  python scripts/notion_okr_seed.py

  # Actually create the DB and rows
  python scripts/notion_okr_seed.py --apply

  # Override the parent page from the CLI
  python scripts/notion_okr_seed.py --apply --parent-page-id <id>

The DB id is persisted to `data/workspaces/okrmonitor-internal/notion.json`
so subsequent pulls find it without re-asking.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Windows cmd defaults to cp1252 which chokes on `≥`, `—`, etc. that appear
# in our OKR text. Reconfigure stdout to UTF-8 so the dry-run preview can
# print every KR. No effect on the Notion API path (HTTP is UTF-8 already).
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

from core import notion_okr, tracker, workspace  # noqa: E402


def _print_dry_run() -> None:
    okrs = tracker.extract_okrs()
    total_krs = sum(len(o["krs"]) for o in okrs)
    print(f"Would create 1 Notion database with {total_krs} rows "
          f"across {len(okrs)} objectives:\n")
    for o in okrs:
        print(f"  O{o['objective_num']} — {o['objective']}")
        for kr in o["krs"]:
            print(f"    {kr['id']:>4}  {kr['description'][:70]}"
                  f"  ({kr['owner_pod']}, due {kr['due']})")
    print()
    print("Re-run with --apply to push to Notion.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="Actually call the Notion API. Without this, dry-run.")
    parser.add_argument("--parent-page-id", default=None,
                        help="Override NOTION_PARENT_PAGE_ID env.")
    parser.add_argument("--title", default="OKRs",
                        help="Title for the Notion database.")
    args = parser.parse_args()

    workspace.assert_internal()

    if not args.apply:
        _print_dry_run()
        return 0

    parent_id = (args.parent_page_id
                 or os.environ.get("NOTION_PARENT_PAGE_ID", "").strip())
    if not parent_id:
        print("ERR: NOTION_PARENT_PAGE_ID not set and --parent-page-id not "
              "provided.\n     See INSTRUCTIONS.md → 'Set up the OKR "
              "database' for how to get this value.", file=sys.stderr)
        return 2

    if not os.environ.get("NOTION_API_KEY"):
        print("ERR: NOTION_API_KEY not set in .env.", file=sys.stderr)
        return 2

    res = notion_okr.seed_database(parent_page_id=parent_id, title=args.title)
    print(json.dumps(res, indent=2))
    print()
    print(f"✓ Seed complete. {res['rows_created']} OKRs are now in Notion.")
    print(f"  Database id saved to "
          f"data/workspaces/{workspace.INTERNAL_WORKSPACE_ID}/notion.json")
    print()
    print("Next: paste this into .env so the daily pull can find it without "
          "re-reading workspace files:")
    print(f"  NOTION_OKR_DATABASE_ID={res['database_id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
