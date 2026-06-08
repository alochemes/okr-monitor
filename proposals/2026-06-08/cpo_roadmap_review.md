# Roadmap pressure test — MVP 27 days late, zero design partners, critical path exposed

The MVP deadline (2026-05-12) has passed without a live product, and KR1.2 (5 design partners) and KR1.4 (time-to-first-narrative ≤30 min) are both at zero with the Product Hunt launch (KR3.4) 7 days away — defer Product Hunt immediately and collapse all Sprint 1 scope to a single forcing function: one design partner reading one real narrative this week. Everything else is noise until that happens.

## Proposed scope changes
- **DEFER** — Product Hunt launch (2026-06-15)  
  → `post-pilot` · KR impact: `3.4`  
  _Why:_ Launching on Product Hunt with zero active design partners, no live product, and no case study (KR1.5 still at zero) will produce a bottom-of-the-day result and burn the one-shot opportunity; the dogfood gate in §10 (two consecutive useful Fridays) has not been cleared, making this launch premature by the team's own stated standard.
- **RESHAPE** — Sprint 1 goal from '5 design partners using product weekly' to '1 design partner reads 1 real narrative from their own data'  
  → `Sprint 1` · KR impact: `1.2, 1.4, 1.3`  
  _Why:_ KR1.4 (time-to-first-narrative ≤30 min) and KR1.3 (mapper precision ≥85%) cannot be measured without a live integration pulling real customer data; collapsing to a single design partner unblocks both KRs and the §10 dogfood gate without requiring the full 5-partner onboarding machinery to be production-ready.
- **DEFER** — SOC2-readiness checklist (0/45 items, Engineering pod KR)  
  → `Sprint 2` · KR impact: `1.1`  
  _Why:_ Zero design partners are blocked on SOC2 today; pursuing 45 checklist items before the product has a single active user is a high-cost distraction from KR1.1 (MVP live) and the §9 High risk that mapper precision may be below threshold — fix the product first, then the compliance wrapper.
- **DEFER** — Full 5-integration launch (GitHub + Linear + Jira + Slack + Notion simultaneously)  
  → `Sprint 2` · KR impact: `1.4`  
  _Why:_ KR1.4 only requires one end-to-end path to produce a narrative in ≤30 min; shipping GitHub + Linear alone covers the modal ICP stack and cuts integration surface area by 60%, directly buying down the §9 High risk of silent ingestion breakage before any customer data is live.
- **ADD** — OKR-Mapper live-LLM eval run (dry-run → real) as a hard gate before any design partner onboarding  
  → `Sprint 1` · KR impact: `1.3, 1.4`  
  _Why:_ The eval framework is built (50-event set, REPORT.md wired) but has never produced a real precision number — §9 explicitly flags mapper precision as the highest-severity risk, and onboarding a design partner before knowing whether precision clears 85% risks producing a narrative that 'reads like nonsense' and poisons the NPS measurement (KR1.5) before it starts.

## Risks if unchanged
- Product Hunt launch on 2026-06-15 with no live product and no design partners will permanently consume the one-shot PH opportunity and likely land outside top 20, damaging KR3.4 irreversibly.
- OKR-Mapper precision has never been measured against real LLM output; onboarding design partners before clearing the 85% threshold risks a narrative quality failure that collapses KR1.5 NPS before it can be measured.
- The 300-pilot target (KR2.1) requires ~25 pilots by 2026-06-09 per the milestone calendar — the tracker shows 0 cumulative pilots, meaning the M1 ramp is already missed and M2 (75 pilots by 2026-07-09) is now the de facto survival threshold.

## Decisions needed from operator
- [ ] Will you pull the Product Hunt launch from 2026-06-15, and if so, what is the new trigger condition — is it 'two consecutive useful Fridays' per §10, or a specific pilot count?
- [ ] Which single integration (GitHub or Linear) do you want to ship first to unblock the one-design-partner forcing function, given that both are at 0/5 integrations live today?

_Confidence: 0.62_
_Reasoning: The tracker's own milestone calendar and KR current-values make the slippage unambiguous — MVP was due 2026-05-12, today is 2026-06-08, and every customer-facing KR (1.2, 1.3, 1.4, 1.5, 2.1) reads 'n/a' or zero, which is strong evidence for a scope collapse rather than an acceleration. Confidence is capped at 0.62 because there is no design-partner feedback in the tracker (§8 is entirely blank), no real LLM eval run has completed, and the operator may have context on integrations progress or partner conversations that hasn't been committed to TRACKER.md — the tracker explicitly notes 'Last updated: 2026-05-02', meaning 37 days of actual work are invisible to this analysis._