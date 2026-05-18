# Roadmap pressure test — MVP deadline in 6 days, zero design partners signed

The 2026-05-19 KR1.2 target (5 active design partners) is effectively missed with zero in pipeline; defer it to Sprint 1 and redirect all remaining Sprint 0 capacity to shipping a demoable, Vercel-deployed product that produces one real narrative. The OKR-Mapper eval set must reach 200 events and run against a live LLM before any GTM motion restarts — without a real precision number, KR1.3 is unverifiable and every demo is a liability.

## Proposed scope changes
- **DEFER** — Design partner onboarding target of 5 active partners (KR1.2) from Sprint 0 to Sprint 1  
  → `Sprint 1` · KR impact: `1.2, 1.4`  
  _Why:_ Zero partners are in the pipeline as of today and the deadline is tomorrow; forcing the number now produces low-quality partners who haven't seen a working product. Deferring to 2026-05-26 preserves the KR without burning founder credibility on a half-built demo.
- **DEFER** — Slack integration (one of the 5 planned integrations in the Engineering pod KR)  
  → `Sprint 1` · KR impact: `1.4`  
  _Why:_ Slack ingestion carries the highest privacy/legal risk (§9 open question, no DPA template yet) and is the lowest-signal source for the OKR-Mapper at this eval-set size; dropping it from Sprint 0 removes a High risk blocker and frees ~2–3 days of integration-engineer capacity for Vercel deploy and GitHub wiring, which are on the demo critical path.
- **RESHAPE** — OKR-Mapper eval set: grow from 50 to 200 labeled events using live-LLM runs against dogfood data, not hand-labeling  
  → `n/a` · KR impact: `1.3`  
  _Why:_ The eval framework is done but the set is at 50 events and the precision number is still 0% (dry-run mocks); KR1.3 requires ≥85% P @ ≥70% R on 200 events by 2026-05-12 (already past). Reshaping the grow-out to use live-LLM runs on the existing dogfood event log is faster than hand-labeling 150 synthetic events and produces a more honest precision signal before the first design-partner demo.
- **DEFER** — SOC2-readiness checklist (0/45 items, Engineering pod KR)  
  → `Sprint 2` · KR impact: `?`  
  _Why:_ No design partner is asking for SOC2 at the pilot stage and the checklist is 0% complete; any Sprint 0 time spent here is directly off the demo critical path with zero KR1.3 or KR1.4 impact. Defer explicitly so it doesn't silently slip into Sprint 1 either.
- **ADD** — Hard launch gate: operator must read two consecutive auto-generated narratives rated ≥4/5 before any design-partner demo is booked  
  → `n/a` · KR impact: `1.4, 1.5`  
  _Why:_ §10 dogfooding rule already states this gate but it is not enforced in the milestone calendar; making it an explicit blocking condition prevents a demo on a product that produces a bad narrative, which would crater KR1.5 NPS before it is even measured. This is a forced move given zero design-partner feedback exists.

## Risks if unchanged
- Demoing to design partners before a real precision number exists (KR1.3 still at 0% on live LLM) means the narrative quality is unknown — a single bad narrative in a demo kills the pilot pipeline.
- Slack integration without a DPA template (§9 High risk, due 2026-05-12, not shipped) exposes the first design partner to a privacy incident before the product has any credibility to absorb it.
- Treating KR1.2's 2026-05-19 deadline as live with zero pipeline creates pressure to onboard any warm body as a 'design partner,' polluting the feedback signal and distorting KR1.5 NPS.

## Decisions needed from operator
- [ ] Will you accept a one-week slip on KR1.2 (design partners) to 2026-05-26 in exchange for a demoable product with a verified precision number, or do you want to book demos this week on the current unverified narrative quality?
- [ ] Should Slack integration be deferred to Sprint 1 entirely, or is there a specific design partner whose stack requires Slack ingestion to make the demo feel complete?

_Confidence: 0.52_
_Reasoning: The tracker is internally consistent and the critical-path gaps (zero partners, zero live-LLM precision number, Vercel not deployed) are unambiguous — those drive the defer recommendations with high confidence. Confidence is capped at 0.52 because there is no design-partner feedback wired in anywhere in the tracker, so the relative weight of 'narrative quality' vs 'integration breadth' in the demo is unknown; the Slack deferral in particular could be wrong if a Tier-1 target runs Slack-only. The launch-gate addition is a forced move from §10's own stated rule, not a new opinion._