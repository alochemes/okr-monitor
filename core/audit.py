"""Append-only JSONL audit log. One file per UTC day under data/audit/.

Every consequential decision in the system writes one event here. The audit
log is the system of record for "why did the agent do X" — SQLite is the
queryable view, this is the source.

Events are flat JSON objects. Schema is intentionally permissive so we can
evolve fields without migrations; readers must tolerate unknown keys.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from typing import Any

from core.paths import AUDIT_DIR

_LOCK = threading.Lock()


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _today_path() -> str:
    return str(AUDIT_DIR / f"{datetime.now(timezone.utc).date().isoformat()}.jsonl")


def emit(
    *,
    run_id: str | None,
    agent: str,
    action: str,
    subject_type: str | None = None,
    subject_id: str | None = None,
    payload: dict[str, Any] | None = None,
    model: str | None = None,
    tokens_in: int | None = None,
    tokens_out: int | None = None,
    cost_usd: float | None = None,
    severity: str = "info",
) -> None:
    """Append one audit event. Never raises on disk error — audit must not
    take down the pipeline. Failures are written to stderr."""
    event = {
        "ts": _utcnow_iso(),
        "run_id": run_id,
        "agent": agent,
        "action": action,
        "severity": severity,
        "subject_type": subject_type,
        "subject_id": subject_id,
        "model": model,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": cost_usd,
        "pid": os.getpid(),
        "payload": payload or {},
    }
    line = json.dumps(event, separators=(",", ":"), ensure_ascii=False, default=str)
    try:
        with _LOCK:
            with open(_today_path(), "a", encoding="utf-8") as f:
                f.write(line + "\n")
    except OSError as exc:  # pragma: no cover
        import sys

        print(f"[audit] write failure: {exc}\n  event={line[:300]}", file=sys.stderr)
