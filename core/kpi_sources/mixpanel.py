"""Mixpanel KPI source.

API:        https://mixpanel.com/api/2.0  (Query API)
Docs:       https://developer.mixpanel.com/reference/query-api
Auth (v0):  Service Account credentials in `MIXPANEL_SA_USERNAME` +
            `MIXPANEL_SA_SECRET` + `MIXPANEL_PROJECT_ID`. Create at
            Project Settings → Service Accounts → + Add Service Account.
Effort:     1 day.
Status:     STUB — Sprint 3.

----

Implementation notes:

- Endpoints we'll use:
    /events                — raw event counts in a window
    /jql                   — for derived metrics (DAU/WAU/MAU, retention)
    /funnels?funnel_id=…   — for conversion KPIs
- Auth: Basic base64("{username}:{secret}").
- Daily aggregation: query for the last 24h, write one row per metric.

----

Customer config:

    kpi_sources:
      - kind: mixpanel
        config:
          project_id: 12345
          metrics:
            - name: weekly_active_users
              kind: jql
              jql: "function main() { ... }"      # written by us in onboarding
              green_threshold: ">=10000"
              alert_threshold: "<5000"
            - name: signup_to_first_value_p50_seconds
              kind: funnel
              funnel_id: 67890
              metric: "median"
              green_threshold: "<240"
              alert_threshold: ">600"
"""

from __future__ import annotations

from typing import Any


def fetch(workspace_slug: str, *, config: dict[str, Any]) -> list[dict[str, Any]]:
    raise NotImplementedError(
        "Mixpanel KPI source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 3)."
    )
