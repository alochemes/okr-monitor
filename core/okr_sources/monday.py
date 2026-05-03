"""Monday.com OKR source.

API:        https://api.monday.com/v2  (GraphQL)
Docs:       https://developer.monday.com/api-reference/docs
Auth (v0):  Personal API token in `MONDAY_API_TOKEN`. Generate at
            <workspace>.monday.com → Profile → Developers → My Access
            Tokens. Production uses Monday OAuth (Sprint 3+).
Effort:     1 day (clones the Notion DB-as-OKR pattern).
Status:     STUB — not yet implemented.

----

How customers set their board up (matches the Notion column convention
so the playbook is "use these column names, in any tool"):

  1. Create a Monday board called "OKRs". Item names = KR IDs ("1.1").
  2. Add columns:
       - Objective       (Status — one option per company-level Objective)
       - Statement       (Long Text)
       - Target          (Text)
       - Current         (Text)
       - Owner Pod       (Status — Strategy / Product/Design / Engineering / AI/Data / GTM / Customer/Ops)
       - Due Date        (Date)
       - Status          (Status — 🔴 Not started / 🟡 In progress / 🟠 At risk / 🟢 On track / ✅ Complete)
  3. Share `boards.read` access with the OKR Monitor integration user.

----

Implementation notes:

- Use a single GraphQL query: `query { boards(ids: [<id>]) { items_page
  { items { name column_values { ... } } } } }`. Cursor-paginate via
  `items_page.cursor` until empty.
- Map `column_values` → canonical KR fields by column title (NOT by id —
  ids change between board copies).
- Status values come back as the option text; reuse
  `core.notion_okr._normalize_status` for the 5-value enum mapping.
- Idempotency on output is guaranteed by the canonical shape; nothing
  source-specific to track.

----

Customer config in `data/workspaces/<slug>/workspace.yaml`:

    okr_source:
      kind: monday
      config:
        board_id: "1234567890"
"""

from __future__ import annotations

from typing import Any


def fetch_okrs(workspace_slug: str, *, config: dict[str, Any]) -> list[dict[str, Any]]:
    raise NotImplementedError(
        "Monday.com OKR source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 1)."
    )
