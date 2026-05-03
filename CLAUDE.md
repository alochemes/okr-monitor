# okr-monitor — Project Notes

> **Session start:** before doing anything else this session, read [`.claude/SESSION_RULES.md`](.claude/SESSION_RULES.md) and follow its session-start ritual exactly. If the user says "wrap up," follow [`.claude/END_OF_SESSION_PROMPT.md`](.claude/END_OF_SESSION_PROMPT.md). The rest of this file is the project's domain context.

---

This is the agent system for **OKR Monitor**, a B2B SaaS that connects company OKRs to the actual work happening in code, tickets, and conversations, and surfaces drift in real time.

The system is **operator-in-the-loop**, not autonomous. Each agent emits proposals; the operator (CEO) approves, edits, or rejects; the system measures the operator's edits and degrades agent autonomy when quality drifts. We are also our own first customer (dogfood) — the agents live inside the same product they help build.

## Operating bar

**IQ=160.** The operator expects every action to clear a high bar. Concretely, in this repo that means:
- Read the relevant files **before** proposing a change. Don't guess at APIs, schemas, or column names — open the file.
- When something fails, find the **root cause** before patching the symptom. The CI push race wasn't a flaky workflow; it was a missing rebase. The 535 SMTP error wasn't the From domain; it was wrong SMTP_USER vs the app password's owning account. State the diagnosis explicitly, then fix.
- For any non-trivial change, verify it ran: build the web app, render the daily report, run `tests/test_signals_math.py`, etc. "Should work" is not done.
- Don't add features the user didn't ask for. Don't refactor working code (the inline strategy-pod pipelines stay) unless there's a reason. Don't write defensive code for impossible states.
- Match scope. A bug fix doesn't need a sweeping reorganization. A one-line change doesn't need a new module.
- Ask when ambiguous, act when not. "Want me to also do X?" is fine after the requested work is done — not in place of it.

## Operating model

- The operator is `alochemes@gmail.com` (CEO). Single reviewer for now.
- Agents do not act on the world directly. They write **proposals** to a queue. The operator reviews via `cli/review.py`.
- Every consequential action is logged twice: a row in SQLite (`data/okr_monitor.db`) and a JSONL event under `data/audit/YYYY-MM-DD.jsonl`. Treat divergence as a bug.
- Cost discipline matters. Cheap models filter and summarize; expensive models judge and synthesize. Default workhorse is `claude-sonnet-4-6` with prompt caching pinned to the system block.

## Source of truth

- `TRACKER.md` is the canonical source for OKRs, agent roster, decisions, and risks. Agents read it via `core/tracker.py`. **If you change TRACKER.md, the next agent run sees the new state.**
- `config/company.yaml` is the OKR Monitor identity (mission, ICP, voice). Loaded into every agent's system prompt and cached.
- `config/<agent>.yaml` is per-agent configuration (model choice, output format, run cadence).

## Promotion gate (planned, not yet implemented)

Same posture as skinmap_agents:
- **Stage 0** — Proposals only. Default. Nothing acts on the world.
- **Stage 1** — Trusted proposals. Same as Stage 0 plus a "ship as proposed" affordance.
- **Stage 2** — Auto-execute scoped actions (e.g. drafting outbound emails for review, opening Linear tickets). Per-action env-var kill switches.

For Sprint 0 (Strategy pod), only Stage 0 exists. Proposals → review queue → CEO decides.

## Code conventions

- Python 3.11+. `sqlite3` from stdlib (no SQLAlchemy). `anthropic` SDK with prompt caching on stable system prompts.
- Modules small and single-purpose. Pipelines explicit (`pipeline.py`), never implicit.
- Side-effecting functions take a `dry_run: bool` parameter when relevant. Default to whatever the calling script passes — never default to `False` in a function signature for anything that mutates remote state or spends money.
- All LLM calls go through `core/llm.py` so token accounting and audit happen in one place. Do not call `anthropic.Anthropic()` directly elsewhere.
- All DB writes go through `core/store.py`. Do not embed SQL in agent code.
- All TRACKER.md reads go through `core/tracker.py`. Do not parse the markdown in agent code.

## Adding a new agent

1. Create `agents/<name>/` with at minimum a `pipeline.py` exporting `run()` and a `prompts/` directory.
2. Add per-agent config under `config/<name>.yaml`.
3. Add a script under `scripts/run_<name>.py` that wires CLI args to `agents.<name>.pipeline.run`.
4. Update `TRACKER.md` §4 — flip the agent's status flag.

## Files that are stubs (not yet built)

- The 26 non-Strategy agents (Product, Engineering, AI/Data, GTM, Customer/Ops). See TRACKER.md §4 for status.
- Source ingestion (GitHub, Linear, Jira, Slack, Notion). Comes online with Sprint 0 engineering work.
- The web app (Next.js + Supabase). The Python agent system here is the brain; the web app is the customer surface.
- Promotion gate code (`core/promotion.py`). Add when an agent first wants Stage 1 capability.
