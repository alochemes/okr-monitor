"""Generate a weekly narrative covering the trailing 7 days.

Usage:
  python scripts/run_narrative.py
  python scripts/run_narrative.py --end 2026-05-09       # narrative ending on a specific date
  python scripts/run_narrative.py --days 14              # 2-week window
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
except ImportError:
    pass

from agents.narrative import pipeline  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--end", type=date.fromisoformat, default=None,
                   help="ISO date for the period end. Defaults to today.")
    p.add_argument("--days", type=int, default=7,
                   help="Window size in days. Default 7.")
    args = p.parse_args()

    stats = pipeline.run(period_end=args.end, period_days=args.days)
    print(json.dumps(stats, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
