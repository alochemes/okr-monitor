"""GitLab work-event source.

API:        https://gitlab.com/api/v4  (or self-hosted instance)
Docs:       https://docs.gitlab.com/ee/api/
Auth (v0):  PAT in `GITLAB_TOKEN` with `read_api` + `read_repository`.
Effort:     1 day (clones core.github_ingest structure).
Status:     STUB — Sprint 4 (long-tail).

Implementation notes:
- Endpoint: GET `/projects/{id}/repository/commits?since={iso}`
- Endpoint: GET `/projects/{id}/merge_requests?state=all&updated_after={iso}`
- Source event id: `gitlab:{project_id}@{sha}` for commits, MR pattern same.

Customer config:

    work_event_sources:
      - kind: gitlab
        config:
          host:    "gitlab.com"        # or self-hosted
          projects: [12345, 67890]
"""

from __future__ import annotations

from typing import Any


def poll(workspace_slug: str, *, config: dict[str, Any],
         since_days: int = 7) -> dict[str, Any]:
    raise NotImplementedError(
        "GitLab work-event source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 4+)."
    )
