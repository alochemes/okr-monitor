# Integration matrix — design + buildout plan

> Companion to the pilot intake questionnaire (`notion/03_playbooks/04_pilot_intake_questionnaire.md`).
> Sections 3–4 of the intake ask "where do your OKRs / KPIs / commits /
> tickets / docs / chat / pipeline live?" — this doc maps each answer to
> the integration we need, the effort to build it, and the canonical
> output shape.

OKR Monitor must read FROM whatever stack the customer already runs.
**Any combination of these tools must work.** This doc is the source of
truth for that buildout.

---

## 0. Three categories of integration

| Category | Purpose | Output goes to | Examples |
|---|---|---|---|
| **OKR sources** | The KR catalog the mapper maps WORK to | `data/workspaces/<slug>/okrs.json` + `TRACKER.md §2` (regen) | Notion, Asana Goals, Mooncamp, Lattice, Workboard, Coda, Monday, Google Docs |
| **Work-event sources** | The WORK to be mapped to KRs | `work_events` table (idempotent on `source_event_id`) | GitHub, GitLab, Bitbucket, Linear, Jira, Asana tasks, Shortcut, GitHub Issues, Slack, Teams, Discord, Confluence, Google Drive, Coda, HubSpot, Salesforce, Pipedrive, Attio |
| **KPI sources** | The metrics that should always be green (alerts on red) | `kpi_daily` table + KPI dashboard render | Datadog, Mixpanel, Amplitude, PostHog, Grafana |

Every customer has SOME mix of these. We must support arbitrary
combinations. The architecture is: each source is an isolated module
with one well-defined contract; the orchestrator dispatches by the
workspace's declared integrations.

---

## 1. Contract per category

### 1a. OKR sources

`core/okr_sources/<source>.py` exposes:

```python
def fetch_okrs(workspace_slug: str, *, config: dict) -> list[dict]:
    """Returns canonical OKR shape:
    [
      {"objective_num": int|None, "objective": str, "krs": [
         {"id": str, "description": str, "target": str, "current": str,
          "owner_pod": str, "due": str, "status": str},
         ...
      ]},
      ...
    ]
    """
```

Same shape as `core.tracker.extract_okrs()`. Sources missing fields
normalize: empty string for free-text, position-1 for `objective_num`,
status mapped to our 5-value enum via `core.notion_okr._normalize_status`.

### 1b. Work-event sources

`core/work_event_sources/<source>.py` exposes:

```python
def poll(workspace_slug: str, *, config: dict, since_days: int = 7) -> dict:
    """Fetch recent activity from the source and upsert into work_events.
    Returns stats: {events_seen, events_written, errors}.

    Idempotency: schema-level UNIQUE(source, source_event_id) — replays
    are safe. Composite source_event_id when state matters
    (e.g. `ENG-42@issue_completed` so a transition counts separately).
    """
```

Returns stats; mutates `work_events` via `store.upsert_work_event`.

### 1c. KPI sources

`core/kpi_sources/<source>.py` exposes:

```python
def fetch(workspace_slug: str, *, config: dict) -> list[dict]:
    """Returns one row per KPI per day, in the shape:
    [{"day": "2026-05-02", "metric": "p95_latency_ms",
      "value": 142.0, "tags": {...}}, ...]

    Caller writes via store.write_kpi(). Whether a KPI is RED is
    decided downstream (operator-set thresholds in workspace.yaml).
    """
```

---

## 2. Status table — what's shipped, what's stubbed, what's planned

### 2a. OKR sources

| Source | Native OKR? | Auth (v0) | Effort | Status |
|---|---|---|---|---|
| **Notion** | no — user-modeled DB | Internal Integration token | — | ✅ shipped (`core/notion_okr.py`) |
| **Monday.com** | no — user-modeled board | Personal API token (GraphQL) | 1 day | 🟡 stub (`core/okr_sources/monday.py`) |
| **Coda** | no — user-modeled doc/table | API token | 1 day | 🟡 stub |
| **Asana Goals** | yes — `Goal` type with parent/sub | PAT | 1.5 days | 🟡 stub |
| **Mooncamp** | yes — purpose-built | API key | 1 day | 🟡 stub |
| **Lattice** | yes — Goals API | OAuth 2.0 | 1.5 days | 🟡 stub |
| **Workboard** | yes — purpose-built | PAT | 2 days | 🟡 stub |
| **Google Docs** | no — pure prose | OAuth + LLM extraction | 3+ days | 🟡 stub (deferred) |
| **CSV / paste** | no | none — file upload | 0.5 day | 🟡 stub (universal fallback) |

