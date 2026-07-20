# Week of 2026-07-20: Close the pilot gap or miss the cycle

At 175 pilots due by 2026-08-09 and 300 by 2026-08-28, the GTM engine must be producing ~18 net-new pilots per business day starting now — there is no evidence it is. The OKR-Mapper precision number (KR1.3) is still unconfirmed against a live LLM, which means the core product claim is unverified at the moment we need it most for conversion.

## Priorities
1. **Confirm the current cumulative pilot count, measure the daily acquisition run-rate, and if below 12/day, activate all three GTM channels (outbound sequences, content inbound, community) in parallel this week — not sequentially.**  
   Owner: `GTM` · KR `2.1` · Due `2026-07-25`  
   _Why:_ The M3 milestone of 175 pilots is due 2026-08-09 — 20 days away — and the tracker shows 0 confirmed pilots; closing that gap requires a verified run-rate by Friday or the cycle target is mathematically unreachable.
2. **Run the OKR-Mapper eval set against the live LLM (OKR_MONITOR_DRY_RUN=false) and publish the precision/recall number; if below 85% P / 70% R, treat it as a P0 and block design-partner expansion until fixed.**  
   Owner: `AI/Data` · KR `1.3` · Due `2026-07-23`  
   _Why:_ KR1.3 is the load-bearing product claim — every pilot conversion conversation rests on it — and it has never been measured against a real LLM call; an unverified precision number is an unmitigated High risk per §9.
3. **Lock pricing and publish it internally so the pilot-to-paid-intent funnel (KR2.3) has a number to convert against before the cycle ends.**  
   Owner: `Strategy` · KR `2.3` · Due `2026-07-25`  
   _Why:_ Pricing was flagged as unresolved in §9 with a target of 2026-05-19 — it is now two months overdue, and without a price, the 25% paid-intent KR is unmeasurable and every pilot exit conversation is directionless.

## Risks to watch
- KR2.1 (300 pilots) requires ~18 net-new pilots/business day from today; any week below that pace makes the cycle target unrecoverable.
- Slack ingestion DPA template was due 2026-05-12 per §9 — if unshipped, any pilot using Slack integration is a legal exposure and a blocker to activation.
- KR2.2 pilot activation rate (≥60% read ≥1 narrative) is unmeasured; low activation silently kills the paid-intent funnel even if pilot volume hits target.
- Product Hunt launch (KR3.4) was scheduled 2026-06-15 — no evidence it fired; if it slipped, the inbound content flywheel for M3 is missing a major spike.
- Anthropic balance and daily circuit-breaker status are unconfirmed for current spend levels; at real pilot scale, the $50–$100 load may be exhausted.

## Decisions needed from operator
- [ ] What is the actual cumulative pilot count today, and which acquisition channel has produced the most — outbound, content, or community?
- [ ] Has pricing been locked? If not, what is blocking it — competitive benchmarking, conversion data, or something else?
- [ ] Did the Product Hunt launch happen on 2026-06-15, and if not, is it still planned — and for when?

_Confidence: 0.35_
_Reasoning: The tracker was last updated 2026-05-02 — 79 days ago — so every KR still shows 'Not started' or 0, which almost certainly does not reflect reality; the priorities are derived from milestone math (M3 = 175 pilots by 2026-08-09) and the two unmitigated High risks (mapper precision unverified, Slack DPA unshipped) rather than from observed current state. Confidence is low because the actual pilot count, live eval results, pricing status, and Product Hunt outcome are all unknown from the tracker alone — the operator must supply ground truth before this brief can be fully calibrated._