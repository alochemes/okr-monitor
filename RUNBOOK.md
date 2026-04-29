# OKR Monitor — Operator Runbook

The handbook for day-to-day operating. If you're new here, read [README.md](README.md) first; this file assumes you know what OKR Monitor is.

---

## Daily rhythm

| Time | What happens | What you do |
|---|---|---|
| **Throughout the day** | Work happens (commits, proposals, decisions). Each proposal becomes a `work_event`. | Just work. |
| **7pm Pacific** | Daily routine fires. CEO/CPO/CFO/analytics_ops generate the OWNER/FINANCE report. Email arrives (if SMTP configured) and `reports/daily/YYYY-MM-DD/OWNER_FINANCE_REPORT.md` is committed to GitHub. | Read the email. Skim the KPI dashboard at the top. Spend ≤5 min on the synopses. |
| **Sunday 6pm Pacific** | Sunday routine fires. Full strategy pod drafts proposals. OKR-Mapper sweeps the week's events. Narrative writes the weekly story. | Open the brief Monday morning. Walk the queue. |
| **Monday morning** | New brief in `proposals/<sunday-date>/MONDAY_BRIEF.md`. Pending agent proposals queued. | `python -m cli.review --all` — approve/edit/reject each proposal (~10 min). Update TRACKER.md §6 sprint log. |

---

## The five commands you'll use most

```bash
# 1. See where every KR stands right now (one-line per KR with verdict, events, days remaining)
python -m cli.status

# 2. Detail on a single KR (event-level evidence)
python -m cli.status --kr 1.3

# 3. Walk the queue of pending agent proposals
python -m cli.review --all

# 4. Run a single agent right now, REAL (costs ~$0.02)
OKR_MONITOR_DRY_RUN=false python scripts/run_ceo.py

# 5. Generate a daily report on demand (skip email send)
OKR_MONITOR_DRY_RUN=false python scripts/daily_evening.py --no-email
```

---

## Reviewing proposals (the operator queue)

When you run `python -m cli.review --all`, each pending proposal shows up in turn. For each you have:

| Choice | What it does | When to pick |
|---|---|---|
| **(a)pprove** | Records the proposal as accepted, edit_distance = 0. | Proposal is shippable as-written. |
| **(e)dit** | Opens the markdown in your editor; saves your version; records edit_distance. | Mostly right but you want to tweak. The edit_distance is a trust signal we use to decide future autonomy. |
| **(r)eject** | Records as rejected with optional reason. | Proposal is wrong — wrong KR, wrong direction, hallucinated facts. |
| **(d)efer** | Leaves it in the queue. | Need more info before deciding. |
| **(s)kip** | Move on, leave in queue. | Saving for a focused session. |
| **(q)uit** | Exit the review session. | |

The trust signal: if you're consistently editing CEO proposals heavily, that means the CEO agent isn't well-tuned for the current sprint context — worth a prompt revision. If you're approving 100% unedited for ≥10 consecutive proposals, that agent has earned credibility for higher autonomy.

---

## What's where (operator-facing files)

| File / dir | Purpose | Updated by |
|---|---|---|
| `TRACKER.md` | Single source of truth — OKRs, agents, decisions, risks. | You (manually) + agents (status flags) |
| `proposals/YYYY-MM-DD/` | Sunday strategy pod output + weekly narrative. | Sunday routine |
| `reports/daily/YYYY-MM-DD/OWNER_FINANCE_REPORT.md` | Daily 7pm OWNER/FINANCE brief. | Daily routine |
| `data/okr_monitor.db` | Local SQLite — proposals, events, mappings, signals. | Every agent run. **Gitignored** (cloud sandbox is ephemeral; markdown in `proposals/` and `reports/` is the durable record). |
| `data/audit/YYYY-MM-DD.jsonl` | Append-only audit log of every consequential decision. | `core/audit.emit()` from every agent. **Gitignored.** |
| `.env` | Local secrets (Anthropic API key, SMTP creds). **Gitignored.** | You |
| `.env.example` | Template — safe to commit, no secrets. | Committed |

---

