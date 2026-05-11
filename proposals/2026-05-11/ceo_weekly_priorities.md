# Week of 2026-05-11: MVP deadline tomorrow — ship or slip the cycle

KR1.1 (MVP live on Vercel) is due 2026-05-12 and is at ~25% completion — missing this milestone cascades into design partner onboarding, NPS measurement, and the Product Hunt date. Two High-severity risks remain unmitigated: OKR-Mapper precision unvalidated on live LLM, and no DPA/privacy decision on Slack ingestion.

## Priorities
1. **Deploy MVP to Vercel with Supabase auth wired and at least one live integration (GitHub) — get to a URL a design partner can log into by 2026-05-12**  
   Owner: `Engineering` · KR `1.1` · Due `2026-05-12`  
   _Why:_ KR1.1 is the load-bearing milestone everything else hangs on — no MVP means no design partners, no NPS, no Product Hunt, and KR1.2/1.4/1.5 all slip in sequence
2. **Run OKR-Mapper eval against the live LLM (flip DRY_RUN=false, execute `python -m tests.eval.run_eval`) and record the precision/recall number — accept ≥85% P / ≥70% R or treat as a P0 bug blocking design partner onboarding**  
   Owner: `AI/Data` · KR `1.3` · Due `2026-05-12`  
   _Why:_ This is the unmitigated High risk in §9 — if mapper precision is below threshold, every narrative we show a design partner reads like nonsense and the product fails its own launch gate
3. **Send outreach to the first 10 Tier-1 targets from `gtm/01_target_list.md` using the Day 5 kit, with the goal of booking 5 design-partner kickoff calls before 2026-05-16**  
   Owner: `GTM` · KR `1.2` · Due `2026-05-16`  
   _Why:_ KR1.2 requires 5 active design partners by 2026-05-19 — with zero in pipeline today, the operator must start dialing this week or the milestone is mathematically unreachable

## Risks to watch
- DPA template for Slack ingestion is due 2026-05-12 (§9 High risk) and has no recorded progress — shipping the MVP without it means the first design partner who asks about Slack privacy has no answer.
- Anthropic balance was $0 at last check (§9 High risk) — confirm the top-up landed before any live eval or demo run; a dry-run MVP is not a shippable MVP.
- KR1.3 eval set is at 50 events against a 200-event target for the 2026-05-05 milestone (already slipped) — precision number on 50 events is directional, not the contractual ≥85% threshold.
- Zero design partners in pipeline (§8) with 8 days to the 2026-05-19 milestone — even one no-show or slow reply kills the KR.
- Pricing still unlocked (§9 Med risk, due 2026-05-19) — design partners will ask what paid looks like; no answer erodes conversion signal from the pilot.

## Decisions needed from operator
- [ ] Is the Anthropic balance topped up and confirmed — can we flip OKR_MONITOR_DRY_RUN=false for the eval run and the MVP demo today?
- [ ] Do we accept the 50-event eval result as the Sprint 0 gate for KR1.3, or do we block design-partner onboarding until the full 200-event set is labeled and scored?
- [ ] Has the DPA template for Slack ingestion been drafted or sourced — and if not, do we launch the MVP with Slack integration disabled until it is?

_Confidence: 0.82_
_Reasoning: KR1.1 at ~25% with a 2026-05-12 deadline and KR1.3 unvalidated on live LLM are the two load-bearing risks per §9 and §5; both are due tomorrow. The design-partner outreach priority follows directly from the 2026-05-19 milestone with zero pipeline. Missing evidence: no sprint log entry after 2026-05-02 — the last 9 days of engineering progress on auth/Vercel/integrations is unrecorded, so KR1.1's true completion percentage could be higher or lower than the 25% estimate from Day 5._