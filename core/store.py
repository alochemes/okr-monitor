"""SQLite-backed state store. The schema is the contract between agents and
review tools — change it deliberately.

Design notes:
- One DB file at data/okr_monitor.db. WAL mode for concurrent reads.
- All timestamps are stored as ISO-8601 UTC strings.
- Every row that represents an LLM-derived artifact carries the run_id and
  the model that produced it, so reproducibility is preserved.
- IDs: UUIDs for internal artifacts. Source-native IDs (github commit sha,
  linear issue id) when those land later.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterator

from core.paths import DB_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id              TEXT PRIMARY KEY,
    agent           TEXT NOT NULL,
    kind            TEXT NOT NULL,
    started_at      TEXT NOT NULL,
    ended_at        TEXT,
    status          TEXT NOT NULL,           -- running | ok | error | aborted
    stats_json      TEXT,
    error_text      TEXT
);

CREATE INDEX IF NOT EXISTS idx_runs_agent_started ON runs(agent, started_at DESC);

-- A proposal is an agent's recommendation to the operator. Nothing acts on the
-- world until a proposal is reviewed and approved.
CREATE TABLE IF NOT EXISTS proposals (
    id              TEXT PRIMARY KEY,        -- uuid
    run_id          TEXT NOT NULL,
    agent           TEXT NOT NULL,
    kind            TEXT NOT NULL,           -- weekly_priorities | roadmap_review | architecture_review | pricing_model | ...
    title           TEXT NOT NULL,
    summary         TEXT NOT NULL,
    body_md         TEXT NOT NULL,           -- the full proposal as markdown
    evidence_json   TEXT NOT NULL,           -- structured payload (source rows, KR refs, etc.)
    confidence      REAL,                    -- 0..1, agent's self-rated confidence
    model           TEXT NOT NULL,
    tokens_in       INTEGER,
    tokens_out      INTEGER,
    cost_usd        REAL,
    created_at      TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs(id)
);

CREATE INDEX IF NOT EXISTS idx_proposals_agent_kind_created
    ON proposals(agent, kind, created_at DESC);

-- A review is the operator's decision on a proposal. Edits are tracked so we
-- can compute "how much did the operator change" — the same trust signal
-- skinmap_agents uses for promotion gating.
CREATE TABLE IF NOT EXISTS proposal_reviews (
    id                  TEXT PRIMARY KEY,
    proposal_id         TEXT NOT NULL UNIQUE,
    decision            TEXT NOT NULL,       -- approve | edit | reject | defer
    final_text          TEXT,                -- the operator's final markdown if edited
    edit_distance       REAL,                -- 0..1 normalized; 0 = unchanged
    time_to_review_s    INTEGER,
    reviewed_by         TEXT NOT NULL,
    reviewed_at         TEXT NOT NULL,
    notes               TEXT,
    FOREIGN KEY (proposal_id) REFERENCES proposals(id)
);

-- A snapshot of TRACKER.md at the moment an agent ran. Lets us see what state
-- the agent was reasoning over and detect drift between the tracker and the
-- world (commits, tickets) once those land.
CREATE TABLE IF NOT EXISTS tracker_snapshots (
    id              TEXT PRIMARY KEY,
    snapshot_at     TEXT NOT NULL,
    sha256          TEXT NOT NULL,
    content         TEXT NOT NULL,
    UNIQUE(sha256)
);

CREATE INDEX IF NOT EXISTS idx_tracker_snapshots_at ON tracker_snapshots(snapshot_at DESC);

-- A "work event" is anything that happened in the company that can plausibly
-- be tied to a KR: a code commit, a ticket, a Slack thread — and, in our
-- dogfood loop, an internal agent proposal. Source-native ID is preserved so
-- ingestion is idempotent.
CREATE TABLE IF NOT EXISTS work_events (
    id              TEXT PRIMARY KEY,        -- uuid
    source          TEXT NOT NULL,           -- agent_proposal | github | linear | jira | slack | manual
    source_event_id TEXT NOT NULL,           -- proposal_id, commit sha, issue id, etc.
    kind            TEXT,                    -- commit | pr | issue_opened | message | proposal | ...
    title           TEXT NOT NULL,
    body            TEXT,
    actor           TEXT,                    -- agent name, github user, slack user
    occurred_at     TEXT NOT NULL,
    raw_json        TEXT,
    created_at      TEXT NOT NULL,
    UNIQUE(source, source_event_id)
);

CREATE INDEX IF NOT EXISTS idx_work_events_occurred ON work_events(occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_work_events_source_actor ON work_events(source, actor);

-- An okr_mapper output: one row per (event, kr) link with confidence. An event
-- can map to zero, one, or many KRs.
CREATE TABLE IF NOT EXISTS event_kr_mappings (
    id              TEXT PRIMARY KEY,        -- uuid
    event_id        TEXT NOT NULL,
    run_id          TEXT NOT NULL,
    kr_id           TEXT NOT NULL,           -- "1.3", "4.2", etc. — must exist in TRACKER.md §2
    confidence      REAL NOT NULL,           -- 0..1
    reasoning       TEXT,
    model           TEXT NOT NULL,
    tokens_in       INTEGER,
    tokens_out      INTEGER,
    cost_usd        REAL,
    created_at      TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES work_events(id),
    FOREIGN KEY (run_id) REFERENCES runs(id)
);

CREATE INDEX IF NOT EXISTS idx_event_kr_event ON event_kr_mappings(event_id);
CREATE INDEX IF NOT EXISTS idx_event_kr_kr_created ON event_kr_mappings(kr_id, created_at DESC);

-- Output of the narrative agent: a markdown brief covering one time window.
CREATE TABLE IF NOT EXISTS narratives (
    id              TEXT PRIMARY KEY,
    run_id          TEXT NOT NULL,
    period_start    TEXT NOT NULL,           -- ISO date inclusive
    period_end      TEXT NOT NULL,           -- ISO date inclusive
    title           TEXT NOT NULL,
    body_md         TEXT NOT NULL,
    evidence_json   TEXT NOT NULL,           -- {kr_summaries, events_count, mappings_count, ...}
    model           TEXT NOT NULL,
    tokens_in       INTEGER,
    tokens_out      INTEGER,
    cost_usd        REAL,
    created_at      TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs(id)
);

CREATE INDEX IF NOT EXISTS idx_narratives_period ON narratives(period_end DESC);

-- Per-KR computed signals (no LLM). Written by signals_analyst, enriched by
-- forecasting. One row per (kr_id, computed_at) — keep the history so we can
-- chart pace over time.
CREATE TABLE IF NOT EXISTS kr_signals (
    id              TEXT PRIMARY KEY,
    run_id          TEXT NOT NULL,
    kr_id           TEXT NOT NULL,
    computed_at     TEXT NOT NULL,
    -- Mapping-derived counts:
    events_total      INTEGER NOT NULL,
    events_7d         INTEGER NOT NULL,
    events_30d        INTEGER NOT NULL,
    distinct_actors   INTEGER NOT NULL,
    last_event_at     TEXT,
    mean_confidence   REAL,
    -- Forecast columns (populated by forecasting agent; NULL if unparseable):
    target_raw        TEXT,
    target_numeric    REAL,
    current_numeric   REAL,
    due_date          TEXT,
    days_remaining    INTEGER,
    pace_per_day      REAL,
    pace_required     REAL,
    forecast_verdict  TEXT,           -- on_track | drifting | off | qualitative
    forecast_p_hit    REAL,
    FOREIGN KEY (run_id) REFERENCES runs(id)
);

CREATE INDEX IF NOT EXISTS idx_kr_signals_kr_computed ON kr_signals(kr_id, computed_at DESC);

-- KPI rollups (daily). Same shape as skinmap_agents.
CREATE TABLE IF NOT EXISTS kpi_daily (
    day             TEXT NOT NULL,            -- YYYY-MM-DD
    metric          TEXT NOT NULL,
    value           REAL NOT NULL,
    PRIMARY KEY (day, metric)
);
"""


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    conn = _connect()
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Create tables if they don't exist. Idempotent."""
    with connect() as conn:
        conn.executescript(SCHEMA)


