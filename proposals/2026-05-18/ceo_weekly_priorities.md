# Week of 2026-05-18: Close Design Partners, Ship MVP, Lock Pricing

KR1.2 (5 design partners) and KR1.1 (MVP live) are both due tomorrow — neither is started per the tracker. This week is a triage week: determine actual status of both, close any design partners in conversation, and make the three decisions that unblock Sprint 1.

## Priorities
1. **Close at least 3 signed design partners by 2026-05-19 — call every warm lead today, send the pilot intake questionnaire, and book kickoff calls this week.**  
   Owner: `GTM` · KR `1.2` · Due `2026-05-19`  
   _Why:_ KR1.2 is the external dependency everything else hangs on — no design partners means no NPS (KR1.5), no activation data (KR2.2), and no dogfood gate before Product Hunt (KR3.4).
2. **Deploy MVP to Vercel with Supabase auth wired and at least one live integration (GitHub) — this is the Sprint 0 exit gate.**  
   Owner: `Engineering` · KR `1.1` · Due `2026-05-19`  
   _Why:_ KR1.1 was due 2026-05-12 and is still not started per the tracker; every day of slip delays design partner onboarding, the dogfood gate, and the 2026-06-15 Product Hunt launch.
3. **Lock pricing model and publish it internally — CFO agent proposal exists; operator must decide and record the decision in §7 of TRACKER.md.**  
   Owner: `Strategy` · KR `2.3` · Due `2026-05-19`  
   _Why:_ The 'pilot → paid intent' KR (KR2.3) is unmeasurable without a price, and the Med-severity pricing risk in §9 is now overdue against its own stated mitigation deadline of 2026-05-19.

## Risks to watch
- Slack ingestion privacy risk is High and unmitigated — DPA template was due 2026-05-12; if design partners onboard this week without it, we have a legal exposure.
- OKR-Mapper precision is unvalidated on live LLM — the eval framework exists but KR1.3 has no real precision number yet; if <85%, the narrative is broken before the first design partner sees it.
- Discovery call milestone (10 calls, ICP locked, eval set built) was due 2026-05-05 — no evidence in the tracker it was completed; ICP assumptions may still be unvalidated.
- The dogfood gate (two consecutive useful auto-narratives before showing any design partner) may not have been cleared — if it hasn't, we risk showing a broken product.
- Anthropic balance was $0 at last recorded state — if not topped up, all live agent runs remain in dry-run and the auto-narrative pipeline cannot produce real output for design partners.

## Decisions needed from operator
- [ ] What is the actual current status of KR1.1 and KR1.2 — are there design partners in conversation and is the MVP further along than the tracker shows, or are both genuinely at zero?
- [ ] Has the DPA template for Slack ingestion been drafted — and if not, do we block design partner onboarding on private-channel access until it is, or onboard public-channels-only as a stopgap?
- [ ] What is the pricing model — specifically, what does a pilot cost after the free pilot period, and what triggers the 'paid intent' signal we are measuring in KR2.3?

_Confidence: 0.42_
_Reasoning: The tracker was last updated 2026-05-02; today is 2026-05-18, so 16 days of actual work are unrecorded. KR1.1 and KR1.2 show 'not started' but significant scaffolding and GTM kit work was completed in Sprint 0 — real status is likely better than the tracker reflects. Priorities are driven by the two overdue milestones (2026-05-12 MVP, 2026-05-19 design partners) and the two unmitigated High risks (Slack privacy, Anthropic balance). Confidence is low because the tracker gap means I cannot distinguish 'not started' from 'in progress but unlogged.'_