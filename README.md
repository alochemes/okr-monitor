# OKR Monitor

> A B2B SaaS that connects company OKRs to the actual work happening in code, tickets, and conversations — and surfaces drift in real time, before quarter-end.

This repository is the **agent system** behind OKR Monitor. It is operator-in-the-loop: agents propose; the operator approves; the system measures and degrades agent autonomy when quality drifts. We are also our own first customer — the same agents that ship the product also report on the company building it.

---

## What this is

If you're a Chief of Staff or Head of Operations and you've ever spent your Monday morning DM-ing five people to find out whether the OKRs you set are actually being worked on, this is for you.

**The wedge:** every Friday, you get a one-page exec summary of which OKRs are on track, which are drifting, and exactly which work is — and isn't — moving the needle.

**The mechanism:**
1. We ingest "work events" from the systems you already use (GitHub, Linear/Jira, Slack, Notion).
2. An agent called **OKR-Mapper** classifies every event against your KRs with a confidence score.
3. **Signals-Analyst** rolls those mappings into per-KR rolling counts (events per 7d/30d).
4. **Forecasting** compares current pace to required pace, emitting a verdict per KR: `on_track | active | drifting | stale | off | qualitative`.
5. **Narrative** writes the human story for the week. That's the magic moment.

**The wedge isn't the tooling — it's the framework.** Most pilots arrive with OKRs that need cleanup before they're measurable. The customer-facing playbook in [`notion/03_playbooks/01_customer_okr_kpi_framework.md`](notion/03_playbooks/01_customer_okr_kpi_framework.md) is the artifact we hand every pilot at kickoff. The agents are the delivery mechanism that makes the cleanup stick.

The marketing surface (Next.js landing page in `web/`) is shipped. The product app (logged-in dashboard) is Sprint 0 work.

---

## Who built this

- **Operator/Founder:** Andrew (`andrew@skinmap.com`)
- **Repository:** https://github.com/alochemes/okr-monitor (private)
- **Started:** 2026-04-28
- **MVP target:** 2026-05-12 · **300 pilots target:** 2026-08-28

---

## How the org is structured

The company runs as a 30-agent team across 6 pods. Status of each agent is tracked in [TRACKER.md §4](TRACKER.md). At the time of this README writing:

- **Strategy** (4/4 live): `ceo` · `cpo` · `cto` · `cfo`
- **AI/Data** (4/4 live): `okr_mapper` · `narrative` · `signals_analyst` · `forecasting`
- **Product/Design** (5/5 live): `pm` · `ux_researcher` · `ux_designer` · `ui_designer` · `copywriter`
- **Engineering** (7/7 live): `backend_architect` · `frontend_lead` · `integrations_engineer` · `data_pipeline` · `ai_engineer` · `platform` · `security`
- **GTM** (6/6 live): `founder_sales` · `demand_gen` · `content` · `growth_hacker` · `sales_engineer` · `community_pr`
- **Customer/Ops** (4/4 live): `pilot_pm` · `onboarding` · `analytics_ops` · `support`

KR4.1 ✅ — full 30-agent org online.

---

## What runs when (cadences)

| Cadence | What happens | Where |
|---|---|---|
| **Every Sunday 6pm Pacific** | Strategy pod (CEO/CPO/CTO/CFO) drafts proposals · OKR-Mapper sweeps new events · Narrative writes the weekly story | Remote routine `trig_01Q99GjcE5D58K5WzLt4cJsC` → commits to `proposals/YYYY-MM-DD/` |
| **Every day 7pm Pacific** | OWNER/FINANCE status report — CEO daily synopsis · CPO product roadmap · CFO 14-day cost projection · Analytics-Ops growth metrics · KPI dashboard at top | Remote routine `trig_01BMMoRNTGDwuVshakfmapS6` → commits to `reports/daily/YYYY-MM-DD/` + emails if SMTP configured |
| **On demand** | Any single agent: `python scripts/run_<agent>.py` (dev: dry-run by default; real: prefix `OKR_MONITOR_DRY_RUN=false`) | Local terminal |
| **Continuous** | `python -m cli.review` to walk the queue of pending agent proposals | Local terminal |
| **Continuous** | `python -m cli.status` to see the live KR scoreboard | Local terminal |
| **Continuous** | `python -m cli.kpis` to see operational K1–K10 (cost cap, builds, tests, runway) | Local terminal |
| **Continuous** | `python scripts/run_ab_report.py` for landing-page A/B (PostHog) | Local terminal |

