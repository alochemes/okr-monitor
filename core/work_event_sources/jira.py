"""Jira work-event source.

API:        https://your-domain.atlassian.net/rest/api/3
Docs:       https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro
Auth (v0):  Email + API token in `JIRA_EMAIL` + `JIRA_API_TOKEN`.
            Generate token at id.atlassian.com → Security → API tokens.
            Auth header: `Basic base64(email:token)`.
Effort:     1.5 days.
Status:     STUB — Sprint 2.

----

Implementation notes:

- Endpoint: GET `/rest/api/3/search?jql={jql}` with JQL filter, e.g.
  `project = ENG AND updated >= -7d ORDER BY updated DESC`.
- Pagination: `startAt` + `maxResults` (default 50, max 100).
- Issue states: parse `fields.status.name` against status-category
  (`To Do` / `In Progress` / `Done`) for the kind mapping:
    To Do       → issue_opened
    In Progress → issue_in_progress
    Done        → issue_completed (use `fields.resolutiondate`)
- Source event id: `{cloud_id}:{issue_key}@{kind}`.

----

Customer config:

    work_event_sources:
      - kind: jira
        config:
          domain:   "acme.atlassian.net"
          projects: ["ENG", "PROD"]    # optional; omit to include all
"""

from __future__ import annotations

from typing import Any


def poll(workspace_slug: str, *, config: dict[str, Any],
         since_days: int = 7) -> dict[str, Any]:
    raise NotImplementedError(
        "Jira work-event source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 2)."
    )
