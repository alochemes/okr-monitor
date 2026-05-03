"""KPI-source registry. Each entry maps a source key to its module +
status. See `notion/02_product/04_okr_source_integrations.md` §2c.

A KPI source returns one row per (metric, day):
    {"day": "YYYY-MM-DD", "metric": str, "value": float, "tags": dict}

Threshold logic (green/yellow/red) lives in workspace.yaml, not in the
source — the source's job is to fetch the number; "is this OK?" is an
operator-set question.
"""

from __future__ import annotations

REGISTRY: dict[str, dict[str, str]] = {
    "datadog":   {"name": "Datadog",   "auth": "api+app_keys",     "status": "stub"},
    "mixpanel":  {"name": "Mixpanel",  "auth": "service_account",  "status": "stub"},
    "amplitude": {"name": "Amplitude", "auth": "api+secret",       "status": "planned"},
    "posthog":   {"name": "PostHog",   "auth": "api_key",          "status": "planned"},
    "grafana":   {"name": "Grafana",   "auth": "api_token",        "status": "planned"},
}


def list_sources() -> list[dict[str, str]]:
    order = {"shipped": 0, "in_progress": 1, "stub": 2, "planned": 3, "deferred": 4}
    return sorted(
        [{"key": k, **v} for k, v in REGISTRY.items()],
        key=lambda x: (order.get(x["status"], 9), x["name"]),
    )
