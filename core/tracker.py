"""Read and lightly parse TRACKER.md.

The full markdown is the truth. This module exposes:
- `load_text()` — return the raw file (cached per process unless `reload=True`).
- `extract_section(name)` — slice a top-level `## N. Title` section.
- `extract_okrs()` — pull objectives + KR tables from §2 into structured dicts.
- `extract_agent_roster()` — parse §4 into a list of {num, name, pod, status}.

We deliberately do NOT try to parse everything. Agents read the raw markdown
in their system prompt. Structured extraction is a convenience for analytics
and for the future web UI.
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

from core.paths import TRACKER_PATH


@lru_cache(maxsize=1)
def _cached_text() -> str:
    if not TRACKER_PATH.exists():
        raise FileNotFoundError(f"TRACKER.md not found at {TRACKER_PATH}")
    return TRACKER_PATH.read_text(encoding="utf-8")


def load_text(*, reload: bool = False) -> str:
    """Return the raw TRACKER.md content. Pass reload=True to bypass cache."""
    if reload:
        _cached_text.cache_clear()
    return _cached_text()


_SECTION_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.MULTILINE)


def extract_section(number: int) -> str:
    """Return the body of section `## N. ...` up to the next `## ` header.
    Empty string if not found."""
    text = load_text()
    matches = list(_SECTION_RE.finditer(text))
    for i, m in enumerate(matches):
        if int(m.group(1)) == number:
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            return text[start:end].strip()
    return ""


# ---------- OKR table parsing -------------------------------------------

# A KR row in the markdown looks like:
#   | 1.1 | MVP deployed to production | live on Vercel | not started | Engineering | 2026-05-12 | 🔴 Not started |
_KR_ROW_RE = re.compile(
    r"^\|\s*(\d+\.\d+)\s*\|"
    r"\s*([^|]+?)\s*\|"
    r"\s*([^|]+?)\s*\|"
    r"\s*([^|]+?)\s*\|"
    r"\s*([^|]+?)\s*\|"
    r"\s*([^|]+?)\s*\|"
    r"\s*([^|]+?)\s*\|\s*$",
    re.MULTILINE,
)
_OBJECTIVE_RE = re.compile(r"^###\s+O(\d+)\s+—\s+(.+?)\s*$", re.MULTILINE)


def extract_okrs() -> list[dict[str, Any]]:
    """Parse §2 into [{objective_num, objective, krs: [{id, target, current,
    owner, due, status, ...}]}]. Returns [] on parse miss."""
    body = extract_section(2)
    if not body:
        return []

    objectives: list[dict[str, Any]] = []
    obj_matches = list(_OBJECTIVE_RE.finditer(body))
    for i, m in enumerate(obj_matches):
        start = m.end()
        end = obj_matches[i + 1].start() if i + 1 < len(obj_matches) else len(body)
        obj_block = body[start:end]
        krs: list[dict[str, Any]] = []
        for row in _KR_ROW_RE.finditer(obj_block):
            kr_id, desc, target, current, owner, due, status = (
                row.group(j).strip() for j in range(1, 8)
            )
            if kr_id.lower() == "kr":
                continue
            krs.append({
                "id": kr_id,
                "description": desc,
                "target": target,
                "current": current,
                "owner_pod": owner,
                "due": due,
                "status": status,
            })
        objectives.append({
            "objective_num": int(m.group(1)),
            "objective": m.group(2).strip(),
            "krs": krs,
        })
    return objectives


# ---------- Agent roster parsing -----------------------------------------

# Roster row:
#   | 1 | ceo | Strategy | 🔴 | `agents/ceo/` |
_ROSTER_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|"
    r"\s*([a-z_]+)\s*\|"
    r"\s*([^|]+?)\s*\|"
    r"\s*([^|]+?)\s*\|"
    r"\s*`([^`]+)`\s*\|\s*$",
    re.MULTILINE,
)


def extract_agent_roster() -> list[dict[str, Any]]:
    body = extract_section(4)
    if not body:
        return []
    out: list[dict[str, Any]] = []
    for row in _ROSTER_ROW_RE.finditer(body):
        out.append({
            "num": int(row.group(1)),
            "name": row.group(2).strip(),
            "pod": row.group(3).strip(),
            "status": row.group(4).strip(),
            "path": row.group(5).strip(),
        })
    return out
