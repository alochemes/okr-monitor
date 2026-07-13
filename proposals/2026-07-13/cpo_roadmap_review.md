# Roadmap pressure test — MVP deadline passed; pivot to pilot conversion

The 2026-05-12 MVP deadline and the 2026-05-19 design-partner target are both 8+ weeks in the past with no recorded completion, making KR1.1–KR1.4 the critical unresolved risk for the entire cycle. Every remaining resource should collapse onto live-product deployment and the first measurable time-to-first-narrative run; anything that doesn't directly serve those two outcomes should be deferred immediately.

## Proposed scope changes
- **DEFER** — SOC2-readiness checklist (45 items, Engineering pod KR)  
  → `post-pilot` · KR impact: `?`  
  _Why:_ Zero design partners are recorded in §8, so no enterprise procurement gate is active. SOC2 work consumes Security + Platform bandwidth that is urgently needed to get KR1.1 (MVP live) and KR1.4 (≤30 min time-to-first-narrative) across the line before the cycle ends on 2026-08-28.
- **DEFER** — Forecasting agent P(hit) calibration and Brier-score target (AI/Data pod KR ≤0.15)  
  → `Sprint 2` · KR impact: `1.3, 1.4`  
  _Why:_ The forecasting agent already emits verdict heuristics (on_track/drifting/off) which are sufficient for the demo critical path; calibrated P(hit) requires real per-KR conversion data that does not exist yet. Shipping this now adds AI-Eng load without moving KR1.3 or KR1.4.
- **DEFER** — Product Hunt launch (KR3.4, scheduled 2026-06-15)  
  → `post-pilot` · KR impact: `?`  
  _Why:_ The launch date has already passed with no recorded execution; re-scheduling it now without live design-partner proof points or a measurable NPS (KR1.5) would waste the one-shot attention window. Defer until KR1.2 (5 active design partners) and KR1.5 (NPS ≥50) are confirmed.
- **RESHAPE** — OKR-Mapper eval set: grow from 50 to 200 labeled events (Sprint 0 milestone 2026-05-05)  
  → `Sprint 1` · KR impact: `1.3`  
  _Why:_ The 50-event framework is built and the milestone date is long past; the remaining 150 events are pure data-labeling work that can run in parallel with live-product deployment rather than blocking it. KR1.3 precision target (≥85% P @ ≥70% R) still requires a real LLM run, which is the actual blocker — not dataset size.
- **ADD** — Weekly cycle-end viability checkpoint: explicit go/no-go on KR2.1 (300 pilots) given 46 days remaining  
  → `Sprint 1` · KR impact: `1.2, 1.4`  
  _Why:_ The tracker shows 0 pilots and 0 design partners as of last update with 46 days left in the cycle; at the stated ramp (25 by 2026-06-09, 75 by 2026-07-09) the target is already missed by at least one milestone gate. A formal operator checkpoint now prevents the team from optimizing for a KR that may need to be reset rather than chased.

## Risks if unchanged
- With 46 days left and 0 pilots recorded, KR2.1 (300 pilots) is mathematically unreachable without a scope reset — continuing to treat it as the live target misdirects GTM effort.
- The High risk in §9 ('OKR-Mapper precision is the whole product') remains unmitigated because no real LLM eval run has been recorded; a design partner demo before precision is confirmed risks permanently damaging the first impression.
- The Slack privacy risk (§9, High) has no recorded DPA template completion past the 2026-05-12 target date, meaning any live pilot ingesting Slack data is currently operating without a legal instrument.

## Decisions needed from operator
- [ ] Is KR2.1 (300 pilots by 2026-08-28) still the operative target, or should it be reset to a number achievable from a standing start in 46 days — and if reset, what is the revised number?
- [ ] Has the MVP been deployed to production (KR1.1) and have any design partners been onboarded (KR1.2), or is the tracker genuinely reflecting zero progress on both — and if so, what is the single blocking constraint?

_Confidence: 0.45_
_Reasoning: All recommendations are driven by the gap between the tracker's last-updated date (2026-05-02) and today (2026-07-13) — 72 days of unrecorded progress creates high uncertainty about actual state. The tracker shows 0 pilots, 0 design partners, and no live MVP as of its last entry, but it is plausible that significant work shipped after 2026-05-02 and simply was not committed back to TRACKER.md. The confidence score reflects that gap: if the MVP is live and design partners are active, several of these recommendations are moot; if the tracker is accurate, the cycle is in a critical recovery situation. No design-partner feedback is wired in per §10, which removes the most important signal for validating any of these scope calls._