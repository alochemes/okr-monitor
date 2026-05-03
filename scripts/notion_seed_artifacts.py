"""Seed our internal Notion workspace with the customer-flow artifacts —
filled out as if OKR Monitor were itself a pilot. We are pilot #0 (dogfood).

What this creates under `NOTION_PARENT_PAGE_ID`:

  - "Intake — YYYY-MM-DD"   — the full pilot intake questionnaire (blank,
                              ready for the operator to fill out)
  - "5-in-5 — YYYY-MM-DD"   — the standalone fillable 5-in-5 worksheet

These pages live in OUR Notion workspace under OUR parent page. They are
NOT the templates — the templates stay clean in `notion/03_playbooks/`.
What we push here is the operator's *fillable instance* — the same shape
each pilot will get in their own Notion later (Sprint 1 wires that flow).

Idempotency note: re-running creates new pages alongside the old ones —
Notion has no "upsert by title" primitive. Run once. If you want to redo,
delete the existing pages in Notion first.

Usage:
  # Dry-run — prints what would be created, no API call.
  python scripts/notion_seed_artifacts.py

  # Apply.
  python scripts/notion_seed_artifacts.py --apply

  # Override the parent page from the CLI (defaults to NOTION_PARENT_PAGE_ID env).
  python scripts/notion_seed_artifacts.py --apply --parent-page-id <id>

  # Skip one of the artifacts.
  python scripts/notion_seed_artifacts.py --apply --no-intake
  python scripts/notion_seed_artifacts.py --apply --no-5in5
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

# Force UTF-8 stdout so the dry-run preview doesn't crash on non-ASCII.
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

from core import notion_okr, notion_pages, workspace  # noqa: E402


_INTAKE_TEMPLATE = ROOT / "notion" / "03_playbooks" / "04_pilot_intake_questionnaire.md"


# Standalone fillable 5-in-5 worksheet. Lifted from
# `notion/03_playbooks/01_customer_okr_kpi_framework.md` §4 + §10B and
# tightened into a pure-form artifact so it can stand alone in Notion.
_FIVE_IN_FIVE = """\
# 5-in-5 worksheet

> Pick **one** Objective for the current quarter. Set a 5-minute timer. Write 5 candidate Key Results for that Objective. Don't edit, don't debate, don't look at others' drafts. Fast and rough.
>
> If multiple people are doing this, **everyone runs it separately** before the kickoff and brings their drafts. Refine in the room.

---

## Round 1 — 5 minutes (silent, no editing)

**Objective for this quarter:**

(write here — qualitative, ambitious, time-bound, outcome not activity)

---

**Candidate KR 1:**

(write here)

**Candidate KR 2:**

(write here)

**Candidate KR 3:**

(write here)

**Candidate KR 4:**

(write here)

**Candidate KR 5:**

(write here)

---

## Round 2 — 10 minutes (read aloud, cluster)

Cluster duplicates. The room produces 8–15 unique candidates.

**Clustered candidates:**

(write here — bullet list)

---

## Round 3 — 5 minutes (vote)

Each person picks their top 3. Tally.

**Top-voted candidates:**

(write here — top 3 by vote count)

---

## Round 4 — pick

Pressure-test each top-voted candidate against the 6 KR rules:

1. Numeric — has a number, a unit, and a deadline
2. Observable in a system you already have
3. Outcome metric, not vanity metric
4. One KR = one number (no `and`s)
5. ≤5 KRs per Objective
6. ≤5 Objectives per company per quarter

If a top-voted KR fails a rule, fix it on the spot or drop it.

---

## Final KRs (canonical shape)

> [Verb] [metric] from [baseline] to [target] by [date]

**KR-1:**

(write here)

**KR-2:**

(write here)

**KR-3:**

(write here)

---

## Examples (reference only — do not copy)

- Increase pilot-to-paid conversion from 0% to 25% by 2026-08-28.
- Reduce p95 API latency from 320ms to 150ms by 2026-06-30.
- Raise NPS from 12 to 50 (5 design partners) by 2026-05-26.

---

## What happens after

