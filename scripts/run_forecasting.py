"""Compute per-KR forecast verdicts. Reads latest signals + TRACKER.md.
Pure compute, no LLM."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

from agents.forecasting import pipeline  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--date", type=date.fromisoformat, default=None,
                   help="Override 'today' for backfill or testing.")
    args = p.parse_args()
    stats = pipeline.run(today=args.date)
    print(json.dumps(stats, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
