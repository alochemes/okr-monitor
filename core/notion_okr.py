"""Notion OKR ingest + seed.

Notion is canonical for OKRs. This module owns three responsibilities:

  1. **Schema** — define what an OKR row looks like in Notion (the column
     contract between humans and the system).

  2. **Seed (push)** — create an OKR database under a parent page and
     populate it from `tracker.extract_okrs()`. One-time, run once after
     the Notion integration is set up.

  3. **Pull (fetch)** — read all rows from the Notion OKR database, return
     them as structured Python, cache to `data/workspaces/<slug>/okrs.json`,
     and regenerate `TRACKER.md §2` so the agent system sees the same
     shape it always has.

The agent system (mapper, signals, narrative) keeps reading TRACKER.md
unchanged. Humans now edit OKRs in Notion. Pulled changes land in the
agent system on the next daily run.
"""

from __future__ import annotations

import json
import os
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from core import notion_client, tracker, workspace
from core.paths import TRACKER_PATH


# ---------------------------------------------------------------------------
# Notion OKR database schema
# ---------------------------------------------------------------------------
#
# Property names are the column titles humans see in Notion. We MATCH on
# these names when reading; renaming a column in Notion will break the
# pull until we re-seed (which is fine — Notion is canonical).
#
# - `KR ID` (title): "1.1", "1.2", … — unique row identifier.
# - `Objective` (select): "O1 — Ship a magical MVP …" — copy of the H3.
# - `Statement` (rich_text): "MVP deployed to production".
# - `Target` (rich_text): "live on Vercel" or "≥85% P @ ≥70% R".
# - `Current` (rich_text): "not started" or "0".
# - `Owner Pod` (select): "Engineering" / "AI/Data" / …
# - `Due Date` (date): YYYY-MM-DD.
# - `Status` (select): one of the values in `STATUS_OPTIONS` below.

STATUS_OPTIONS = [
    {"name": "🔴 Not started", "color": "red"},
    {"name": "🟡 In progress", "color": "yellow"},
    {"name": "🟠 At risk",     "color": "orange"},
    {"name": "🟢 On track",    "color": "green"},
    {"name": "✅ Complete",    "color": "green"},
]

OWNER_POD_OPTIONS = [
    {"name": "Strategy",       "color": "purple"},
    {"name": "Product/Design", "color": "pink"},
    {"name": "Engineering",    "color": "blue"},
    {"name": "AI/Data",        "color": "blue"},
    {"name": "GTM",            "color": "orange"},
    {"name": "Customer/Ops",   "color": "green"},
]


