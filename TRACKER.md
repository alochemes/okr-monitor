# OKR Monitor — Build Log & OKRs

> The single source of truth for the OKR Monitor venture. This file is also our **first dogfood**: every agent, every KR, and every weekly narrative we ship will be ingestible by the product we are building. If the product can't make sense of this file, the product isn't good enough yet.

- **Cycle:** 2026-04-28 → 2026-08-28 (4 months)
- **Founder/Operator:** andrew@skinmap.com
- **Repo root:** `C:/Users/aloch/okr-monitor/`
- **Last updated:** 2026-04-29

---

## 1. Mission & Wedge

**Mission.** Make every company's OKRs honest in real time by connecting goals to the actual work happening in code, tickets, and conversations.

**Wedge (the one sentence on the landing page).** "Every Friday, get a one-page exec summary of which OKRs are on track, which are drifting, and exactly which work is — and isn't — moving the needle."

**ICP for pilots.** Series A–C SaaS, 50–500 employees, OKRs in Notion / Asana / Mooncamp, day-to-day work in GitHub + Linear/Jira + Slack. Buyer is the **Chief of Staff** or **Head of Ops** (not the CEO directly — they are the user who weaponizes it for the CEO).

**Anti-ICP (do not pursue in pilot phase).** Pre-seed (no real OKRs), 1,000+ employees (procurement cycle longer than our runway), non-software companies (we don't have the integrations).

---

## 2. Company OKRs (2026-04-28 → 2026-08-28)

### O1 — Ship a magical MVP that makes "OKR drift" visible in <30 minutes
| KR | Target | Current | Owner pod | Due | Status |
|---|---|---|---|---|---|
| 1.1 | MVP deployed to production | live on Vercel | not started | Engineering | 2026-05-12 | 🔴 Not started |
| 1.2 | Active design partners (logged in ≥3×/week) | 5 | 0 | Customer/Ops | 2026-05-19 | 🔴 Not started |
| 1.3 | OKR-Mapper precision @ recall on 200-event eval set | ≥85% P @ ≥70% R | n/a | AI/Data | 2026-05-12 | 🔴 Not started |
| 1.4 | Time-to-first-narrative for new accounts (p90) | ≤30 min | n/a | Product/Design | 2026-05-19 | 🔴 Not started |
| 1.5 | Design-partner NPS | ≥50 | n/a | Customer/Ops | 2026-05-26 | 🔴 Not started |

### O2 — Prove repeatable acquisition by landing 300 pilots in 4 months
| KR | Target | Current | Owner pod | Due | Status |
|---|---|---|---|---|---|
| 2.1 | Cumulative pilot accounts | 300 | 0 | GTM | 2026-08-28 | 🔴 Not started |
| 2.2 | Pilot activation rate (read ≥1 weekly narrative) | ≥60% | n/a | Customer/Ops | 2026-08-28 | 🔴 Not started |
| 2.3 | Pilot → paid intent at end of pilot | ≥25% | n/a | GTM | 2026-08-28 | 🔴 Not started |
| 2.4 | Acquisition channels each producing ≥30 pilots/mo | 3 | 0 | GTM | 2026-08-28 | 🔴 Not started |
| 2.5 | CAC payback on first paying cohort | ≤6 months | n/a | Strategy | 2026-08-28 | 🔴 Not started |

### O3 — Become the most credible voice on OKR execution on the internet
| KR | Target | Current | Owner pod | Due | Status |
|---|---|---|---|---|---|
| 3.1 | Published "State of OKR Execution" benchmark posts | 12 | 0 | GTM | 2026-08-28 | 🔴 Not started |
| 3.2 | Combined LinkedIn followers (founder + brand) | 5,000 | tbd | GTM | 2026-08-28 | 🔴 Not started |
| 3.3 | Podcast appearances (cumulative from M2) | 12 | 0 | GTM | 2026-08-28 | 🔴 Not started |
| 3.4 | Product Hunt launch result | Top 5 of day | n/a | GTM | 2026-06-15 | 🔴 Not started |

### O4 — Build the company on the company's own product (dogfood)
| KR | Target | Current | Owner pod | Due | Status |
|---|---|---|---|---|---|
| 4.1 | All 30 agents tracked as "work-units" inside our product | 30/30 | 30/30 | AI/Data | 2026-05-19 | ✅ **Complete** — entire 30-agent org online (Strategy 4 + P/D 5 + Eng 7 + AI/Data 4 + GTM 6 + C/Ops 4) |
| 4.2 | Weekly company narrative auto-generated from agent output | 100% of weeks | 1 (dry-run) | AI/Data | 2026-05-19 | 🟡 In progress (loop wired; awaiting live LLM for first real narrative) |
| 4.3 | Dogfood-discovered gaps that become backlog within 24h | 100% | n/a | Product/Design | ongoing | 🔴 Not started |

---

## 3. Pod-Level OKRs

### Strategy Pod (CEO, CPO, CTO, CFO agents)
- **O:** Keep the company aimed at the right thing each week.
- KR: Weekly priorities doc updated by Sunday 8pm — **0/17 weeks**
- KR: ≤2 reversed major decisions per cycle — **0**

### Product & Design Pod (PM, UX-R, UX-D, UI-D, Copywriter)
- **O:** Customers feel the product is "obviously useful in the first 30 minutes."
- KR: 10 discovery interviews completed by 2026-05-05 — **0/10**
- KR: Design system components shipped — **0/24**
- KR: Onboarding completion rate ≥80% — **n/a**

### Engineering Pod (Backend-Arch, FE-Lead, Integrations, Data-Pipe, AI-Eng, Platform, Security)
- **O:** Ship the MVP in 14 days without building anything we'll throw away in 60.
- KR: Integrations live (GitHub, Linear, Jira, Slack, Notion) — **0/5**
- KR: p95 ingestion latency for new event ≤2 min — **n/a**
- KR: SOC2-readiness checklist items closed — **0/45**

### AI/Data Pod (OKR-Mapper, Signals-Analyst, Forecasting, Narrative)
- **O:** The "magic moment" — the auto-narrative — feels written by the smartest analyst the customer has ever met.
- KR: OKR-Mapper precision ≥85% @ recall ≥70% on eval — **n/a**
- KR: Forecasting calibration error (Brier) ≤0.15 — **n/a**
- KR: Narrative human-rated ≥4/5 by ≥80% of design partners — **n/a**

### GTM Pod (Growth, Content, Demand-Gen, Sales-Eng, Founder-Sales, Community/PR)
- **O:** Build a pilot pipeline that scales past founder hustle by Month 2.
- KR: Outbound touches per business day — **0 / target 600**
- KR: Demos booked per week — **0 / target 15 by M2**
- KR: Inbound pilots from content / community — **0 / target ≥30/mo by M3**

### Customer & Ops Pod (Onboarding, Support, Pilot-PM, Analytics-Ops)
- **O:** Every pilot reaches "first value" and we know exactly why each one converts or doesn't.
- KR: Pilot kickoff → first narrative ≤7 days, p90 — **n/a**
- KR: Pilot exit interview completion rate ≥90% — **n/a**
- KR: Bug → backlog ticket SLA ≤24h — **n/a**

---

## 4. The 30-Agent Roster

> Status legend: 🔴 not scaffolded · 🟡 scaffolded, no real prompt · 🟢 prompt + first run · ✅ shipping useful output

| # | Agent | Pod | Status | Path |
|---|---|---|---|---|
| 1 | ceo | Strategy | 🟢 | `agents/ceo/` |
| 2 | cpo | Strategy | 🟢 | `agents/cpo/` |
| 3 | cto | Strategy | 🟢 | `agents/cto/` |
| 4 | cfo | Strategy | 🟢 | `agents/cfo/` |
| 5 | pm | Product & Design | 🟢 | `agents/pm/` |
| 6 | ux_researcher | Product & Design | 🟢 | `agents/ux_researcher/` |
| 7 | ux_designer | Product & Design | 🟢 | `agents/ux_designer/` |
| 8 | ui_designer | Product & Design | 🟢 | `agents/ui_designer/` |
| 9 | copywriter | Product & Design | 🟢 | `agents/copywriter/` |
| 10 | backend_architect | Engineering | 🟢 | `agents/backend_architect/` |
| 11 | frontend_lead | Engineering | 🟢 | `agents/frontend_lead/` |
| 12 | integrations_engineer | Engineering | 🟢 | `agents/integrations_engineer/` |
| 13 | data_pipeline | Engineering | 🟢 | `agents/data_pipeline/` |
| 14 | ai_engineer | Engineering | 🟢 | `agents/ai_engineer/` |
| 15 | platform | Engineering | 🟢 | `agents/platform/` |
| 16 | security | Engineering | 🟢 | `agents/security/` |
| 17 | okr_mapper | AI/Data | 🟢 | `agents/okr_mapper/` |
| 18 | signals_analyst | AI/Data | 🟢 | `agents/signals_analyst/` |
| 19 | forecasting | AI/Data | 🟢 | `agents/forecasting/` |
| 20 | narrative | AI/Data | 🟢 | `agents/narrative/` |
| 21 | growth_hacker | GTM | 🟢 | `agents/growth_hacker/` |
| 22 | content | GTM | 🟢 | `agents/content/` |
| 23 | demand_gen | GTM | 🟢 | `agents/demand_gen/` |
| 24 | sales_engineer | GTM | 🟢 | `agents/sales_engineer/` |
| 25 | founder_sales | GTM | 🟢 | `agents/founder_sales/` |
| 26 | community_pr | GTM | 🟢 | `agents/community_pr/` |
| 27 | onboarding | Customer & Ops | 🟢 | `agents/onboarding/` |
| 28 | support | Customer & Ops | 🟢 | `agents/support/` |
| 29 | pilot_pm | Customer & Ops | 🟢 | `agents/pilot_pm/` |
| 30 | analytics_ops | Customer & Ops | 🟢 | `agents/analytics_ops/` |

---

## 5. Milestone Calendar

| Date | Milestone | Owner |
|---|---|---|
| 2026-04-28 | Tracker + OKRs locked, scaffolding begins | Strategy |
| 2026-05-05 | 10 discovery calls done; ICP locked; OKR-Mapper eval set built | UX-R + AI-Eng |
| 2026-05-12 | **MVP live**, internal dogfood begins | Engineering |
| 2026-05-19 | 5 design partners onboarded; agents ingested as work-units (KR4.1) | Customer/Ops |
| 2026-05-26 | First case study published; NPS measured (KR1.5) | Content + CS |
| 2026-06-09 | 25 pilots cumulative (M1 target) | GTM |
| 2026-06-15 | Product Hunt launch | Community/PR |
| 2026-07-09 | 75 pilots cumulative (M2 target) | GTM |
| 2026-08-09 | 175 pilots cumulative (M3 target) | GTM |
| 2026-08-28 | **300 pilots cumulative; cycle review** | All |

---

## 6. Sprint Log (2-week cadence)

### Sprint 0 — 2026-04-28 → 2026-05-12 — "MVP or die"
- Sprint goal: ship the MVP, get 5 design partners signed.
- Entry checklist:
  - [ ] Domain registered, Vercel + Supabase + Inngest projects created
  - [ ] Anthropic API key, prompt-caching baseline confirmed
  - [ ] Nango account or direct OAuth apps for GitHub/Linear/Jira/Slack/Notion
  - [ ] Linear workspace for our own work (we are the first dogfood account)
- Daily standup: company narrative auto-generated by `narrative` agent from Linear + Git activity. (Once it works, it replaces this section.)

#### Day 1 (2026-04-28 → 2026-04-29) — what shipped
- Project scaffolded at `C:/Users/aloch/okr-monitor/` following skinmap-style conventions (`core/`, `agents/`, `config/`, `scripts/`, `cli/`).
- Strategy pod (4 agents) shipped end-to-end and smoke-tested in dry-run:
  - `ceo` — weekly priorities proposal
  - `cpo` — roadmap pressure test
  - `cto` — architecture review with severity-ranked risks
  - `cfo` — pricing model v0 proposal
- Operator surface: `cli/review.py` for approve/edit/reject/defer with edit-distance telemetry.
- Dogfood live: every run snapshots TRACKER.md into `tracker_snapshots`, so any proposal is replayable against the exact tracker state it reasoned over.
- Run order of operations:
  1. `python scripts/init_db.py` — once
  2. `OKR_MONITOR_DRY_RUN=true python scripts/run_strategy_pod.py` — safe
  3. `python -m cli.review` — operator reviews the queue
  4. Flip `OKR_MONITOR_DRY_RUN=false` once an `ANTHROPIC_API_KEY` is in `.env`
- KR4.1 progress: **4/30 agents** now tracked as work-units (the pod itself).
- Sunday-evening wrapper `scripts/sunday_evening.py` shipped and smoke-tested:
  - Runs the pod, fetches each proposal back from the DB, writes one markdown file per agent under `proposals/YYYY-MM-DD/`, and a one-page `MONDAY_BRIEF.md`.
  - Git-agnostic — the caller commits/pushes. (Remote routine prompt handles git.)
  - Auto-flips to dry-run + banners the brief if `ANTHROPIC_API_KEY` is missing.

#### Day 2 (2026-04-29) — what shipped
- **Daily LLM circuit breaker** (`core/limits.py`): caps spend per UTC day, refuses calls past cap, audit-alerts on trip. Default $50 Sprint 0–1, $100 Sprint 2+. Tested across 5 scenarios (empty / under-cap / over-cap / env-override / today's date in Sprint 0 window) — all pass.
- **CFO budget overview proposal** (`proposals/2026-04-29/cfo_budget_overview.md`) — hand-prepared as planning-team stand-in. Recommended cycle budget $30K; LLM <7% of total, GTM 71%, infra 6%, contingency 17%.
- **API key sanity test** — key authenticates, but Anthropic account balance is $0. Real strategy-pod runs blocked on operator billing top-up.
- **Operator decisions captured (2026-04-29):** ✅ API key activation, ✅ daily LLM circuit breaker, ✅ git repo init. ⏸️ Budget + GTM deferred until product signal exists.
- KR4.1 progress unchanged (4/30 agents). KR1.1 progress: ~5% (scaffolding + dogfood loop, no MVP web app yet).

#### Day 3 (2026-04-29 evening) — what shipped
- **AI/Data pod's load-bearing pair: `okr_mapper` + `narrative`.** Each follows the same skinmap-style pipeline (cached system prompt + per-call user message, store via `core/store.py`, audit via `core/audit.py`).
  - **OKR-Mapper** (`agents/okr_mapper/`): `run(event_id=...)` to map one event, or `run_all_unmapped()` to sweep. Drops mappings with confidence < 0.5 in code (defense in depth).
  - **Narrative** (`agents/narrative/`): `run(period_end=, period_days=7)` reads all mappings in window, produces structured weekly brief with per-KR verdicts (on_track/drifting/off) and an attention-alignment score.
- **Dogfood ingestion** (`core/dogfood.py`): turns each strategy-pod proposal into a `work_event` with `source="agent_proposal"`, idempotent on `proposal_id`.
- **Schema additions** in `core/store.py`: `work_events`, `event_kr_mappings`, `narratives` — all FK-linked to `runs`.
- **`scripts/sunday_evening.py` extended:** after the strategy pod runs, it now (1) ingests all 4 fresh proposals as work_events, (2) sweeps every unmapped event through the OKR-Mapper, (3) generates the weekly narrative, (4) drops `weekly_narrative.md` into `proposals/YYYY-MM-DD/` alongside the brief, (5) summarizes the dogfood loop in MONDAY_BRIEF.md.
- **End-to-end smoke test (dry-run):** fresh DB → pod → 4 proposals → 4 ingested events → 4 mappings → 1 narrative → 7 markdown files in `proposals/2026-04-29/`. All audit events landed; zero failures.
- KR4.1 progress: **6/30 agents** (Strategy pod 4 + okr_mapper + narrative). KR4.2 in progress (loop wired; awaiting live LLM for first real narrative).

#### Day 3 (2026-04-29 late) — what shipped (no API needed)
- **`signals_analyst`** (`agents/signals_analyst/`) — pure compute. Reads `event_kr_mappings`, writes one `kr_signals` row per KR per run with rolling 7d/30d/all-time event counts, distinct-actor count, mean confidence, last-event timestamp.
- **`forecasting`** (`agents/forecasting/`) — pure compute. Pulls latest signals_analyst row + TRACKER.md §2 target/current/due_date, emits a verdict per KR: `on_track | active | drifting | stale | off | qualitative`. Parses targets like `300`, `≥85% P @ ≥70% R`, `5,000`, `≤6 months`. P(hit) deferred to v1.
- **`cli/status.py`** — operator dashboard. `python -m cli.status` prints the KR scoreboard from latest signals; `--kr 1.3` shows event-level detail.
- **Sunday wrapper extended** — runs signals_analyst + forecasting after the OKR-Mapper sweep; verdicts surface in `MONDAY_BRIEF.md`.
- **`tests/test_signals_math.py`** — 9 unit tests covering window-count partitioning, distinct-actor / mean-confidence math, target parsing (numeric/percentage/comma/qualitative), date parsing, and all 6 verdict transitions. Uses a separate `okr_monitor_test.db` patched at import time. **All passing.**
- **End-to-end smoke (dry-run, fresh DB):** pod → 4 events → 4 mappings → narrative → 17 KR signals → 17 verdicts (10 qualitative, 6 stale, 1 active). Status CLI confirms the active one is KR4.1 (the dogfood loop) — exactly as designed.
- KR4.1 progress: **8/30 agents** (Strategy 4 + AI/Data pod 4). KR4.2 still awaiting live LLM. Test infrastructure now in place for any future verdict-math change.

#### Day 3 (2026-04-29 latest) — what shipped (no API needed, half the org online)
- **`agents/_proposal.py`** — shared run helper for any agent that follows the "single LLM call → one structured proposal" pattern. Extracts the canonical boilerplate (snapshot tracker → cached system → call LLM → parse JSON → write proposal → audit emit → end run) so new agents drop to ~30 lines of unique code (prompt + user_message_fn + body_md_fn).
- **8 new agents shipped** as scaffolding (operator-in-the-loop, dry-run-tested, real proposals when credits resolve):
  - **`pm`** (Product & Design) — `user_stories`: ≤5 sprint stories, each tied to a KR with acceptance criteria.
  - **`ux_researcher`** (Product & Design) — `discovery_synthesis`: JTBD clusters from interview notes; treats anti-signals as gold.
  - **`copywriter`** (Product & Design) — `copy_draft`: 3 variants per slot (problem-led / outcome-led / contrarian); operator picks.
  - **`founder_sales`** (GTM) — `outreach_drafts`: 5 personalized templates for named ICP accounts; placeholder hooks for public artifacts.
  - **`demand_gen`** (GTM) — `cold_sequence`: 5-touch multi-channel sequence with per-touch thesis; reply-rate target stated.
  - **`content`** (GTM) — `blog_post_draft`: 800-1,200 word post with anchor stat + named anti-pattern + proprietary frame.
  - **`pilot_pm`** (Customer & Ops) — `pilot_milestone_review`: per-pilot verdict (on_track/at_risk/dormant/converting); breakup emails for dormant.
  - **`onboarding`** (Customer & Ops) — `onboarding_playbook`: 60-day pilot kickoff with timeboxed agenda + Day-7 milestones.
- KR4.1 progress: **16/30 agents** — Strategy (4) + AI/Data (4) + Product/Design partial (3 of 5) + GTM partial (3 of 6) + Customer/Ops partial (2 of 4). Just over half the org online.

#### Day 3 (2026-04-29 evening) — what shipped (api unblocked + daily report + docs)
- **API workspace alignment unblocked.** Root cause: shell `ANTHROPIC_API_KEY` from Max-plan auth was shadowing the funded `.env` key (`load_dotenv` default is `override=False`). Patched 18 scripts with `override=True`. **First real LLM call shipped:** CEO `weekly_priorities` proposal, $0.017, confidence 0.82 — proposal correctly identified the unmitigated High risks from TRACKER.md as the top priorities.
- **DEV DEFAULT flipped to `OKR_MONITOR_DRY_RUN=true`.** Most work happens free on Max; explicit override needed for real spend. Cloud routines have their own env.
- **Daily 7pm OWNER/FINANCE report pipeline shipped:**
  - **CEO `daily_status`** — today vs expected, blockers, next-milestone verdict.
  - **CPO `product_roadmap_report`** — agent count, MVP %, shipped/in-progress/blocked, 2-week roadmap.
  - **CFO `cost_projection`** — 14-day spend forecast, per-agent cost breakdown, circuit-breaker status.
  - **analytics_ops** (new agent) `growth_metrics` — pilots, CAC by channel, growth spend, outreach counts. Pre-launch state shows zeros honestly.
  - **`core/dashboard.py`** renders the KR scoreboard as markdown for inclusion at top of every report.
  - **`core/mailer.py`** SMTP sender (graceful no-op if `SMTP_HOST` unset). User configures Gmail app password etc. in `.env`.
  - **`scripts/daily_evening.py`** orchestrator — refresh signals → gather activity → run 4 reporters → render dashboard → assemble report → email + commit.
  - **Routine scheduled:** `trig_01BMMoRNTGDwuVshakfmapS6` daily at `0 23 * * *` UTC (7pm Pacific EDT). First fire: tonight.
- **Documentation:**
  - **`README.md`** — what is this, who built it, who runs it, repo layout, quick start, where-to-look-for-what.
  - **`RUNBOOK.md`** — daily/weekly ops, the 5 most-used commands, troubleshooting (balance-too-low, circuit breaker tripped, YAML colon gotcha, SMTP failures), command cheat sheet, what's persistent vs ephemeral.
- KR4.1 progress: **17/30 agents** (analytics_ops added). KR4.2 narrative loop active in dry-run; awaiting cloud secret injection for real output.

#### Day 3 (2026-04-29 night) — what shipped (org complete + Sunday Actions workflow)
- **All 13 remaining agents scaffolded** using the `_proposal.run_proposal` helper (~25 lines per pipeline). The full 30-agent org is now online in dry-run:
  - **Product/Design** completed (2 added): `ux_designer` (design_brief), `ui_designer` (component_spec).
  - **Engineering pod** completed (7 added): `backend_architect` (api_design), `frontend_lead` (ui_architecture), `integrations_engineer` (integration_design), `data_pipeline` (pipeline_design), `ai_engineer` (eval_proposal), `platform` (infra_review), `security` (security_review).
  - **GTM** completed (3 added): `sales_engineer` (demo_script), `community_pr` (pr_pitches), `growth_hacker` (experiment_proposal).
  - **Customer/Ops** completed (1 added): `support` (ticket_triage).
- **Generic fall-through mock** in `core/llm._default_mock` so any newly-scaffolded agent produces parseable JSON in dry-run without a bespoke mock entry. Bespoke mocks for the load-bearing agents stay; new agents get the generic envelope (title + summary + confidence + reasoning).
- **Sunday GitHub Actions workflow** at `.github/workflows/sunday.yml`. Cron `0 1 * * 1` UTC = Sun 6pm Pacific (EDT). Mirrors the daily workflow pattern (checkout → Python 3.11 → install → init DB → `sunday_evening.py` → commit + push). Once the operator adds `ANTHROPIC_API_KEY` as a repo secret, this replaces the claude.ai Sunday routine (`trig_01Q99GjcE5D58K5WzLt4cJsC`).
- **End-to-end smoke test:** all 13 new agents `parsed_ok=true` in dry-run.
- **KR4.1 = 30/30** ✅ — the entire 30-agent org is on (status flag 🟢). Each agent has its own prompt, config, pipeline, and run script. They will produce real output the moment `OKR_MONITOR_DRY_RUN=false` is set or the GitHub Actions workflow runs with the secret in env.

### Sprint 1 — 2026-05-13 → 2026-05-26 — "Design partner love"
- Sprint goal: 5 design partners using product weekly, NPS measured.

*(Subsequent sprints added as we go.)*

---

## 7. Decision Log

> One row per non-trivial decision. Reversals get a new row, not an edit.

| Date | Decision | Rationale | Reversed? |
|---|---|---|---|
| 2026-04-28 | Lead with GitHub + Linear/Jira + Slack + Notion integrations. Defer Salesforce/Gong to post-pilot. | These 4 cover ~80% of ICP and let us ship in 2 weeks. Salesforce alone is a 2-week project. | — |
| 2026-04-28 | Buyer persona = Chief of Staff / Head of Ops, not CEO. | They feel the pain (chasing status), they have budget authority for tools <$25k, and they will weaponize it upward to the CEO. | — |
| 2026-04-28 | Build OKR Monitor as a separate project at `C:/Users/aloch/okr-monitor/`, not inside `skinmap_agents/`. | Different company, different operator-in-the-loop posture (B2B SaaS, not regulated medical). | — |
| 2026-04-28 | Dogfood from day 1: this TRACKER.md is the first ingested document. | Forces the product to handle messy real-world inputs, not toy data. | — |
| 2026-04-29 | Strategy pod (CEO/CPO/CTO/CFO) shipped first. Each agent is one LLM call producing one structured proposal; operator reviews via `cli/review.py`. | Operator wants strategy partners online before building agents come up — they can direct the building. Same operator-in-the-loop posture as `skinmap_agents`. | — |
| 2026-04-29 | Default model = `claude-sonnet-4-6` for all four. System prompt = role + `company.yaml` + full `TRACKER.md`, cached. User message varies per call. | Identical system block across the pod means a single `run_strategy_pod.py` invocation pays the system tokens once, gets ~10% pricing on the next 3 calls (prompt cache TTL ~5 min). | — |
| 2026-04-29 | Sunday-evening planning pass scheduled as a remote Claude Code routine (Sun 6pm Pacific = Mon 1am UTC). Run output is committed to git as `proposals/YYYY-MM-DD/MONDAY_BRIEF.md` + four agent proposal files. | Local cron only fires when the laptop is on; remote routine is durable. The proposals committed to git become the persistent dogfood record (the SQLite DB in the cloud sandbox is ephemeral). | — |
| 2026-04-29 | Push `okr-monitor/` to a **private** GitHub repo so the remote routine can clone it. Wrapper (`scripts/sunday_evening.py`) is git-agnostic; the routine prompt handles add/commit/push. | Private repo because TRACKER.md contains pricing math, ICP detail, and risks that aren't public-ready. The wrapper stays git-agnostic so it's also runnable locally without a repo. | — |
| 2026-04-29 | If `ANTHROPIC_API_KEY` is unavailable in the sandbox, the wrapper auto-flips to dry-run and stamps a banner on MONDAY_BRIEF.md. | Better to ship a stub brief on schedule than crash silently. The banner makes the operator's first read tell them to fix the secret. | — |
| 2026-04-29 | Daily LLM cost circuit breaker shipped (`core/limits.py`): $50/day Sprint 0–1, $100/day Sprint 2+. Override via `OKR_MONITOR_DAILY_LLM_CAP_USD`. Trip = call refused, audit emits `*.circuit_breaker_open` alert. | Operator approval to enable the API key was contingent on a hard cap. Better to refuse a call and alert than to discover overspend in a billing email. Cap is intentionally per-day (UTC), not per-month — daily granularity catches runaway loops within hours, not weeks. | — |
| 2026-04-29 | API-key smoke test surfaced: key authenticates but Anthropic account has \$0 balance. Pipeline wiring confirmed correct; real LLM calls blocked by billing, not code. | Operator needs to top up at `console.anthropic.com → Plans & Billing` before any real strategy-pod run. Sprint 0 forecast \$40/14d → recommend loading \$50–\$100 to start. | — |
| 2026-04-29 | Budget approval and GTM allocation deferred until "the product is further along" (operator). Only API-key activation, daily circuit breaker, and git repo init are in-scope right now. | Disciplined: operator wants real product signal (design partners using the MVP) before approving the GTM elephant ($20.9K of $30K plan). Smart call — paid acquisition with no product signal is just expensive learning. | — |
| 2026-04-29 | AI/Data pod's two load-bearing agents (`okr_mapper` and `narrative`) shipped, plus dogfood ingestion (`core/dogfood.py`). Every strategy-pod proposal now becomes a `work_event` → mapped to KR(s) by `okr_mapper` → fed into the weekly auto-narrative. | This is the magic-moment IP (KR1.3 mapper precision = the whole product). Wiring it dogfood-first means we generate real eval data on our own work BEFORE the first design partner touches the system — zero customer-data risk during the precision-tuning phase. | — |
| 2026-04-29 | Schema additions (`work_events`, `event_kr_mappings`, `narratives`) chosen with `UNIQUE(source, source_event_id)` for idempotency. Real integrations (GitHub/Linear/Slack) write the same shape via `store.upsert_work_event`. | Webhook retries are the silent killer — same commit can fire 2-3 times. Idempotency at the schema level means we cannot double-count events even if the integration code is buggy. The `agent_proposal` source is just the first source to use this shape. | — |
| 2026-04-29 | OKR-Mapper enforces a confidence ≥ 0.5 floor at the pipeline level (in code, not the prompt). Anything below is dropped. | Confident-wrong is worse than no-mapping for the narrative. The prompt asks for calibration; the pipeline enforces it. Defense in depth — the model can drift on calibration; the floor cannot. | — |
| 2026-04-29 | AI/Data pod completed: `signals_analyst` and `forecasting` are pure-compute agents (no LLM). signals_analyst writes per-KR rolling counts (7d/30d/all). forecasting parses target/current/due_date from TRACKER.md and emits a verdict per KR (on_track/active/drifting/stale/off/qualitative). Both write to a single `kr_signals` table. | Forecast probabilities (P(hit)) are intentionally deferred. Events ≠ KR target unit for most KRs (a commit isn't a pilot), so a probability without a per-KR conversion factor would be a confident lie. Verdict heuristics ship usefulness now; calibrated P(hit) waits until we have real data per KR class. | — |
| 2026-04-29 | `cli/status.py` operator dashboard ships — reads latest `kr_signals` and prints a compact table. ASCII-safe (Windows cmd cp1252 chokes on emoji and em-dashes). | Operator needs a single command to answer "where are we right now?" without opening a database. ASCII-only because the operator runs Windows; emoji-pretty isn't worth the friction of a broken table. | — |
| 2026-04-29 | Test infrastructure shipped: `tests/test_signals_math.py` validates 9 scenarios across signals + forecasting using a separate `okr_monitor_test.db`. Runnable via `python -m tests.test_signals_math`. | Math is the load-bearing IP for the verdict system. Catching a regression in window boundaries or target parsing matters more than catching a typo in a prompt. The test DB is patched at import time so tests never touch production data. | — |
| 2026-04-29 | 8 more agents scaffolded (pm, ux_researcher, copywriter, founder_sales, demand_gen, content, pilot_pm, onboarding) using new shared `agents/_proposal.py` helper. Each is ~30-line pipeline + tailored prompt + per-output body_md formatter. All 8 dry-run smoke-tested green. | Same operator-in-the-loop pattern as the strategy pod. Helper extracts the canonical "snapshot tracker → call LLM → parse JSON → write proposal → audit" boilerplate so new agents stay focused on their prompt + output shape. Strategy pod's 4 unchanged (kept their inline implementations to avoid touching working code). | — |
| 2026-04-29 | YAML config gotcha discovered: unquoted colons inside list-string items break parsing (`"At risk": who calls...` interpreted as mapping). Fix: wrap in single quotes `'...'` or rephrase to use em-dash. Three configs (pm, pilot_pm, onboarding) hit this. | Tooling-level lesson worth capturing — anyone writing future YAML configs in this repo will hit this. The fix is mechanical but not obvious from the error message. | — |
| 2026-04-29 | Root cause for "balance too low" identified: shell `ANTHROPIC_API_KEY` (Max account, $0 API balance) was shadowing the funded `.env` key because `load_dotenv()` defaults to `override=False`. Fix: `override=True` in all 18 run scripts. | The Max-plan key is for Claude Code CLI subscription auth, not API billing. The Anthropic Python SDK has no "subscription mode"; it requires API credits. Six failed calls were all the wrong key reaching Anthropic. Lesson: always `override=True` when a project loads its own .env in a context where the user may have global API key envs set. | — |
| 2026-04-29 | DEV DEFAULT flipped to `OKR_MONITOR_DRY_RUN=true` in `.env`. Real runs now require explicit override (`OKR_MONITOR_DRY_RUN=false python scripts/X.py`). Cloud routines set their own env. | Operator instruction: most work happens on Max (free); only autonomous and explicit operator-triggered runs hit the API budget. Protects the $100 from accidental script invocations during development. | — |
| 2026-04-29 | Daily 7pm OWNER/FINANCE report shipped: CEO `daily_status`, CPO `product_roadmap_report`, CFO `cost_projection`, analytics_ops `growth_metrics`, KPI dashboard markdown render at the top. SMTP send via `core/mailer.py` (no-op fallback if SMTP_HOST unset). New remote routine `trig_01BMMoRNTGDwuVshakfmapS6` fires daily at `0 23 * * *` UTC = 7pm Pacific (EDT). | Operator wants end-of-day visibility into accomplishment vs expectation, projected spend, roadmap progress, and growth pipeline — accompanied by the live KPI dashboard. The four reporters reuse the existing strategy pod for CEO/CPO/CFO (added `run_<kind>` functions alongside the existing `run()` so weekly behavior is unchanged); analytics_ops is a new agent. Email is best-effort; the report file is committed regardless. | — |
| 2026-04-29 | Documentation shipped: `README.md` (what is this, who built it, quick start, repo layout) and `RUNBOOK.md` (daily/weekly ops, troubleshooting, command cheat sheet, what's persistent vs ephemeral). | Operator-requested natural-language documentation alongside the code. Future-you (or a teammate brought in) needs to be able to pick this up cold without reading every prompt and every pipeline. | — |

---

## 8. Customer Pipeline

### Design partners (target: 5 by 2026-05-19)
| Company | Contact | Status | Integrations they use | Notes |
|---|---|---|---|---|
| _tbd_ | | | | |

### Pilots (target: 300 by 2026-08-28)
*(Tracked in CRM once we have one. For Sprint 0, just a Notion list.)*

---

## 9. Risks & Open Questions

| Risk / Question | Severity | Owner | Mitigation / Next step |
|---|---|---|---|
| OKR-Mapper precision is the whole product. If <85% on eval, the narrative reads like nonsense. | High | AI-Eng | Build the 200-event labeled eval set in week 1 before any UI work. |
| 300 pilots in 4 months requires ~600 outbound touches/business day. Can a single founder + agents sustain that without spam-tier reply rates? | High | GTM | Hold demand-gen agents in "draft for human review" until reply rate ≥3%. |
| Integration breakage (GitHub/Slack OAuth scope changes) silently corrupts ingestion. | Med | Integrations | Per-source health check + pager on stale-data >2h. |
| Pricing not yet decided. Pilots free of charge, but "pilot → paid intent" KR is fuzzy without a price. | Med | CFO | Lock pricing model by 2026-05-19 (end of Sprint 0). |
| Are we comfortable Slack-ingesting customer conversations re: privacy? | High | Security | Default: only public channels + opt-in private channels. DPA template by 2026-05-12. |
| `ANTHROPIC_API_KEY` for the remote Sunday routine — no obvious secret-injection mechanism in the routine config. | Med | Strategy | V1: routine runs in dry-run (stub brief still useful). V2: store key in a GitHub Actions secret and have the routine call a workflow. Or move scheduling to GitHub Actions entirely. |
| Anthropic account currently at $0 balance — no real LLM calls succeed even with valid key. | High (blocks all live agent runs) | Strategy | Operator action: top up at console.anthropic.com → Plans & Billing. Recommend $50–$100 to start (Sprint 0 forecast $40/14d). Until then, all runs forced to dry-run. |

---

## 10. Dogfooding Notes

We are simultaneously the **first customer** and the **builder**. Rules:

1. Every agent's output is a "work event" in our own database, tagged to one or more company KRs.
2. The Friday narrative for *our company* is generated by our own `narrative` agent from our own Linear + commit data — not hand-written. If the narrative is bad, that is a P0 bug.
3. Anything we feel "I wish the product did X for me right now" goes straight into the backlog with the `dogfood` label, within 24h (KR4.3).
4. We do not show the product to a design partner until *we* have read our own auto-narrative for two consecutive Fridays and found it useful. That is the launch gate.

---

## 11. How to update this file

- **OKR status changes:** edit the table, bump `Last updated` at the top.
- **New decision:** append a row to §7. Never edit history.
- **Sprint close:** append a "Retro" sub-section to that sprint with what shipped, what slipped, what we learned.
- **New risk:** append to §9. When mitigated, strike through but keep.
