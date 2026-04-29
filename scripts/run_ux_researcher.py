"""Run one UX-Researcher discovery_synthesis pass."""

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

from agents.ux_researcher import pipeline  # noqa: E402


def main() -> int:
    print(json.dumps(pipeline.run(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
