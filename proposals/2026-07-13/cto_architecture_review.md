_(model output did not parse as JSON; raw below)_

```
```json
{
  "title": "Architecture review — SQLite + Vercel + single-vendor LLM at 75-pilot inflection",
  "summary": "SQLite as the production store and a single Anthropic dependency are the two choices most likely to compound into pain between now and 300 pilots; both are deferrable but need a dated decision, not silence. The webhook idempotency design is sound, but the health-check and audit-trail gaps in the live integration layer are unmitigated High risks with no Engineering KR owner.",
  "risks": [
    {
      "area": "data",
      "severity": "high",
      "risk": "SQLite is the production store (implied by `core/store.py` and the ephemeral-DB note in §7); concurrent webhook writes from 5+ integrations at 75+ pilots will produce SQLITE_BUSY errors and silent event drops under any non-trivial write rate.",
      "mitigation": "Add a Supabase (Postgres) connection string to `.env` and swap `store.py` to use `psycopg2` with a connection pool of 5; SQLite stays as the test DB. The schema is already FK-clean — migration is a 1-day mechanical port, not a redesign.",
      "effort": "2d"
    },
    {
      "area": "architecture",
      "severity": "high",
      "risk": "The Engineering pod KR 'p95 ingestion latency ≤2 min' has no queue choice recorded anywhere in §7 or §3; without a durable queue, a slow or crashing integration handler blocks the entire ingestion path and the KR is unmeasurable.",
      "mitigation": "Adopt Inngest (already listed in Sprint 0 entry checklist) as the durable queue for all webhook handlers: each incoming event enqueues a job, the job calls `store.upsert_work_event` + `okr_mapper.run`. Instrument p95 via Inngest's built-in run-duration metrics. This is the queue choice that was deferred — make it now.",
      "effort": "2d"
    },
    {
      "area": "integrations",
      "severity": "high",
      "risk": "§9 flags integration breakage (GitHub/Slack OAuth scope changes) as Med with 'per-source health check + pager on stale-data >2h' as the mitigation, but no Engineering KR owns this and no implementation exists; at 75 pilots a silent stale-data window goes undetected for days.",
      "mitigation": "Add a `last_event_at` column per `(account_id, source)` to `kr_signals`; the daily evening script alerts (email via `core/mailer.py`) if any active account's source has `last_event_at > 2h`. This is a 4-hour addition to `scripts/daily_evening.py` — no new infrastructure.",
      "effort": "1d"
    },
    {
      "area": "security",
      "severity": "high",
      "risk": "Slack ingestion privacy risk (§9) has 'DPA template by 2026-05-12' as the mitigation; today is 2026-07-13 — if this shipped without a DPA and pilots are ingesting Slack data, every pilot account is a GDPR/CCPA liability with no contractual cover.",
      "mitigation": "Confirm DPA status immediately: if not signed with any pilot, gate Slack ingestion behind an explicit per-account opt-in flag in the DB (`slack_ingestion_enabled BOOLEAN DEFAULT FALSE`) and do not flip it until a DPA is countersigned. One day to add the flag and the gate; DPA template is a legal task, not engineering.",
      "effort": "1d"
    },
    {
      "area": "cost",
      "severity": "high",
      "risk": "LLM cost scales with account count: at 300 pilots, the `narrative` agent runs weekly per account; if average context is 4K tokens and Sonnet pricing holds, that is ~$0.30/account/week = $90/week in narrative alone, before OKR-Mapper sweeps — the $50/day circuit breaker will trip every Friday.",
      "mitigation": "Add a per-account token budget cap in `core/limits.py` (default 8K tokens/account/week across all agents); raise the Friday circuit-breaker ceiling to $200 with operator approval, or switch narrative to Haiku for accounts with <10 active KRs. Decide which before onboarding pilot 50.",
      "effort": "1d"
    },
    {
      "area": "architecture",
      "severity": "med",
      "risk": "The `ANTHROPIC_API_KEY` secret-injection problem for the remote Sunday routine (§9) was marked 'V2: move to GitHub Actions' in May; the GitHub Actions sunday.yml workflow exists but it is unclear whether the secret is actually injected — if not, every Sunday brief for the past 10 weeks has been a dry-run stub.",
      "mitigation": "Verify `ANTHROPIC_API_KEY` is set as a GitHub Actions repo secret (`Settings → Secrets → Actions`) and that `sunday.yml` references it via `env: ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}`; add a post-run assertion that `OKR_MONITOR_DRY_RUN` was false in the workflow log.",
      "effort": "1d"
    },
    {
      "area": "observability",
      "severity": "med",
      "risk": "The SOC2-readiness KR claims 0/45 checklist items closed as of the last update; at 75 pilots, enterprise buyers will ask for a security posture doc and the answer is currently 'we have an audit log and a circuit breaker' — not enough to unblock a procurement.",
      "mitigation": "Tech-debt: assign the security agent (`agents/security/`) to produce a gap analysis against the 45-item checklist as its next proposal; operator reviews and picks the 10 items closeable in <1 week (encryption at rest, secret rotation, access logging). Do not block pilots on full SOC2 — block enterprise tier only.",
      "effort": "tech-debt"
    },
    {
      "area": "data",
      "severity": "med",
      "risk": "No data-residency decision exists in §7; Series A–C SaaS buyers in the EU will ask where their OKR and work-event data lives, and 'Vercel + SQLite on a cloud sandbox' is not an answer that survives a security review.",
      "mitigation": "Add a one-row decision to §7: 'US-only data residency for pilot phase; EU residency deferred to GA.' Surface this in the pilot intake questionnaire (§ pilot intake) so EU-headquartered prospects self-select out during pilots, not during procurement.",
      "effort": "1d"
    },
    {
      "area": "integrations",
      "severity": "med",
      "risk": "Webhook idempotency is correctly handled at the schema level (`UNIQUE(source, source_event_id)`) per §7, but there is no test covering the race condition where two webhook deliveries for the same event arrive within milliseconds and both pass the SELECT-before-INSERT check before either commits.",
      "mitigation": "Replace the SELECT-before-INSERT pattern with an `INSERT OR IGNORE` (SQLite) or `INSERT ... ON CONFLICT DO NOTHING` (Postgres) in `store.upsert_work_event`; add one test in `test_signals_math.py` that calls upsert twice with the same `source_event_id` and asserts exactly one row.",
      "effort": "1d"
    },
    {
      "area": "cost",
      "severity": "low",
      "risk": "Pricing is still unresolved (§9 flags it as Med, due 2026-05-19); today is 2026-07-13 and 'pilot → paid intent ≥25%' (KR2.3) is unmeasurable without a price — pilots converting to 'intent' with no number attached is a vanity metric.",
      "mitigation": "Tech-debt: operator must lock a price before pilot 76 (the M2 milestone); the CFO agent's next `cost_projection` proposal should include a pricing recommendation as a required output field. This is a business decision, not an engineering one — flag it here because KR
```