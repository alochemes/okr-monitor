"""Run all four strategy-pod agents in sequence.

Putting them in one process maximizes Anthropic prompt-cache hits — the
system block is identical across CEO/CPO/CTO/CFO (same company.yaml + same
TRACKER.md), so calls 2-4 read the system tokens from cache at ~10% cost.

Usage:
  python scripts/run_strategy_pod.py
  OKR_MONITOR_DRY_RUN=true python scripts/run_strategy_pod.py
"""

from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
except ImportError:
    pass

from agents.ceo import pipeline as ceo_pipe  # noqa: E402
from agents.cpo import pipeline as cpo_pipe  # noqa: E402
from agents.cto import pipeline as cto_pipe  # noqa: E402
from agents.cfo import pipeline as cfo_pipe  # noqa: E402


_AGENTS = [
    ("ceo", ceo_pipe),
    ("cpo", cpo_pipe),
    ("cto", cto_pipe),
    ("cfo", cfo_pipe),
]


def main() -> int:
    out: dict[str, object] = {}
    exit_code = 0
    for name, mod in _AGENTS:
        try:
            out[name] = mod.run()
        except Exception as exc:  # keep going; one bad agent shouldn't kill the pod
            out[name] = {"error": str(exc), "trace": traceback.format_exc()}
            exit_code = 1
    print(json.dumps(out, indent=2, default=str))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
