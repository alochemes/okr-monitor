"""Tests for core/tracker.py — the markdown parser.

The tracker parser is load-bearing: every agent embeds TRACKER.md content
in its system prompt, and signals_analyst + forecasting key off the parsed
KR list. Regressions here silently degrade the entire org.

Run with:
  python -m tests.test_tracker_parser
"""

from __future__ import annotations

import os
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))
os.environ["OKR_MONITOR_DRY_RUN"] = "true"

from core import paths, tracker  # noqa: E402


class TrackerParser(unittest.TestCase):
    """Tests use a synthetic tracker file so we don't depend on the real one."""

    # Built line-by-line to avoid any textwrap.dedent surprises with
    # mixed indentation. This is the literal markdown bytes written to disk.
    SYNTH = "\n".join([
        "# Synthetic tracker",
        "",
        "## 1. Mission",
        "",
        "Some mission text.",
        "",
        "## 2. Company OKRs (cycle)",
        "",
        "### O1 — Become the default tool",
        "",
        "| KR | Description | Target | Current | Owner pod | Due | Status |",
        "|---|---|---|---|---|---|---|",
        "| 1.1 | Reach NPS target | NPS reaches 50 | 12 | Customer/Ops | 2026-08-28 | yellow In progress |",
        "| 1.2 | Enterprise pilot count | Land 5 enterprise pilots | 0 | GTM | 2026-08-28 | red Not started |",
        "",
        "### O2 — Ship the magic moment",
        "",
        "| KR | Description | Target | Current | Owner pod | Due | Status |",
        "|---|---|---|---|---|---|---|",
        "| 2.1 | Mapper precision | OKR-Mapper precision >=85% | n/a | AI/Data | 2026-05-12 | red Not started |",
        "",
        "## 4. The Agent Roster",
        "",
        "| # | Agent | Pod | Status | Path |",
        "|---|---|---|---|---|",
        "| 1 | ceo | Strategy | green | `agents/ceo/` |",
        "| 2 | cpo | Strategy | green | `agents/cpo/` |",
        "| 3 | okr_mapper | AI/Data | yellow | `agents/okr_mapper/` |",
        "",
        "## 9. Risks",
        "",
        "Some risk text.",
        "",
    ])

    def setUp(self) -> None:
        # tracker.py imports TRACKER_PATH at module-top, so we have to
        # patch the binding INSIDE the tracker module, not on paths.
        self._original_path = tracker.TRACKER_PATH
        self._tmp = _ROOT / "data" / "tracker_test.md"
        self._tmp.parent.mkdir(parents=True, exist_ok=True)
        self._tmp.write_text(self.SYNTH, encoding="utf-8")
        tracker.TRACKER_PATH = self._tmp
        tracker._cached_text.cache_clear()

    def tearDown(self) -> None:
        tracker.TRACKER_PATH = self._original_path
        tracker._cached_text.cache_clear()
        if self._tmp.exists():
            self._tmp.unlink()

    def test_load_text_returns_full_file(self) -> None:
        text = tracker.load_text(reload=True)
        self.assertIn("Synthetic tracker", text)
        self.assertIn("OKR-Mapper precision", text)

    def test_extract_section_returns_correct_body(self) -> None:
        body = tracker.extract_section(2)
        self.assertIn("O1", body)
        self.assertIn("Become the default tool", body)
        # Should NOT include §1 or §4 content
        self.assertNotIn("Some mission text", body)
        self.assertNotIn("Synthetic tracker", body)
        self.assertNotIn("ceo", body.split("\n")[0])

    def test_extract_section_missing_returns_empty(self) -> None:
        self.assertEqual(tracker.extract_section(99), "")

    def test_extract_okrs_two_objectives_three_krs(self) -> None:
        objectives = tracker.extract_okrs()
        self.assertEqual(len(objectives), 2)
        self.assertEqual(objectives[0]["objective_num"], 1)
        self.assertEqual(objectives[0]["objective"], "Become the default tool")
        self.assertEqual(len(objectives[0]["krs"]), 2)
        self.assertEqual(objectives[1]["objective_num"], 2)
        self.assertEqual(len(objectives[1]["krs"]), 1)

    def test_extract_okrs_kr_fields_populated(self) -> None:
        kr = tracker.extract_okrs()[0]["krs"][0]
        self.assertEqual(kr["id"], "1.1")
        # 'description' column is captured into kr["description"];
        # the numeric target is in kr["target"].
        self.assertIn("NPS", kr["target"])
        self.assertEqual(kr["current"], "12")
        self.assertEqual(kr["owner_pod"], "Customer/Ops")
        self.assertEqual(kr["due"], "2026-08-28")
        self.assertIn("In progress", kr["status"])

    def test_extract_agent_roster_status_glyph_field_present(self) -> None:
        # Status glyph (an emoji or word) should round-trip non-empty.
        for row in tracker.extract_agent_roster():
            self.assertTrue(row["status"], f"empty status for row {row}")

    def test_extract_okrs_kr_ids_unique_and_dotted(self) -> None:
        all_ids = [
            kr["id"]
            for obj in tracker.extract_okrs()
            for kr in obj["krs"]
        ]
        self.assertEqual(all_ids, ["1.1", "1.2", "2.1"])
        self.assertEqual(len(set(all_ids)), len(all_ids))

    def test_extract_agent_roster_three_agents(self) -> None:
        roster = tracker.extract_agent_roster()
        self.assertEqual(len(roster), 3)

    def test_extract_agent_roster_fields_populated(self) -> None:
        ceo = tracker.extract_agent_roster()[0]
        self.assertEqual(ceo["num"], 1)
        self.assertEqual(ceo["name"], "ceo")
        self.assertEqual(ceo["pod"], "Strategy")
        # Synthetic file uses the literal string "green" instead of the 🟢
        # emoji to keep the source ASCII-clean — parser preserves whatever's
        # in the cell.
        self.assertEqual(ceo["status"], "green")
        self.assertEqual(ceo["path"], "agents/ceo/")


