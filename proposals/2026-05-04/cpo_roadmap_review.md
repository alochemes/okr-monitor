# Roadmap pressure test — 8 days to MVP, critical path exposed

The MVP deadline (2026-05-12) is 8 days away and zero integrations are live, auth is unwired, and Vercel is undeployed — these three gaps block KR1.4 entirely and should consume all remaining Sprint 0 capacity. Defer the 200-event eval set grow-out and all GTM kit refinement to Sprint 1 to protect the critical path.

## Proposed scope changes
- **DEFER** — Grow eval set from 50 to 200 labeled events (KR1.3 Sprint 0 milestone, §5 2026-05-05)  
  → `Sprint 1` · KR impact: `1.3`  
  _Why:_ The eval framework is done and 50 events are labeled; precision is blocked on live LLM, not on event count. Spending 2–3 days growing to 200 before a single integration is live means measuring a system that has no real input data — defer the grow-out until GitHub ingestion produces real events to validate against.
- **DEFER** — Supabase auth wiring and magic-link login (web/app/app/login/page.tsx)  
  → `Sprint 1` · KR impact: `1.4`  
  _Why:_ Design partners in the first 30-minute demo session can be walked through the dashboard by the founder on a shared screen — auth is not required to demonstrate KR1.4 time-to-first-narrative. Wiring Supabase auth before the first integration is live inverts the priority; defer until at least one data source is flowing.
- **RESHAPE** — Integration scope for Sprint 0: ship exactly ONE integration (GitHub) end-to-end; defer Linear/Jira/Slack/Notion  
  → `Sprint 1` · KR impact: `1.3, 1.4`  
  _Why:_ The §7 decision log already deferred Salesforce/Gong, but the Engineering pod KR still lists 5 integrations for Sprint 0. One live integration producing real work_events is sufficient to hit KR1.3 (mapper precision on real data) and demonstrate KR1.4 to design partners; shipping 5 half-baked integrations is the highest-probability way to miss the 2026-05-12 deadline entirely.
- **DEFER** — DPA template and Slack privacy review (§9 High risk, 2026-05-12 target)  
  → `Sprint 1` · KR impact: `1.2`  
  _Why:_ Slack is now deferred to Sprint 1, so the DPA is not blocking any Sprint 0 design-partner onboarding; the risk remains real but the deadline pressure is self-imposed. Deferring to Sprint 1 (before any Slack data is ingested) preserves the mitigation without consuming Sprint 0 engineering days.
- **ADD** — Vercel deploy + environment variable wiring as an explicit Sprint 0 exit gate (currently implicit, not listed as a tracked task)  
  → `n/a` · KR impact: `1.1, 1.4`  
  _Why:_ KR1.1 requires 'live on Vercel' by 2026-05-12 but no deploy task appears in the sprint log or entry checklist — it is assumed but untracked. Making it an explicit gate with a named owner prevents it from being the last-hour surprise that slips the milestone.

## Risks if unchanged
- With 8 days left and 0 of 5 integrations live, attempting all 5 integrations plus auth plus Vercel deploy in parallel fragments engineering attention and makes KR1.1 (MVP live) a near-certain miss.
- Growing the eval set to 200 events before live LLM ingestion produces real data means KR1.3 precision is measured on synthetic events — the number will not predict real-world mapper performance and will give false confidence going into design-partner demos.
- No design partners are in the pipeline (§8 is empty as of last update) and the 2026-05-05 discovery-call milestone has likely slipped — KR1.2 (5 partners by 2026-05-19) is at risk regardless of MVP scope, but a missed 2026-05-12 deploy makes it mathematically impossible.

## Decisions needed from operator
- [ ] Which single integration ships in Sprint 0 — GitHub is the recommendation given commit-level signal is the clearest OKR-drift indicator, but confirm this is the integration your first design-partner candidates actually use daily.
- [ ] Has the 2026-05-05 discovery-call milestone (10 calls done, ICP locked) been hit or slipped — if slipped, KR1.2 (5 design partners by 2026-05-19) needs a revised date or the Sprint 1 goal must be reset before GTM agents are unthrottled?

_Confidence: 0.62_
_Reasoning: The sprint log through Day 5 (2026-05-02) is detailed and credible; the gap analysis between what shipped (scaffolding, eval framework, GTM kit, dashboard skeleton) and what is required for KR1.1/KR1.4 (live deploy, real data flowing, mapper running on real events) is clear. Confidence is capped at 0.62 because there is no design-partner feedback in the tracker — the 30-minute demo critical path is inferred from the KR definitions, not validated by a real session — and the §8 customer pipeline is entirely empty, making KR1.2 trajectory invisible._