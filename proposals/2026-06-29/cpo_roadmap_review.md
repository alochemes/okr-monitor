# Roadmap pressure test — MVP is 47 days late; critical path is broken

The MVP deadline (KR1.1, 2026-05-12) was missed by 47 days with no retro, no slip decision, and no revised plan in the tracker — this is the most consequential gap. Defer everything that isn't (a) getting the Vercel deploy live with Supabase auth, (b) wiring one real integration, and (c) producing a real OKR-Mapper precision number, because without those three, KR1.2 and KR1.4 are structurally unreachable.

## Proposed scope changes
- **DEFER** — All 5 integrations (GitHub, Linear, Jira, Slack, Notion) shipping in parallel  
  → `Sprint 1` · KR impact: `1.1, 1.4`  
  _Why:_ The critical path to KR1.4 (time-to-first-narrative ≤30 min) needs exactly one working integration for the demo; shipping all five in parallel dilutes engineering focus and is the most likely reason KR1.1 slipped. Defer Jira, Slack, and Notion to Sprint 1; ship GitHub + Linear only for the MVP.
- **DEFER** — SOC2-readiness checklist (0/45 items, Engineering pod KR)  
  → `post-pilot` · KR impact: `1.1`  
  _Why:_ Zero design partners are in the pipeline (KR1.2 = 0); no pilot will block on SOC2 before the product exists. Forty-five checklist items are a material Sprint 0/1 tax on the same engineers who need to ship auth and integrations.
- **RESHAPE** — OKR-Mapper eval set: grow from 50 to 200 labeled events  
  → `n/a` · KR impact: `1.3`  
  _Why:_ The framework is done and the 50-event set exists, but the 200-event milestone (2026-05-05) is now 55 days overdue with no precision number yet. Reshape the target: run the live-LLM eval on the existing 50 events immediately to get a real precision number, then grow to 200 only if precision is below 85% and more data is needed to diagnose failures — don't grow the set as a prerequisite to knowing where you stand.
- **DEFER** — Product Hunt launch (KR3.4, 2026-06-15 target)  
  → `Sprint 2` · KR impact: `1.2`  
  _Why:_ The launch date has already passed (today is 2026-06-29) with no design partners logged in and no MVP deployed — launching to Product Hunt now would surface a product with 0 social proof and no activation path, burning the one-shot launch moment. Defer until KR1.2 ≥ 3 active design partners.
- **ADD** — Explicit slip decision + revised milestone calendar committed to TRACKER.md  
  → `n/a` · KR impact: `1.1, 1.2, 1.3, 1.4`  
  _Why:_ The tracker has no retro for Sprint 0, no revised dates, and no acknowledged slip — the dogfood product cannot generate a useful narrative from a tracker with stale milestones, and the operator cannot make good prioritization calls without a current plan. This is a forced move: without a revised calendar, every KR due date is fiction and the weekly narrative is noise.

## Risks if unchanged
- KR1.2 (5 active design partners by 2026-05-19) is now 41 days past due with 0 partners — the customer pipeline section is empty, meaning the GTM kit shipped in Day 5 was never executed, and the cycle's O2 targets (300 pilots by 2026-08-28) are mathematically unreachable without an immediate course correction.
- KR1.3 precision is still 'n/a' because no live LLM eval has run — the product's core IP is unvalidated 47 days after the MVP deadline, meaning every demo is a liability until this number exists.
- The tracker's stale milestone dates mean the dogfood narrative agent will generate a brief that marks every KR as 'stale' or 'off', which is accurate but useless for decision-making — the product is failing its own KR4.2 (weekly narrative useful) by operating on bad inputs.

## Decisions needed from operator
- [ ] What is the new MVP live date (KR1.1) and the new design-partner target date (KR1.2) — will you commit revised dates to the tracker this week so the narrative and forecast agents have a current plan to reason over?
- [ ] Has any outbound from the Day 5 GTM kit been executed, and if not, is the blocker the missing MVP (no demo to show) or operator bandwidth — because the answer changes whether the next action is 'ship the deploy' or 'run discovery calls against a Loom walkthrough'?

_Confidence: 0.62_
_Reasoning: The tracker's sprint log ends at Day 5 (2026-05-02) with no Sprint 0 retro, no Sprint 1 log, and no updated KR statuses — 58 days of work are invisible, so all scope recommendations are inferred from what was planned versus what the KR table still shows as 'not started'. Confidence would increase significantly with a Sprint 0 retro entry, a revised milestone calendar, and the first real OKR-Mapper precision number. The Product Hunt defer is the highest-confidence call (the date has passed); the integration sequencing defer is the highest-leverage call if the MVP is still in progress._