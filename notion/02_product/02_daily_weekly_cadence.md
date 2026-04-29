# Daily / weekly cadence — what fires when

> The complete schedule of automated runs. If you ever want to know "why is this email in my inbox?" or "why did this commit appear from `github-actions[bot]`?" — the answer is here.

---

## At a glance

| Time (Pacific) | What fires | Where it runs | What lands |
|---|---|---|---|
| Mon–Fri **continuous** | Operator runs (interactive `cli/review.py`, `cli/status.py`, manual agent runs) | Local terminal | DB + audit log |
| Sun **6 PM** | Strategy pod + dogfood + weekly narrative | GitHub Actions (`.github/workflows/sunday.yml`) | `proposals/YYYY-MM-DD/` |
| Daily **7 PM** | OWNER/FINANCE report — CEO, CPO, CFO, analytics_ops + KPI dashboard | GitHub Actions (`.github/workflows/daily.yml`) | `reports/daily/YYYY-MM-DD/` + email |
| Daily TBD | OKR-Mapper sweep (when integrations land) | Cloud cron | `event_kr_mappings` rows |
| Hourly TBD | Signals-Analyst + Forecasting refresh | Cloud cron | `kr_signals` rows |

**All cron expressions are stated in UTC** to avoid DST drift. We document each in the workflow file; the comment block names the equivalent local time and the November DST update.

---

## Sunday 6 PM Pacific — strategy pod + dogfood + narrative

**Cron:** `0 1 * * 1` UTC (= Sunday 6 PM PDT during March–November; in PST after DST cutover, change to `0 2 * * 1`).

**Trigger:** GitHub Actions, `.github/workflows/sunday.yml`. Runnable manually from the Actions tab via `Run workflow`.

**Steps:**

1. Checkout repo, set up Python 3.11, install deps, init SQLite.
2. Run `scripts/sunday_evening.py`:
   - **Strategy pod** — CEO/CPO/CTO/CFO each emit one proposal:
     - CEO: `weekly_priorities` (top 3 priorities for the upcoming week)
     - CPO: `roadmap_review` (scope changes — defer / cut / add / reshape)
     - CTO: `architecture_review` (severity-ranked risks)
     - CFO: `pricing_model` (tier proposal with CAC math)
   - **Dogfood loop** — each new proposal becomes a `work_event` (idempotent on proposal_id). OKR-Mapper sweeps any unmapped events.
   - **Signals-Analyst + Forecasting** refresh per-KR counts and verdicts.
   - **Narrative** generates the weekly company brief.
3. Bot commits `proposals/YYYY-MM-DD/` (5 markdown files) and pushes to `main`.

**What you read Monday morning:** `proposals/<sunday-date>/MONDAY_BRIEF.md`. Then run `python -m cli.review --all` — ~10 min walking the queue.

**Cost per run:** ~$0.05 (4 strategy proposals at ~$0.012 each + a few mapper calls + the narrative).

---

## Daily 7 PM Pacific — OWNER/FINANCE report

**Cron:** `0 23 * * *` UTC (= 7 PM PDT during March–November; in PST after DST cutover, change to `0 0 * * *`).

**Trigger:** GitHub Actions, `.github/workflows/daily.yml`. Manual trigger available.

**Steps:**

1. Checkout, Python 3.11, install, init SQLite.
2. Run `scripts/daily_evening.py`:
   - Refresh `kr_signals` + forecast (no LLM cost).
   - Gather today's activity (events, mappings, proposals, spend).
   - Run four reporters in sequence:
     - **CEO `daily_status`** — what was accomplished today vs what the sprint plan implied; blockers; next-milestone verdict.
     - **CPO `product_roadmap_report`** — agent count, MVP completion estimate, shipped/in-progress/blocked, next-2-week milestones.
     - **CFO `cost_projection`** — today's spend, 7d avg, 14d total, projected next 14 and 30 days, per-agent cost breakdown, circuit-breaker status.
     - **analytics_ops `growth_metrics`** — pilots, CAC by channel, growth spend, outreach activity. Pre-launch: zeros.
   - Render the **KPI dashboard** as a markdown table at the top of the report.
   - Assemble the report body, write to `reports/daily/YYYY-MM-DD/OWNER_FINANCE_REPORT.md`.
   - Send via SMTP if configured (`SMTP_HOST` set in env), else file-only.
3. Bot commits `reports/daily/YYYY-MM-DD/` and pushes to `main`.

**What you receive:** an email at 7 PM with the full report (KPI dashboard + 4 sections + footer). Subject example: `OKR Monitor — Daily OWNER/FINANCE — 2026-04-29 · 17 KRs · 1 active · 6 stale · 10 qualitative`.

**Cost per run:** ~$0.07 (4 reporters at ~$0.018 each + signals/forecasting which are free).

---

## Continuous — operator-initiated

Run any of these locally on demand. **All default to dry-run** (free) — prepend `OKR_MONITOR_DRY_RUN=false` for real.

```bash
# Single agent (dry-run by default)
python scripts/run_<agent>.py

# Single agent for real (~$0.02)
OKR_MONITOR_DRY_RUN=false python scripts/run_<agent>.py

# Full strategy pod for real (~$0.05)
OKR_MONITOR_DRY_RUN=false python scripts/run_strategy_pod.py

# Operator review queue
python -m cli.review --all

# Live KR scoreboard
python -m cli.status
python -m cli.status --kr 1.3   # detail for one KR

# A/B experiment report (PostHog)
python scripts/run_ab_report.py
```

---

## When integrations land — additional cadences

These don't fire yet. They will once the integrations engineer ships the GitHub / Linear / Slack / Notion connectors.

| Source | Cadence | Mechanism |
|---|---|---|
| GitHub | webhook on push, PR, review | event-driven; each event hits `/api/ingest/github` |
| Linear / Jira | webhook on issue events | event-driven |
| Slack | event API for messages in opted-in channels | event-driven |
| Notion | polling — every 15 min for changes to OKR + project pages | scheduled job |
| OKR-Mapper sweep | every 30 min (sweep any unmapped events) | scheduled job |
| Signals-Analyst refresh | hourly (idempotent — no harm in over-frequency) | scheduled job |

Idempotency is enforced at the schema level: `UNIQUE(source, source_event_id)` on `work_events`. Webhook re-deliveries can't double-count.

---

## Failure modes & where they surface

| Symptom | What's wrong | Where to look |
|---|---|---|
| GitHub Actions workflow red | Likely missing or wrong `ANTHROPIC_API_KEY` secret, or daily cap tripped | Actions tab → run logs |
| Email never arrives but report committed | SMTP not configured, or wrong app password | `email` field in script JSON output (in workflow logs) |
| `cli.status` shows all KRs as "qualitative" | Target/current values in TRACKER.md aren't numeric | TRACKER.md §2 — fill in numeric targets |
| Daily LLM cap tripped | Too many real runs in one UTC day | Audit log: search for `circuit_breaker_open` |
| Sunday brief is dry-run stub | Cloud routine env doesn't have `ANTHROPIC_API_KEY` | Actions secret config |

Detailed troubleshooting: `RUNBOOK.md → When something breaks`.
