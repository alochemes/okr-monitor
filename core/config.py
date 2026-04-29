"""Typed access to YAML config with light validation. The YAML is canonical;
this module is a thin loader, not a schema engine."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import yaml

from core.paths import CONFIG_DIR


@lru_cache(maxsize=None)
def _load(name: str) -> dict[str, Any]:
    path = CONFIG_DIR / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Missing config: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def company() -> dict[str, Any]:
    return _load("company")


def agent(name: str) -> dict[str, Any]:
    return _load(name)


def reload_all() -> None:
    """Drop the cache. Call after editing a YAML at runtime (rare)."""
    _load.cache_clear()
