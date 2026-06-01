# Week of 2026-06-01: Close design partners, hit 25-pilot milestone, unblock eval

The 2026-06-09 milestone of 25 cumulative pilots is 8 days out with zero pilots in the pipeline — this is the single most urgent gap. KR1.1 (MVP live) and KR1.2 (5 design partners) are both overdue as of 2026-05-19, meaning the entire pilot funnel is blocked on product and partner work that should already be done.

## Priorities
1. **Convert at least 3 of the discovery-call targets into signed design partners this week — use the gtm/ kit, run the 5-in-5 exercise on the call, and get them logging in.**  
   Owner: `GTM` · KR `1.2` · Due `2026-06-05`  
   _Why:_ KR1.2 (5 design partners active ≥3×/week) is 13 days overdue and is the prerequisite for KR1.5, the case study, and any credible pilot conversion — without it the 2026-06-09 25-pilot milestone is unreachable.
2. **Deploy MVP to Vercel with Supabase auth wired and at least one live integration (GitHub) so design partners can actually log in and receive a narrative.**  
   Owner: `Engineering` · KR `1.1` · Due `2026-06-05`  
   _Why:_ KR1.1 was due 2026-05-12 and is still not live; no design partner can reach 'first value' without a deployed product, and the dogfood launch gate (two consecutive useful auto-narratives) cannot be cleared until auth + ingestion are real.
3. **Run the OKR-Mapper eval against the 200-event labeled set with OKR_MONITOR_DRY_RUN=false and record the precision/recall number — if below 85%/70%, treat it as a P0 and begin prompt iteration immediately.**  
   Owner: `AI/Data` · KR `1.3` · Due `2026-06-04`  
   _Why:_ KR1.3 precision is the load-bearing IP of the product; the eval framework is built and the Anthropic balance is funded, so there is no remaining blocker — shipping a narrative to design partners before this number is confirmed is a reputational risk the company cannot afford.

## Risks to watch
- Slack ingestion privacy risk (High, §9) has no DPA template in place — the 2026-05-12 deadline passed; do not onboard any design partner with Slack enabled until this is resolved.
- Zero pilots with 8 days to the 25-pilot milestone (2026-06-09) means the M1 GTM target will slip unless outbound volume starts immediately this week.
- OKR-Mapper precision is unconfirmed against real LLM calls — if <85%, the narrative quality is unknown and showing the product to design partners risks destroying early trust.
- Pricing is still unlocked (due 2026-05-19 per §9) — 'pilot → paid intent' (KR2.3) cannot be measured without a price, and design partners will ask.
- KR4.2 (weekly auto-narrative 100% of weeks) is in-progress but the dogfood launch gate requires two consecutive useful narratives before any external demo — clock is running.

## Decisions needed from operator
- [ ] What is the pricing model for paid conversion — is there a number to give design partners who ask this week, or do we explicitly defer and on what timeline?
- [ ] Is the DPA / Slack privacy policy ready to unblock Slack ingestion for design partners, or do we launch with GitHub-only and add Slack in Sprint 2?
- [ ] Has the Anthropic API key been added as a GitHub Actions secret so the Sunday workflow fires with real LLM calls, or is the Sunday routine still running in dry-run?

_Confidence: 0.62_
_Reasoning: Priorities 1–3 are driven by three overdue milestones (KR1.1 due 2026-05-12, KR1.2 due 2026-05-19, KR1.3 due 2026-05-12) and the imminent 2026-06-09 25-pilot milestone with zero current pipeline. The main evidence gap is that TRACKER.md has not been updated since 2026-05-02 — it is possible that discovery calls were completed, design partners were signed, or the MVP was partially deployed in the intervening 30 days, which would change the ranking; without a tracker update, all KRs are treated as still at their last-known state (not started / 25% complete)._