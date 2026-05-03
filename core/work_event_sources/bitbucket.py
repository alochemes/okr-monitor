"""Bitbucket work-event source.

API:        https://api.bitbucket.org/2.0
Docs:       https://developer.atlassian.com/cloud/bitbucket/rest/intro/
Auth (v0):  App password in `BITBUCKET_APP_PASSWORD` + workspace user.
            Generate at Personal Settings → App passwords.
Effort:     1 day.
Status:     STUB — Sprint 4 (long-tail).

Implementation notes:
- Endpoint: GET `/repositories/{workspace}/{repo_slug}/commits` (pagelen=100).
- Endpoint: GET `/repositories/{workspace}/{repo_slug}/pullrequests?state=...`.
- Source event id: `bitbucket:{ws}/{repo}@{hash}` for commits.

Customer config:

    work_event_sources:
      - kind: bitbucket
        config:
          workspace: "acme"
          repos:    ["api", "web"]
"""

from __future__ import annotations

from typing import Any


def poll(workspace_slug: str, *, config: dict[str, Any],
         since_days: int = 7) -> dict[str, Any]:
    raise NotImplementedError(
        "Bitbucket work-event source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 4+)."
    )
