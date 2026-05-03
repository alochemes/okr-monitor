"""Build the integration-status snapshot read by the web app.

Lives next to `core/dashboard.py` because it serves the same purpose:
turn database state into a JSON file the front-end consumes.

Output shape (`web/public/integration_status.json`):

    {
      "schema": 1,
      "generated_at": "<utc iso>",
      "workspace_slug": "okrmonitor-internal",
      "sources": [
        {
          "category": "okr-sources" | "work-events.<subcat>" | "kpi-sources",
          "kind": "<source key>",
          "status": "connected" | "partial" | "stale" | "error" | "not_configured",
          "last_sync_at": "<iso or null>",
          "stats_24h": {"events_written": 12},
          "error": null
        },
        ...
      ]
    }

The status is derived as follows:
  - registry status `shipped` + run in last 25h with status=ok → connected
  - registry status `shipped` + run in last 25h with status=error → error
  - registry status `shipped` + last run >25h or never → stale
  - registry status `shipped` + no env credential → not_configured
  - registry status `stub` / `planned` / `deferred` → not_configured
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from core import kpi_sources, okr_sources, store, work_event_sources, workspace


# --- Map registry source key → the audit-log "agent" name used by the
# poller. Keep in sync as new sources ship.

# Map registry source key → the audit-log "agent" name used by the
# poller. Sources that don't write run rows (Notion pull is sync, not
# a poll) get a None and use a source-specific freshness probe below.

SHIPPED_AGENT: dict[str, str | None] = {
    "notion": None,                  # uses okrs.json mtime instead
    "github": "github_ingest",
    "linear": "linear_ingest",
}


def _env_credential_present(source_key: str) -> bool:
    """Check whether the env credential for a source is set. Conservative
    — when in doubt we say YES so we don't false-flag a configured pilot."""
    env_keys = {
        "notion":     ["NOTION_API_KEY"],
        "github":     ["GITHUB_TOKEN"],
        "linear":     ["LINEAR_API_KEY"],
        "monday":     ["MONDAY_API_TOKEN"],
        "asana":      ["ASANA_PAT"],
        "mooncamp":   ["MOONCAMP_API_KEY"],
        "coda":       ["CODA_API_TOKEN"],
        "lattice":    [],          # OAuth — different check (skip for v0)
        "workboard":  ["WORKBOARD_PAT"],
        "google_docs": [],         # OAuth — skip
        "csv":        [],          # no credential needed
        "gitlab":     ["GITLAB_TOKEN"],
        "bitbucket":  ["BITBUCKET_APP_PASSWORD"],
        "jira":       ["JIRA_API_TOKEN", "JIRA_EMAIL"],
        "asana_tasks": ["ASANA_PAT"],
        "shortcut":   ["SHORTCUT_API_TOKEN"],
        "github_issues": ["GITHUB_TOKEN"],
        "slack":      ["SLACK_BOT_TOKEN"],
        "teams":      [],
        "discord":    ["DISCORD_BOT_TOKEN"],
        "notion_docs": ["NOTION_API_KEY"],
        "confluence": ["CONFLUENCE_API_TOKEN", "CONFLUENCE_EMAIL"],
        "google_drive": [],
        "coda_docs":  ["CODA_API_TOKEN"],
        "hubspot":    ["HUBSPOT_PRIVATE_APP_TOKEN"],
        "salesforce": [],
        "pipedrive":  ["PIPEDRIVE_API_TOKEN"],
        "attio":      ["ATTIO_API_KEY"],
        "datadog":    ["DATADOG_API_KEY", "DATADOG_APP_KEY"],
        "mixpanel":   ["MIXPANEL_SA_USERNAME", "MIXPANEL_SA_SECRET"],
        "amplitude":  ["AMPLITUDE_API_KEY", "AMPLITUDE_SECRET"],
        "posthog":    ["POSTHOG_API_KEY"],
        "grafana":    ["GRAFANA_API_TOKEN"],
    }.get(source_key, [])
    if not env_keys:
        return source_key == "csv"
    return all(os.environ.get(k, "").strip() for k in env_keys)


def _last_run_for_agent(agent: str) -> tuple[str | None, str | None, dict[str, Any] | None]:
    """Return (ended_at_iso, status, stats_dict) for the most recent run row
    of the given agent, or (None, None, None) if none."""
    with store.connect() as conn:
        row = conn.execute(
            "SELECT ended_at, status, stats_json FROM runs WHERE agent = ?"
            " AND ended_at IS NOT NULL ORDER BY started_at DESC LIMIT 1",
            (agent,),
        ).fetchone()
    if not row:
        return None, None, None
    stats: dict[str, Any] | None = None
    if row["stats_json"]:
        try:
            stats = json.loads(row["stats_json"])
        except json.JSONDecodeError:
            stats = None
    return row["ended_at"], row["status"], stats