### 2b. Work-event sources

| Source | Type | Auth (v0) | Effort | Status |
|---|---|---|---|---|
| **GitHub** | code | PAT | — | ✅ shipped (`core/github_ingest.py`) |
| **Linear** | tickets | API key | — | ✅ shipped (`core/linear_ingest.py`) |
| **GitLab** | code | PAT | 1 day (clones GitHub structure) | 🟡 stub |
| **Bitbucket** | code | App password | 1 day | 🟡 stub |
| **Jira** | tickets | API token (Atlassian) | 1.5 days | 🟡 stub |
| **Asana tasks** | tickets | PAT | 1 day | 🟡 stub (shares HTTP client w/ Asana Goals) |
| **Shortcut** | tickets | API token | 1 day | 🟡 stub |
| **GitHub Issues** | tickets | reuses `GITHUB_TOKEN` | 0.5 day | 🟡 stub (extends `github_ingest`) |
| **Slack** | chat | Bot token (`SLACK_BOT_TOKEN`) | 2 days | 🟡 stub (highest customer-DPA work) |
| **Microsoft Teams** | chat | Graph API OAuth | 3 days | 🟡 stub |
| **Discord** | chat | Bot token | 1.5 days | 🟡 stub |
| **Confluence** | docs | Atlassian API token | 1.5 days | 🟡 stub |
| **Google Drive** | docs | OAuth + Drive API | 2 days | 🟡 stub |
| **Coda** | docs | API token (shares w/ Coda OKRs) | 1 day | 🟡 stub |
| **HubSpot** | CRM | Private app token | 1.5 days | 🟡 stub |
| **Salesforce** | CRM | Connected App + OAuth | 3 days | 🟡 stub |
| **Pipedrive** | CRM | API token | 1 day | 🟡 stub |
| **Attio** | CRM | API key | 1 day | 🟡 stub |

### 2c. KPI sources

| Source | Auth (v0) | Effort | Status |
|---|---|---|---|
| **Datadog** | API key + App key | 1.5 days | 🟡 stub |
| **Mixpanel** | Service Account or Project token | 1 day | 🟡 stub |
| **Amplitude** | API key + Secret | 1 day | 🟡 stub |
| **PostHog** | Personal API key | 1 day | 🟡 stub |
| **Grafana** | API token | 1.5 days | 🟡 stub |

**Total stub coverage**: 27 modules across 3 categories. Total buildout
estimate: **~33 engineer-days** to ship every stub. Realistic Sprint
sequencing below.

---

## 3. Priority order — what to ship and when

Optimized for customer coverage and operator dogfood.

### Sprint 1 (post-MVP, weeks 3–4) — operator dogfood + ICP-80%

Goal: any combination of {GitHub, Linear, Notion, Slack, Monday} works
for our first design partners. After this sprint, an Andrew-grade
operator can run the full loop on real data.

- [ ] **Slack** — work_events ingestion (2 days). Highest leverage —
      Slack threads are the dominant signal in many ICPs. Includes DPA
      template for opt-in private channels.
- [ ] **Monday.com** — both OKRs and work_events (2 days, shared GQL
      client). Operator's day-job tool — eat-our-own-cooking double-up.
- [ ] **`core/okr_pull.py` orchestrator** (1 day) — extract dispatch
      from `scripts/notion_okr_pull.py` so source #2 doesn't need a
      script of its own.

### Sprint 2 (weeks 5–6) — ICP coverage

Goal: serve any pilot whose stack is mainstream.

- [ ] **Asana** (Goals + tasks, shared client, 2 days)
- [ ] **Jira** (1.5 days)
- [ ] **Coda** (OKRs + docs, shared client, 1.5 days)
- [ ] **Mooncamp** (1 day, OKR-native)
- [ ] **CSV/paste OKR fallback** (0.5 day) — universal safety net

### Sprint 3 (weeks 7–8) — enterprise + KPIs

- [ ] **Lattice** (1.5 days, first OAuth source — also unblocks the
      multi-tenant OAuth platform work)
