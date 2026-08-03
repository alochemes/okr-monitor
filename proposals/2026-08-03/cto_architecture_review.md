_(model output did not parse as JSON; raw below)_

```
```json
{
  "title": "Architecture review — SQLite + ephemeral cloud sandbox at 175-pilot inflection",
  "summary": "The single most dangerous architectural choice is SQLite in an ephemeral cloud sandbox as the production store at the point where 175 pilots are expected by 2026-08-09 — concurrent webhook writes will corrupt it and any sandbox restart silently wipes all ingestion history. The second critical gap is that five integrations are claimed as Engineering pod KRs with zero evidence of OAuth app registration, webhook endpoint existence, or idempotency testing against real provider retry behavior.",
  "risks": [
    {
      "area": "data",
      "severity": "high",
      "risk": "SQLite is the production store (§7 schema decisions, `core/store.py`) and the cloud sandbox DB is explicitly called ephemeral (§7 2026-04-29 Sunday routine decision) — at 175 pilots with concurrent GitHub/Linear/Jira/Slack/Notion webhooks, concurrent writes will hit SQLITE_BUSY or silent corruption, and any sandbox restart wipes all event history with no recovery path.",
      "mitigation": "Provision a Supabase Postgres instance (already in the Sprint 0 entry checklist, §6) and migrate `core/store.py` to use the Supabase connection string via env var; SQLite stays for local dev only. The schema is already FK-normalized so migration is a driver swap, not a redesign.",
      "effort": "2d"
    },
    {
      "area": "integrations",
      "severity": "high",
      "risk": "Engineering pod KR 'Integrations live (GitHub, Linear, Jira, Slack, Notion) — 0/5' is still at zero as of the last recorded state, yet KR1.4 (time-to-first-narrative ≤30 min) and KR1.1 (MVP live) both depend on at least one real integration — without a working inbound webhook there is no event data and the entire mapper→signals→narrative pipeline runs on dogfood-only stub data.",
      "mitigation": "Unblock GitHub integration first (highest ICP coverage, simplest OAuth scope): register the GitHub OAuth App, wire `POST /webhooks/github` to `store.upsert_work_event`, deploy to Vercel, and smoke-test with a real push event. This single integration unblocks KR1.3 eval on real data and KR1.4 timing.",
      "effort": "2d"
    },
    {
      "area": "integrations",
      "severity": "high",
      "risk": "Webhook idempotency is declared at the schema level (UNIQUE on source+source_event_id, §7 2026-04-29) but there is no evidence of a webhook signature verification layer — any unauthenticated POST to `/webhooks/github` or `/webhooks/slack` can inject arbitrary events into the mapper pipeline, poisoning KR signal counts and narratives for all accounts.",
      "mitigation": "Add HMAC-SHA256 signature verification middleware for each provider (GitHub uses `X-Hub-Signature-256`, Slack uses `X-Slack-Signature`) before the route handler; reject 401 on mismatch. This is a one-function-per-provider addition with no schema changes.",
      "effort": "1d"
    },
    {
      "area": "cost",
      "severity": "high",
      "risk": "At 175 pilots (2026-08-09 milestone), each account running the full mapper→narrative pipeline weekly means ~175 narrative LLM calls + up to 175×N mapper calls per week; the $50–$100/day circuit breaker (§7, `core/limits.py`) is calibrated for a single-account dogfood load and will trip daily, silently blocking all real customer pipelines without per-account cost isolation.",
      "mitigation": "Add a per-account daily LLM spend cap (e.g. $0.50/account/day) tracked in `kr_signals` or a new `account_spend` table, and raise the global cap to reflect the actual pilot fleet size; log per-account overages to the audit trail so the CFO cost_projection agent can surface them.",
      "effort": "2d"
    },
    {
      "area": "security",
      "severity": "high",
      "risk": "Slack ingestion privacy risk is listed as High in §9 with mitigation 'DPA template by 2026-05-12' — there is no evidence this shipped, and at 175 pilots ingesting Slack data without a signed DPA or documented channel-scope consent, a single customer complaint triggers GDPR/CCPA exposure that could end the company.",
      "mitigation": "Gate Slack integration activation behind a per-account consent flag in the DB and require a signed DPA (even a click-wrap version) before the Slack OAuth flow completes; default scope to public channels only as stated in §9.",
      "effort": "1d"
    },
    {
      "area": "architecture",
      "severity": "med",
      "risk": "The p95 ingestion latency KR (≤2 min) has no queue — events go directly from webhook handler to synchronous mapper LLM call, meaning a slow Anthropic response or rate-limit during a burst (e.g. a large GitHub push with 50 commits) blocks the HTTP response and causes webhook provider retries, which the idempotency layer will correctly deduplicate but the latency KR will silently fail.",
      "mitigation": "Decouple webhook receipt from mapper execution: webhook handler writes the raw event to `work_events` and returns 200 immediately; a background worker (Inngest is already in the Sprint 0 checklist, §6) picks up unmapped events and calls the mapper async. This also makes the p95 measurement meaningful.",
      "effort": "2d"
    },
    {
      "area": "observability",
      "severity": "med",
      "risk": "KPI K6 (GitHub Actions workflow success rate ≥95%) is the only pipeline health signal, but it covers only the Sunday/daily scheduled runs — there is no alerting on webhook delivery failures, mapper confidence degradation over time, or stale-data per integration (§9 mentions a per-source health check as a mitigation but it is not in any KR or shipped artifact).",
      "mitigation": "Add a `source_health` table with last-event-received timestamp per (account, source); the existing `daily_evening.py` already runs signals_analyst — extend it to emit a stale-source alert (>2h since last event for an active account) to the audit log and surface it in the OWNER/FINANCE report.",
      "effort": "1d"
    },
    {
      "area": "security",
      "severity": "med",
      "risk": "OAuth tokens for GitHub/Linear/Jira/Slack/Notion are stored somewhere (Nango or direct, per §6 checklist) but there is no mention of token encryption at rest or rotation handling — a DB dump or repo secret leak exposes all customer OAuth tokens permanently.",
      "mitigation": "If using Nango, confirm it handles token encryption (it does by default); if storing tokens directly in Supabase, enable column-level encryption via pgcrypto for the tokens table before any real customer connects an integration.",
      "effort": "1d"
    },
    {
      "area": "architecture",
      "severity": "med",
      "risk": "The OKR-Mapper eval set is 50 labeled events (§6 Day 5) against a KR1.3 target of 200 events by 2026-05-12 — as of the last recorded state the grow-out to 200 is described as 'just adding entries' but there is no evidence it completed, meaning the ≥85% precision claim has never been validated on a representative set and could be masking systematic failures on specific KR classes.",
      "mitigation": "Run `python -m tests.eval.run_eval` with `OKR_MONITOR_DRY_RUN=false` against the current dataset and publish the REPORT.md precision/recall numbers in the next TRACKER.md update; if the dataset is still <200 events, treat KR1.3 as red until it is.",
      "effort": "1d"
    },
    {
      "area": "data",
      "severity": "low",
      "risk": "The `kr_signals.json` file written by `daily_evening.py` to `
```