## Daily report — what you're getting at 7pm

The email/file at `reports/daily/YYYY-MM-DD/OWNER_FINANCE_REPORT.md` has 5 sections:

1. **KPI Dashboard** — table of every KR with its verdict, 7d/30d/all-time event counts, days remaining, target, current, required pace per day. This is the "real-time scoreboard" — it's also what `python -m cli.status` shows.
2. **CEO synopsis** — what was accomplished today vs what the sprint plan implied should ship today. Names blockers and gives a one-liner verdict on the next milestone.
3. **CPO product roadmap report** — agent count, MVP completion estimate, features shipped this week, in-progress, blocked, next-2-week milestones, scope recommendation.
4. **CFO cost & token projection** — today's spend, 7d avg, 14d total, projected next 14 and 30 days, per-agent cost breakdown, circuit-breaker status, recommended action.
5. **Growth metrics** (analytics_ops) — pilot count, growth spend, CAC by channel, outreach activity, flagged issues. Pre-launch state for now (0 pilots).

If you want to see a sample, the file lands in `reports/daily/YYYY-MM-DD/` and is committed to the repo each day.

---

## When something breaks

### Symptom: agent run returns "Your credit balance is too low"

The funded API key in `.env` is being shadowed by a different `ANTHROPIC_API_KEY` in your shell environment (e.g., from your Max subscription auth).

**Check:**
```bash
python -c "import os; print('shell key prefix:', os.environ.get('ANTHROPIC_API_KEY','')[:16])"
```
If the printed prefix doesn't match the prefix in `.env`, something is shadowing it.

**Fix:** all our run scripts already pass `override=True` to `load_dotenv()`. So this should not happen anymore. If it does, check that the script is invoking the standard pattern (look at any `scripts/run_*.py` for reference).

### Symptom: "balance too low" but the .env key IS the funded one

The Anthropic workspace tied to that key has $0 even though you topped up another workspace. Check at `console.anthropic.com → Settings → Workspaces` — credits are workspace-scoped. Generate a new API key from the workspace that holds the credits.

### Symptom: daily LLM cost circuit breaker tripped

You've hit the daily cap ($50/day Sprint 0–1, $100/day Sprint 2+). The audit log will have an `*.circuit_breaker_open` event with severity `alert`. You can:
- Override for one run: `OKR_MONITOR_DAILY_LLM_CAP_USD=200 python scripts/run_X.py`
- Wait until midnight UTC for the cap to reset
- Investigate which agent ran away — `cli/budget.py` (when implemented) or query the DB:
  ```sql
  SELECT agent, SUM(cost_usd) FROM proposals WHERE created_at LIKE '2026-04-29%' GROUP BY agent;
  ```

### Symptom: a YAML config fails to parse

Unquoted colons inside list-string items break PyYAML — `"At risk": who calls...` is interpreted as a mapping. Fix: wrap the line in single quotes or rephrase to use an em-dash. (Three configs hit this in early scaffolding — see TRACKER.md §7 entry from 2026-04-29.)

### Symptom: cloud routine runs in dry-run mode

The remote sandbox doesn't have `ANTHROPIC_API_KEY` set. `daily_evening.py` and `sunday_evening.py` both auto-fall-back to dry-run with a clear banner in the report.

**Fix options:**
- (Easiest, when available) Inject the secret into the routine env via the routine config in `claude.ai/code/routines/<id>`.
- (Workaround) Move scheduling to GitHub Actions, which has first-class secret management. Action would call `python scripts/daily_evening.py` with the secret in env.

### Symptom: SMTP send fails

Default behavior: report still gets written to `reports/daily/YYYY-MM-DD/` even if email fails. Check the `email` field in the script output for the failure reason.

For Gmail SMTP: you need an **app password**, not your normal Google password. Generate one at `myaccount.google.com → Security → 2-Step Verification → App passwords`.

### Symptom: math test fails after a code change

```bash
python -m tests.test_signals_math
```
9 tests cover signals + forecasting math. If one fails, read the assertion message — the most likely causes:
- Window boundary changed in `signals_analyst._compute_for_kr`.
- Target parser regex broke in `forecasting._parse_numeric`.
- Verdict logic changed in `forecasting._verdict`.

