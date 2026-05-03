"""Notion OKR source — thin wrapper over `core.notion_okr.fetch_okrs`.

Status: shipped. Notion is the reference implementation; this wrapper
exists so the dispatcher in `core/okr_pull.py` (Sprint 1) can treat
Notion the same as any other source.

See `core/notion_okr.py` for the actual implementation.
"""

from __future__ import annotations

from typing import Any

from core import notion_okr


def fetch_okrs(workspace_slug: str, *, config: dict[str, Any]) -> list[dict[str, Any]]:
    """Pull OKRs from the configured Notion DB. `config` keys:
       - database_id (required) — the Notion OKR DB id

    Returns canonical OKR shape (see design doc §1a)."""
    db_id = config.get("database_id") or notion_okr.configured_database_id(workspace_slug)
    if not db_id:
        return []
    return notion_okr.fetch_okrs(db_id)
