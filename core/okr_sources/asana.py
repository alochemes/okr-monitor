"""Asana Goals OKR source.

API:        https://app.asana.com/api/1.0  (REST)
Docs:       https://developers.asana.com/reference/goals
Auth (v0):  Personal Access Token in `ASANA_PAT`. Generate at
            asana.com → Settings → Apps → Manage Developer Apps → +
            New access token. Production uses Asana OAuth (Sprint 3+).
Effort:     1.5 days.
Status:     STUB — not yet implemented.

----

Asana has a NATIVE OKR concept (Goals API), so customers don't model
columns themselves. We pull `Goal` objects with their parent/sub
relationships:

  - Top-level goal (no parent) → Objective
  - Sub-goal (parent_goal set)  → Key Result

This means Asana customers don't need to follow our column convention —
just connect and it Just Works.

----

Implementation notes:

- Endpoint: GET `/workspaces/{workspace_gid}/goals?team={team_gid}` (team
  optional). Pull `?opt_fields=name,owner,due_on,status,metric,parent_goal,is_workspace_level`.
- Asana `status.color` values: green, yellow, red, missing →
  normalize via:
    green   → 🟢 On track
    yellow  → 🟠 At risk
    red     → 🔴 Not started (or 🟡 In progress per metric)
    missing → 🔴 Not started
- `metric.current_number_value` + `metric.target_number_value` →
  `current` and `target` (stringify with unit if `unit` present).
- Goals have a `time_period` (Q3 2026, etc.) — use that to populate the
  `objective_num` ordering when present; else assign by API order.

----

Customer config:

    okr_source:
      kind: asana
      config:
        workspace_gid: "12345..."
        team_gid: "67890..."          # optional — narrow to one team's goals

Customer setup:
  1. Connect their Asana account via PAT or (Sprint 3+) OAuth.
  2. Confirm the integration user can see the OKR-tracking team's goals.
  3. (Optional) tag goals with `q3-2026-okrs` for easy scoping.
"""

from __future__ import annotations

from typing import Any


def fetch_okrs(workspace_slug: str, *, config: dict[str, Any]) -> list[dict[str, Any]]:
    raise NotImplementedError(
        "Asana Goals OKR source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 2)."
    )
