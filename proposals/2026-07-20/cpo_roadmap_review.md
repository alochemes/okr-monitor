# Roadmap pressure test — critical path is broken; pilots KR is the real crisis

The MVP deadline (2026-05-12) has passed with no evidence of deployment, design partners, or live integrations — the cycle is now 83 days in with KR2.1 at 0/300 pilots and KR1.2 at 0/5 design partners. The single highest-leverage move is to immediately defer all non-demo-path work and force a 'design partner 1 in 7 days' constraint to generate real signal before the cycle ends.

## Proposed scope changes
- **DEFER** — SOC2-readiness checklist (0/45 items) and DPA template  
  → `Sprint 2` · KR impact: `1.1, 1.4`  
  _Why:_ Zero design partners means zero enterprise procurement conversations requiring SOC2; shipping this now consumes Engineering cycles that should be on the GitHub integration and Vercel deploy. Defer until KR1.2 reaches ≥3 active partners who explicitly ask for it.
- **DEFER** — Forecasting agent P(hit) calibration and Brier score target (≤0.15)  
  → `post-pilot` · KR impact: `1.3, 1.4`  
  _Why:_ The forecasting agent already emits verdict heuristics; calibrated P(hit) requires per-KR conversion data that does not exist until real pilot events flow through the pipeline. Shipping a confident-wrong probability now actively harms KR1.4 (time-to-first-narrative) by making the narrative feel unreliable.
- **RESHAPE** — OKR-Mapper eval set: hold at 50 labeled events, not 200  
  → `n/a` · KR impact: `1.3`  
  _Why:_ The 200-event target was set for 2026-05-05; it is now 2026-07-20 and the eval framework exists but precision is unmeasured against live LLM. Spending time growing the dataset to 200 before a single real integration fires is backwards — run the 50-event set live, get the first real precision number, then grow the set against observed failure modes. KR1.3 (≥85% P @ ≥70% R) is better served by one real-data iteration than a larger synthetic set.
- **DEFER** — Product Hunt launch (KR3.4, scheduled 2026-06-15)  
  → `post-pilot` · KR impact: `1.2`  
  _Why:_ The launch date has already passed with 0 design partners and no live product — launching now or soon with no social proof, no case study, and no NPS data will produce a poor result that is hard to repeat. Defer until KR1.5 (NPS ≥50) is measurable and at least one case study exists.
- **ADD** — Hardcoded 'demo account' data path: static fixture events → mapper → narrative, no live integration required  
  → `n/a` · KR impact: `1.4, 1.2`  
  _Why:_ KR1.4 (time-to-first-narrative ≤30 min) and KR1.2 (5 active design partners) are both blocked because no live integration exists yet — a design partner cannot reach the magic moment. A demo-account fixture path lets the operator run a full narrative demo in a browser today, unblocking discovery calls and partner sign-ups while real integrations are completed in parallel.

## Risks if unchanged
- With 39 days left in the cycle and KR2.1 at 0/300 pilots, the 300-pilot target is arithmetically unreachable without an immediate step-change in both product readiness and GTM velocity — the cycle ends as a total miss on O2.
- The dogfood gate in §10 (two consecutive useful Friday narratives before showing any design partner) has likely never fired because the live LLM + real integration path is not confirmed deployed — this gate may be silently blocking KR1.2 indefinitely.
- All High risks in §9 (mapper precision unmeasured, Slack privacy DPA missing, Anthropic balance) remain open with no recorded mitigation progress, meaning the first design partner demo could fail on any of them simultaneously.

## Decisions needed from operator
- [ ] Is the MVP actually deployed to Vercel with at least one live integration (GitHub or Linear) producing real events, or is the product still running only in local dry-run — and if the latter, what is the specific blocker?
- [ ] Given that the 300-pilot target requires roughly 8 new pilots per day for the remaining 39 days, should O2 be formally revised to a number that reflects what is achievable, or is the operator committing to a GTM blitz that has not yet started?

_Confidence: 0.42_
_Reasoning: The tracker's last recorded activity is 2026-05-02 (Day 5), yet today is 2026-07-20 — 79 days of unrecorded progress means the actual state of deployment, integrations, and design partners is unknown and the tracker is stale by its own §11 update rules. Recommendations are therefore based on the last known state (no live deploy, no design partners, no measured precision) and may be partially invalidated if significant work shipped after May 2. The confidence floor is set by the complete absence of design-partner feedback called out in the system prompt, which means every product-quality judgment here is unvalidated._