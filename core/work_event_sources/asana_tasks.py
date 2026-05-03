"""Asana tasks work-event source. Shares the HTTP client with
`core.okr_sources.asana` (Asana Goals).

API:        https://app.asana.com/api/1.0
Docs:       https://developers.asana.com/reference/tasks
Auth (v0):  PAT in `ASANA_PAT`.
Effort:     1 day (after asana.py exists; mostly different endpoints).
Status:     STUB — Sprint 2.

----

Implementation notes:

- Endpoint: GET `/projects/{gid}/tasks?modified_since={iso}` per project.
  Or `/workspaces/{gid}/tasks/search` for a JQL-ish query.
- Task lifecycle:
    completed=False, assignee_status=upcoming → issue_opened
    completed=False, assignee_status=inbox    → issue_in_progress
    completed=True                             → issue_completed
- Source event id: `asana:task:{gid}@{kind}`.

----

Customer config:

    work_event_sources:
      - kind: asana_tasks
        config:
          workspace_gid: "..."
          project_gids:  ["...", "..."]   # optional
"""

from __future__ import annotations

from typing import Any


def poll(workspace_slug: str, *, config: dict[str, Any],
         since_days: int = 7) -> dict[str, Any]:
    raise NotImplementedError(
        "Asana tasks work-event source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 2)."
    )
