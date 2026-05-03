"""Linear → work_events ingestion (v0).

Polling-based, stdlib-only. Each poll fetches recently-updated issues for one
or more Linear teams via the GraphQL API and upserts each into `work_events`
via `store.upsert_work_event`. Idempotency comes from the schema's
`UNIQUE(source, source_event_id)` — replays are safe.

Auth: `LINEAR_API_KEY` env (Linear personal API key, found at
https://linear.app/<workspace>/settings/api). Linear has no anonymous mode;
without a key this module is a no-op.

Why polling, not webhook (today): same reason as `core/github_ingest`. The
system runs as cron'd scripts. Webhooks land Sprint 1 once the product app
hosts server-side route handlers.

Usage:
    from core import linear_ingest
    res = linear_ingest.poll_workspace(since_days=7)
    # → {"events_written": 8, "events_seen": 23, "issues": 23, ...}
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any

from core import audit, store


_API = "https://api.linear.app/graphql"
_AGENT = "linear_ingest"


# ---------------------------------------------------------------------------
# HTTP

class LinearError(RuntimeError):
    """Non-200 from the Linear GraphQL API, or a GraphQL `errors` payload."""

    def __init__(self, status: int, body: str):
        super().__init__(f"Linear {status}: {body[:300]}")
        self.status = status
        self.body = body


def _gql(query: str, variables: dict[str, Any]) -> dict[str, Any]:
    token = os.environ.get("LINEAR_API_KEY")
    if not token:
        raise LinearError(401, "LINEAR_API_KEY not set")
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        _API, data=payload, method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": token,    # Linear PATs go raw, no "Bearer" prefix
            "User-Agent": "okr-monitor/0.1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        raise LinearError(exc.code, body) from exc
    if data.get("errors"):
        raise LinearError(200, json.dumps(data["errors"])[:500])
    return data.get("data") or {}


# ---------------------------------------------------------------------------
# GraphQL queries

# Pull recently-updated issues across the workspace. Cursor-paginated.
# `filter.updatedAt.gt` lets us bound to the polling window cheaply.
_ISSUES_QUERY = """
query Issues($filter: IssueFilter, $after: String) {
  issues(first: 50, filter: $filter, after: $after,
         orderBy: updatedAt) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id
      identifier
      title
      description
      url
      createdAt
      updatedAt
      completedAt
      canceledAt
      state { name type }
      team { key name }
      assignee { name email displayName }
      creator { name email displayName }
    }
  }
}
"""


# ---------------------------------------------------------------------------
# Mapper

def _state_kind(state_type: str | None, completed_at: str | None,
                canceled_at: str | None) -> str:
    """Map Linear state → work_event kind. Linear state types are roughly:
    backlog | unstarted | started | completed | canceled | triage."""
    if canceled_at:
        return "issue_canceled"
    if completed_at or state_type == "completed":
        return "issue_completed"
    if state_type == "started":
        return "issue_in_progress"
    return "issue_opened"


def _issue_to_event(node: dict[str, Any]) -> dict[str, Any]:
    """Linear issue node → upsert kwargs.

    The composite source_event_id encodes the state so a transition (opened →
    in_progress → completed) becomes a new event row instead of overwriting,
    which lets the mapper credit the closing-of-an-issue separately from
    the opening-of-it for KR purposes.
    """
    state = (node.get("state") or {}).get("type")
    kind = _state_kind(state, node.get("completedAt"), node.get("canceledAt"))

    if kind == "issue_completed":
        occurred_at = node.get("completedAt") or node.get("updatedAt")
    elif kind == "issue_canceled":
        occurred_at = node.get("canceledAt") or node.get("updatedAt")
    elif kind == "issue_in_progress":
        occurred_at = node.get("updatedAt")
    else:
        occurred_at = node.get("createdAt") or node.get("updatedAt")

    actor = (
        (node.get("assignee") or {}).get("displayName")
        or (node.get("creator") or {}).get("displayName")
        or (node.get("creator") or {}).get("email")
        or "unknown"
    )

    identifier = node.get("identifier") or node.get("id")
    title = (node.get("title") or "").strip()[:200] or identifier
    body = (node.get("description") or "").strip() or None

    return {
        "source": "linear",
        "source_event_id": f"{identifier}@{kind}",
        "kind": kind,
        "title": title,
        "body": body,
        "actor": actor,
        "occurred_at": occurred_at or _utcnow_iso(),
        "raw": {
            "id": node.get("id"),
            "identifier": identifier,
            "url": node.get("url"),
            "team": (node.get("team") or {}).get("key"),
            "state": (node.get("state") or {}).get("name"),
        },
    }


# ---------------------------------------------------------------------------
# Polling

def poll_workspace(
    *,
    since_days: int = 7,
    team_key: str | None = None,
    page_cap: int = 5,
) -> dict[str, Any]:
    """Poll Linear for recently-updated issues. Idempotent.

    `team_key` (e.g. "ENG") narrows by team; omit to pull workspace-wide.
    `page_cap` bounds pagination — keep small; we're polling for "recent
    activity" not full backfill.
    """
    since_iso = (datetime.now(timezone.utc) - timedelta(days=since_days)).isoformat()
    run_id = store.start_run(agent=_AGENT, kind="poll_workspace")
    stats: dict[str, Any] = {
        "since": since_iso, "team_key": team_key,
        "issues": 0, "events_seen": 0, "events_written": 0, "errors": [],
    }
    try:
        gql_filter: dict[str, Any] = {"updatedAt": {"gt": since_iso}}
        if team_key:
            gql_filter["team"] = {"key": {"eq": team_key}}

        cursor: str | None = None
        page = 0
        while page < page_cap:
            page += 1
            data = _gql(_ISSUES_QUERY, {"filter": gql_filter, "after": cursor})
            block = (data or {}).get("issues") or {}
            nodes = block.get("nodes") or []
            for node in nodes:
                stats["issues"] += 1
                stats["events_seen"] += 1
                try:
                    _, was_new = store.upsert_work_event(**_issue_to_event(node))
                except Exception as exc:    # pragma: no cover
                    stats["errors"].append({
                        "issue": node.get("identifier"), "error": str(exc),
                    })
                    continue
                if was_new:
                    stats["events_written"] += 1

            page_info = block.get("pageInfo") or {}
            if not page_info.get("hasNextPage"):
                break
            cursor = page_info.get("endCursor")
            if not cursor:
                break

        audit.emit(
            run_id=run_id, agent=_AGENT, action="poll_workspace.complete",
            payload={k: v for k, v in stats.items() if k != "errors"},
        )
        store.end_run(run_id, status="ok", stats=stats)
        return stats
    except LinearError as exc:
        stats["errors"].append({"http_status": exc.status, "body": exc.body[:500]})
        audit.emit(run_id=run_id, agent=_AGENT, action="poll_workspace.api_error",
                   severity="error",
                   payload={"status": exc.status, "body": exc.body[:300]})
        store.end_run(run_id, status="error", stats=stats, error=str(exc))
        raise
    except Exception as exc:    # pragma: no cover
        store.end_run(run_id, status="error", stats=stats, error=str(exc))
        audit.emit(run_id=run_id, agent=_AGENT, action="poll_workspace.exception",
                   severity="error", payload={"error": str(exc)})
        raise


# ---------------------------------------------------------------------------

def is_configured() -> bool:
    return bool(os.environ.get("LINEAR_API_KEY"))


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