# ---------- Runs ----------------------------------------------------------

def start_run(agent: str, kind: str) -> str:
    run_id = str(uuid.uuid4())
    with connect() as conn:
        conn.execute(
            "INSERT INTO runs (id, agent, kind, started_at, status)"
            " VALUES (?, ?, ?, ?, 'running')",
            (run_id, agent, kind, _utcnow()),
        )
    return run_id


def end_run(run_id: str, status: str, stats: dict | None = None, error: str | None = None) -> None:
    with connect() as conn:
        conn.execute(
            "UPDATE runs SET ended_at = ?, status = ?, stats_json = ?, error_text = ?"
            " WHERE id = ?",
            (_utcnow(), status, json.dumps(stats or {}), error, run_id),
        )


# ---------- Tracker snapshots --------------------------------------------

def upsert_tracker_snapshot(content: str) -> tuple[str, bool]:
    """Insert a tracker snapshot if its sha256 is new. Returns (snapshot_id,
    was_new). Idempotent: same content → same row."""
    sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
    with connect() as conn:
        existing = conn.execute(
            "SELECT id FROM tracker_snapshots WHERE sha256 = ?", (sha,),
        ).fetchone()
        if existing:
            return existing["id"], False
        sid = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO tracker_snapshots (id, snapshot_at, sha256, content)"
            " VALUES (?, ?, ?, ?)",
            (sid, _utcnow(), sha, content),
        )
        return sid, True


