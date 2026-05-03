"""Coda OKR source.

API:        https://coda.io/apis/v1  (REST)
Docs:       https://coda.io/developers/apis/v1
Auth (v0):  API token in `CODA_API_TOKEN`. Generate at Account Settings →
            API Settings → Generate API Token.
Effort:     1 day (same shape as Notion DB ingest).
Status:     STUB — not yet implemented.

----

Coda has no native OKR concept — same situation as Notion. Customers
model OKRs in a Coda *table* with our canonical columns.

----

Implementation notes:

- Endpoints:
    GET /docs/{docId}/tables/{tableIdOrName}    — table metadata
    GET /docs/{docId}/tables/{tableId}/rows     — paginated rows
- Reuse the Notion column convention (KR ID, Statement, Target, Current,
  Owner Pod, Due Date, Status). Customer's `tableIdOrName` can be
  literal name "OKRs" or the system-generated id.
- Status mapping: same 5-value enum via
  `core.notion_okr._normalize_status`.

----

Customer config:

    okr_source:
      kind: coda
      config:
        doc_id:   "abc-XYZ123"
        table_id: "OKRs"             # or the generated id

Customer setup:
  1. Create a "OKRs" table in their Coda doc with the prescribed columns.
  2. Generate an API token with read access to that doc.
  3. Paste token into our intake or the /app/integrations UI.
"""

from __future__ import annotations

from typing import Any


def fetch_okrs(workspace_slug: str, *, config: dict[str, Any]) -> list[dict[str, Any]]:
    raise NotImplementedError(
        "Coda OKR source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 2)."
    )
