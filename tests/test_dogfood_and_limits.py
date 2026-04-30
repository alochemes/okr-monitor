"""Tests for core/dogfood.py + extended cases for core/limits.py.

dogfood.py turns each strategy proposal into a work_event. If this breaks,
the dogfood loop silently dies and the OKR-Mapper has nothing to map.
limits.py already has 5 tests; we add edge-case coverage here.

Run with:
  python -m tests.test_dogfood_and_limits
"""

from __future__ import annotations

import os
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))
os.environ["OKR_MONITOR_DRY_RUN"] = "true"

from core import paths  # noqa: E402

_TEST_DB = _ROOT / "data" / "okr_monitor_dogfood_test.db"
_TEST_DB.parent.mkdir(parents=True, exist_ok=True)
if _TEST_DB.exists():
    _TEST_DB.unlink()
paths.DB_PATH = _TEST_DB

from core import dogfood, limits, store  # noqa: E402


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _seed_proposal(*, agent: str = "ceo", kind: str = "weekly_priorities",
                   title: str = "Stub priorities") -> str:
    """Insert a fake proposal directly so we can test dogfood ingestion."""
    run_id = store.start_run(agent=agent, kind=kind)
    pid = store.write_proposal(
        run_id=run_id, agent=agent, kind=kind,
        title=title, summary="stub summary",
        body_md="# stub\n\nbody", evidence={"stub": True},
        confidence=0.7, model="test::stub",
        tokens_in=10, tokens_out=20, cost_usd=0.001,
    )
    return pid


class DogfoodIngestion(unittest.TestCase):
    def setUp(self) -> None:
        if _TEST_DB.exists():
            _TEST_DB.unlink()
        store.init_db()

    def test_ingest_one_proposal_creates_one_event(self) -> None:
        pid = _seed_proposal()
        with store.connect() as conn:
            row = dict(conn.execute(
                "SELECT id, agent, kind, title, summary, body_md, confidence, created_at"
                " FROM proposals WHERE id = ?", (pid,),
            ).fetchone())
        eid, was_new = dogfood.ingest_proposal_as_event(row)
        self.assertTrue(was_new)
        with store.connect() as conn:
            ev = conn.execute(
                "SELECT * FROM work_events WHERE id = ?", (eid,)
            ).fetchone()
        self.assertIsNotNone(ev)
        self.assertEqual(ev["source"], "agent_proposal")
        self.assertEqual(ev["source_event_id"], pid)
        self.assertEqual(ev["actor"], "ceo")
        self.assertIn("proposal.weekly_priorities", ev["kind"])

    def test_ingest_proposal_twice_is_idempotent(self) -> None:
        pid = _seed_proposal()
        with store.connect() as conn:
            row = dict(conn.execute(
                "SELECT id, agent, kind, title, summary, body_md, confidence, created_at"
                " FROM proposals WHERE id = ?", (pid,),
            ).fetchone())
        eid1, was_new1 = dogfood.ingest_proposal_as_event(row)
        eid2, was_new2 = dogfood.ingest_proposal_as_event(row)
        self.assertEqual(eid1, eid2)
        self.assertTrue(was_new1)
        self.assertFalse(was_new2)
        # And only one work_event row exists.
        with store.connect() as conn:
            count = conn.execute(
                "SELECT COUNT(*) AS n FROM work_events WHERE source_event_id = ?",
                (pid,),
            ).fetchone()["n"]
        self.assertEqual(count, 1)

    def test_ingest_recent_proposals_walks_all(self) -> None:
        for i in range(3):
            _seed_proposal(title=f"Stub {i}")
        out = dogfood.ingest_recent_proposals(limit=10)
        self.assertEqual(len(out), 3)
        self.assertTrue(all(r["was_new"] for r in out))
        # Re-running should mark all as not-new.
        out2 = dogfood.ingest_recent_proposals(limit=10)
        self.assertEqual(len(out2), 3)
        self.assertFalse(any(r["was_new"] for r in out2))


class LimitsEdgeCases(unittest.TestCase):
    def setUp(self) -> None:
        if _TEST_DB.exists():
            _TEST_DB.unlink()
        store.init_db()
        os.environ.pop("OKR_MONITOR_DAILY_LLM_CAP_USD", None)

    def test_record_negative_spend_is_noop(self) -> None:
        limits.reset_today()
        limits.record_spend(-1.0)
        self.assertEqual(limits.spent_today(), 0.0)

    def test_record_zero_spend_is_noop(self) -> None:
        limits.reset_today()
        limits.record_spend(0.0)
        self.assertEqual(limits.spent_today(), 0.0)

    def test_record_accumulates_via_upsert(self) -> None:
        limits.reset_today()
        limits.record_spend(0.10)
        limits.record_spend(0.25)
        limits.record_spend(0.05)
        self.assertAlmostEqual(limits.spent_today(), 0.40, places=4)

    def test_env_override_invalid_falls_back_to_default(self) -> None:
        os.environ["OKR_MONITOR_DAILY_LLM_CAP_USD"] = "not-a-number"
        try:
            cap = limits.daily_cap_usd()
            self.assertIn(cap, (50.0, 100.0))   # falls back to date-based default
        finally:
            del os.environ["OKR_MONITOR_DAILY_LLM_CAP_USD"]

    def test_reset_today_clears_spend(self) -> None:
        limits.record_spend(5.0)
        self.assertEqual(limits.spent_today(), 5.0)
        limits.reset_today()
        self.assertEqual(limits.spent_today(), 0.0)


def main() -> int:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in (DogfoodIngestion, LimitsEdgeCases):
        suite.addTests(loader.loadTestsFromTestCase(cls))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
