# Roadmap pressure test — critical path is broken; ship integrations or miss every KR

The MVP deadline passed 76 days ago (2026-05-12) and the tracker shows zero design partners, zero integrations live, and no real OKR-Mapper precision number — the three dependencies that gate every downstream KR. Defer all GTM scaling and content work immediately; the only thing that matters before 2026-08-28 is getting one integration live, one real precision number, and five design partners generating narratives.

## Proposed scope changes
- **DEFER** — Product Hunt launch (2026-06-15 milestone, KR3.4) and all O3 content/podcast/benchmark work  
  → `post-pilot` · KR impact: `3.1, 3.2, 3.3, 3.4`  
  _Why:_ With zero design partners and no live product as of 2026-07-27, a Product Hunt launch would be a credibility-destroying event, not a growth lever. O3 KRs are vanity until O1 is proven; deferring frees operator attention for the only thing that can save the cycle.
- **RESHAPE** — Integration scope: cut GitHub + Slack + Notion for Sprint 0 remainder; ship GitHub-only as the single live integration  
  → `Sprint 1` · KR impact: `1.1, 1.4`  
  _Why:_ KR1.4 (time-to-first-narrative ≤30 min) only requires one real event source to demonstrate the magic moment; GitHub commits are the highest-signal, lowest-OAuth-friction source for an engineering-led ICP. Shipping four integrations simultaneously is what caused the slip — one working integration beats four half-built ones for every design-partner demo.
- **DEFER** — SOC2-readiness checklist (0/45 items, Engineering pod KR) and DPA template  
  → `Sprint 2` · KR impact: `1.1`  
  _Why:_ No design partner is blocked on SOC2 compliance at the pilot stage for a Series A–C tool; this work is consuming Engineering bandwidth that must go to the GitHub integration and Vercel deploy. The High risk on Slack privacy (§9) is mitigated by deferring Slack ingestion itself.
- **RESHAPE** — OKR-Mapper eval set: stop at current 50-event set; run live-LLM precision now rather than growing to 200 events first  
  → `n/a` · KR impact: `1.3`  
  _Why:_ KR1.3 requires ≥85% precision on a 200-event set by 2026-05-12 — that deadline is 76 days past. The framework is built; the blocker is that every eval run has been dry-run (0% precision against mocks). Running the 50-event set against the live LLM today produces a real signal within hours and unblocks the narrative quality gate (§10 dogfood rule) that is the actual launch gate for design partners.
- **ADD** — Emergency design-partner blitz: operator dials 10 Tier-1 targets from gtm/01_target_list.md this week using the shipped outreach kit, targeting 2 committed design partners by 2026-08-04  
  → `n/a` · KR impact: `1.2, 1.4, 1.5`  
  _Why:_ KR1.2 (5 active design partners) is the leading indicator for every O2 KR; the outreach kit, interview guide, and onboarding playbook are all shipped and ready. With 32 days left in the cycle, even 2 design partners generating weekly narratives would produce enough signal to validate KR1.4 and KR1.5 — but zero outbound touches have been logged, making this a forced move.

## Risks if unchanged
- With 32 days left and zero design partners, KR1.2 (5 partners), KR1.4 (time-to-first-narrative), and KR1.5 (NPS ≥50) are all mathematically unreachable — the cycle closes with O1 entirely unproven.
- The §10 dogfood launch gate ('two consecutive Fridays of useful auto-narrative') has never been cleared because no real LLM eval has run; every design-partner demo would be showing a dry-run stub, which destroys the 'inevitable' first-30-minutes impression the demo critical path requires.
- O2's 300-pilot target (KR2.1) requires ~600 outbound touches/day per §9 — with no product to demo and no design-partner case study, any outbound at scale now produces spam-tier reply rates and burns the ICP list before the product is ready.

## Decisions needed from operator
- [ ] Will you commit to running the live-LLM OKR-Mapper eval against the 50-event set this week (requires flipping OKR_MONITOR_DRY_RUN=false and confirming Anthropic balance ≥$10) — yes or no, because every other unblock depends on knowing whether the mapper precision is above or below 85%?
- [ ] Given that the cycle ends 2026-08-28 and O2's 300-pilot KR is now unreachable in 32 days without a live product, do you want to reforecast O2 to a defensible number (e.g., 10 paying-intent pilots from 5 design partners) and redirect all GTM agent output toward design-partner conversion rather than cold outbound volume?

_Confidence: 0.55_
_Reasoning: The tracker is internally consistent and detailed through Day 5 (2026-05-02), but there is no sprint log entry for the 86 days between 2026-05-02 and today (2026-07-27), meaning the actual state of integrations, design partners, and mapper precision is unknown — the tracker's 'not started' statuses may be stale. Recommendations are driven by the structural gap between the 2026-05-12 MVP deadline and today's date, the §10 dogfood launch gate never being cleared, and the §9 High risks (mapper precision, Anthropic balance) still showing as unmitigated. Confidence would rise significantly with a single data point: whether any real LLM eval has run._