class TrackerParserResilience(unittest.TestCase):
    """Edge cases — broken/empty/missing tables."""

    def setUp(self) -> None:
        self._original_path = tracker.TRACKER_PATH
        self._tmp = _ROOT / "data" / "tracker_resilience_test.md"
        self._tmp.parent.mkdir(parents=True, exist_ok=True)
        tracker.TRACKER_PATH = self._tmp
        tracker._cached_text.cache_clear()

    def tearDown(self) -> None:
        tracker.TRACKER_PATH = self._original_path
        tracker._cached_text.cache_clear()
        if self._tmp.exists():
            self._tmp.unlink()

    def test_extract_okrs_empty_file_returns_empty_list(self) -> None:
        self._tmp.write_text("# Empty\n\n## 2. Company OKRs\n\n_(none yet)_\n", encoding="utf-8")
        self.assertEqual(tracker.extract_okrs(), [])

    def test_extract_okrs_no_section_two_returns_empty(self) -> None:
        self._tmp.write_text("# No OKRs section here\n\n## 9. Risks\n\nstuff", encoding="utf-8")
        self.assertEqual(tracker.extract_okrs(), [])

    def test_extract_agent_roster_no_section_four_returns_empty(self) -> None:
        self._tmp.write_text("# No roster here\n", encoding="utf-8")
        self.assertEqual(tracker.extract_agent_roster(), [])

    def test_load_text_raises_when_file_missing(self) -> None:
        if self._tmp.exists():
            self._tmp.unlink()
        with self.assertRaises(FileNotFoundError):
            tracker.load_text(reload=True)


def main() -> int:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in (TrackerParser, TrackerParserResilience):
        suite.addTests(loader.loadTestsFromTestCase(cls))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
