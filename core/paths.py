"""Resolve filesystem locations once. Avoid hardcoding paths in modules."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
AUDIT_DIR = DATA_DIR / "audit"
REPORTS_DIR = ROOT / "reports"
DB_PATH = DATA_DIR / "okr_monitor.db"
TRACKER_PATH = ROOT / "TRACKER.md"

for d in (DATA_DIR, AUDIT_DIR, REPORTS_DIR):
    d.mkdir(parents=True, exist_ok=True)