## Adjacent surfaces

- **`web/`** — marketing landing page (Next.js 15 + Tailwind, deployed to Vercel). Editorial design, single accent color, mock printed memo as the hero asset. Includes PostHog A/B testing on hero headline + CTA. Build verified: 13.6 kB page, 174 kB First Load JS, 5 routes. See [`web/README.md`](web/README.md).
- **`notion/`** — knowledge base in markdown, drag-importable into Notion. 9 docs covering company identity, full product runbook, daily/weekly cadence, the customer-facing OKR/KPI framework (the wedge), KB-mining playbook, 60-day pilot kickoff, pilot intake questionnaire, team + workflow + tech stack diagrams (Mermaid), and social media setup. See [`notion/00_MASTER_INDEX.md`](notion/00_MASTER_INDEX.md).
- **`reports/daily/YYYY-MM-DD/`** — committed daily OWNER/FINANCE briefs (auto-generated 7pm Pacific by GitHub Actions).
- **`reports/ab/YYYY-MM-DD.md`** — A/B experiment reports (run on demand: `python scripts/run_ab_report.py`).
- **`proposals/YYYY-MM-DD/`** — committed weekly strategy-pod briefs + per-agent proposals (auto-generated Sundays).
- **`data/health_checks/<slug>/`** — per-customer pilot artifacts: `intake.yaml` (their filled-in questionnaire) and `HEALTH_CHECK.md` (the lead-magnet brief we send back, generated by `scripts/run_okr_health_check.py`).
- **`.github/workflows/`** — `daily.yml` (daily 7pm) and `sunday.yml` (Sunday 6pm) GitHub Actions cron workflows. Replace the older claude.ai routines once secrets are configured. See [`INSTRUCTIONS.md`](INSTRUCTIONS.md).

---

## Quick start

```bash
# 1. Clone (or you already have the repo)
git clone https://github.com/alochemes/okr-monitor.git
cd okr-monitor

# 2. Install Python deps (Python 3.11+)
pip install -r requirements.txt

# 3. Initialize the local SQLite database
python scripts/init_db.py

# 4. Copy env template and fill in your API key
cp .env.example .env
# Edit .env — paste ANTHROPIC_API_KEY from console.anthropic.com (the workspace
# with funded credits, not the Claude.ai Max subscription one).
# Default is OKR_MONITOR_DRY_RUN=true — see "How dry-run works" below.

# 5. Run a dry-run smoke test (free, no API calls)
python scripts/sunday_evening.py     # full Sunday flow
python scripts/daily_evening.py --no-email   # full daily flow, no email send

# 6. See the proposals + KPI scoreboard
python -m cli.status
python -m cli.review --list

# 7. To get REAL output (costs $0.02 per agent, $0.05 for full pod):
OKR_MONITOR_DRY_RUN=false python scripts/run_ceo.py
```

---

## How dry-run works (and why you should care)

The `OKR_MONITOR_DRY_RUN` env var controls whether agents make real Anthropic API calls or return canned stub JSON. **Default is `true`** — this protects the API budget from accidental script runs during development.

**To make a real LLM call**, set it explicitly per command:
```bash
OKR_MONITOR_DRY_RUN=false python scripts/run_ceo.py
```

**Cloud routines** (Sunday + daily) read their own env. They're set up to run real once `ANTHROPIC_API_KEY` is injectable into the routine sandbox (currently a manual operator task — see TRACKER.md §9 risks).

The wrapper scripts (`sunday_evening.py`, `daily_evening.py`) auto-fall-back to dry-run with a clear banner if `ANTHROPIC_API_KEY` is missing — so the routines never silently bill nothing or crash hard.

