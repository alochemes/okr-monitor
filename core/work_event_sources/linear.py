"""Linear work-event source — thin wrapper over `core.linear_ingest`.

Status: shipped. See `core/linear_ingest.py`.
"""

from __future__ import annotations

from typing import Any

from core import linear_ingest


def poll(workspace_slug: str, *, config: dict[str, Any],
         since_days: int = 7) -> dict[str, Any]:
    """Pull recently-updated issues. `config` keys:
       - team_key: optional Linear team key (e.g. "ENG"); omit for workspace-wide.
    """
    if not linear_ingest.is_configured():
        return {"ok": True, "skipped": "no_api_key",
                "events_written": 0, "events_seen": 0}
    return linear_ingest.poll_workspace(
        since_days=since_days,
        team_key=config.get("team_key"),
    )