def _stats_24h(agent: str) -> dict[str, int]:
    """Sum events_written across the last 24h of poller runs for `agent`."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    with store.connect() as conn:
        rows = conn.execute(
            "SELECT stats_json FROM runs WHERE agent = ? AND started_at >= ?",
            (agent, cutoff),
        ).fetchall()
    written = 0
    seen = 0
    for r in rows:
        if not r["stats_json"]:
            continue
        try:
            s = json.loads(r["stats_json"])
        except json.JSONDecodeError:
            continue
        written += int(s.get("events_written") or 0)
        seen += int(s.get("events_seen") or 0)
    return {"events_written": written, "events_seen": seen}


def _resolve_status(
    *, registry_status: str, agent: str | None, has_credential: bool,
    ended_at: str | None, run_status: str | None,
) -> str:
    if registry_status != "shipped":
        return "not_configured"
    if not has_credential:
        return "not_configured"
    if ended_at is None:
        return "stale"
    age_h = _hours_since(ended_at)
    if run_status == "error":
        return "error"
    if age_h is not None and age_h > 25:
        return "stale"
    return "connected"


def _hours_since(iso: str) -> float | None:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return None
    delta = datetime.now(timezone.utc) - dt
    return delta.total_seconds() / 3600.0


def _notion_freshness() -> tuple[str | None, dict[str, int]]:
    """Notion pull doesn't write a run row — derive freshness from the
    workspace cache file's mtime + the objective/kr count."""
    cache = workspace.artifact_path("okrs.json")
    if not cache.exists():
        return None, {}
    mtime = datetime.fromtimestamp(cache.stat().st_mtime, tz=timezone.utc)
    try:
        payload = json.loads(cache.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return mtime.isoformat(), {}
    objs = payload.get("objectives") or []
    kr_total = sum(len(o.get("krs") or []) for o in objs)
    return mtime.isoformat(), {"objectives": len(objs), "krs": kr_total}


def _row(*, key: str, name: str, category: str, registry_status: str) -> dict[str, Any]:
    has_cred = _env_credential_present(key)
    agent = SHIPPED_AGENT.get(key)
    ended_at: str | None = None
    run_status: str | None = None
    last_stats: dict[str, Any] | None = None
    stats_24h: dict[str, int] = {}

    if key == "notion" and registry_status == "shipped":
        ended_at, stats_24h = _notion_freshness()
        run_status = "ok" if ended_at else None
    elif agent:
        ended_at, run_status, last_stats = _last_run_for_agent(agent)
        stats_24h = _stats_24h(agent)

    error_msg: str | None = None
    if run_status == "error" and last_stats and isinstance(last_stats, dict):
        errs = last_stats.get("errors") or []
        if errs:
            error_msg = json.dumps(errs[0])[:240]

    status = _resolve_status(
        registry_status=registry_status, agent=agent,
        has_credential=has_cred, ended_at=ended_at, run_status=run_status,
    )
    return {
        "category": category,
        "kind": key,
        "name": name,
        "status": status,
        "last_sync_at": ended_at,
        "stats_24h": stats_24h,
        "error": error_msg,
    }


def build_snapshot(*, slug: str | None = None) -> dict[str, Any]:
    """Compose the snapshot for the given workspace (defaults to internal)."""
    slug = slug or workspace.current_workspace_id()
    sources: list[dict[str, Any]] = []

    for entry in okr_sources.list_sources():
        sources.append(_row(
            key=entry["key"], name=entry["name"],
            category="okr-sources", registry_status=entry["status"],
        ))
    for entry in work_event_sources.list_sources():
        sources.append(_row(
            key=entry["key"], name=entry["name"],
            category=f"work-events.{entry['subcat']}",
            registry_status=entry["status"],
        ))
    for entry in kpi_sources.list_sources():
        sources.append(_row(
            key=entry["key"], name=entry["name"],
            category="kpi-sources", registry_status=entry["status"],
        ))

    return {
        "schema": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workspace_slug": slug,
        "sources": sources,
    }


def write_snapshot(path: Path, *, slug: str | None = None) -> Path:
    """Write the snapshot to `path` atomically. Returns the path."""
    payload = build_snapshot(slug=slug)
    tmp = path.with_suffix(".json.tmp")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    tmp.replace(path)
    return path
