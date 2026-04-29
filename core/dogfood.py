"""Internal dogfood loop: every agent proposal becomes a `work_event` so the
OKR-Mapper can map it to KRs and the Narrative agent can summarize it
alongside whatever real customer events come in later (commits, tickets,
Slack threads).

This is not a generic ingestion API — it knows the shape of `proposals`. When
real integrations land in Sprint 0/1, they'll write to `work_events` directly
via `store.upsert_work_event` with their own source-native IDs.
"""

from __future__ import annotations

from typing import Any

from core import audit, store


def ingest_proposal_as_event(proposal_row: dict[str, Any]) -> tuple[str, bool]:
    """Turn one proposal into one work_event. Idempotent on proposal_id."""
    eid, was_new = store.upsert_work_event(
        source="agent_proposal",
        source_event_id=proposal_row["id"],
        kind=f"proposal.{proposal_row.get('kind', 'unknown')}",
        title=proposal_row.get("title") or "(untitled proposal)",
        body=proposal_row.get("body_md") or proposal_row.get("summary") or "",
        actor=proposal_row.get("agent"),
        occurred_at=proposal_row["created_at"],
        raw={"proposal_id": proposal_row["id"],
             "agent": proposal_row.get("agent"),
             "kind": proposal_row.get("kind"),
             "model": proposal_row.get("model"),
             "confidence": proposal_row.get("confidence")},
    )
    audit.emit(
        run_id=None, agent="dogfood", action="proposal.ingested",
        subject_type="work_event", subject_id=eid,
        payload={"proposal_id": proposal_row["id"],
                 "was_new": was_new, "agent": proposal_row.get("agent")},
    )
    return eid, was_new


def ingest_recent_proposals(limit: int = 20) -> list[dict[str, Any]]:
    """Walk recent proposals and ingest any that aren't already work_events.
    Returns a list of {proposal_id, event_id, was_new} dicts."""
    out: list[dict[str, Any]] = []
    with store.connect() as conn:
        rows = conn.execute(
            """
            SELECT p.id, p.agent, p.kind, p.title, p.summary, p.body_md,
                   p.confidence, p.model, p.created_at
            FROM proposals p
            ORDER BY p.created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    for r in rows:
        eid, was_new = ingest_proposal_as_event(dict(r))
        out.append({"proposal_id": r["id"], "event_id": eid, "was_new": was_new})
    return out
