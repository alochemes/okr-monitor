"""Mooncamp OKR source.

API:        https://api.mooncamp.com  (REST)
Docs:       https://docs.mooncamp.com/api
Auth (v0):  API key in `MOONCAMP_API_KEY`. Generate at Settings → API
            in the Mooncamp web app.
Effort:     1 day (cleanest API of all the OKR-native tools).
Status:     STUB — not yet implemented.

----

Mooncamp is purpose-built for OKRs. The data model is native:
  Objective → Key Result (numeric / boolean / milestone)

So the integration is the cleanest of all OKR sources — no schema
modeling required from the customer.

----

Implementation notes:

- Endpoint: GET `/v1/objectives?cycle={cycle_id}` returns objectives
  with embedded KRs. Pagination is `cursor`-style.
- KR types: `numeric` (target+current as numbers), `boolean`
  (true/false), `milestone` (list of completed milestones). All
  three normalize to the canonical `target` / `current` strings.
- Mooncamp status: on_track / at_risk / off_track / completed →
  map directly to our 5-value enum.

----

Customer config:

    okr_source:
      kind: mooncamp
      config:
        cycle_id: "abcdef"           # which OKR cycle to read
        team_id: "..."               # optional — narrow to one team

Customer setup:
  1. Generate an API key in Mooncamp.
  2. Note the cycle_id from the URL of the cycle they want monitored.
  3. Paste the key into our intake or (Sprint 4+) the /app/integrations UI.
"""

from __future__ import annotations

from typing import Any


def fetch_okrs(workspace_slug: str, *, config: dict[str, Any]) -> list[dict[str, Any]]:
    raise NotImplementedError(
        "Mooncamp OKR source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 2)."
    )
