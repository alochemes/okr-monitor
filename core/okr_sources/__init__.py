"""OKR-source registry. Each entry maps a source key (used in
`workspace.yaml`'s `okr_source.kind`) to its module + status.

Adding a source:
  1. Implement `core/okr_sources/<key>.py` with `fetch_okrs(slug, *, config)`
     returning the canonical OKR shape (see
     `notion/02_product/04_okr_source_integrations.md` §1a).
  2. Update this registry's status to "shipped".
  3. Mirror in `web/lib/integrations/registry.ts` so the UI knows.

Status values:
  - shipped     — fully implemented, in production use
  - in_progress — partially implemented, behind a feature flag
  - stub        — module exists with clear docstring; raises NotImplementedError
  - planned     — not yet stubbed; listed here for visibility
  - deferred    — explicitly out of scope until further notice (reasoning in source)
"""

from __future__ import annotations

REGISTRY: dict[str, dict[str, str]] = {
    "notion":     {"name": "Notion",       "auth": "internal_token", "status": "shipped"},
    "monday":     {"name": "Monday.com",   "auth": "api_token",      "status": "stub"},
    "asana":      {"name": "Asana Goals",  "auth": "pat",            "status": "stub"},
    "mooncamp":   {"name": "Mooncamp",     "auth": "api_key",        "status": "stub"},
    "coda":       {"name": "Coda",         "auth": "api_token",      "status": "stub"},
    "lattice":    {"name": "Lattice",      "auth": "oauth2",         "status": "planned"},
    "workboard":  {"name": "Workboard",    "auth": "pat",            "status": "planned"},
    "google_docs":{"name": "Google Docs",  "auth": "oauth2+llm",     "status": "deferred"},
    "csv":        {"name": "CSV / paste",  "auth": "none",           "status": "stub"},
}


def list_sources() -> list[dict[str, str]]:
    """Sorted by status (shipped → stub → planned → deferred), then name."""
    order = {"shipped": 0, "in_progress": 1, "stub": 2, "planned": 3, "deferred": 4}
    return sorted(
        [{"key": k, **v} for k, v in REGISTRY.items()],
        key=lambda x: (order.get(x["status"], 9), x["name"]),
    )