---

## Operator commands cheat sheet

```bash
# DEV — DEFAULT (free)
python -m cli.status                           # KR scoreboard
python -m cli.status --kr 1.3                  # one-KR detail
python -m cli.review --list                    # list pending proposals
python -m cli.review                           # review oldest pending
python -m cli.review --all                     # walk every pending in order
python scripts/run_ceo.py                      # dry-run (cheap stub)
python scripts/sunday_evening.py               # dry-run full Sunday flow
python scripts/daily_evening.py --no-email     # dry-run full daily flow

# REAL ($)
OKR_MONITOR_DRY_RUN=false python scripts/run_ceo.py
OKR_MONITOR_DRY_RUN=false python scripts/run_strategy_pod.py
OKR_MONITOR_DRY_RUN=false python scripts/sunday_evening.py
OKR_MONITOR_DRY_RUN=false python scripts/daily_evening.py

# OVERRIDE CIRCUIT BREAKER (rare)
OKR_MONITOR_DAILY_LLM_CAP_USD=200 OKR_MONITOR_DRY_RUN=false python scripts/<x>.py

# TESTS (free, no API)
python -m tests.test_signals_math

# SETUP / DR
python scripts/init_db.py                      # idempotent — safe to re-run
```

---

## What's persistent vs ephemeral

| Lives forever (in git) | Ephemeral (gitignored, local only) |
|---|---|
| `TRACKER.md` (decisions, OKRs, agent roster) | `data/okr_monitor.db` (SQLite — proposals, events, mappings, signals) |
| `proposals/YYYY-MM-DD/*.md` (committed by Sunday routine) | `data/audit/*.jsonl` (per-day audit logs) |
| `reports/daily/YYYY-MM-DD/*.md` (committed by daily routine) | `.env` (secrets) |
| All code, prompts, configs | `__pycache__/`, `.venv/`, etc. |

**Implication:** if your laptop dies, you lose the SQLite DB and audit log but NOT the proposals or reports. The cloud sandbox runs every routine on a fresh DB — so the DB is genuinely throwaway. The markdown in git is the durable record.

If you want long-term audit retention, periodically back up `data/audit/*.jsonl` to S3 or a private gist.

---

## How to add a new agent (quick reference)

1. `mkdir agents/<name>` and create `__init__.py`, `pipeline.py`, `prompts/<kind>.md`.
2. In `pipeline.py`, use `agents._proposal.run_proposal()` for the standard pattern.
3. Create `config/<name>.yaml` with `model`, `max_tokens`, `temperature`, `cadence`, `output_kinds`.
4. Create `scripts/run_<name>.py` (copy any existing — they're 25 lines each).
5. Add a mock response in `core/llm._default_mock` for the new action key (so dry-run produces sensible JSON).
6. Update `TRACKER.md §4` — flip the status flag from 🔴 to 🟢.

Test in dry-run (free):
```bash
python scripts/run_<name>.py
```
Then test for real (~$0.02):
```bash
OKR_MONITOR_DRY_RUN=false python scripts/run_<name>.py
```

---

## Promotion gates (planned, not yet implemented)

The system is designed to support three stages of agent autonomy:

- **Stage 0** (current default) — Proposals only. Nothing acts on the world. Operator reviews via `cli/review.py`.
- **Stage 1** — Trusted proposals. Same as Stage 0 plus a "ship as drafted" affordance. Earned by sustained low edit-distance.
- **Stage 2** — Auto-execute scoped actions (e.g. drafting outbound emails for review, opening Linear tickets). Per-action env-var kill switches.

The promotion criteria, tripwires, and demotion logic live in the skinmap_agents repo as a reference implementation. We'll port it here when an agent is ready for Stage 1.

---

## When in doubt

- Read `TRACKER.md` §7 — every non-trivial decision is captured there with rationale.
- Read `CLAUDE.md` — project conventions for code changes.
- Run `python -m cli.status` — see the live state without opening a database.
