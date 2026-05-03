"""Datadog KPI source.

API:        https://api.datadoghq.com/api/v1  (or your region's host)
Docs:       https://docs.datadoghq.com/api/latest/metrics/
Auth (v0):  API key + Application key in `DATADOG_API_KEY` +
            `DATADOG_APP_KEY`. Generate both at Organization Settings →
            API/Application Keys.
Effort:     1.5 days.
Status:     STUB — Sprint 3 priority (first KPI source).

----

What we pull:

For each KPI declared in `workspace.yaml`, we run the customer's metric
query against Datadog's metric API at a daily cadence. Result becomes
one `kpi_daily` row.

----

Implementation notes:

- Endpoint: GET `/v1/query?query={metric_query}&from={epoch}&to={epoch}`.
- Each KPI in workspace.yaml has:
    name              — friendly metric name we display
    query             — Datadog metric query string
    aggregation       — "p95" | "avg" | "sum" | "count" (default "avg")
    green_threshold   — e.g. "<200" or ">=99.95"
    alert_threshold   — e.g. ">300"
- Threshold logic lives in `core.kpi_evaluator` (TBD) — this module
  only fetches numbers.

----

Customer config:

    kpi_sources:
      - kind: datadog
        config:
          site: "datadoghq.com"     # or "datadoghq.eu"
          metrics:
            - name: api_p95_latency_ms
              query: "p95:trace.api.latency{env:prod}"
              green_threshold: "<200"
              alert_threshold: ">300"
            - name: error_rate_pct
              query: "sum:trace.api.errors{env:prod}.as_count() / sum:trace.api.hits{env:prod}.as_count() * 100"
              green_threshold: "<1"
              alert_threshold: ">3"
"""

from __future__ import annotations

from typing import Any


def fetch(workspace_slug: str, *, config: dict[str, Any]) -> list[dict[str, Any]]:
    raise NotImplementedError(
        "Datadog KPI source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 3)."
    )
