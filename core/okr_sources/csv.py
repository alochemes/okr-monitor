"""CSV / paste OKR source — universal fallback for any tool we don't
yet have a native integration for.

API:        none — accepts a CSV file path
Auth (v0):  none
Effort:     0.5 day.
Status:     STUB — not yet implemented.

----

When a customer's OKR tool isn't in our registry (or is a Google Doc
we haven't built the LLM extractor for yet), they can export to CSV or
paste the columns into our `/health-check` form. Same canonical schema:

    KR ID, Statement, Target, Current, Owner Pod, Due Date, Status

----

Implementation notes:

- Accept either a file path on disk or a CSV string. Use `csv.DictReader`.
- Validate required columns are present; raise with a clear message
  pointing at the column-name reference in INSTRUCTIONS.md.
- Parse Date column with `datetime.fromisoformat`; tolerate empty.
- Status normalization via `core.notion_okr._normalize_status`.

----

Customer config:

    okr_source:
      kind: csv
      config:
        path: "data/workspaces/<slug>/okrs.csv"
        # or:
        upload_id: "..."           # set by the /app/health-check form
"""

from __future__ import annotations

from typing import Any


def fetch_okrs(workspace_slug: str, *, config: dict[str, Any]) -> list[dict[str, Any]]:
    raise NotImplementedError(
        "CSV OKR source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 2)."
    )
