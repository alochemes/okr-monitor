"""Slack work-event source.

API:        https://slack.com/api  (Web API + Events API)
Docs:       https://api.slack.com/methods
Auth (v0):  Bot token in `SLACK_BOT_TOKEN`. Create a Slack App at
            api.slack.com/apps → install to workspace → copy
            "Bot User OAuth Token" (starts with `xoxb-`).
Effort:     2 days. Highest customer-DPA work of any source — Slack
            content is the most sensitive ingest we do.
Status:     STUB — Sprint 1 priority.

----

What we ingest:

- Messages in OPT-IN channels only (default deny). The customer lists
  channels in `workspace.yaml`; we don't read anything else.
- Threads: a thread root + replies counts as one logical "thread" event
  (kind=`thread`) with the root's title. Replies enrich the thread but
  don't each create a separate work_event — that would 10× the noise.
- Reactions and DMs: NEVER ingested. (Reactions are private-ish; DMs
  are out of scope and would require a User token, which we refuse.)

What we don't ingest:
- Files / attachments (link only — file body might be PII).
- DMs and group DMs.
- Any channel the customer hasn't explicitly opted in.

----

Slack scopes the bot needs:
- `channels:read`     — list public channels
- `channels:history`  — read message history in opted-in public channels
- `groups:history`    — read message history in opted-in private channels
- `users:read`        — resolve actor names

----

Implementation notes:

- Endpoint: `conversations.history?channel={id}&oldest={epoch}` for each
  opted-in channel. Cursor-paginate via `response_metadata.next_cursor`.
- Thread expansion: when `reply_count>0`, fetch `conversations.replies`
  for the thread root and concatenate the first ~5 replies into the
  body (cap at 2000 chars).
- Source event id: `slack:{channel_id}:{ts}` where `ts` is the message
  timestamp. Replies use `slack:{channel_id}:{thread_ts}:{ts}`.
- Actor: `users.info?user={id}` resolves to display name + email.
  Cache user lookups within one poll run.

----

DPA template (sent to customer before they enable Slack):

  - We read messages only in channels you list.
  - We never read DMs.
  - We never train on your data.
  - You can revoke at any time by uninstalling the Slack App.

The DPA template lives at `notion/03_playbooks/05_slack_dpa.md` (TBD,
Sprint 1 deliverable alongside the integration).

----

Customer config:

    work_event_sources:
      - kind: slack
        config:
          channels: ["product", "eng-prs", "design-partners"]
          # OR: include_all_public: true   (rare — DPA risk)
"""

from __future__ import annotations

from typing import Any


def poll(workspace_slug: str, *, config: dict[str, Any],
         since_days: int = 7) -> dict[str, Any]:
    raise NotImplementedError(
        "Slack work-event source is scaffolded but not implemented. "
        "See notion/02_product/04_okr_source_integrations.md §3 (Sprint 1, highest priority)."
    )
