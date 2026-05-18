_(model output did not parse as JSON; raw below)_

```
```json
{
  "title": "Architecture review — SQLite + ephemeral sandbox will break at first real customer",
  "summary": "The combination of SQLite-on-local-disk and an ephemeral cloud sandbox means every Sunday run starts with a blank database, making all rolling-window KR signals meaningless the moment a real customer's data needs to persist. Three additional high-severity gaps — no webhook idempotency enforcement at the HTTP layer, no real OAuth integration code despite KR1.1 being 10 days past due, and Slack ingestion shipping without a DPA — compound into a product that cannot safely onboard even one design partner.",
  "risks": [
    {
      "area": "data",
      "severity": "high",
      "risk": "SQLite is the only store; the cloud sandbox is ephemeral, so every remote run (Sunday, daily) starts with a blank DB — all rolling 7d/30d signals and historical mappings are lost on each run, making KR signals permanently stale for any real customer account.",
      "mitigation": "Provision a Supabase Postgres instance (already in the Sprint 0 entry checklist), swap `core/store.py` connection string to `DATABASE_URL` env var, and migrate the three schema tables; SQLite stays for local dev only.",
      "effort": "2d"
    },
    {
      "area": "integrations",
      "severity": "high",
      "risk": "KR1.1 (MVP live) is 6 days past its 2026-05-12 deadline and zero integrations are live (0/5 in §3 Engineering KRs), meaning design partners cannot be onboarded even if discovery calls close — the entire pilot pipeline (KR1.2, KR2.1) is blocked.",
      "mitigation": "Scope-cut to one integration only (GitHub webhooks via Nango) for the first design partner; defer Linear/Jira/Slack/Notion to Sprint 1 — ship one working end-to-end data path over five half-working ones.",
      "effort": "2d"
    },
    {
      "area": "security",
      "severity": "high",
      "risk": "Slack ingestion is in scope (§7 decision log, §9 risk row) but the DPA template was due 2026-05-12 and is not marked complete — onboarding any pilot that connects Slack without a signed DPA is a GDPR/CCPA liability that could kill the first enterprise reference customer.",
      "mitigation": "Block Slack integration activation behind a feature flag that requires `dpa_signed=true` on the account row; ship a one-page DPA template (Bonterms or equivalent) this week — legal boilerplate, not custom drafting.",
      "effort": "1d"
    },
    {
      "area": "integrations",
      "severity": "high",
      "risk": "Webhook idempotency is enforced at the schema layer (UNIQUE source+source_event_id) but there is no HTTP-layer deduplication — a GitHub webhook retry during a slow DB write will hit the upsert twice within the same transaction window and may produce duplicate `event_kr_mappings` rows if the upsert is not truly atomic.",
      "mitigation": "Add a Redis or Postgres advisory lock (or a simple `INSERT OR IGNORE` + check-then-act pattern) around the upsert in `store.upsert_work_event`; add a test that fires the same payload twice concurrently and asserts exactly one mapping row.",
      "effort": "1d"
    },
    {
      "area": "cost",
      "severity": "high",
      "risk": "The OKR-Mapper runs `run_all_unmapped()` on every Sunday and daily pass — at 300 pilot accounts each with hundreds of events, a single daily run could map tens of thousands of events and blow the $100/day circuit breaker or generate a surprise Anthropic bill before the operator notices.",
      "mitigation": "Add a per-account daily mapping quota (e.g., max 200 events/account/day) in `core/limits.py` alongside the existing dollar cap; log skipped events to the audit trail so they are retried next cycle rather than silently dropped.",
      "effort": "1d"
    },
    {
      "area": "architecture",
      "severity": "med",
      "risk": "The p95 ingestion latency KR (≤2 min) has no queue — events go synchronously from webhook handler to OKR-Mapper LLM call, meaning a slow Anthropic response or rate-limit during a burst will cause webhook timeouts and GitHub/Linear will stop retrying after 3 failures.",
      "mitigation": "Add Inngest (already in the Sprint 0 entry checklist) as the async job queue between webhook receipt and OKR-Mapper invocation; the webhook handler returns 200 immediately and enqueues the mapping job.",
      "effort": "2d"
    },
    {
      "area": "observability",
      "severity": "med",
      "risk": "KPI K6 (GitHub Actions success rate) is 'n/a — just enabled' and there is no alerting on integration health beyond a stale-data >2h check that is itself listed as a future mitigation in §9 — a broken GitHub webhook will be discovered by a design partner, not by the team.",
      "mitigation": "Wire a Slack webhook (or email via the existing `core/mailer.py`) to the GitHub Actions failure notification; add a cron job that queries each connected account's last event timestamp and alerts if >2h with no events during business hours.",
      "effort": "1d"
    },
    {
      "area": "security",
      "severity": "med",
      "risk": "OAuth tokens for GitHub/Linear/Jira/Slack/Notion will be stored somewhere (Nango or direct) but there is no mention of token encryption at rest or rotation policy — a leaked DB backup exposes all customer source integrations.",
      "mitigation": "Confirm Nango encrypts tokens at rest (it does by default); if storing any tokens directly, use Supabase Vault or `pgcrypto`; add a SOC2-checklist item for token rotation policy (this is one of the 45 open SOC2 items in §3).",
      "effort": "1d"
    },
    {
      "area": "data",
      "severity": "med",
      "risk": "The `kr_signals.json` file written by `daily_evening.py` to `web/public/` is a flat file served statically — at 300 accounts this becomes 300 separate files or one file with all customer data mixed, both of which are wrong (data leakage or unscalable file management).",
      "mitigation": "Replace the static JSON file bridge with a Next.js API route that queries Supabase with the authenticated user's account_id; remove `web/public/kr_signals.json` from the architecture before the first external pilot is onboarded.",
      "effort": "2d"
    },
    {
      "area": "architecture",
      "severity": "low",
      "risk": "The `claude-sonnet-4-6` model string is hardcoded across all 30 agent configs — an Anthropic model deprecation or a better cost/quality tradeoff (e.g., Haiku for signals_analyst which does zero LLM work anyway) requires touching 30 files.",
      "mitigation": "Tech-debt: centralize model selection in `config/models.yaml` with per-agent overrides; do this before Sprint 2 when agent count and call volume make per-file changes risky.",
      "effort": "tech-debt"
    }
  ],
  "decisions_needed_from_operator": [
    "Is Nango the confirmed OAuth/integration platform, or are we building direct OAuth apps — this determines whether the GitHub integration can ship in 2 days or 2 weeks, and it is the single blocker on KR1.1 and every design partner onboarding?",
    "Given KR1.1 is 6 days past due and 0/5 integrations are live, should Sprint 1 goal be revised from 'design partner love' to 'one integration end-to-end + one design partner' to avoid committing to 5 partners on a product with no live data pipeline?"
  ],
  "confidence": 0.82,
  "reasoning": "The risks are derived directly from the gap between what §7 decisions describe
```