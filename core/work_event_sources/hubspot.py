"""HubSpot CRM work-event source.

API:        https://api.hubapi.com  (REST)
Docs:       https://developers.hubspot.com/docs/api/overview
Auth (v0):  Private App token in `HUBSPOT_PRIVATE_APP_TOKEN`. Create at
            HubSpot Settings → Integrations → Private Apps → Create.
Effort:     1.5 days.
Status:     STUB — Sprint 3.

----

What we ingest (high-signal CRM events):

  - Deal created                   → kind=crm_deal_opened
  - Deal stage progressed          → kind=crm_deal_stage_changed
  - Deal closed-won                → kind=crm_deal_won
  - Deal closed-lost               → kind=crm_deal_lost
  - Meeting logged on a deal       → kind=crm_meeting_logged

We don't ingest contact-level activity (too noisy). Mapper learns to
tie crm_deal_won events to KR2.3 (paid intent), KR2.5 (CAC payback), etc.

----

Implementation notes:

- Endpoint: GET `/crm/v3/objects/deals?properties=...&filterGroups=...`.
- Use the activity timeline endpoint:
  `/crm/v3/objects/deals/{dealId}/associations/notes` and meetings.
- Source event id: `hubspot:deal:{id}@{kind}` (state-aware so transitions
  count separately).

----

Required private-app scopes:
  - crm.objects.deals.read
  - crm.objects.contacts.read   (for actor resolution only)

----

Customer config:

    work_event_sources:
      - kind: hubspot
        config:
          pipeline_ids: ["12345"]      # optional — narrow to one pipeline
"""

from __future__ import annotations

from typing import Any


def poll(workspace_slug: str, *, config: dict[str, Any],
         since_days: int = 7) -> dict[str, Any]:
    raise NotImplementedError(
        "HubSpot work-event source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 3)."
    )
