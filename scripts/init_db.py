"""Create the SQLite schema. Idempotent. Run once after cloning."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import store  # noqa: E402
from core.paths import DB_PATH  # noqa: E402


def main() -> int:
    store.init_db()
    print(f"DB initialized at: {DB_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
