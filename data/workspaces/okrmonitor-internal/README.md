# `okrmonitor-internal/` — our own workspace (dogfood)

This is OKR Monitor's own organizational data, treated like a customer
account by the code paths it flows through. We are workspace #1; this
directory is the cache layer between our Notion workspace (canonical) and
the Python brain (read path).

## What lives here

| File | Source of truth | Pulled by |
|---|---|---|
| `workspace.yaml` | this file (manually edited) | `core/workspace.py` |
| `okrs.json` | our Notion OKR database | `scripts/notion_okr_pull.py` |
| `notion.json` | created by seed; lists our Notion DB IDs | `scripts/notion_okr_seed.py` |
| `intake.md` | our Notion intake page (when filled out) | (not yet wired) |
| `5in5.md` | our Notion 5-in-5 page | (not yet wired) |
| `health-check.md` | our Notion health-check page | (not yet wired) |

## Why this is committed to git

The whole point of dogfood is transparency: every artifact our customers
will produce, we produce too, in the same shape. Committing them lets
future-us audit "did we eat our own cooking?" by looking at git history.

**Pilot workspaces (`data/workspaces/<pilot-slug>/`) are gitignored.** That
is the production-data boundary. Customer files never touch our repo.

## How a pilot workspace differs

- Created via `python scripts/init_workspace.py --slug <slug> --name "<name>" --kind pilot`
  (script TBD — Sprint 1).
- Contents are gitignored (see `.gitignore`).
- Code paths take `--workspace <slug>` so the operator (or scheduler) is
  always explicit about which org's data they're touching.
- Our `core/workspace.assert_internal()` guards prevent any operation
  that mutates this repo (e.g. `TRACKER.md` regeneration) from running
  against a pilot workspace.