**Cost per real run** (as of 2026-04-29):
- Strategy pod (4 agents): ~$0.05
- OKR-Mapper per event: ~$0.0075 (effective, including re-maps)
- Narrative (weekly): ~$0.02 per account
- Daily report (4 agents): ~$0.07
- See `proposals/2026-04-29/cfo_budget_overview.md` for full cost model

---

## Repository layout

```
okr-monitor/
├── TRACKER.md              ← single source of truth — OKRs, agent roster, decisions, risks
├── README.md               ← you are here
├── RUNBOOK.md              ← operator playbook — daily/weekly tasks, debugging
├── CLAUDE.md               ← project notes for Claude Code agents
│
├── agents/                 ← one subdir per agent
│   ├── _base.py            ← shared system-prompt assembler (cached)
│   ├── _proposal.py        ← shared "single LLM call → one proposal" runner
│   ├── ceo/                ← weekly_priorities + daily_status
│   ├── cpo/                ← roadmap_review + product_roadmap_report
│   ├── cfo/                ← pricing_model + cost_projection
│   ├── cto/                ← architecture_review
│   ├── okr_mapper/         ← maps work_events → KR(s) with confidence
│   ├── narrative/          ← weekly company narrative
│   ├── signals_analyst/    ← pure compute: per-KR rolling counts (no LLM)
│   ├── forecasting/        ← pure compute: per-KR verdicts (no LLM)
│   ├── analytics_ops/      ← daily growth metrics
│   ├── pm/, ux_researcher/, copywriter/, founder_sales/,
│   │   demand_gen/, content/, pilot_pm/, onboarding/   ← scaffolded
│
├── core/
│   ├── llm.py              ← Anthropic wrapper with prompt caching + dry-run
│   ├── store.py            ← SQLite (WAL) — all reads/writes go through here
│   ├── audit.py            ← append-only JSONL event log
│   ├── tracker.py          ← parses TRACKER.md
│   ├── dogfood.py          ← turns each proposal into a work_event
│   ├── limits.py           ← daily LLM cost circuit breaker
│   ├── budgets.py          ← per-run cost/time/step caps
│   ├── dashboard.py        ← KR scoreboard markdown renderer
│   ├── mailer.py           ← SMTP sender (no-op if SMTP_HOST unset)
│   └── config.py, paths.py
│
├── config/                 ← per-agent yaml (model, cadence, output_kinds)
│   └── company.yaml        ← OKR Monitor identity (cached into every system prompt)
│
├── scripts/                ← CLI runners (one per agent + 2 orchestrators)
│   ├── sunday_evening.py   ← full Sunday flow (strategy + dogfood + narrative)
│   ├── daily_evening.py    ← full daily 7pm OWNER/FINANCE report
│   └── run_<agent>.py      ← single-agent runners
│
├── cli/
│   ├── review.py           ← operator queue: approve/edit/reject/defer proposals
│   └── status.py           ← live KR scoreboard
│
├── tests/                  ← unit tests (pure-Python, no API)
│   └── test_signals_math.py
│
├── proposals/YYYY-MM-DD/   ← Sunday output: 4 strategy proposals + brief + narrative
├── reports/daily/YYYY-MM-DD/  ← Daily output: OWNER_FINANCE_REPORT.md
└── data/                   ← gitignored: SQLite DB + audit JSONL
```

---

## Adding a new agent

1. Create `agents/<name>/` with `__init__.py`, `pipeline.py`, and a `prompts/<kind>.md`.
2. The pipeline can use `agents._proposal.run_proposal()` for the standard pattern (snapshot tracker → call LLM → write proposal → audit).
3. Add `config/<name>.yaml` with at minimum: `model`, `max_tokens`, `temperature`, `cadence`, `output_kinds`.
4. Add `scripts/run_<name>.py` (a 25-line runner — copy any existing one as template).
5. Add a mock response in `core/llm._default_mock` for the new action key.
6. Update [TRACKER.md §4](TRACKER.md) — flip the agent's status flag.

The strategy pod's older agents have inline pipelines (~100 lines each). New agents using `_proposal.run_proposal` are ~30 lines. Either pattern is fine — don't refactor working code without a reason.

---

## Why this design (one paragraph)

OKR Monitor is built on a few stubborn beliefs.

