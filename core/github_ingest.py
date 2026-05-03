"""GitHub → work_events ingestion (v0).

Polling-based, stdlib-only. Each poll fetches commits + pull requests for one
repo via the REST API and upserts each into `work_events` via
`store.upsert_work_event`. Idempotency comes from the schema's
`UNIQUE(source, source_event_id)` — replays are safe.

Auth: `GITHUB_TOKEN` env (a fine-grained PAT scoped to the target repo, or a
classic PAT with `repo` scope). Anonymous calls work for public repos but hit
60 req/h vs 5,000 req/h authenticated.

Why polling, not webhook (today): the system runs as cron'd scripts (no
long-running server). Webhook receiver lands when the product app gets
server-side route handlers in Sprint 1. Polling daily from `daily_evening.py`
covers the dogfood need (KR1.3 real eval data, KR4.1 dogfood agent visibility)
without standing up new infra.

Usage:
    from core import github_ingest
    res = github_ingest.poll_repo("alochemes", "okr-monitor", since_days=7)
    # → {"events_written": 12, "events_seen": 47, "commits": 35, "prs": 12}
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any, Iterator

from core import audit, store


_API = "https://api.github.com"
_AGENT = "github_ingest"
_USER_AGENT = "okr-monitor/0.1 (+https://github.com/alochemes/okr-monitor)"


# ---------------------------------------------------------------------------
# HTTP

def _headers() -> dict[str, str]:
    h = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": _USER_AGENT,
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


class GitHubError(RuntimeError):
    """Raised on non-200 from the GitHub API. Carries status + body for
    debugging; callers can choose to swallow (e.g. 404 on a deleted repo)."""

    def __init__(self, status: int, url: str, body: str):
        super().__init__(f"GitHub {status} on {url}: {body[:200]}")
        self.status = status
        self.url = url
        self.body = body


def _get(url: str, params: dict[str, Any] | None = None) -> tuple[Any, dict[str, str]]:
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=_headers())
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            headers = {k.lower(): v for k, v in resp.getheaders()}
            return data, headers
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        raise GitHubError(exc.code, url, body) from exc


def _paginate(url: str, params: dict[str, Any], *, page_cap: int = 5) -> Iterator[Any]:
    """Yield items across pages. `page_cap` bounds total pages — callers
    should keep this small (we're polling for "recent activity," not a
    full history backfill)."""
    p = dict(params)
    p.setdefault("per_page", 100)
    p["page"] = 1
    while p["page"] <= page_cap:
        items, _hdrs = _get(url, p)
        if not items:
            return
        for it in items:
            yield it
        if len(items) < p["per_page"]:
            return
        p["page"] += 1


# ---------------------------------------------------------------------------
# Work-event mappers — convert GitHub payload → store.upsert_work_event kwargs

def _commit_to_event(owner: str, repo: str, c: dict[str, Any]) -> dict[str, Any]:
    """REST /repos/{owner}/{repo}/commits row → upsert kwargs."""
    sha = c.get("sha", "")
    commit = c.get("commit") or {}
    msg = (commit.get("message") or "").strip()
    title = msg.splitlines()[0][:200] if msg else f"commit {sha[:7]}"
    body = "\n".join(msg.splitlines()[1:]).strip() or None
    author = (
        (c.get("author") or {}).get("login")
        or (commit.get("author") or {}).get("name")
        or "unknown"
    )
    occurred_at = (commit.get("author") or {}).get("date") or _utcnow_iso()
    return {
        "source": "github",
        "source_event_id": f"{owner}/{repo}@{sha}",
        "kind": "commit",
        "title": title,
        "body": body,
        "actor": author,
        "occurred_at": occurred_at,
        "raw": {
            "owner": owner, "repo": repo, "sha": sha,
            "url": c.get("html_url"),
        },
    }


def _pr_to_event(owner: str, repo: str, pr: dict[str, Any]) -> dict[str, Any]:
    """REST /repos/{owner}/{repo}/pulls row → upsert kwargs."""
    number = pr.get("number")
    title = (pr.get("title") or "").strip()[:200] or f"PR #{number}"
    body = (pr.get("body") or "").strip() or None
    actor = (pr.get("user") or {}).get("login") or "unknown"

    # Use the most-recent event timestamp so the same PR can be re-ingested
    # when its state changes. The composite source_event_id encodes the state
    # so that a merge produces a new row instead of overwriting "opened."
    state = pr.get("state") or "open"
    if pr.get("merged_at"):
        state, occurred_at = "merged", pr["merged_at"]
    elif state == "closed":
        occurred_at = pr.get("closed_at") or pr.get("updated_at") or _utcnow_iso()
    else:
        occurred_at = pr.get("created_at") or _utcnow_iso()

    return {
        "source": "github",
        "source_event_id": f"{owner}/{repo}#PR{number}@{state}",
        "kind": f"pr_{state}",
        "title": title,
        "body": body,
        "actor": actor,
        "occurred_at": occurred_at,
        "raw": {
            "owner": owner, "repo": repo, "number": number, "state": state,
            "url": pr.get("html_url"),
        },
    }


# ---------------------------------------------------------------------------
# Polling entry points

def poll_repo(
    owner: str,
    repo: str,
    *,
    since_days: int = 7,
    include_commits: bool = True,
    include_prs: bool = True,
    page_cap: int = 5,
) -> dict[str, Any]:
    """Poll one repo for recent commits + PRs. Idempotent.

    Returns a stats dict suitable for logging into the daily report. Does NOT
    raise on individual upsert failures; the caller can read `events_seen`
    minus `events_written` to detect drops.
    """
    since_iso = (datetime.now(timezone.utc) - timedelta(days=since_days)).isoformat()
    run_id = store.start_run(agent=_AGENT, kind="poll_repo")
    stats: dict[str, Any] = {
        "owner": owner, "repo": repo, "since": since_iso,
        "commits": 0, "prs": 0,
        "events_seen": 0, "events_written": 0, "errors": [],
    }
    try:
        if include_commits:
            for c in _paginate(
                f"{_API}/repos/{owner}/{repo}/commits",
                {"since": since_iso}, page_cap=page_cap,
            ):
                stats["commits"] += 1
                stats["events_seen"] += 1
                _, was_new = store.upsert_work_event(**_commit_to_event(owner, repo, c))
                if was_new:
                    stats["events_written"] += 1

        if include_prs:
            # PRs aren't filtered by `since`; we sort updated-desc and stop
            # once we cross the window.
            for pr in _paginate(
                f"{_API}/repos/{owner}/{repo}/pulls",
                {"state": "all", "sort": "updated", "direction": "desc"},
                page_cap=page_cap,
            ):
                updated = pr.get("updated_at") or ""
                if updated and updated < since_iso:
                    break
                stats["prs"] += 1
                stats["events_seen"] += 1
                try:
                    _, was_new = store.upsert_work_event(**_pr_to_event(owner, repo, pr))
                except Exception as exc:  # pragma: no cover
                    stats["errors"].append({"pr": pr.get("number"), "error": str(exc)})
                    continue
                if was_new:
                    stats["events_written"] += 1

        audit.emit(
            run_id=run_id, agent=_AGENT, action="poll_repo.complete",
            subject_type="github_repo", subject_id=f"{owner}/{repo}",
            payload={k: v for k, v in stats.items() if k != "errors"},
        )
        store.end_run(run_id, status="ok", stats=stats)
        return stats
    except GitHubError as exc:
        stats["errors"].append({"http_status": exc.status, "body": exc.body[:500]})
        audit.emit(run_id=run_id, agent=_AGENT, action="poll_repo.api_error",
                   severity="error", subject_type="github_repo",
                   subject_id=f"{owner}/{repo}",
                   payload={"status": exc.status, "url": exc.url})
        store.end_run(run_id, status="error", stats=stats, error=str(exc))
        raise
    except Exception as exc:    # pragma: no cover
        store.end_run(run_id, status="error", stats=stats, error=str(exc))
        audit.emit(run_id=run_id, agent=_AGENT, action="poll_repo.exception",
                   severity="error", payload={"error": str(exc)})
        raise


def poll_repos(
    repos: list[tuple[str, str]],
    *,
    since_days: int = 7,
) -> dict[str, Any]:
    """Poll a list of (owner, repo) tuples. One bad repo doesn't block the
    others — failures are recorded per-repo and the function returns once
    every repo has been attempted."""
    out: dict[str, Any] = {
        "repos": len(repos), "events_written": 0, "events_seen": 0, "per_repo": [],
    }
    for owner, repo in repos:
        try:
            res = poll_repo(owner, repo, since_days=since_days)
            out["events_seen"] += res["events_seen"]
            out["events_written"] += res["events_written"]
            out["per_repo"].append(res)
        except Exception as exc:    # pragma: no cover
            out["per_repo"].append({
                "owner": owner, "repo": repo, "ok": False, "error": str(exc),
            })
    return out


# ---------------------------------------------------------------------------

def configured_repos() -> list[tuple[str, str]]:
    """Read repos to poll from env. Format: `GITHUB_INGEST_REPOS=owner/repo,owner2/repo2`.

    Falls back to the dogfood account (`alochemes/okr-monitor`) so that a
    fresh `daily_evening.py` run on a clean checkout still produces real
    events without operator config."""
    raw = os.environ.get("GITHUB_INGEST_REPOS", "alochemes/okr-monitor").strip()
    out: list[tuple[str, str]] = []
    for tok in raw.split(","):
        tok = tok.strip()
        if not tok or "/" not in tok:
            continue
        owner, repo = tok.split("/", 1)
        out.append((owner.strip(), repo.strip()))
    return out


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
