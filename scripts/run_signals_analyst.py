"""Compute kr_signals for every KR in TRACKER.md §2. No LLM cost."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

from agents.signals_analyst import pipeline  # noqa: E402


def main() -> int:
    stats = pipeline.run()
    print(json.dumps(stats, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
