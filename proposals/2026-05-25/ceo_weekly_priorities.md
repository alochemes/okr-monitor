# Week of 2026-05-25: Close Design Partners, Ship MVP, Lock Pricing

KR1.2 (5 design partners) and KR1.1 (MVP live) are both due this week and show no logged progress — missing either collapses the Sprint 1 launch gate and the entire pilot ramp. The dogfood rule blocks showing the product to any design partner until two consecutive auto-narratives have been read and found useful, which means the MVP must ship before any partner onboarding can complete.

## Priorities
1. **Deploy MVP to Vercel with Supabase auth and at least one live integration (GitHub) so the dogfood narrative gate can be cleared this week**  
   Owner: `Engineering` · KR `1.1` · Due `2026-05-26`  
   _Why:_ KR1.1 was due 2026-05-12 and is still not live — every downstream milestone (design partners, NPS, Product Hunt) is blocked until production exists
2. **Book and conduct kickoff calls with at least 3 qualified ICP accounts using the gtm/ discovery kit, targeting signed design-partner agreements by 2026-05-28**  
   Owner: `GTM` · KR `1.2` · Due `2026-05-28`  
   _Why:_ KR1.2 (5 design partners by 2026-05-19) is already overdue with zero pipeline logged — without partners, KR1.5 NPS and the 2026-05-26 case study milestone are impossible
3. **Decide and document pricing model (per-seat, flat, or usage-based with a specific number) so pilot-to-paid conversion intent can be measured against KR2.3**  
   Owner: `Strategy` · KR `2.3` · Due `2026-05-28`  
   _Why:_ Pricing was due to be locked by 2026-05-19 per the decision log and remains open — running pilots without a price makes KR2.3 (≥25% paid intent) unmeasurable and undermines every sales conversation

## Risks to watch
- OKR-Mapper precision is unvalidated on live LLM — if the 200-event eval set has not been run against a real API call, KR1.3 (≥85% P @ ≥70% R) is unknown and the narrative quality is unverified before design partners see it.
- Slack ingestion DPA template was due 2026-05-12 and is not marked complete — onboarding any design partner with Slack connected before the DPA is in place is a legal exposure.
- The dogfood launch gate (two consecutive useful auto-narratives) has not been cleared — showing the product to design partners before this gate is met violates the stated rule and risks a bad first impression.
- KR1.5 (design-partner NPS ≥50) is due 2026-05-26 tomorrow with zero partners onboarded — this KR will slip; the question is whether it slips by days or by weeks.
- Product Hunt launch is 2026-06-15 (21 days away) with no live product, no design-partner testimonials, and no case study — the launch will be weak without at least 2 weeks of partner usage data.

## Decisions needed from operator
- [ ] What is the pricing model for paid conversion — per-seat, flat monthly, or usage-based — and what is the specific price point to use in pilot-to-paid conversations starting this week?
- [ ] Has the Anthropic API balance been topped up and is OKR_MONITOR_DRY_RUN=false confirmed for the Sunday and daily cloud routines, or are all agent runs still in dry-run mode?
- [ ] Should the Product Hunt launch date of 2026-06-15 be held given the MVP is not yet live, or should it be pushed to allow at least 2 weeks of design-partner usage data before launch?

_Confidence: 0.62_
_Reasoning: The tracker's last update is 2026-05-02 and today is 2026-05-25 — 23 days of execution are unlogged, so all KR statuses are assumed unchanged from their last recorded state (all 🔴 except KR4.1 ✅ and KR4.2 🟡). Priorities are driven by the two overdue load-bearing milestones (KR1.1 due 2026-05-12, KR1.2 due 2026-05-19) and the unmitigated High risk on pricing (decision log: due 2026-05-19, still open). Confidence is limited by the 23-day gap — it is possible the MVP shipped and partners were onboarded without a tracker update, which would change all three priorities._