**Operator-in-the-loop, not autonomous.** Every consequential action is a proposal the operator reviews. We measure how much the operator edits each proposal (edit-distance) and use that as a trust signal. Auto-execution requires earning a "promotion gate" (planned, not yet implemented).

**Dogfood first.** The product is its own first customer. Every agent run is a `work_event` in our own database. The `okr_mapper` maps those events to our own KRs. The `narrative` agent generates our weekly story from our own data. If the product can't make sense of our own work, the product isn't good enough yet.

**Honest verdicts beat confident wrong.** OKR-Mapper drops mappings with confidence < 0.5 in code (the prompt asks for calibration; the pipeline enforces a floor). Narrative will say "no work tied to this KR this period" when that's true — it won't manufacture a positive story.

**Cost discipline by default.** A daily LLM circuit breaker caps spend per UTC day. Dry-run is the dev default (you have to opt into spending money). Prompt caching is on for every system block — the strategy pod's $0.018-per-call drops to ~$0.005 on calls 2-4 thanks to cache reuse.

For more, read [TRACKER.md §7 Decision Log](TRACKER.md) — every non-trivial choice is captured there with rationale.

---

## Where to look for what

| You want to know... | Read this |
|---|---|
| What are the company's current OKRs? | `TRACKER.md` §2 |
| Which agents exist and what's their status? | `TRACKER.md` §4 or `python -m cli.status` |
| What did the strategy pod propose this week? | `proposals/<latest-date>/MONDAY_BRIEF.md` |
| What was today's status? | `reports/daily/<today>/OWNER_FINANCE_REPORT.md` |
| Why did we make decision X? | `TRACKER.md` §7 (Decision Log) |
| What's the budget plan? | `proposals/2026-04-29/cfo_budget_overview.md` |
| What's the architecture? | `CLAUDE.md` + `core/store.py` schema |
| How do I do day-to-day operator tasks? | `RUNBOOK.md` |
| Does the math actually work? | `python -m tests.test_signals_math` (9 tests, all green) |

---

## Status as of 2026-04-30

- **30/30 agents** live (KR4.1 ✅) — full org online, dry-run-tested
- **9 commits** on `main` (~200 files, ~30k LOC)
- **2 cloud routines** scheduled + **2 GitHub Actions workflows** ready (replace routines once secrets configured)
- **9/9 math tests** passing (`python -m tests.test_signals_math`)
- **10 KPIs** defined and tracked (`python -m cli.kpis` — 7 green, 1 red, 2 unknown at last run)
- **First real CEO proposal** generated for $0.017 — quality verified
- **Marketing landing page** built and build-verified (Next.js 15 + Tailwind, ready to deploy)
- **Notion KB foundation** complete — 9 docs including the customer-facing OKR/KPI framework and the pilot intake questionnaire
- **OKR Health Check generator** shipped — turns a customer's intake YAML into the lead-magnet brief
- **PostHog A/B testing** wired on the landing page (2 experiments: `hero_headline`, `hero_cta`) + reporting CLI
- **MVP product app:** not started · This is Sprint 0 engineering work
- **First design partner kickoff target:** 2026-05-19

See [`TRACKER.md`](TRACKER.md) for the full state, every decision with rationale, and the cycle OKRs + KPIs.

---

## Where to start reading

If you're new to this repo, read in this order:

1. [`TRACKER.md`](TRACKER.md) — single source of truth (OKRs, KPIs, decisions, risks, sprint log)
2. [`notion/02_product/01_how_it_works.md`](notion/02_product/01_how_it_works.md) — full product runbook
3. [`notion/02_product/03_team_and_workflow_diagrams.md`](notion/02_product/03_team_and_workflow_diagrams.md) — Mermaid diagrams of the org + data flow + tech stack
4. [`notion/03_playbooks/01_customer_okr_kpi_framework.md`](notion/03_playbooks/01_customer_okr_kpi_framework.md) — the wedge (what we sell)
5. [`RUNBOOK.md`](RUNBOOK.md) — daily/weekly operator tasks + troubleshooting
6. [`INSTRUCTIONS.md`](INSTRUCTIONS.md) — tonight's setup tasks (Gmail SMTP + GitHub Actions secrets)
