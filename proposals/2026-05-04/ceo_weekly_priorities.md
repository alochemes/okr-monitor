# Week of 2026-05-04: MVP deadline in 8 days — three blockers must clear now

KR1.1 (MVP live) is due 2026-05-12 and sits at ~25% with auth, integrations, and Vercel deploy still unbuilt. Two unmitigated High risks — OKR-Mapper precision unverified and Slack privacy DPA missing — will block design partner onboarding the moment the MVP ships.

## Priorities
1. **Ship Vercel deploy + Supabase auth wiring + first live integration (GitHub) so KR1.1 is production-live by 2026-05-12**  
   Owner: `Engineering` · KR `1.1` · Due `2026-05-12`  
   _Why:_ At ~25% complete with 8 days left, every day without a deployed, auth-gated product is a day the 2026-05-19 design-partner milestone (KR1.2) also slips — it cascades to KR1.4, KR1.5, and the Product Hunt date.
2. **Run OKR-Mapper eval against live LLM on the 50-event set (top up Anthropic balance first) and confirm precision trajectory toward ≥85% before any design partner sees the product**  
   Owner: `AI/Data` · KR `1.3` · Due `2026-05-09`  
   _Why:_ This is the highest-severity unmitigated risk in §9 — if mapper precision is below threshold, the narrative is broken and the dogfood launch gate (two consecutive useful Fridays) cannot be cleared in time for design partners.
3. **Execute discovery outreach using the Day 5 GTM kit — book and complete all 10 discovery calls to lock ICP and secure 5 design-partner commitments**  
   Owner: `GTM` · KR `1.2` · Due `2026-05-09`  
   _Why:_ The 2026-05-05 milestone (10 discovery calls done, ICP locked) is already one day past; zero pipeline exists and KR1.2 requires 5 signed design partners by 2026-05-19 — the outreach kit is ready, the bottleneck is operator dials.

## Risks to watch
- Anthropic balance at $0 blocks all live LLM runs — operator must top up at console.anthropic.com before any real eval or agent output is possible.
- Slack DPA template due 2026-05-12 is unmitigated and unstarted — missing it blocks any design partner from opting into Slack ingestion at onboarding.
- Pricing model still undecided; KR2.3 (pilot → paid intent ≥25%) is unmeasurable without a price, and the lock date of 2026-05-19 is 15 days away.
- Discovery call milestone (2026-05-05) already slipped by one day with zero calls completed — each additional day compresses the design-partner recruitment window before 2026-05-19.
- Sunday GitHub Actions workflow requires ANTHROPIC_API_KEY as a repo secret — without it, weekly narratives remain dry-run stubs and the dogfood launch gate cannot be cleared.

## Decisions needed from operator
- [ ] Will you top up the Anthropic API balance this week (recommended $50–$100) to unblock live LLM eval and real agent runs — yes/no and by when?
- [ ] Which 10 discovery call targets from the Tier 1 list will you personally dial this week, and will you block calendar time before Friday 2026-05-08 to complete them?
- [ ] Should the Slack DPA template be drafted by the Security agent this week for operator review, or is Slack ingestion being deferred past the MVP launch?

_Confidence: 0.82_
_Reasoning: KR1.1 at ~25% with an 8-day deadline and KR1.3 as an unmitigated High risk are unambiguous load-bearing priorities per the §9 risk table and §5 milestone calendar. The discovery call slip is confirmed by the sprint log (zero calls, 2026-05-05 milestone passed). Missing evidence: no visibility into how many hours of engineering capacity are available this week, and no confirmation that the Anthropic balance has been topped up — both affect whether priority 1 and 2 are achievable on the stated deadlines._