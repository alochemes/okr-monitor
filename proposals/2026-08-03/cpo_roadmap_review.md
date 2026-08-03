# Roadmap pressure test — MVP deadline passed; pivot to pilot conversion

The 2026-05-12 MVP deadline and the 2026-05-19 design-partner onboarding milestone are both 11+ weeks in the past with no recorded completion, making KR1.1, KR1.2, KR1.3, and KR1.4 the critical failures to triage immediately. With 25 days left in the cycle, the only recoverable KRs are O2 (pilots) and O3 (content/brand), but only if the product is actually live — which the tracker does not confirm.

## Proposed scope changes
- **ADD** — Emergency tracker update: record actual status of KR1.1 (MVP live), KR1.2 (design partners), KR1.3 (mapper precision), KR1.4 (time-to-first-narrative) as of today 2026-08-03  
  → `n/a` · KR impact: `1.1, 1.2, 1.3, 1.4`  
  _Why:_ Every KR in §2 still shows 'Not started' or 'n/a' with no sprint retro closing Sprint 0 or Sprint 1; without ground truth on what is actually live, every other scope decision is speculation and the cycle-end review on 2026-08-28 will be unauditable.
- **DEFER** — SOC2-readiness checklist (0/45 items, Engineering pod KR) and DPA template (§9 risk, due 2026-05-12)  
  → `post-pilot` · KR impact: `1.1, 1.2`  
  _Why:_ With 25 days left and pilot count almost certainly far below the 175-cumulative M3 target due 2026-08-09, compliance work consumes engineering cycles that must go to integration stability and onboarding speed; no Series A–C SaaS pilot will block on SOC2 for a free pilot.
- **DEFER** — Forecasting agent P(hit) calibration and Brier-score KR (AI/Data pod, target ≤0.15)  
  → `Sprint 2` · KR impact: `1.3, 1.4`  
  _Why:_ The decision log explicitly deferred P(hit) until real per-KR conversion data exists; that data cannot exist if design partners are not yet active, and shipping a confident-wrong probability into the narrative directly undermines KR1.4 (time-to-first-narrative ≤30 min feels magical, not broken).
- **RESHAPE** — Product Hunt launch (KR3.4, target Top 5, scheduled 2026-06-15)  
  → `post-pilot` · KR impact: `1.2, 2.1`  
  _Why:_ The launch date has already passed with no recorded result in §5 or §6; if it did not fire, relaunching without design-partner testimonials and a live product narrative is a wasted slot — reshape to a post-pilot launch anchored to a case study (KR1.5 NPS ≥50 as social proof) rather than a cold launch.
- **CUT** — Outbound volume target of 600 touches/business day (GTM pod KR) for the remainder of this cycle  
  → `n/a` · KR impact: `2.1, 2.4`  
  _Why:_ §9 flags this as High risk with a hold-until-reply-rate-≥3% gate; with 25 days left and no confirmed reply-rate data in the tracker, hitting 600/day now produces spam-tier deliverability damage that will hurt the next cycle more than it helps KR2.1 in this one — cut the volume target and focus outbound on the 50 Tier-1 accounts already named in gtm/01_target_list.md.

## Risks if unchanged
- If KR1.1 (MVP live) is still not confirmed by 2026-08-10, the cycle ends with zero measurable progress on O1 and O2, making the 2026-08-28 cycle review a post-mortem rather than a retro.
- Running high-volume outbound (600/day) without a confirmed reply-rate gate risks domain blacklisting that persists into the next cycle, permanently impairing KR2.4 (3 acquisition channels ≥30 pilots/mo).
- The tracker has no sprint retro for Sprint 0 or Sprint 1, meaning dogfood-discovered gaps (KR4.3, 100% within 24h) are almost certainly untracked and the product is being built without the feedback loop the dogfood rule in §10 requires.

## Decisions needed from operator
- [ ] Is the MVP (KR1.1) actually live on Vercel today, and if so, what are the real current values for KR1.2 (active design partners), KR1.3 (mapper precision on eval set), and KR1.4 (p90 time-to-first-narrative)?
- [ ] Given 25 days remain and the M3 pilot target (175 cumulative by 2026-08-09) is almost certainly missed, should the cycle goal be formally re-scoped to 'prove the magic moment with ≥5 design partners and publish ≥1 case study' rather than defending the 300-pilot number?

_Confidence: 0.35_
_Reasoning: Confidence is low because the tracker has not been updated since 2026-05-02 — all Sprint 0 milestones, Sprint 1 work, and three months of execution are unrecorded, so every recommendation is based on the absence of evidence rather than evidence of absence. The scope changes are driven by the 25-day remaining window and the structural risks flagged in §9, both of which are durable regardless of actual ship state. The single highest-value action is the emergency tracker update (scope_change #1) because it converts this analysis from speculation to fact._