def _objective_select_options(okrs: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Build the Objective-property option list from current OKRs. Notion
    selects need every value pre-declared, so we read TRACKER.md once and
    register one option per Objective."""
    return [
        {"name": _objective_label(o), "color": "default"}
        for o in okrs
    ]


def _objective_label(o: dict[str, Any]) -> str:
    """`O1 — Ship a magical MVP …` (matches TRACKER.md §2)."""
    n = o.get("objective_num")
    title = o.get("objective", "").strip()
    return f"O{n} — {title}"


def _normalize_status(status: str) -> str:
    """Map TRACKER.md statuses (which contain emoji + text already) to one
    of `STATUS_OPTIONS`. Conservative — unknown values become 'Not started'."""
    s = status.strip()
    # The TRACKER.md statuses already include emoji + label. Match by
    # substring of the label part to be tolerant of wording drift.
    if "complete" in s.lower():
        return "✅ Complete"
    if "on track" in s.lower():
        return "🟢 On track"
    if "at risk" in s.lower():
        return "🟠 At risk"
    if "in progress" in s.lower() or "🟡" in s:
        return "🟡 In progress"
    return "🔴 Not started"


def _parse_due(raw: str) -> str | None:
    """TRACKER.md `due` cells look like `2026-05-12` or `ongoing`. Returns
    the ISO date string or None for non-dates."""
    s = raw.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s
    return None


# ---------------------------------------------------------------------------
# Schema (database create payload)

def _database_schema(okrs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "KR ID": {"title": {}},
        "Objective": {
            "select": {"options": _objective_select_options(okrs)},
        },
        "Statement": {"rich_text": {}},
        "Target": {"rich_text": {}},
        "Current": {"rich_text": {}},
        "Owner Pod": {"select": {"options": OWNER_POD_OPTIONS}},
        "Due Date": {"date": {}},
        "Status": {"select": {"options": STATUS_OPTIONS}},
    }


# ---------------------------------------------------------------------------
# Seed (push TRACKER.md §2 → Notion)
# ---------------------------------------------------------------------------

def create_database(*, parent_page_id: str, title: str,
                     okrs: list[dict[str, Any]]) -> dict[str, Any]:
    """Create the OKR database under `parent_page_id`. The parent page must
    already have the Notion integration connected (see INSTRUCTIONS.md)."""
    body = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": _database_schema(okrs),
    }
    return notion_client.post("/databases", body)


def _row_payload(database_id: str, kr: dict[str, Any],
                  objective_label: str) -> dict[str, Any]:
    due = _parse_due(kr.get("due", ""))
    props: dict[str, Any] = {
        "KR ID":     {"title":     [{"type": "text", "text": {"content": kr["id"]}}]},
        "Objective": {"select":    {"name": objective_label}},
        "Statement": {"rich_text": [{"type": "text", "text": {"content": kr.get("description", "")[:1900]}}]},
        "Target":    {"rich_text": [{"type": "text", "text": {"content": kr.get("target", "")[:1900]}}]},
        "Current":   {"rich_text": [{"type": "text", "text": {"content": kr.get("current", "")[:1900]}}]},
        "Owner Pod": {"select":    {"name": kr.get("owner_pod", "").strip() or "Strategy"}},
        "Status":    {"select":    {"name": _normalize_status(kr.get("status", ""))}},
    }
    if due:
        props["Due Date"] = {"date": {"start": due}}
    return {"parent": {"database_id": database_id}, "properties": props}


def seed_database(
    *, parent_page_id: str, title: str = "OKRs",
) -> dict[str, Any]:
    """Create the OKR database and populate it from current TRACKER.md §2.

    Returns `{"database_id": str, "page_ids": [str], "rows_created": int}`.
    Persists the database id into the workspace's `notion.json` so future
    pulls can find it without re-asking.
    """
    workspace.assert_internal()    # never seed against a customer's Notion
    okrs = tracker.extract_okrs()
    if not okrs:
        raise RuntimeError("No OKRs found in TRACKER.md §2 — refusing to seed.")

    db = create_database(parent_page_id=parent_page_id, title=title, okrs=okrs)
    db_id = db["id"]

    page_ids: list[str] = []
    for obj in okrs:
        label = _objective_label(obj)
        for kr in obj["krs"]:
            page = notion_client.post("/pages", _row_payload(db_id, kr, label))
            page_ids.append(page["id"])

    # Persist the IDs for the pull script.
    save_notion_ids(database_id=db_id, parent_page_id=parent_page_id)

    return {"database_id": db_id, "page_ids": page_ids,
            "rows_created": len(page_ids)}


# ---------------------------------------------------------------------------
# Pull (Notion → cache + TRACKER.md §2)
# ---------------------------------------------------------------------------

def fetch_okrs(database_id: str) -> list[dict[str, Any]]:
    """Read every row from the Notion OKR database and return them as a
    list of dicts in TRACKER.md `extract_okrs()` shape — one entry per
    objective, each with a `krs` list."""
    rows = list(notion_client.query_database_all(
        database_id, sorts=[{"property": "KR ID", "direction": "ascending"}],
    ))

    # Group by objective, keyed by the Objective-select label.
    by_obj: dict[str, dict[str, Any]] = {}
    for row in rows:
        props = row.get("properties") or {}
        kr_id = notion_client.read_text(props.get("KR ID", {}))
        if not kr_id:
            continue
        obj_label = notion_client.read_select(props.get("Objective", {}))
        statement = notion_client.read_text(props.get("Statement", {}))
        target    = notion_client.read_text(props.get("Target", {}))
        current   = notion_client.read_text(props.get("Current", {}))
        owner     = notion_client.read_select(props.get("Owner Pod", {}))
        due       = notion_client.read_date(props.get("Due Date", {}))
        status    = notion_client.read_select(props.get("Status", {}))

        if obj_label not in by_obj:
            num = _parse_objective_num(obj_label)
            by_obj[obj_label] = {
                "objective_num": num,
                "objective": _strip_obj_prefix(obj_label, num),
                "krs": [],
            }
        by_obj[obj_label]["krs"].append({
            "id": kr_id,
            "description": statement,
            "target": target,
            "current": current,
            "owner_pod": owner,
            "due": due or "",
            "status": status,
        })

    # Sort by objective_num then by KR id (numeric within objective).
    out = sorted(by_obj.values(), key=lambda o: o["objective_num"] or 999)
    for o in out:
        o["krs"].sort(key=_kr_sort_key)
    return out


_OBJ_LABEL_RE = re.compile(r"^O(\d+)\s+—\s*(.+)$")


def _parse_objective_num(label: str) -> int | None:
    m = _OBJ_LABEL_RE.match(label.strip())
    return int(m.group(1)) if m else None


def _strip_obj_prefix(label: str, num: int | None) -> str:
    if num is None:
        return label
    m = _OBJ_LABEL_RE.match(label.strip())
    return m.group(2).strip() if m else label


def _kr_sort_key(kr: dict[str, Any]) -> tuple[int, int]:
    parts = (kr.get("id") or "0.0").split(".")
    try:
        return (int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return (999, 999)


# ---------------------------------------------------------------------------
# Cache + TRACKER.md §2 regeneration

def write_okrs_cache(okrs: list[dict[str, Any]],
                      *, slug: str | None = None) -> Path:
    """Write the structured OKRs to `data/workspaces/<slug>/okrs.json`."""
    p = workspace.artifact_path("okrs.json", slug)
    payload = {
        "schema": 1,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "objectives": okrs,
    }
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                 encoding="utf-8")
    return p


def render_section_2(okrs: list[dict[str, Any]],
                      *, cycle_label: str | None = None) -> str:
    """Render the structured OKRs back into the TRACKER.md §2 markdown shape.

    7-column table — `KR | Statement | Target | Current | Owner pod | Due |
    Status`. The original TRACKER.md was malformed (6-col header but 7-col
    rows); the regenerated version uses a matching 7-col header so future
    readers don't get confused.
    """
    cycle = cycle_label or _detect_cycle_label() or ""
    lines: list[str] = []
    suffix = f" ({cycle})" if cycle else ""
    lines.append(f"## 2. Company OKRs{suffix}")
    lines.append("")
    for obj in okrs:
        lines.append(f"### O{obj['objective_num']} — {obj['objective']}")
        lines.append("| KR | Statement | Target | Current | Owner pod | Due | Status |")
        lines.append("|---|---|---|---|---|---|---|")
        for kr in obj["krs"]:
            lines.append(
                f"| {kr['id']} | "
                f"{_md_cell(kr.get('description'))} | "
                f"{_md_cell(kr.get('target'))} | "
                f"{_md_cell(kr.get('current'))} | "
                f"{_md_cell(kr.get('owner_pod'))} | "
                f"{_md_cell(kr.get('due'))} | "
                f"{_md_cell(kr.get('status'))} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _md_cell(v: str | None) -> str:
    """Escape pipes in cell values so the table doesn't break."""
    s = (v or "").strip().replace("|", r"\|")
    return s or "—"


def _detect_cycle_label() -> str | None:
    """Pull the cycle range out of the existing §2 header so we don't lose
    `(2026-04-28 → 2026-08-28)` on regeneration."""
    text = TRACKER_PATH.read_text(encoding="utf-8")
    m = re.search(r"^##\s+2\.\s+Company OKRs\s*\(([^)]+)\)\s*$", text, re.MULTILINE)
    return m.group(1) if m else None


_S2_REGION_RE = re.compile(
    r"(?P<head>^##\s+2\.[^\n]*\n)"
    r"(?P<body>.*?)"
    r"(?P<tail>(?:\n---\n+)?##\s+3\.)",
    re.DOTALL | re.MULTILINE,
)


def replace_tracker_section_2(new_md: str) -> None:
    """Atomically replace §2 of TRACKER.md with `new_md`. Preserves the
    `## 2. …` header and the divider that precedes `## 3. …`.

    Refuses to run unless the active workspace is `okrmonitor-internal` —
    customer data must never reach this file.
    """
    workspace.assert_internal()

    text = TRACKER_PATH.read_text(encoding="utf-8")
    m = _S2_REGION_RE.search(text)
    if not m:
        raise RuntimeError(
            "Could not locate §2 / §3 boundary in TRACKER.md. The pull "
            "script refuses to overwrite the file when it can't find the "
            "section anchors — fix the markdown manually first."
        )

    # `new_md` already includes the `## 2. …` header (from render_section_2).
    # Drop our generated header so we don't duplicate the existing one.
    body_lines = new_md.splitlines()
    if body_lines and body_lines[0].startswith("## 2. "):
        body_lines = body_lines[1:]
        # Skip a single leading blank line if present.
        if body_lines and not body_lines[0].strip():
            body_lines = body_lines[1:]
    body_only = "\n".join(body_lines).rstrip() + "\n"

    rebuilt = (
        text[: m.start("body")]
        + "\n" + body_only + "\n---\n\n"
        + text[m.start("tail") + len("\n---\n\n"):]
        if "\n---\n\n## 3." in m.group(0) else
        text[: m.start("body")]
        + "\n" + body_only + "\n"
        + text[m.start("tail"):]
    )

    # Atomic write.
    tmp = TRACKER_PATH.with_suffix(".md.tmp")
    tmp.write_text(rebuilt, encoding="utf-8")
    tmp.replace(TRACKER_PATH)


# ---------------------------------------------------------------------------
# Notion ID persistence (per workspace)

def save_notion_ids(*, database_id: str | None = None,
                     parent_page_id: str | None = None,
                     slug: str | None = None) -> dict[str, Any]:
    """Merge new ids into `data/workspaces/<slug>/notion.json`."""
    p = workspace.artifact_path("notion.json", slug)
    data: dict[str, Any] = {}
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8")) or {}
        except json.JSONDecodeError:
            data = {}
    if database_id is not None:
        data["okr_database_id"] = database_id
    if parent_page_id is not None:
        data["parent_page_id"] = parent_page_id
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def load_notion_ids(slug: str | None = None) -> dict[str, Any]:
    p = workspace.artifact_path("notion.json", slug)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def configured_database_id(slug: str | None = None) -> str | None:
    """Resolve the OKR DB id for `slug`. Order of precedence:
       1. `NOTION_OKR_DATABASE_ID` env (lets cron override per-run)
       2. `notion.json` in the workspace dir
    """
    env_val = os.environ.get("NOTION_OKR_DATABASE_ID", "").strip()
    if env_val:
        return env_val
    return load_notion_ids(slug).get("okr_database_id") or None


# ---------------------------------------------------------------------------
# High-level: pull-and-update

def pull_and_update(*, slug: str | None = None,
                    database_id: str | None = None,
                    update_tracker: bool = True) -> dict[str, Any]:
    """Pull OKRs from Notion, refresh the cache, and (if `update_tracker`)
    regenerate TRACKER.md §2.

    Returns a stats dict. Safe to call from `daily_evening.py`.
    """
    db_id = database_id or configured_database_id(slug)
    if not db_id:
        return {"ok": False, "skipped": "no_database_id_configured",
                "objectives": 0, "krs": 0}

    okrs = fetch_okrs(db_id)
    cache_path = write_okrs_cache(okrs, slug=slug)
    kr_count = sum(len(o["krs"]) for o in okrs)

    tracker_updated = False
    if update_tracker and workspace.is_internal(slug):
        try:
            new_md = render_section_2(okrs)
            replace_tracker_section_2(new_md)
            tracker.load_text(reload=True)    # bust the lru_cache
            tracker_updated = True
        except Exception as exc:    # pragma: no cover
            return {
                "ok": False, "error": str(exc),
                "objectives": len(okrs), "krs": kr_count,
                "cache_path": str(cache_path),
                "tracker_updated": False,
            }

    return {
        "ok": True,
        "database_id": db_id,
        "objectives": len(okrs),
        "krs": kr_count,
        "cache_path": str(cache_path),
        "tracker_updated": tracker_updated,
    }
