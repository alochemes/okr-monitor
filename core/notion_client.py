"""Minimal Notion REST client. Stdlib-only.

Single place where we talk to api.notion.com. Other modules
(`core.notion_okr`, future `core.notion_intake`, etc.) compose calls from
this module so we have one auth path, one error type, one place to bump
the API version.

`scripts/notion_import.py` (the KB importer) was written before this
module existed and has its own inline client; it can be migrated later
without changing behavior.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Iterator


_API = "https://api.notion.com/v1"
_VERSION = "2022-06-28"


class NotionError(RuntimeError):
    """Raised when Notion returns a non-2xx response or when the SDK key is
    missing. Carries `status` + `body` for debugging."""

    def __init__(self, status: int, body: str, *, hint: str | None = None):
        msg = f"Notion {status}: {body[:300]}"
        if hint:
            msg += f"\n  hint: {hint}"
        super().__init__(msg)
        self.status = status
        self.body = body


def _token() -> str:
    tok = os.environ.get("NOTION_API_KEY", "").strip()
    if not tok:
        raise NotionError(
            401, "NOTION_API_KEY not set",
            hint="See INSTRUCTIONS.md → 'Set up the Notion integration'.",
        )
    return tok


def _request(method: str, path: str, body: dict | None = None) -> dict[str, Any]:
    url = f"{_API}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {_token()}")
    req.add_header("Notion-Version", _VERSION)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "okr-monitor/0.1")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = resp.read().decode("utf-8")
            return json.loads(payload) if payload else {}
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        hint = None
        if exc.code == 401:
            hint = "Token rejected — check NOTION_API_KEY in .env."
        elif exc.code == 404:
            hint = (
                "Notion 404 usually means the integration hasn't been "
                "granted access to that page/DB. In Notion: ⋯ → "
                "Connections → add 'OKR Monitor'."
            )
        raise NotionError(exc.code, body_text, hint=hint) from exc


# ---------- Verbs ----------------------------------------------------------

def get(path: str) -> dict[str, Any]:
    return _request("GET", path)


def post(path: str, body: dict[str, Any]) -> dict[str, Any]:
    return _request("POST", path, body)


def patch(path: str, body: dict[str, Any]) -> dict[str, Any]:
    return _request("PATCH", path, body)


# ---------- Database queries with pagination ------------------------------

def query_database_all(database_id: str,
                        filter_: dict | None = None,
                        sorts: list[dict] | None = None,
                        page_size: int = 100) -> Iterator[dict[str, Any]]:
    """Yield every row in a Notion DB. Handles cursor pagination."""
    body: dict[str, Any] = {"page_size": page_size}
    if filter_:
        body["filter"] = filter_
    if sorts:
        body["sorts"] = sorts
    cursor: str | None = None
    while True:
        if cursor:
            body["start_cursor"] = cursor
        elif "start_cursor" in body:
            del body["start_cursor"]
        data = post(f"/databases/{database_id}/query", body)
        for row in data.get("results") or []:
            yield row
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
        if not cursor:
            break


# ---------- Tiny helpers for property reads -------------------------------

def read_text(prop: dict[str, Any]) -> str:
    """Extract a plain string from a rich_text or title property."""
    if not prop:
        return ""
    arr = prop.get("rich_text") or prop.get("title") or []
    return "".join(seg.get("plain_text", "") for seg in arr).strip()


def read_select(prop: dict[str, Any]) -> str:
    if not prop:
        return ""
    sel = prop.get("select")
    return (sel or {}).get("name", "") if sel else ""


def read_date(prop: dict[str, Any]) -> str:
    if not prop:
        return ""
    d = prop.get("date") or {}
    return (d.get("start") or "")[:10]