# ---------- Proposals ----------------------------------------------------

def write_proposal(
    *,
    run_id: str,
    agent: str,
    kind: str,
    title: str,
    summary: str,
    body_md: str,
    evidence: dict,
    confidence: float | None,
    model: str,
    tokens_in: int | None,
    tokens_out: int | None,
    cost_usd: float | None,
) -> str:
    pid = str(uuid.uuid4())
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO proposals (id, run_id, agent, kind, title, summary, body_md,
                evidence_json, confidence, model, tokens_in, tokens_out, cost_usd, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (pid, run_id, agent, kind, title, summary, body_md,
             json.dumps(evidence), confidence, model,
             tokens_in, tokens_out, cost_usd, _utcnow()),
        )
    return pid


def list_pending_proposals(limit: int = 50) -> list[sqlite3.Row]:
    """Proposals with no review row yet, newest first."""
    with connect() as conn:
        cur = conn.execute(
            """
            SELECT p.id AS proposal_id, p.run_id, p.agent, p.kind, p.title,
                   p.summary, p.body_md, p.evidence_json, p.confidence,
                   p.model, p.created_at
            FROM proposals p
            LEFT JOIN proposal_reviews r ON r.proposal_id = p.id
            WHERE r.id IS NULL
            ORDER BY p.created_at DESC
            LIMIT ?
            """,
            (limit,),
        )
        return list(cur.fetchall())


def write_proposal_review(
    *,
    proposal_id: str,
    decision: str,
    final_text: str | None,
    edit_distance: float | None,
    time_to_review_s: int | None,
    reviewed_by: str,
    notes: str | None = None,
) -> str:
    rid = str(uuid.uuid4())
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO proposal_reviews (id, proposal_id, decision, final_text,
                edit_distance, time_to_review_s, reviewed_by, reviewed_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (rid, proposal_id, decision, final_text, edit_distance,
             time_to_review_s, reviewed_by, _utcnow(), notes),
        )
    return rid


# ---------- Work events --------------------------------------------------

