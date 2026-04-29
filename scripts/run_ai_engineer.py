"""Run one AI-Engineer eval_proposal pass."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
except ImportError:
    pass
from agents.ai_engineer import pipeline  # noqa: E402

if __name__ == "__main__":
    print(json.dumps(pipeline.run(), indent=2, default=str))
