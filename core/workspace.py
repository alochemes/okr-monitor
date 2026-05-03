"""Workspace abstraction — the unit of separation between OKR Monitor's
own data ("dogfood") and customer data.

A *workspace* is one organization's data: their OKRs, their integrations,
their work events, their narratives. Two workspaces never mix.

Slugs (used as filesystem paths) must match `[a-z0-9-]+` so they're safe
on every platform we care about. Our own workspace is `okrmonitor-internal`.

Per-workspace artifacts live under `data/workspaces/<slug>/`:
  - `okrs.json`     — cached structured OKRs (canonical source: Notion)
  - `intake.md`     — pilot intake questionnaire answers (per pilot)
  - `5in5.md`       — output of the 5-in-5 exercise
  - `health-check.md` — generated OKR Health Check report
  - `workspace.yaml`  — metadata (name, kind, contacts, integrations)
  - `notion.json`     — Notion DB IDs (OKRs DB id, parent page id, …)

Multi-tenancy migration status (2026-05-02):
  - This module + Notion-OKR ingest are workspace-aware from day 1.
  - The existing per-org tables (`work_events`, `event_kr_mappings`,
    `kr_signals`, `narratives`, `proposals`, `runs`) do NOT yet carry a
    `workspace_id` column. They implicitly belong to `okrmonitor-internal`.
  - Before pilot #1 onboards, those tables MUST get a `workspace_id` column
    + backfill to `okrmonitor-internal`. Tracking issue: see TRACKER.md §9
    "Multi-tenant readiness" risk row (added 2026-05-02).
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml

from core.paths import DATA_DIR


# The slug for our own (internal / dogfood) workspace. Other code keys off
# this constant — never hardcode the literal elsewhere.
INTERNAL_WORKSPACE_ID = "okrmonitor-internal"


# Active workspace for the current process. Defaults to the internal one
# until multi-tenancy lands. Override with the OKR_MONITOR_WORKSPACE_ID env
# var when running tools against a pilot's data (e.g. the eventual
# `python scripts/run_okr_mapper.py --workspace acme-corp`).
def current_workspace_id() -> str:
    val = os.environ.get("OKR_MONITOR_WORKSPACE_ID", "").strip()
    return val or INTERNAL_WORKSPACE_ID


_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


def validate_slug(slug: str) -> str:
    """Raise ValueError if `slug` isn't a safe workspace identifier."""
    if not _SLUG_RE.match(slug):
        raise ValueError(
            f"Invalid workspace slug: {slug!r}. Must match [a-z0-9-]+, "
            "≤63 chars, must start with [a-z0-9]."
        )
    return slug


# ---------- Filesystem layout -----------------------------------------------

WORKSPACES_DIR = DATA_DIR / "workspaces"


def workspace_dir(slug: str | None = None) -> Path:
    """Return `data/workspaces/<slug>/`. Creates the directory if missing."""
    s = validate_slug(slug or current_workspace_id())
    p = WORKSPACES_DIR / s
    p.mkdir(parents=True, exist_ok=True)
    return p


def artifact_path(name: str, slug: str | None = None) -> Path:
    """Path to a named artifact in the workspace (e.g. 'okrs.json'). Does NOT
    create the file — callers handle existence."""
    return workspace_dir(slug) / name


# ---------- Workspace metadata (workspace.yaml) -----------------------------

def load_metadata(slug: str | None = None) -> dict[str, Any]:
    """Load `workspace.yaml` for the workspace. Returns {} if absent."""
    p = artifact_path("workspace.yaml", slug)
    if not p.exists():
        return {}
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{p} must be a YAML mapping at top level")
    return data


def save_metadata(meta: dict[str, Any], slug: str | None = None) -> None:
    """Write `workspace.yaml` atomically."""
    p = artifact_path("workspace.yaml", slug)
    tmp = p.with_suffix(".yaml.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        yaml.safe_dump(meta, f, sort_keys=False, default_flow_style=False)
    tmp.replace(p)


def init_workspace(
    *, slug: str, name: str, kind: str, contacts: list[str] | None = None,
    integrations: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a new workspace dir + workspace.yaml. Idempotent — re-runs
    update only the fields explicitly passed.

    `kind` is "internal" (us) or "pilot" (a customer). The kind determines
    git policy and is checked by code paths that need to be sure they
    aren't touching customer data (or vice versa).
    """
    if kind not in ("internal", "pilot"):
        raise ValueError(f"kind must be 'internal' or 'pilot', got {kind!r}")
    validate_slug(slug)
    workspace_dir(slug)    # ensures dir exists
    meta = load_metadata(slug)
    meta.update({
        "slug": slug,
        "name": name,
        "kind": kind,
    })
    if contacts is not None:
        meta["contacts"] = contacts
    if integrations is not None:
        meta["integrations"] = integrations
    save_metadata(meta, slug)
    return meta


# ---------- Helpers for callers ---------------------------------------------

def is_internal(slug: str | None = None) -> bool:
    """True iff the named workspace is OUR workspace. Use this in code paths
    that should never touch customer data (e.g. operations that mutate the
    repo's TRACKER.md)."""
    return (slug or current_workspace_id()) == INTERNAL_WORKSPACE_ID


def assert_internal(slug: str | None = None) -> None:
    """Raise if we're not in the internal workspace. Call this at the top
    of any function that writes to repo-tracked files (TRACKER.md, etc.)."""
    s = slug or current_workspace_id()
    if s != INTERNAL_WORKSPACE_ID:
        raise RuntimeError(
            f"This operation only runs against {INTERNAL_WORKSPACE_ID!r}, "
            f"but the active workspace is {s!r}. Refusing to mix dogfood "
            "and customer data."
        )
