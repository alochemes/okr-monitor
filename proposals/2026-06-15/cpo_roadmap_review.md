# Roadmap pressure test — MVP deadline passed; pivot to partner activation

The 2026-05-12 MVP deadline has passed with no evidence of a live Vercel deploy, zero design partners logged in, and KR1.3 precision still unmeasured against real LLM output — defer all Sprint 1 feature additions and force a 'deploy + first real narrative' gate before any new scope lands. The Product Hunt launch scheduled for today (2026-06-15) should be deferred immediately; launching with zero active design partners and an unmeasured NPS is a one-shot credibility burn.

## Proposed scope changes
- **DEFER** — Product Hunt launch (KR3.4, scheduled today 2026-06-15)  
  → `Sprint 2` · KR impact: `1.2, 1.4, 1.5`  
  _Why:_ KR1.2 shows 0 active design partners and KR1.5 NPS is unmeasured — launching to Product Hunt today means the first 500 visitors hit a product with no social proof, no case study, and no measured time-to-first-narrative. A failed PH launch is harder to recover from than a delayed one; defer until KR1.2 ≥3 and KR1.5 ≥50 are in hand.
- **RESHAPE** — Sprint 1 goal — change from 'design partner love' to 'deploy + first real narrative gate'  
  → `n/a` · KR impact: `1.1, 1.3, 1.4`  
  _Why:_ KR1.1 (MVP live on Vercel) is the prerequisite for every other KR and shows ~25% progress as of the last log entry; the sprint goal of 'design partner love' is unreachable without a deployed product. Reshaping the sprint goal to 'Vercel deploy live + Supabase auth wired + first integration (GitHub) + first real OKR-Mapper precision number' creates a concrete, binary gate that directly serves KR1.1, KR1.3, and KR1.4.
- **DEFER** — SOC2-readiness checklist (0/45 items, Engineering pod KR)  
  → `post-pilot` · KR impact: `1.1`  
  _Why:_ SOC2 is a procurement-cycle requirement for 200+ employee companies; the ICP for the pilot phase is 50–500 employees where a DPA template (already flagged in §9) is sufficient. Forty-five checklist items in parallel with a deploy sprint will fragment engineering attention and push KR1.1 further right.
- **DEFER** — Forecasting agent P(hit) calibration (Brier score ≤0.15, AI/Data pod KR)  
  → `Sprint 2` · KR impact: `1.3`  
  _Why:_ The decision log explicitly deferred P(hit) until real per-KR conversion data exists; with zero pilots and zero real mappings, shipping a Brier-score target now produces a confident lie. Deferring this formally removes it from the active sprint and prevents engineering time being spent on calibration math against synthetic data.
- **ADD** — Forced 'two-Friday narrative' internal gate before any design partner onboarding  
  → `n/a` · KR impact: `1.4, 1.5`  
  _Why:_ §10 Dogfooding Notes already states this rule but it is not tracked as a milestone or gate anywhere in §5 — it is invisible to the sprint. Making it an explicit, dated milestone (target: two consecutive Fridays with operator-rated narrative ≥4/5) directly de-risks KR1.4 (time-to-first-narrative ≤30 min) and KR1.5 (NPS ≥50) by ensuring the product works on our own data before a design partner's clock starts.

## Risks if unchanged
- Launching Product Hunt today with 0 design partners and unmeasured NPS converts a high-leverage channel into a permanent credibility deficit — the listing will show no reviews, no traction, and no narrative, making every future outreach harder.
- With KR1.1 at ~25% and no Vercel deploy confirmed, the 2026-06-09 milestone of 25 cumulative pilots is already missed; continuing to plan Sprint 1 as 'design partner love' without first closing the deploy gap means KR1.2 and KR1.4 slip another full sprint.
- OKR-Mapper precision (KR1.3) has never been measured against a real LLM call — if the first real eval run returns <70% precision, the narrative agent produces garbage and every design partner session becomes a trust-destroying demo rather than a trust-building one.

## Decisions needed from operator
- [ ] Will you commit to a hard 'two consecutive operator-rated Friday narratives ≥4/5' gate before inviting the first design partner — and if so, what is the target date for the first of those two Fridays?
- [ ] Should the Product Hunt launch be formally deferred to a specific future date tied to KR1.2 ≥3 active design partners, or held open as a floating milestone so it doesn't anchor planning conversations prematurely?

_Confidence: 0.55_
_Reasoning: The tracker's last sprint log entry is 2026-05-02 — there are 44 days of silence between that entry and today (2026-06-15), which means KR1.1 through KR1.5 status is unknown; all recommendations assume the worst-case (no silent progress) because no evidence of a deploy, real LLM run, or design partner exists in the tracker. Confidence would rise sharply with a single updated status row in §2 or a confirmed Vercel URL. The Product Hunt defer is the highest-confidence call because the milestone calendar explicitly targets today and the preconditions (KR1.2, KR1.5) are visibly unmet._