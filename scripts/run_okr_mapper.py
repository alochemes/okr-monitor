"""Run the OKR-Mapper on unmapped events.

Usage:
  python scripts/run_okr_mapper.py             # sweep all unmapped, up to 100
  python scripts/run_okr_mapper.py --limit 10  # cap the sweep
  python scripts/run_okr_mapper.py --event <event_id>   # map one specific event
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
except ImportError:
    pass

from agents.okr_mapper import pipeline  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--event", type=str, default=None,
                   help="Map a single event by id. If omitted, sweep all unmapped.")
    p.add_argument("--limit", type=int, default=100,
                   help="Max events per sweep. Ignored if --event is set.")
    args = p.parse_args()

    if args.event:
        stats = pipeline.run(event_id=args.event)
    else:
        stats = pipeline.run_all_unmapped(limit=args.limit)
    print(json.dumps(stats, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
