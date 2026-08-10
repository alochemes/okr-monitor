# Roadmap pressure test — cycle end in 18 days, 300-pilot gap is critical

With 18 days left in the cycle and KR2.1 (300 pilots) almost certainly far short of target, the single highest-leverage move is to defer all remaining Sprint 0/1 infrastructure polish and redirect every available hour to pilot acquisition and activation. The 14-day MVP deadline referenced in the prompt has already passed (it was 2026-05-12); the question now is whether the cycle KRs are salvageable at all.

## Proposed scope changes
- **DEFER** — SOC2-readiness checklist (0/45 items closed per §3 Engineering pod KR)  
  → `post-pilot` · KR impact: `2.1, 2.3`  
  _Why:_ SOC2 is a procurement gate for 500+ employee companies, which are anti-ICP. No Series A–C SaaS pilot in the 50–500 band will block on SOC2 in a free pilot; deferring frees Engineering cycles for integration stability and onboarding, which directly unblock KR2.1 and KR2.3.
- **DEFER** — Forecasting agent P(hit) calibration / Brier score work (AI/Data pod KR: Brier ≤0.15)  
  → `Sprint 2` · KR impact: `1.4, 1.5`  
  _Why:_ The tracker explicitly deferred P(hit) pending real per-KR conversion data; with 18 days left there is no time to collect that data and tune calibration. Verdict heuristics (on_track/drifting/off) already ship the demo-critical-path value for KR1.4 time-to-first-narrative, and polishing a metric that has no baseline yet cannot move KR1.5 NPS in the remaining window.
- **RESHAPE** — Outbound demand-gen volume (GTM pod KR: 600 touches/business day)  
  → `n/a` · KR impact: `2.1, 2.4`  
  _Why:_ The tracker correctly gates demand-gen agents on ≥3% reply rate before scaling; with 18 days left and 0 confirmed pilots in §8, the reshape is to abandon the 600/day volume target entirely and instead run a high-touch founder-direct blitz (20–30 personalised touches/day from §4 founder_sales agent output) targeting the Tier 1 accounts in gtm/01_target_list.md — quality over volume is the only path to any meaningful KR2.1 progress before cycle close.
- **CUT** — Product Hunt launch (KR3.4, milestone 2026-06-15)  
  → `n/a` · KR impact: `3.4`  
  _Why:_ The milestone date was 2026-06-15 — nearly two months ago — and §5 shows no evidence it shipped; it has silently slipped. Formally cutting it removes a false open loop from the tracker and prevents any last-minute scramble that would consume GTM bandwidth needed for KR2.1 in the final 18 days.
- **ADD** — Cycle-close retrospective artifact: honest KR attainment report for investor/advisor use  
  → `n/a` · KR impact: `1.2, 2.1, 2.3`  
  _Why:_ The tracker has no end-of-cycle review artifact planned; with KR2.1 (300 pilots) almost certainly missed and KR1.2 (5 active design partners) status unknown, a candid attainment doc with root-cause analysis is a forced move — it is the primary input to the next cycle's OKR-setting and to any fundraising narrative. This is a one-day effort with outsized strategic value.

## Risks if unchanged
- KR2.1 (300 pilots) will close at near-zero with no scope change — the tracker shows 0 pilots as of last update and 18 days remain, making the target mathematically unreachable without an immediate all-hands pivot to acquisition.
- The Product Hunt launch (KR3.4, due 2026-06-15) has silently slipped by ~8 weeks with no retro row in §7; leaving it open creates false urgency and may trigger a rushed launch that burns GTM credibility at exactly the wrong moment.
- Without a formal cycle-close artifact, the root causes of the O1/O2 misses will not be captured before the next cycle begins, repeating the same planning errors in the next 4-month window.

## Decisions needed from operator
- [ ] Is KR2.1 (300 pilots by 2026-08-28) being treated as a hard target or a directional aspiration — and if hard, is the operator willing to declare it missed now and redirect the final 18 days entirely toward learning (design partner depth) rather than volume?
- [ ] What is the actual current pilot count and design-partner login frequency as of today (2026-08-10)? The tracker's §8 customer pipeline is empty and §2 KR1.2/KR2.1 show 0 — if real data exists outside the tracker, this pressure test may be materially wrong.

_Confidence: 0.45_
_Reasoning: The tracker's last update was 2026-05-02 — over three months ago — meaning all KR current-values, pilot counts, and agent statuses are stale; every recommendation here is inferred from the absence of progress markers rather than confirmed data. The 14-day MVP deadline (2026-05-12) has passed with no retro entry, which is the single strongest signal that execution has diverged significantly from plan. No design-partner feedback is wired in (tracker explicitly notes this), so the demo-critical-path assessment is based on product logic alone, not validated user behavior._