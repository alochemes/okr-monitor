"""Math tests for signals_analyst + forecasting. No LLM, no Anthropic SDK.

Strategy: create synthetic work_events at known offsets from "now",
manually write event_kr_mappings linking them to a fake KR, then run the
two pipelines and assert the computed counts and verdicts.

Run with:
  python -m tests.test_signals_math
"""

from __future__ import annotations

import os
import sys
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

# Use a SEPARATE test DB so we never touch the real one.
_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))
os.environ["OKR_MONITOR_DRY_RUN"] = "true"  # safety: no API calls anywhere

# Redirect DB before importing core.store, so it picks up the test path.
_TEST_DB = _REPO_ROOT / "data" / "okr_monitor_test.db"
_TEST_DB.parent.mkdir(parents=True, exist_ok=True)
if _TEST_DB.exists():
    _TEST_DB.unlink()

# Patch core.paths.DB_PATH at import time.
from core import paths  # noqa: E402

paths.DB_PATH = _TEST_DB

from core import store  # noqa: E402  (must come AFTER paths patch)
from agents.signals_analyst import pipeline as signals_pipe  # noqa: E402
from agents.forecasting import pipeline as forecasting_pipe  # noqa: E402


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _seed_event(*, days_ago: int, source: str = "test", actor: str = "tester",
                title: str = "synthetic event", body: str = "") -> str:
    """Insert one work_event with occurred_at offset days_ago from now."""
    ts = (_utcnow() - timedelta(days=days_ago)).isoformat()
    eid, _ = store.upsert_work_event(
        source=source,
        source_event_id=f"test-{ts}-{title}",
        kind="synthetic",
        title=title,
        body=body,
        actor=actor,
        occurred_at=ts,
    )
    return eid


def _seed_mapping(event_id: str, kr_id: str, confidence: float = 0.9,
                  run_id: str | None = None) -> None:
    rid = run_id or store.start_run(agent="test_seed", kind="seed")
    store.write_event_kr_mappings(
        event_id=event_id, run_id=rid,
        mappings=[{"kr_id": kr_id, "confidence": confidence,
                   "reasoning": "test seed"}],
        model="test::synthetic",
        tokens_in=0, tokens_out=0, cost_usd=0.0,
    )


class SignalsMath(unittest.TestCase):
    def setUp(self) -> None:
        # Fresh DB for each test.
        if _TEST_DB.exists():
            _TEST_DB.unlink()
        store.init_db()

    def test_window_counts_partition_correctly(self) -> None:
        """7d window catches today+yesterday; 30d catches more; total catches all."""
        # 4 events for KR "1.1": today, 6d, 20d, 90d
        for d in (0, 6, 20, 90):
            eid = _seed_event(days_ago=d, title=f"event-{d}d")
            _seed_mapping(eid, "1.1")

        stats = signals_pipe.run()
        per_kr = {p["kr_id"]: p for p in stats["per_kr"]}
        self.assertIn("1.1", per_kr, "KR 1.1 should appear in computed signals")
        s = per_kr["1.1"]
        self.assertEqual(s["events_total"], 4)
        self.assertEqual(s["events_7d"], 2)   # 0d + 6d
        self.assertEqual(s["events_30d"], 3)  # 0d + 6d + 20d

    def test_distinct_actors_and_mean_confidence(self) -> None:
        for actor, conf, days_ago in [
            ("alice", 0.9, 1),
            ("alice", 0.7, 2),
            ("bob", 0.6, 3),
        ]:
            eid = _seed_event(days_ago=days_ago, actor=actor,
                              title=f"e-{actor}-{days_ago}")
            _seed_mapping(eid, "1.1", confidence=conf)
        signals_pipe.run()
        latest = {r["kr_id"]: dict(r) for r in store.latest_kr_signals()}
        self.assertEqual(latest["1.1"]["distinct_actors"], 2)
        self.assertAlmostEqual(latest["1.1"]["mean_confidence"],
                               (0.9 + 0.7 + 0.6) / 3, places=4)

    def test_no_mappings_yields_zero_signal(self) -> None:
        """A KR with no mappings still gets a signal row with all zeros."""
        signals_pipe.run()
        latest = {r["kr_id"]: dict(r) for r in store.latest_kr_signals()}
        # KR 1.1 exists in TRACKER.md, so a row should be written.
        self.assertIn("1.1", latest)
        self.assertEqual(latest["1.1"]["events_total"], 0)
        self.assertEqual(latest["1.1"]["events_7d"], 0)


