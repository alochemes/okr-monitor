# Roadmap pressure test — MVP deadline 2026-05-12, one day out

The MVP deadline is tomorrow and zero integrations are live, auth is unwired, and Vercel is undeployed — defer everything that isn't GitHub ingestion + Supabase auth + Vercel deploy or the KR1.4 30-minute onboarding path will never be testable. The OKR-Mapper eval set is at 50 events against a 200-event target; defer the 200-event milestone rather than let it crowd out the integration work.

## Proposed scope changes
- **DEFER** — OKR-Mapper eval set grow-out from 50 to 200 labeled events  
  → `Sprint 1` · KR impact: `1.3`  
  _Why:_ The eval framework is done and 50 events exist; the 200-event target (KR1.3, due 2026-05-12) cannot be hit without crowding out the GitHub integration that is the only way to generate real precision numbers. Deferring the count to Sprint 1 still lets the first live-LLM precision run happen on 50 events, which is enough signal to unblock KR1.3 directionally.
- **RESHAPE** — Sprint 0 integration scope: ship GitHub only, not all five (GitHub + Linear + Jira + Slack + Notion)  
  → `Sprint 1` · KR impact: `1.1, 1.4`  
  _Why:_ KR1.1 (MVP live by 2026-05-12) and KR1.4 (time-to-first-narrative ≤30 min) require exactly one working data source to demonstrate the magic moment; GitHub is the highest-signal source for the ICP and the one most design partners will have. Shipping all five integrations in one day is a High-severity execution risk (§9 integration breakage risk) and will produce five half-working connectors instead of one solid one.
- **DEFER** — Supabase magic-link auth wiring (login/page.tsx currently a stub)  
  → `Sprint 1` · KR impact: `1.1, 1.4`  
  _Why:_ For the first design-partner demo the operator can bypass auth with a direct /app/dashboard route; wiring Supabase OAuth is a half-day task that risks breaking the build on deadline day. KR1.4 measures time-to-first-narrative, not time-to-login — defer auth hardening until Sprint 1 when design partners need real accounts.
- **DEFER** — SOC2-readiness checklist (0/45 items, Engineering pod KR)  
  → `Sprint 2` · KR impact: `1.1`  
  _Why:_ No design partner at the Series A–C ICP stage will block a free pilot on SOC2 in week one; starting this 45-item checklist now pulls the security agent's attention away from the DPA template (§9 Slack-privacy High risk) which is the only compliance artifact that actually gates pilot onboarding. The DPA should be the only security deliverable in Sprint 1.
- **ADD** — Hardcoded demo-data fallback in /app/dashboard for design-partner first session  
  → `n/a` · KR impact: `1.4`  
  _Why:_ KR1.4 (time-to-first-narrative ≤30 min, p90) is at severe risk if a design partner's GitHub OAuth fails or their OKR source isn't ingested in time; a static but realistic demo dataset baked into the dashboard as a fallback ensures the narrative moment lands in the first 30 minutes regardless of integration state. This is a forced move: without it, KR1.4 is untestable at the 2026-05-19 design-partner deadline.

## Risks if unchanged
- Attempting all five integrations in one day produces five broken connectors; KR1.1 ships as a non-functional MVP and KR1.4 is unmeasurable at the 2026-05-19 design-partner onboarding.
- Without a demo-data fallback, any OAuth or ingestion failure during a design-partner session kills the KR1.4 magic moment and poisons NPS before KR1.5 is even measured.
- Pursuing the 200-event eval target on deadline day delays the first live-LLM OKR-Mapper run, meaning KR1.3 precision is still 'n/a' when design partners arrive — the core IP is unvalidated at pilot launch.

## Decisions needed from operator
- [ ] Will you accept a scoped MVP (GitHub-only integration, auth bypassed for demo) as the KR1.1 'live on Vercel' milestone, or does the definition of done require all five integrations and working auth before you consider it shipped?
- [ ] Should the DPA template (§9 Slack-privacy High risk) be treated as a hard gate before any design partner is onboarded, or can it be delivered in parallel during Sprint 1 while the first 1–2 partners use GitHub-only ingestion with no Slack access?

_Confidence: 0.62_
_Reasoning: The tracker's sprint log is detailed enough to confirm what is and isn't built (integrations = 0/5, auth = stub, Vercel = undeployed, eval = 50/200); the critical-path gaps are unambiguous. Confidence is capped at 0.62 because there is no design-partner feedback in the tracker (§8 pipeline is empty), so the relative weight of KR1.4 demo polish versus KR1.3 precision as the actual conversion driver is unknown — the 'add demo-data fallback' recommendation is a forced move under uncertainty, not a validated insight._