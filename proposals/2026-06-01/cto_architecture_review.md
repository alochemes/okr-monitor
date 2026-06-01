_(model output did not parse as JSON; raw below)_

```
```json
{
  "title": "Architecture review — SQLite + ephemeral cloud sandbox will break at 10 pilots",
  "summary": "The SQLite-in-ephemeral-sandbox architecture (§7: Sunday routine DB is ephemeral) means every cloud run starts with a blank database, making all rolling signal windows, verdict history, and narrative continuity fiction at the moment the first real pilot lands. The second critical gap is that zero integration code exists (Engineering pod KR: '0/5 integrations live') with MVP due 2026-05-12 — already 20 days past due — and no queue, no webhook receiver, and no idempotency layer beyond the schema UNIQUE constraint.",
  "risks": [
    {
      "area": "data",
      "severity": "high",
      "risk": "SQLite DB is ephemeral in the cloud sandbox (§7 2026-04-29 Sunday routine decision explicitly states 'SQLite DB in the cloud sandbox is ephemeral'), so every GitHub Actions run starts with a blank DB — all 7d/30d rolling windows, verdict history, and narrative continuity are zeroed on every run.",
      "mitigation": "Replace SQLite with a persistent Supabase Postgres connection (already chosen per §6 Sprint 0 entry checklist) using the same schema; `store.py` needs only the connection string swapped and `UNIQUE` constraints preserved — one day of work.",
      "effort": "1d"
    },
    {
      "area": "integrations",
      "severity": "high",
      "risk": "Zero of 5 integrations are live (§3 Engineering KR: '0/5') and MVP was due 2026-05-12 — no webhook receiver, no OAuth flow, no real work_events from GitHub/Linear/Jira/Slack/Notion, meaning the entire signal pipeline runs on dogfood agent proposals only.",
      "mitigation": "Scope the first integration (GitHub webhooks only: push + PR events) to a single Vercel API route with HMAC signature verification and upsert into `work_events` via the existing idempotent schema — this is a 2-day spike that unblocks KR1.3 eval with real data.",
      "effort": "2d"
    },
    {
      "area": "integrations",
      "severity": "high",
      "risk": "Webhook idempotency relies solely on the DB UNIQUE constraint (§7 2026-04-29), but if the upsert path raises an exception after partial writes or if the constraint is on `(source, source_event_id)` only, a retry with a different source_event_id (GitHub re-delivery assigns a new delivery ID) will insert a duplicate event and double-count signals.",
      "mitigation": "Add a `raw_payload_hash` column to `work_events` with a second UNIQUE constraint; hash the full webhook body before any parsing so re-deliveries with new delivery IDs are still deduplicated — 1 day.",
      "effort": "1d"
    },
    {
      "area": "cost",
      "severity": "high",
      "risk": "LLM cost at 300 pilots is unmodeled: the narrative agent runs per-account per-week, and at 300 pilots each with potentially hundreds of mapped events in the context window, a single weekly run could exceed the $100/day circuit breaker and silently skip narratives for all accounts after the cap trips.",
      "mitigation": "Add a per-account token budget cap in `narrative/run.py` (truncate event list to the 50 highest-confidence mappings per KR before building the prompt) and make the circuit breaker per-account-per-day rather than global — tech-debt entry now, implement before 50 pilots.",
      "effort": "tech-debt"
    },
    {
      "area": "security",
      "severity": "high",
      "risk": "Slack ingestion privacy risk is listed as High in §9 with mitigation 'DPA template by 2026-05-12' — that date has passed with no evidence of completion, and without a DPA any pilot using Slack ingestion exposes OKR Monitor to GDPR/CCPA liability the moment a EU or California-based pilot signs up.",
      "mitigation": "Block Slack integration from going live until a one-page DPA (data processor agreement) is drafted and countersigned; use a standard SaaS DPA template (Bonterms or equivalent) — 1 day to adapt, operator signs off before any Slack OAuth is enabled.",
      "effort": "1d"
    },
    {
      "area": "security",
      "severity": "med",
      "risk": "OAuth tokens for GitHub/Linear/Jira/Slack/Notion will be stored somewhere (Supabase or env), but there is no decision in §7 about token storage, rotation, or encryption at rest — at 300 pilots this is 300 sets of OAuth credentials with broad repo/workspace read scopes.",
      "mitigation": "Store OAuth tokens encrypted at rest in Supabase using Supabase Vault (built-in, no extra cost) and never log token values in the audit trail — 1 day to wire Vault for the first integration, pattern reused for all subsequent ones.",
      "effort": "1d"
    },
    {
      "area": "architecture",
      "severity": "med",
      "risk": "The `kr_signals.json` file written to `web/public/` by `daily_evening.py` (§6 Day 5) is a single flat file serving all accounts — this works for one dogfood account but will either expose cross-account data or require a separate file per account with no access control at the static-file layer.",
      "mitigation": "Move the dashboard data endpoint from a static JSON file to a Supabase RLS-protected API route (`/api/signals?account_id=`) before the first external pilot is onboarded — tech-debt entry, must be resolved before KR1.2 (design partners) goes live.",
      "effort": "tech-debt"
    },
    {
      "area": "observability",
      "severity": "med",
      "risk": "The only signal that ingestion is working is KPI K6 (GitHub Actions success rate ≥95%) — there is no per-integration staleness alert beyond the §9 mitigation 'pager on stale-data >2h', which has no implementation path described and no owner in the Engineering pod KRs.",
      "mitigation": "Add a `last_event_received_at` column per `(account_id, source)` in a `integration_health` table and a daily check in `daily_evening.py` that emits an audit alert if any active integration has been silent for >4h — 1 day, reuses existing `core/audit.py`.",
      "effort": "1d"
    },
    {
      "area": "architecture",
      "severity": "med",
      "risk": "The p95 ingestion latency KR (≤2 min, §3 Engineering pod) has no queue — webhooks hit a Vercel serverless function that writes synchronously to Supabase; under burst load (a large Linear workspace closing 50 tickets at once) Vercel's 10s function timeout will drop events silently.",
      "mitigation": "Add an Inngest event queue (already in the Sprint 0 entry checklist: 'Inngest projects created') between the webhook receiver and the DB write — the receiver enqueues in <100ms, Inngest retries on failure; this is the intended architecture and just needs to be wired.",
      "effort": "2d"
    },
    {
      "area": "data",
      "severity": "low",
      "risk": "The OKR-Mapper confidence floor of 0.5 (§7) is a hardcoded constant with no per-KR calibration — a KR with sparse events (e.g., KR2.5 CAC payback) will have systematically lower confidence scores and may produce zero mappings, making it permanently 'stale' in the forecast even when real work is happening.",
      "mitigation": "Tech-debt: after the 200-event eval set is complete (KR1.3), compute per-KR confidence distributions and consider per-KR floor thresholds; for now, log the drop rate per KR in the eval report so the operator can see which KRs are being systematically filtered.",
      "effort": "tech-debt"
    }
  ],
  "decisions_needed_from_
```