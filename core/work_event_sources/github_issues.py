"""GitHub Issues work-event source.

Reuses the existing `GITHUB_TOKEN` from `core.github_ingest` — no new
auth. The token already authorizes `issues:read` if it has `repo` scope
or fine-grained `Issues: Read`.

Effort:     0.5 day (extends github_ingest with one more endpoint).
Status:     STUB — Sprint 3.

----

Implementation notes:

- Endpoint: GET `/repos/{owner}/{repo}/issues?state=all&since={iso}`.
- IMPORTANT: GitHub's `/issues` endpoint also returns PRs (PRs are
  technically issues in their data model). Filter out items where
  `pull_request` field is set — those are already ingested by
  `github_ingest.poll_repo`.
- Issue states: open / closed → kind:
    open                       → issue_opened
    closed (state_reason=null) → issue_completed
    closed (state_reason=not_planned / duplicate) → issue_canceled
- Source event id: `{owner}/{repo}#issue{number}@{kind}`.

----

Customer config:

    work_event_sources:
      - kind: github_issues
        config:
          repos: ["acme/api", "acme/web"]
"""

from __future__ import annotations

from typing import Any


def poll(workspace_slug: str, *, config: dict[str, Any],
         since_days: int = 7) -> dict[str, Any]:
    raise NotImplementedError(
        "GitHub Issues work-event source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 3)."
    )
