# How OKR Monitor works (full product runbook)

> The complete operating description of the product, written for an internal team member or a sophisticated customer who wants to understand the mechanism end-to-end. If you only read one product doc, read this one.

---

## The whole thing in one paragraph

OKR Monitor ingests "work events" from the systems where your team actually does work — commits in GitHub, tickets in Linear or Jira, threads in Slack, doc updates in Notion. An agent called **OKR-Mapper** classifies every event against your KRs with a calibrated confidence score (≥0.5 floor, anything below is dropped, not faked). A second agent — **Signals-Analyst** — rolls those mappings into per-KR rolling counts (events / 7d / 30d / all-time). A third — **Forecasting** — compares current pace to required pace and emits a verdict per KR: `on_track | active | drifting | stale | off | qualitative`. Those four feed a **live scoreboard** that reflects the day's events as they land — drift is visible the day it starts. Every Friday at 9 AM, a fourth agent — **Narrative** — writes a one-page exec brief synthesizing the week. The scoreboard is the trust mechanism; the brief is the decision artifact.

---

## Architecture, top-down

### The four load-bearing agents

```
work events ─▶  OKR-Mapper  ─▶  event_kr_mappings table
                    │
                    ▼
                Signals-Analyst  ─▶  kr_signals table (counts)
                    │
                    ▼
                Forecasting     ─▶  kr_signals (verdicts written back)
                    │
                    ▼
                Narrative       ─▶  weekly brief (markdown)
```

| Agent | Cost per call | Cadence | Pure-compute? |
|---|---|---|---|
| `okr_mapper` | ~$0.0075 / event (effective) | per event, batched hourly | No (LLM) |
| `signals_analyst` | $0 | hourly or per-mapper-batch | Yes |
| `forecasting` | $0 | after each signals_analyst run | Yes |
| `narrative` | ~$0.02 / brief | weekly | No (LLM) |

### The four reporters (run on top of the load-bearing four)

| Agent | What it produces | Cadence |
|---|---|---|
| `ceo` | Daily synopsis (today vs expected sprint plan) | daily 7pm |
| `cpo` | Product roadmap report | daily 7pm |
| `cfo` | 14-day cost & token projection | daily 7pm |
| `analytics_ops` | Growth metrics (CAC, pilots, channel) | daily 7pm |

The reporters don't ingest events; they read what's already in the database (proposals, kr_signals, kpi_daily) and synthesize for the operator.

### The 22 supporting agents

22 more agents covering Strategy (CEO/CPO/CTO/CFO weekly proposals), Product/Design (PM, UX-R, UX-D, UI-D, Copywriter), Engineering (7 — backend_architect, frontend_lead, integrations_engineer, data_pipeline, ai_engineer, platform, security), GTM (founder_sales, demand_gen, content, sales_engineer, community_pr, growth_hacker), and Customer/Ops (onboarding, support, pilot_pm). Each emits one structured proposal per run. The operator reviews via `python -m cli.review --all`.

Full roster + status: see `TRACKER.md §4`.

---

## The data model

Five tables hold the load-bearing state. All in SQLite (WAL mode) at `data/okr_monitor.db`. Schema lives in `core/store.py`.

| Table | What it holds |
|---|---|
| `work_events` | One row per ingested event. UNIQUE on `(source, source_event_id)` so re-deliveries don't double-count. |
| `event_kr_mappings` | One row per (event, kr) link with confidence + reasoning. The mapper's output. |
| `kr_signals` | Per-KR rolling counts + forecast verdicts. One row per KR per signals_analyst run. |
| `narratives` | Weekly briefs as markdown bodies + structured evidence JSON. |
| `proposals` | Every agent's output. Reviewed via `cli/review.py`. |

Plus an append-only audit log at `data/audit/YYYY-MM-DD.jsonl` for every consequential decision (every LLM call, every promotion, every commit-back).

---

## Promotion gates (Stage 0/1/2 — planned)

Inherited from `skinmap_agents`. Three stages of agent autonomy:

- **Stage 0** — Proposals only (current default). Nothing acts on the world. Operator reviews everything.
- **Stage 1** — Trusted proposals. Same as Stage 0 plus a "ship as drafted" affordance. Earned by sustained low edit-distance over a window of N reviews.
- **Stage 2** — Auto-execute scoped actions (e.g. drafting outbound emails for review, opening Linear tickets). Per-action env-var kill switches. Tripwires demote to Stage 0 instantly.