When the worksheet is filled out, compare your KRs to what's currently in TRACKER.md §2 / the Notion OKR database. The surprises are signal — adjust the OKRs in Notion (the daily pull will then regenerate TRACKER.md). This *is* the dogfood loop.
"""


def _intake_markdown() -> str:
    """Read the intake template, prepend a small framing for our own use."""
    body = _INTAKE_TEMPLATE.read_text(encoding="utf-8")
    framing = (
        "> **OKR Monitor's own intake — eat-our-own-cooking copy.** "
        "Filled out as if OKR Monitor were a pilot at OKR Monitor. "
        "The template this came from lives at "
        "`notion/03_playbooks/04_pilot_intake_questionnaire.md` and stays "
        "blank for actual pilots.\n\n"
        "---\n\n"
    )
    return framing + body


def _print_dry_run(parent_page_id: str | None,
                    do_intake: bool, do_5in5: bool) -> None:
    print(f"Parent page: {parent_page_id or '(unset)'}")
    print()
    if do_intake:
        if not _INTAKE_TEMPLATE.exists():
            print(f"  - SKIP intake — template not found at {_INTAKE_TEMPLATE}")
        else:
            md = _intake_markdown()
            blocks = notion_pages.md_to_blocks(md)
            print(f"  - Intake — {date.today().isoformat()} "
                  f"({len(md)} chars, {len(blocks)} Notion blocks)")
    if do_5in5:
        blocks = notion_pages.md_to_blocks(_FIVE_IN_FIVE)
        print(f"  - 5-in-5 — {date.today().isoformat()} "
              f"({len(_FIVE_IN_FIVE)} chars, {len(blocks)} Notion blocks)")
    print()
    print("Re-run with --apply to push these to Notion.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="Actually call the Notion API. Without this, dry-run.")
    parser.add_argument("--parent-page-id", default=None,
                        help="Override NOTION_PARENT_PAGE_ID env.")
    parser.add_argument("--no-intake", action="store_true")
    parser.add_argument("--no-5in5", action="store_true")
    args = parser.parse_args()

    workspace.assert_internal()

    parent_id = (args.parent_page_id
                 or os.environ.get("NOTION_PARENT_PAGE_ID", "").strip())
    do_intake = not args.no_intake
    do_5in5 = not args.no_5in5

    if not args.apply:
        _print_dry_run(parent_id or None, do_intake, do_5in5)
        return 0

    if not parent_id:
        print("ERR: NOTION_PARENT_PAGE_ID not set and --parent-page-id not "
              "provided.", file=sys.stderr)
        return 2
    if not os.environ.get("NOTION_API_KEY"):
        print("ERR: NOTION_API_KEY not set in .env.", file=sys.stderr)
        return 2

    today = date.today().isoformat()
    created: dict[str, dict] = {}

    if do_intake:
        if not _INTAKE_TEMPLATE.exists():
            print(f"ERR: intake template missing at {_INTAKE_TEMPLATE}",
                  file=sys.stderr)
            return 1
        page = notion_pages.push_markdown_subpage(
            parent_page_id=parent_id,
            title=f"Intake — {today}",
            markdown=_intake_markdown(),
        )
        created["intake"] = {"id": page["id"], "url": page.get("url")}
        print(f"  ✓ intake:  {page.get('url')}")

    if do_5in5:
        page = notion_pages.push_markdown_subpage(
            parent_page_id=parent_id,
            title=f"5-in-5 — {today}",
            markdown=_FIVE_IN_FIVE,
        )
        created["five_in_five"] = {"id": page["id"], "url": page.get("url")}
        print(f"  ✓ 5-in-5:  {page.get('url')}")

    # Persist the new page IDs into the workspace's notion.json so future
    # tooling (e.g. an answers-puller in Sprint 1) finds them.
    ids = notion_okr.load_notion_ids()
    ids.setdefault("artifacts", {}).update(created)
    notion_okr.save_notion_ids()    # ensures file exists
    notion_path = workspace.artifact_path("notion.json")
    notion_path.write_text(json.dumps(ids, indent=2), encoding="utf-8")

    print()
    print(f"Saved page ids to {notion_path}")
    print()
    print("Open the parent page in Notion — both new sub-pages will appear "
          "under it. Fill them out as you would any pilot intake.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
