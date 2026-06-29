# Week of 2026-06-29: Close the pilot gap before M3 math becomes impossible

At 10 weeks into a 17-week cycle, cumulative pilots are almost certainly near zero — the 75-pilot M2 target (2026-07-09) is 10 days away and there is no evidence it has been hit. If the M2 milestone slips without a course correction this week, the 300-pilot end-state requires an implausible acceleration in the final 7 weeks.

## Priorities
1. **Audit the live pilot count against the M2 target of 75 and immediately activate the outbound sequence at full volume (600 touches/business day) if below 50.**  
   Owner: `GTM` · KR `2.1` · Due `2026-07-02`  
   _Why:_ The M2 milestone of 75 cumulative pilots is due 2026-07-09 — 10 days out — and KR2.1 showed 0 pilots as of last tracker update; missing M2 makes 300 by 2026-08-28 arithmetically implausible.
2. **Run the OKR-Mapper eval set on live LLM (not dry-run) and publish the precision/recall number; if below 85% P / 70% R, declare a P0 and halt new pilot onboarding until fixed.**  
   Owner: `AI/Data` · KR `1.3` · Due `2026-07-01`  
   _Why:_ KR1.3 is the load-bearing IP — every pilot narrative depends on mapper precision, and the eval framework has been ready since 2026-05-02 with no live precision number recorded; shipping pilots onto a sub-threshold mapper destroys NPS and KR1.5.
3. **Confirm the Slack ingestion privacy posture is resolved (DPA template live, default-public-channels-only enforced in code) before any new pilot connects Slack.**  
   Owner: `Engineering` · KR `1.1` · Due `2026-07-03`  
   _Why:_ The Slack privacy risk is flagged High and unmitigated in §9 — the DPA template was due 2026-05-12 and there is no evidence it shipped; onboarding pilots without it is a legal and reputational liability that can kill the company faster than a missed KR.

## Risks to watch
- Slack DPA template was due 2026-05-12 and shows no evidence of completion — any pilot connecting Slack today is an unmitigated High legal risk.
- OKR-Mapper has never run on live LLM against the eval set; the entire product narrative quality is unverified in production.
- M2 pilot target (75 cumulative by 2026-07-09) is 10 days away with no pipeline data visible in §8 — missing it compresses the remaining ramp to an implausible slope.
- Pricing is still unresolved (was due 2026-05-19 per §9) — pilots converting to paid intent (KR2.3) cannot be measured without a price, and the window to set anchoring expectations with early pilots is closing.
- TRACKER.md has not been updated since 2026-05-02 — all KR statuses, pilot counts, and risk mitigations are 8 weeks stale, making this proposal's confidence low.

## Decisions needed from operator
- [ ] What is the actual cumulative pilot count today, and which acquisition channel has produced any pilots at all — this is the single input needed to know whether to accelerate, pivot channel mix, or declare a plan failure?
- [ ] Has pricing been locked? If not, will you set a price this week — even a placeholder — so that pilot-to-paid-intent conversations can begin with a real number?
- [ ] Is the Slack DPA template complete and in use, or does Slack need to be disabled as an integration for all current pilots until it is?

_Confidence: 0.31_
_Reasoning: TRACKER.md was last updated 2026-05-02 — 8 weeks before today — so all KR current values, pilot counts, and risk statuses are stale; the proposal reasons from the last known state (0 pilots, unmitigated High risks, no live eval number) projected forward. The M2 milestone date (2026-07-09) and the unmitigated High risks in §9 are the primary evidence driving all three picks. What is missing: any update to §8 (customer pipeline), any evidence the Slack DPA shipped, any live OKR-Mapper precision number, and any pilot count above zero._