- [ ] **Workboard** (2 days)
- [ ] **HubSpot** (1.5 days)
- [ ] **Datadog** (1.5 days, first KPI source)
- [ ] **Mixpanel / Amplitude / PostHog** (3 days total — pick 2 based
      on first 5 pilots' actual stacks)
- [ ] **GitHub Issues** (0.5 day — extends GitHub ingest)

### Sprint 4+ (post-300-pilot push)

Long-tail:
- GitLab, Bitbucket (code)
- Shortcut (tickets)
- Microsoft Teams, Discord (chat)
- Confluence, Google Drive (docs)
- Salesforce, Pipedrive, Attio (CRM)
- Grafana (KPI)
- Google Docs LLM extractor agent

Order driven by inbound pilot demand — we don't pre-build for shadow
markets.

---

## 4. Customer-flow mapping — answer in intake → integration to wire

The intake questionnaire (sections 3–4) asks the customer where each
piece of their stack lives. Each answer maps to one integration:

| Intake question | Possible answers → integration |
|---|---|
| Q8: Where do OKRs live? | Notion → `okr_sources/notion`. Asana → `okr_sources/asana`. Mooncamp → `okr_sources/mooncamp`. Lattice → `okr_sources/lattice`. Workboard → `okr_sources/workboard`. Coda → `okr_sources/coda`. Monday → `okr_sources/monday`. Google Doc → `okr_sources/google_docs` (or CSV fallback). CSV → `okr_sources/csv`. |
| Q14: KPI dashboard? | Datadog → `kpi_sources/datadog`. Mixpanel → `kpi_sources/mixpanel`. Amplitude → `kpi_sources/amplitude`. PostHog → `kpi_sources/posthog`. Grafana → `kpi_sources/grafana`. |
| Q18: Code? | GitHub → `work_event_sources/github` (shipped). GitLab → `work_event_sources/gitlab`. Bitbucket → `work_event_sources/bitbucket`. |
| Q19: Tickets? | Linear → `work_event_sources/linear` (shipped). Jira → `work_event_sources/jira`. Asana → `work_event_sources/asana_tasks`. Shortcut → `work_event_sources/shortcut`. GitHub Issues → `work_event_sources/github_issues`. |
| Q20: Docs? | Notion → `work_event_sources/notion_docs`. Confluence → `work_event_sources/confluence`. Google Drive → `work_event_sources/google_drive`. Coda → `work_event_sources/coda_docs`. |
| Q21: Async chat? | Slack → `work_event_sources/slack`. Teams → `work_event_sources/teams`. Discord → `work_event_sources/discord`. |
| Q22: Customer pipeline? | HubSpot → `work_event_sources/hubspot`. Salesforce → `work_event_sources/salesforce`. Pipedrive → `work_event_sources/pipedrive`. Attio → `work_event_sources/attio`. |

**Combinatorial reality check.** ~7 categories × ~5 options each = 78,000
combinations on paper. In practice we expect 80% of pilots to fit one of
~12 cluster archetypes (e.g. "GitHub + Linear + Notion + Slack +
Datadog" = the modal SaaS stack). Build sources by ICP frequency, not by
attempting to enumerate.

---

## 5. Workspace configuration shape

`data/workspaces/<slug>/workspace.yaml`:

```yaml
slug: acme-corp
name: Acme Corp
kind: pilot
contacts:
  - sarah@acme.com    # Chief of Staff

okr_source:
  kind: notion        # singular — one OKR catalog per workspace
  config:
    database_id: ...
    parent_page_id: ...

work_event_sources:    # plural — pull from any number simultaneously
  - kind: github
    config:
      repos: ["acme/api", "acme/web"]
  - kind: linear
    config:
      team_keys: ["ENG", "PROD"]
  - kind: slack
    config:
      channels: ["product", "eng-prs"]

kpi_sources:            # plural
  - kind: datadog
    config:
      metrics:
        - name: api_latency_p95_ms
          query: "p95:trace.api.latency{env:prod}"
          green_threshold: "<200"
          alert_threshold: ">300"
  - kind: mixpanel
    config:
      project_id: 12345
      metrics:
        - name: weekly_active_users
          event: "session_start"
          unique_by: "user_id"
          window: "7d"
```

For OUR workspace (`okrmonitor-internal`), the same shape applies. Today
we have `notion` for OKRs, `github` and `linear` for work_events; we add
the rest as we eat our own cooking on each new tool.

---

## 6. Auth strategy across the matrix

### v0 (Sprint 0–2): single-tenant, operator-managed credentials

- All tokens live in `.env`.
- Each customer's pilot has the operator's hand-crafted credential set.
- Works for the first ~5–15 design partners.

### v1 (Sprint 3+): multi-tenant OAuth platform

A single OAuth-orchestrator module (`core/oauth.py`, TBD) handles:
- Notion OAuth, Asana OAuth, Lattice OAuth, Salesforce OAuth, Google
  OAuth (Drive/Docs), Slack OAuth, Atlassian OAuth (Jira/Confluence),
  GitHub App, GitLab OAuth, Microsoft Graph OAuth.
- Per-pilot grant flow surfaced in the product app.
- Token refresh + revocation.

Building this is a one-time platform sprint that unblocks every
OAuth-required source at once. Don't build it before we have a real
pilot whose stack requires it.

### Auth method per source (v0)

| Auth model | Sources |
|---|---|
| Personal/internal API token | Notion, Linear, Mooncamp, Coda, Monday, Discord, Datadog, Mixpanel, Amplitude, PostHog, Grafana, HubSpot, Pipedrive, Attio |
| PAT (GitHub-style) | GitHub, GitLab, Bitbucket, Asana, Shortcut, Workboard |
| Atlassian API token | Jira, Confluence |
| Slack Bot token | Slack |
| OAuth 2.0 (heavy) — defer | Lattice, Salesforce, Microsoft Teams, Google Drive, Google Docs |

---

## 7. Output normalization across sources

Different sources speak different languages. We normalize at ingest so
the mapper sees a consistent shape regardless of origin.

### Work events — `kind` taxonomy

```
commit                   # GitHub, GitLab, Bitbucket
pr_opened / pr_merged    # GitHub, GitLab, Bitbucket
issue_opened             # Linear, Jira, Asana, Shortcut, GH Issues
issue_in_progress        # ditto
issue_completed          # ditto
issue_canceled           # ditto
message                  # Slack, Teams, Discord
thread                   # Slack, Teams, Discord (multi-msg)
doc_created              # Notion, Confluence, Drive, Coda
doc_updated              # ditto
crm_deal_opened          # HubSpot, Salesforce, Pipedrive, Attio
crm_deal_won
crm_deal_lost
crm_meeting_logged
```

Source-specific kinds (e.g. `github.review_requested`) get a prefix
namespace; the mapper learns these in eval. Don't invent new kinds
casually — every new kind needs at least one labeled eval example.

### `actor` field

Always a stable identifier: GitHub login, Linear user email, Slack user
ID. Display name is in `raw_json` if needed.

---

## 8. Why scaffold all 27 stubs at once even though we ship them
## sequentially

Three reasons:

1. **The interface stays honest.** Writing each stub forces us to verify
   the source CAN actually fit the canonical shape. If Asana Goals
   doesn't expose enough fields to populate `current` or `due`, we
   discover it at scaffolding time, not three weeks into a sprint.

2. **Customer conversations get easier.** When a pilot says "we use
   Workboard," we have a one-page doc to send them — the stub's
   docstring IS that doc. Even unshipped, they see we know what we're
   doing.

3. **The registry pattern means new integrations become mechanical.**
   `core/<category>_sources/__init__.py` exposes a `{name: module}` dict
   in each category. Adding source #N means: implement the module,
   register it, write the customer-facing setup doc. No core changes.

---

## 9. What lives where

```
core/
├── notion_okr.py            # OKR-source: Notion (shipped)
├── notion_client.py
├── notion_pages.py
├── notion_ingest_okr.py     # → moves to okr_sources/notion.py in Sprint 1
├── github_ingest.py         # → moves to work_event_sources/github.py
├── linear_ingest.py         # → moves to work_event_sources/linear.py
│
├── okr_sources/
│   ├── __init__.py          # registry: {name: module}
│   ├── _base.py             # contract docstring + helpers (added when 2nd source ships)
│   ├── notion.py            # thin wrapper over notion_okr.fetch_okrs
│   ├── asana.py
│   ├── mooncamp.py
│   ├── lattice.py
│   ├── workboard.py
│   ├── coda.py
│   ├── monday.py
│   ├── google_docs.py
│   └── csv.py
│
├── work_event_sources/
│   ├── __init__.py
│   ├── github.py            # wraps github_ingest
│   ├── linear.py            # wraps linear_ingest
│   ├── gitlab.py
│   ├── bitbucket.py
│   ├── jira.py
│   ├── asana_tasks.py
│   ├── shortcut.py
│   ├── github_issues.py
│   ├── slack.py
│   ├── teams.py
│   ├── discord.py
│   ├── confluence.py
│   ├── google_drive.py
│   ├── coda_docs.py
│   ├── hubspot.py
│   ├── salesforce.py
│   ├── pipedrive.py
│   └── attio.py
│
└── kpi_sources/
    ├── __init__.py
    ├── datadog.py
    ├── mixpanel.py
    ├── amplitude.py
    ├── posthog.py
    └── grafana.py
```

Each stub: 30–60 lines. Module docstring covers (a) what the source
is, (b) auth model, (c) API endpoints, (d) data shape at the source,
(e) customer-setup steps, (f) effort estimate, (g) gotchas. The
function body raises `NotImplementedError` with the docstring URL.

---

## 11. Front-end architecture — `/app/integrations`

The web app must seamlessly handle every integration: connecting,
configuring, monitoring health, viewing ingested data. The shape:

### 11.1 Routes

```
/app/integrations                       — landing: 7 category cards, per-category counts
/app/integrations/<category>            — list of sources in that category
/app/integrations/<category>/<source>   — detail: status, last sync, config, recent events
/app/integrations/<category>/<source>/connect    — OAuth start / token paste form
/app/integrations/<category>/<source>/configure  — per-source config (channels, repos, etc.)
/app/integrations/health                — operator health board: every source's status, side-by-side
```

Categories:
- `okr-sources` (8 sources)
- `work-events` — `code` (3), `tickets` (5), `docs` (4), `chat` (3), `crm` (4)
- `kpi-sources` (5 sources)

### 11.2 Phased approach — what each Sprint ships in the UI

**Phase 1 — Sprint 0–1: read-only status page.** The product app
displays each source's connection status from the snapshot file
`web/public/integration_status.json` (written by `daily_evening.py`,
analogous to `kr_signals.json`). Operator still configures via `.env`
and CLI scripts. The UI shows:

- Per-source: 🟢 connected / 🟡 partial / 🔴 not configured / 🟠 error.
- Last successful sync timestamp.
- Events ingested in the last 24h.
- "How to set up" button → opens INSTRUCTIONS.md the right anchor.

This is the minimum that lets the operator see the system at a glance
and lets prospects see "yes, OKR Monitor knows how to read from X."

**Phase 2 — Sprint 2–3: writeable config UI.** Add a backend API surface
the web can write to. Two viable options:

| Option | Pros | Cons |
|---|---|---|
| **A. Supabase as config store.** Move `workspace.yaml` and `notion.json` into Supabase tables. Web R/W via Supabase JS. Python reads same DB. | Standard SaaS pattern. RLS handles tenancy. | Adds DB-as-a-service dependency to the Python brain (or a sync layer). |
| **B. Python HTTP API.** Stand up a small FastAPI service that owns config. Web calls it. Python brain reads its own filesystem state. | Python brain stays the source of truth. Clean separation of read-models vs write-models. | New runtime to host (Render, Fly.io, or Vercel Functions wrapping Python). |

**Recommendation: Option A in Sprint 2** because Supabase is already
chosen for auth — the same project hosts the config tables. The Python
brain pulls config from Supabase at the start of each cron run instead
of reading `workspace.yaml` directly. Migration: write a one-shot script
that uploads the current YAML to Supabase, then point everything at
Supabase.

**Phase 3 — Sprint 4+: self-serve onboarding.** Pilot signs up at
`/app/login`, lands on `/app/integrations`, walks through 3 connection
flows (one per category they use), sees their first narrative within
30 minutes (KR1.4). The connection flows are OAuth-first, with a
"paste your token" fallback for sources that allow it.

### 11.3 Front-end registry mirrors the back-end

The web app needs to know which sources exist *without* a round-trip to
the Python brain on every page load. Solution: a TypeScript registry
that mirrors `core/<category>_sources/__init__.py`:

```typescript
// web/lib/integrations/registry.ts
export const INTEGRATIONS = {
  "okr-sources": {
    notion:    { name: "Notion",     status: "shipped",     auth: "internal_token" },
    monday:    { name: "Monday.com", status: "in_progress", auth: "api_token" },
    asana:     { name: "Asana",      status: "stub",        auth: "pat" },
    mooncamp:  { name: "Mooncamp",   status: "stub",        auth: "api_key" },
    lattice:   { name: "Lattice",    status: "stub",        auth: "oauth2" },
    workboard: { name: "Workboard",  status: "stub",        auth: "pat" },
    coda:      { name: "Coda",       status: "stub",        auth: "api_token" },
    monday:    { name: "Monday.com", status: "stub",        auth: "api_token" },
    google_docs: { name: "Google Docs", status: "deferred", auth: "oauth2" },
    csv:       { name: "CSV / paste", status: "stub",       auth: "none" },
  },
  // ... work-events, kpi-sources
} as const;
```

A drift-detector test runs in CI: parses both registries and fails the
build if the TypeScript and Python versions disagree. Cheap to write,
catches the most common kind of drift.

### 11.4 The "integration card" component

Reusable across every page. Same shape regardless of category:

```tsx
<IntegrationCard
  source="github"
  category="work-events.code"
  status="connected"
  lastSyncAt="2026-05-02T19:50:00Z"
  events24h={20}
  config={{ repos: ["alochemes/okr-monitor"] }}
  ctaUrl="/app/integrations/work-events/github/configure"
/>
```

Renders a v2-console-aesthetic card with: source name, status dot, last
sync, mini-stat, primary CTA. Composes into grids for the landing page,
and into a row in the health board.

### 11.5 Robustness — the UI must not break

Every page that touches integrations must handle, without crashing:

1. **`integration_status.json` missing** — render a "not yet synced"
   placeholder, link to the operator-setup INSTRUCTIONS section.
2. **A source's stats are stale** (>48h since last sync) — render the
   status as 🟠, surface the staleness explicitly.
3. **A source is configured but failing** (auth expired, API down) —
   render 🔴 with the last error message and a "reconnect" CTA.
4. **A source is unknown** (registry drift) — fall back to a neutral
   tile that says "unrecognized integration <slug> — please update the
   client."
5. **No integrations configured** — render a "Get started" empty state
   that walks through the 3 most common (Notion + GitHub + Slack).

Test all 5 in `web/__tests__/integrations.test.tsx` before shipping.

### 11.6 What the daily run writes for the front-end

`scripts/daily_evening.py` extends to write a second snapshot:

```json
// web/public/integration_status.json
{
  "schema": 1,
  "generated_at": "2026-05-02T23:50:00Z",
  "workspace_slug": "okrmonitor-internal",
  "sources": [
    {
      "category": "okr-sources",
      "kind": "notion",
      "status": "connected",
      "last_sync_at": "2026-05-02T22:00:00Z",
      "stats_24h": { "objectives": 4, "krs": 17 },
      "error": null
    },
    {
      "category": "work-events.code",
      "kind": "github",
      "status": "connected",
      "last_sync_at": "2026-05-02T22:01:00Z",
      "stats_24h": { "events_written": 2 },
      "error": null
    },
    {
      "category": "work-events.tickets",
      "kind": "linear",
      "status": "connected",
      "last_sync_at": "2026-05-02T22:01:30Z",
      "stats_24h": { "events_written": 0 },
      "error": null
    }
    // ... one entry per source declared in workspace.yaml
  ]
}
```

This is the contract between the Python brain (writer) and the web
(reader). Same versioned-schema pattern as `kr_signals.json` — bump
`schema` and the front-end can refuse to render mismatched payloads.

---

## 12. Risk row — added to TRACKER.md §9

> **Integration matrix coverage gap.** Sprint 0 ships 3 of 27 known
> integrations (GitHub, Linear, Notion-OKR). Mainstream pilot stacks
> (GitHub + Linear + Notion + Slack + Datadog) require Slack and Datadog
> at minimum. Mitigation: Slack ships Sprint 1, Datadog Sprint 3.
> Pilots whose stack falls outside the supported set get either (a) a
> manual CSV/paste fallback for OKRs and (b) an honest "we don't ingest
> from X yet" caveat for work-events. Tracking via this design doc.
