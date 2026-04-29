"""Run one CEO planning pass.

Usage:
  python scripts/run_ceo.py
  OKR_MONITOR_DRY_RUN=true python scripts/run_ceo.py   # safe; no API spend
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
except ImportError:
    pass

from agents.ceo import pipeline  # noqa: E402


def main() -> int:
    stats = pipeline.run()
    print(json.dumps(stats, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