Currently all 30 agents are Stage 0. Promotion logic from `skinmap_agents/core/promotion.py` is ported when the first agent is ready for Stage 1.

---

## Cost discipline

Two layers of cap:

1. **Per-run budget** (`core/budgets.py`) — runtime + LLM-call + USD cap per pipeline invocation.
2. **Daily LLM circuit breaker** (`core/limits.py`) — caps spend per UTC day. $50/day Sprint 0–1, $100/day Sprint 2+. Override via `OKR_MONITOR_DAILY_LLM_CAP_USD=<n>`. Trip = call refused, audit alert emitted.

Plus the dev default of `OKR_MONITOR_DRY_RUN=true` so accidental script runs don't burn credits. Real runs require explicit `OKR_MONITOR_DRY_RUN=false python scripts/run_X.py`.

---

## Integrations

Day-one targets:

| Source | What we ingest | Auth | Status |
|---|---|---|---|
| GitHub | commits, PRs, reviews, issues | GitHub App, repo:read | Spec'd, not built |
| Linear | issues, projects, cycles | OAuth, read scope | Spec'd, not built |
| Jira | issues, sprints, epics | OAuth, read scope | Spec'd, not built |
| Slack | indexed channels & threads (opt-in per channel) | OAuth, channels:history | Spec'd, not built |
| Notion | OKR docs + project pages | OAuth, page-level access | Spec'd, not built |

The `integrations_engineer` agent's first proposal will be the GitHub design. See `agents/integrations_engineer/prompts/integration_design.md`.

**Privacy posture:** Slack ingestion defaults to public channels only; private channels are opt-in. No customer data is used to train LLMs (Anthropic API has prompt-data-used-for-training off by default; we keep it off). DPA template ships before the first design partner onboarding.

---

## What customers actually receive

Two surfaces, two cadences:

1. **The live scoreboard at `/app/dashboard`** — checkable anytime, reflects today's ingested events. The CoS who wants to know "are we on track for KR-2 right now?" gets the answer in one click. No daily email, no notification spam — availability is the value, not a ritual.
2. **The Friday 9 AM brief** — the decision-grade artifact. Every Friday at 9 AM (their timezone), they get one of these in their inbox:

```
Subject: OKR Monitor — Brief 17.26 — 3 of 7 KRs at risk

VERDICT
Three of seven KRs at risk this quarter. Engineering shipped 80% of work
against KR-1; Customer Success shipped 0% against KR-3. Reallocate or
restate.

KR-1   ON TRACK    7d events: 24
       "Reduce p95 API latency to <150ms"
       cited: fix(perf): tune redis pipeline, drop p95 to 138ms

KR-2   DRIFTING    7d events:  4
       "Land 5 enterprise pilots by EOQ"
       no new pilots since Apr 12; 1 booked Q1 carryover

KR-3   OFF         7d events:  0
       "Reach 80 NPS in dashboard surface"
       no work tied this quarter — restate or reassign

[...]

ACTION THIS WEEK
Move two engineers from KR-1 to KR-3, or formally close KR-3 with a
written rationale. The current allocation cannot hit both.
```

Plus a daily 7 PM "OWNER/FINANCE" digest with the live KPI dashboard, accomplishments-vs-expectations, cost projection, and growth metrics.

---

## What changes if a KR is wrong

The OKR-Mapper sees every commit, ticket, and Slack thread. If the operator updates the KR text in their OKR doc (Notion / Asana / Mooncamp), the mapper detects the change at the next sync and **re-maps the last 30 days of events** against the new KR. The narrative agent's next brief reflects the updated mapping. There is no "save and don't forget" — the KR doc is the live spec.

---

## Where to start reading the code

| You want to understand... | Read this |
|---|---|
| The whole company state | `TRACKER.md` |
| How agents work | `agents/_proposal.py` + `agents/ceo/pipeline.py` |
| The data model | `core/store.py` (top of file = SCHEMA) |
| The Friday brief flow | `scripts/sunday_evening.py` |
| The daily 7pm flow | `scripts/daily_evening.py` |
| The verdict math | `agents/forecasting/pipeline.py` |

Or run `python -m cli.status` to see the live KR scoreboard.