class ForecastVerdicts(unittest.TestCase):
    def setUp(self) -> None:
        if _TEST_DB.exists():
            _TEST_DB.unlink()
        store.init_db()

    def test_qualitative_when_target_or_current_not_numeric(self) -> None:
        """KR with non-numeric target (e.g. 'live on Vercel') gets 'qualitative'."""
        signals_pipe.run()
        # KR 1.1 target = "live on Vercel" → not numeric → qualitative
        forecasting_pipe.run(today=date(2026, 4, 29))
        latest = {r["kr_id"]: dict(r) for r in store.latest_kr_signals()}
        self.assertEqual(latest["1.1"]["forecast_verdict"], "qualitative",
                         f"KR 1.1 target='live on Vercel' should be qualitative; "
                         f"got {latest['1.1']['forecast_verdict']}")

    def test_off_when_due_date_passed_and_gap_remains(self) -> None:
        """KR with numeric target/current but past due_date → off."""
        signals_pipe.run()
        # KR 2.1: target=300, current=0, due=2026-08-28; pretend today=2026-09-01 → off
        forecasting_pipe.run(today=date(2026, 9, 1))
        latest = {r["kr_id"]: dict(r) for r in store.latest_kr_signals()}
        s = latest.get("2.1")
        self.assertIsNotNone(s)
        self.assertEqual(s["forecast_verdict"], "off",
                         f"KR 2.1 past due with gap should be 'off'; got {s['forecast_verdict']}")
        self.assertLess(s["days_remaining"], 0)

    def test_active_when_recent_events_and_time_remaining(self) -> None:
        """KR with numeric target, time remaining, and at least one event in
        the last 7 days → 'active'."""
        # Seed two recent events on KR 2.1.
        for d in (1, 3):
            eid = _seed_event(days_ago=d, title=f"recent-{d}d")
            _seed_mapping(eid, "2.1")
        signals_pipe.run()
        forecasting_pipe.run(today=date(2026, 4, 29))
        latest = {r["kr_id"]: dict(r) for r in store.latest_kr_signals()}
        s = latest["2.1"]
        self.assertEqual(s["forecast_verdict"], "active")
        self.assertGreater(s["events_7d"], 0)

    def test_stale_when_no_recent_events_and_time_remaining(self) -> None:
        """Numeric KR, no events in 7d, time remaining → 'stale'."""
        # Seed one old event (40 days ago — outside 30d window).
        eid = _seed_event(days_ago=40, title="ancient")
        _seed_mapping(eid, "2.1")
        signals_pipe.run()
        forecasting_pipe.run(today=date(2026, 4, 29))
        latest = {r["kr_id"]: dict(r) for r in store.latest_kr_signals()}
        s = latest["2.1"]
        self.assertEqual(s["forecast_verdict"], "stale")
        self.assertEqual(s["events_7d"], 0)


class TargetAndDateParsing(unittest.TestCase):
    """Direct unit tests for the parsing helpers."""

    def test_numeric_extracts_first_number(self) -> None:
        from agents.forecasting.pipeline import _parse_numeric
        self.assertEqual(_parse_numeric("300"), 300.0)
        self.assertEqual(_parse_numeric("≥85% P @ ≥70% R"), 85.0)
        self.assertEqual(_parse_numeric("5,000"), 5000.0)
        self.assertEqual(_parse_numeric("≤6 months"), 6.0)
        self.assertEqual(_parse_numeric("30/30"), 30.0)
        self.assertIsNone(_parse_numeric("live on Vercel"))
        self.assertIsNone(_parse_numeric(None))
        self.assertIsNone(_parse_numeric(""))

    def test_iso_date_extracts_due(self) -> None:
        from agents.forecasting.pipeline import _parse_iso_date
        self.assertEqual(_parse_iso_date("2026-05-12"), date(2026, 5, 12))
        self.assertEqual(_parse_iso_date("due 2026-08-28!"), date(2026, 8, 28))
        self.assertIsNone(_parse_iso_date("ongoing"))
        self.assertIsNone(_parse_iso_date(None))


def main() -> int:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in (SignalsMath, ForecastVerdicts, TargetAndDateParsing):
        suite.addTests(loader.loadTestsFromTestCase(cls))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
