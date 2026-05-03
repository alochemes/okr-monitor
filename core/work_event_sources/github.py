"""GitHub work-event source — thin wrapper over `core.github_ingest`.

Status: shipped. See `core/github_ingest.py` for the implementation.
"""

from __future__ import annotations

from typing import Any

from core import github_ingest


def poll(workspace_slug: str, *, config: dict[str, Any],
         since_days: int = 7) -> dict[str, Any]:
    """Pull commits + PRs for the configured repos.
    `config` keys:
       - repos: list of "owner/repo" strings (or env GITHUB_INGEST_REPOS).
    """
    repos_cfg = config.get("repos") or []
    repos = []
    for r in repos_cfg:
        if isinstance(r, str) and "/" in r:
            owner, name = r.split("/", 1)
            repos.append((owner.strip(), name.strip()))
    if not repos:
        repos = github_ingest.configured_repos()
    return github_ingest.poll_repos(repos, since_days=since_days)