def upsert_work_event(
    *,
    source: str,
    source_event_id: str,
    kind: str | None,
    title: str,
    body: str | None,
    actor: str | None,
    occurred_at: str,
    raw: dict | None = None,
) -> tuple[str, bool]:
    """Insert a work_event if (source, source_event_id) is new. Returns
    (event_id, was_new). Idempotent — same source+id → same row, returns
    existing id with was_new=False."""
    with connect() as conn:
        existing = conn.execute(
            "SELECT id FROM work_events WHERE source = ? AND source_event_id = ?",
            (source, source_event_id),
        ).fetchone()
        if existing:
            return existing["id"], False
        eid = str(uuid.uuid4())
        conn.execute(
            """
            INSERT INTO work_events (id, source, source_event_id, kind, title,
                body, actor, occurred_at, raw_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (eid, source, source_event_id, kind, title, body, actor,
             occurred_at, json.dumps(raw or {}), _utcnow()),
        )
        return eid, True


def list_unmapped_events(limit: int = 100) -> list[sqlite3.Row]:
    """Events with no event_kr_mappings row yet. Newest first."""
    with connect() as conn:
        cur = conn.execute(
            """
            SELECT e.id, e.source, e.source_event_id, e.kind, e.title, e.body,
                   e.actor, e.occurred_at
            FROM work_events e
            LEFT JOIN event_kr_mappings m ON m.event_id = e.id
            WHERE m.id IS NULL
            ORDER BY e.occurred_at DESC
            LIMIT ?
            """,
            (limit,),
        )
        return list(cur.fetchall())


def list_events_in_window(*, start_iso: str, end_iso: str) -> list[sqlite3.Row]:
    with connect() as conn:
        cur = conn.execute(
            "SELECT * FROM work_events WHERE occurred_at >= ? AND occurred_at <= ?"
            " ORDER BY occurred_at",
            (start_iso, end_iso),
        )
        return list(cur.fetchall())


# ---------- Event ↔ KR mappings ------------------------------------------

def write_event_kr_mappings(
    *,
    event_id: str,
    run_id: str,
    mappings: list[dict],   # [{kr_id, confidence, reasoning}]
    model: str,
    tokens_in: int | None,
    tokens_out: int | None,
    cost_usd: float | None,
) -> list[str]:
    """Insert one row per (event, kr) link. Returns the new mapping ids."""
    ids: list[str] = []
    with connect() as conn:
        for m in mappings:
            mid = str(uuid.uuid4())
            conn.execute(
                """
                INSERT INTO event_kr_mappings (id, event_id, run_id, kr_id,
                    confidence, reasoning, model, tokens_in, tokens_out, cost_usd, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (mid, event_id, run_id, str(m["kr_id"]),
                 float(m.get("confidence", 0.0)),
                 m.get("reasoning"),
                 model, tokens_in, tokens_out, cost_usd, _utcnow()),
            )
            ids.append(mid)
    return ids


def list_mappings_in_window(*, start_iso: str, end_iso: str) -> list[sqlite3.Row]:
    """All mappings whose event occurred in [start, end]. Joined with the
    event so the narrative agent has the title/body without a second query."""
    with connect() as conn:
        cur = conn.execute(
            """
            SELECT m.id AS mapping_id, m.kr_id, m.confidence, m.reasoning,
                   e.id AS event_id, e.source, e.kind, e.title, e.body,
                   e.actor, e.occurred_at
            FROM event_kr_mappings m
            JOIN work_events e ON e.id = m.event_id
            WHERE e.occurred_at >= ? AND e.occurred_at <= ?
            ORDER BY m.kr_id, e.occurred_at
            """,
            (start_iso, end_iso),
        )
        return list(cur.fetchall())


# ---------- Narratives ---------------------------------------------------

def write_narrative(
    *,
    run_id: str,
    period_start: str,
    period_end: str,
    title: str,
    body_md: str,
    evidence: dict,
    model: str,
    tokens_in: int | None,
    tokens_out: int | None,
    cost_usd: float | None,
) -> str:
    nid = str(uuid.uuid4())
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO narratives (id, run_id, period_start, period_end,
                title, body_md, evidence_json, model, tokens_in, tokens_out,
                cost_usd, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (nid, run_id, period_start, period_end, title, body_md,
             json.dumps(evidence), model, tokens_in, tokens_out,
             cost_usd, _utcnow()),
        )
    return nid


# ---------- KR signals (no-LLM compute) ----------------------------------

def write_kr_signal(
    *,
    run_id: str,
    kr_id: str,
    computed_at: str,
    events_total: int,
    events_7d: int,
    events_30d: int,
    distinct_actors: int,
    last_event_at: str | None,
    mean_confidence: float | None,
    # Forecast fields — caller passes None when not yet computed.
    target_raw: str | None = None,
    target_numeric: float | None = None,
    current_numeric: float | None = None,
    due_date: str | None = None,
    days_remaining: int | None = None,
    pace_per_day: float | None = None,
    pace_required: float | None = None,
    forecast_verdict: str | None = None,
    forecast_p_hit: float | None = None,
) -> str:
    sid = str(uuid.uuid4())
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO kr_signals (id, run_id, kr_id, computed_at,
                events_total, events_7d, events_30d, distinct_actors,
                last_event_at, mean_confidence,
                target_raw, target_numeric, current_numeric, due_date,
                days_remaining, pace_per_day, pace_required,
                forecast_verdict, forecast_p_hit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (sid, run_id, kr_id, computed_at,
             events_total, events_7d, events_30d, distinct_actors,
             last_event_at, mean_confidence,
             target_raw, target_numeric, current_numeric, due_date,
             days_remaining, pace_per_day, pace_required,
             forecast_verdict, forecast_p_hit),
        )
    return sid


def latest_kr_signals() -> list[sqlite3.Row]:
    """One row per KR — the most recently computed signal for each."""
    with connect() as conn:
        cur = conn.execute(
            """
            SELECT s.* FROM kr_signals s
            JOIN (
                SELECT kr_id, MAX(computed_at) AS max_ca
                FROM kr_signals GROUP BY kr_id
            ) t ON s.kr_id = t.kr_id AND s.computed_at = t.max_ca
            ORDER BY s.kr_id
            """
        )
        return list(cur.fetchall())


def list_mappings_for_kr(kr_id: str) -> list[sqlite3.Row]:
    """All mappings for one KR with the joined event row, newest first."""
    with connect() as conn:
        cur = conn.execute(
            """
            SELECT m.id AS mapping_id, m.confidence, m.reasoning,
                   e.id AS event_id, e.source, e.kind, e.title, e.actor,
                   e.occurred_at
            FROM event_kr_mappings m
            JOIN work_events e ON e.id = m.event_id
            WHERE m.kr_id = ?
            ORDER BY e.occurred_at DESC
            """,
            (kr_id,),
        )
        return list(cur.fetchall())


# ---------- KPI -----------------------------------------------------------

def write_kpi(day: str, metric: str, value: float) -> None:
    with connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO kpi_daily (day, metric, value) VALUES (?, ?, ?)",
            (day, metric, value),
        )


def read_kpi_window(metric: str, days: int) -> list[sqlite3.Row]:
    with connect() as conn:
        cur = conn.execute(
            "SELECT day, value FROM kpi_daily WHERE metric = ?"
            " ORDER BY day DESC LIMIT ?",
            (metric, days),
        )
        return list(cur.fetchall())
