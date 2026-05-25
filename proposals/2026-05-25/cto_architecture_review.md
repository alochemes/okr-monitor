_(model output did not parse as JSON; raw below)_

```
```json
{
  "title": "Architecture review — SQLite + ephemeral cloud sandbox will break at 10 pilots",
  "summary": "The SQLite-in-ephemeral-sandbox architecture (§7, 2026-04-29 Sunday routine decision) means every cloud run starts with a blank database, so all historical signals, mappings, and narratives are lost between runs — the product's core value (drift detection over time) cannot function. Separately, zero integration code exists 13 days before the MVP deadline (KR Engineering: '0/5 integrations live'), making KR1.4 (≤30 min time-to-first-narrative) physically unreachable.",
  "risks": [
    {
      "area": "data",
      "severity": "high",
      "risk": "SQLite DB is ephemeral in the cloud sandbox (explicitly noted in §7 2026-04-29 Sunday routine decision); every scheduled run starts blank, so rolling 7d/30d signals and narrative history are permanently lost — drift detection is impossible without persistence.",
      "mitigation": "Provision a Supabase Postgres instance (already in Sprint 0 entry checklist §6) and replace all `store.py` SQLite calls with a Postgres connection string via `DATABASE_URL` env var; SQLite stays for local dev only.",
      "effort": "2d"
    },
    {
      "area": "integrations",
      "severity": "high",
      "risk": "Engineering pod KR shows 0/5 integrations live with MVP deadline 2026-05-12 (already passed) and design-partner onboarding at 2026-05-19; without at least GitHub ingestion, `work_events` table contains only agent proposals, making the OKR-Mapper eval (KR1.3) and narrative (KR4.2) run on synthetic data only.",
      "mitigation": "Scope GitHub webhook integration to a single event type (push + PR merge) with the idempotency key already designed (`UNIQUE(source, source_event_id)` per §7); wire it to `store.upsert_work_event` — this is the minimum to unblock real eval data.",
      "effort": "2d"
    },
    {
      "area": "integrations",
      "severity": "high",
      "risk": "OAuth tokens for GitHub/Linear/Jira/Slack/Notion are not stored anywhere in the described architecture; when a token expires or is revoked, ingestion silently stops with no alert, violating the §9 'stale-data >2h' mitigation that is listed but not implemented.",
      "mitigation": "Add a `integration_credentials` table (account_id, source, encrypted_token, expires_at, last_successful_ingest_at) and a daily health-check job that alerts via the existing audit log if `last_successful_ingest_at` is >2h stale for any active account.",
      "effort": "1d"
    },
    {
      "area": "security",
      "severity": "high",
      "risk": "The §9 Slack privacy risk ('are we comfortable Slack-ingesting customer conversations') has a mitigation of 'DPA template by 2026-05-12' — that date has passed with no evidence of delivery, and design partners are being onboarded now; ingesting Slack without a signed DPA is a GDPR/CCPA liability.",
      "mitigation": "Block Slack integration activation for any account until a DPA checkbox is confirmed in the onboarding flow; ship a one-page DPA using a standard template (Bonterms or equivalent) — legal review is not required to ship a template, only to sign a custom one.",
      "effort": "1d"
    },
    {
      "area": "architecture",
      "severity": "high",
      "risk": "The `kr_signals.json` file written by `daily_evening.py` to `web/public/` is the only data bridge between the Python backend and the Next.js dashboard; at multiple concurrent accounts this becomes a single shared file with no per-account isolation, exposing every customer's KR data to every other customer.",
      "mitigation": "Replace the static JSON file with a Supabase RLS-protected API route (`/api/kr-signals?account_id=X`) before the first external design partner is onboarded — this is a pre-condition for multi-tenancy, not an optimization.",
      "effort": "2d"
    },
    {
      "area": "cost",
      "severity": "med",
      "risk": "The narrative agent sends the full window of `event_kr_mappings` as context; at 300 pilots each with 7 days of GitHub + Linear events, a single narrative run could easily exceed 100K tokens per account, making the $100/day circuit breaker trip on the first busy Friday batch.",
      "mitigation": "Cap the narrative agent's input to the top-N events per KR by confidence score (N=10 is sufficient for signal); add a per-account token estimate log line so cost per account is visible before the batch scales.",
      "effort": "1d"
    },
    {
      "area": "data",
      "severity": "med",
      "risk": "The OKR-Mapper eval set has 50 labeled events (§6 Day 5) against a KR1.3 target of 200 events by 2026-05-05 (already missed); precision/recall numbers from 50 events have wide confidence intervals and will not reliably predict production behavior, especially for the 10 negative examples.",
      "mitigation": "Grow the eval set to 200 events before any design partner sees a narrative — this is pure data-labeling work with no code changes required; the framework is already wired (`tests/eval/dataset.py`).",
      "effort": "2d"
    },
    {
      "area": "observability",
      "severity": "med",
      "risk": "The audit log (`core/audit.py`) writes to stderr and a local DB; in the cloud sandbox there is no persistent log aggregation, so circuit-breaker trips, failed LLM calls, and ingestion errors are invisible after the sandbox session ends.",
      "mitigation": "Add a one-line Supabase insert to `core/audit.py` for every audit event (same Postgres instance as the main DB); this gives a persistent, queryable audit trail and satisfies the SOC2-readiness checklist item for audit logging (Engineering pod KR: 0/45 items closed).",
      "effort": "1d"
    },
    {
      "area": "architecture",
      "severity": "med",
      "risk": "The p95 ingestion latency KR (≤2 min) has no queue — events go directly from webhook to `store.upsert_work_event` to OKR-Mapper LLM call in a synchronous chain; a slow Anthropic response or rate-limit holds the webhook open and will cause GitHub/Linear to retry, creating duplicate processing despite the idempotency key.",
      "mitigation": "Add Inngest (already in the Sprint 0 entry checklist) as the async queue between webhook receipt and OKR-Mapper invocation; webhook handler returns 200 immediately, Inngest retries with backoff, idempotency key prevents double-mapping.",
      "effort": "2d"
    },
    {
      "area": "security",
      "severity": "low",
      "risk": "The `ANTHROPIC_API_KEY` secret injection for GitHub Actions is listed as unresolved in §9 ('no obvious secret-injection mechanism'); if the Sunday workflow runs without the secret it silently falls back to dry-run, which means the operator may believe real narratives are being generated when they are not.",
      "mitigation": "Add the key as a GitHub Actions repository secret (`ANTHROPIC_API_KEY`) and assert `OKR_MONITOR_DRY_RUN=false` explicitly in the workflow YAML; the existing banner on MONDAY_BRIEF.md is a good fallback but the secret should be wired now that the repo exists.",
      "effort": "1d"
    }
  ],
  "decisions_needed_from_operator": [
    "Is Supabase Postgres the confirmed persistence layer for production (it's in the Sprint 0 checklist but never confirmed as decided), or is there a different hosted DB choice — this decision blocks the ephemeral-DB fix, the multi-tenancy fix, and the persistent audit log simultaneously?",
    "Will design partners be onboarded before a signed DPA and per-
```