# Week of 2026-06-22: Close the pilot gap before M2 target slips permanently

The 75-pilot M2 milestone is due 2026-07-09 — 17 days away — and the pipeline shows zero cumulative pilots against a target that requires ~4-5 new pilots per business day starting now. KR1.1 (MVP live) status is unconfirmed as of the last tracker update, which means every downstream KR is at risk.

## Priorities
1. **Confirm MVP production status and, if not live, ship the Vercel deploy + Supabase auth this week — no other work matters until KR1.1 is green.**  
   Owner: `Engineering` · KR `1.1` · Due `2026-06-24`  
   _Why:_ KR1.1 was due 2026-05-12 and is still listed as 'Not started' in the tracker — if it has shipped, update TRACKER.md immediately; if it hasn't, it is 6 weeks overdue and blocks every pilot, every design partner, and the Product Hunt launch.
2. **Book and run at least 15 pilot demos this week using the GTM kit already built, targeting the Tier 1 outreach list, to close the gap toward the 75-pilot M2 target by 2026-07-09.**  
   Owner: `GTM` · KR `2.1` · Due `2026-06-26`  
   _Why:_ Zero pilots are on the board with 17 days to the 75-pilot M2 milestone — the math requires immediate acceleration and the outreach scripts, target list, and calendaring kit are already built and waiting.
3. **Run the OKR-Mapper eval on the live LLM (not dry-run) against the 200-event set and record the precision/recall number — accept or escalate based on the ≥85% P / ≥70% R threshold.**  
   Owner: `AI/Data` · KR `1.3` · Due `2026-06-26`  
   _Why:_ KR1.3 was due 2026-05-12 with no current measurement; mapper precision is the core product IP and the launch gate for dogfood sign-off — without a real number, we cannot credibly demo or onboard design partners.

## Risks to watch
- KR1.2 (5 design partners) was due 2026-05-19 and the pipeline table is still empty — no design partners means no NPS measurement, no case study, and no Product Hunt social proof.
- Product Hunt launch (KR3.4) is scheduled 2026-06-15 — it may have already passed with zero pilots and no confirmed MVP; confirm whether it was executed or needs to be rescheduled.
- The Slack-ingestion privacy risk (High, §9) has no confirmed DPA template shipped — this blocks any pilot that uses Slack as an integration.
- Pricing is still undecided (§9, Med) — the 'pilot → paid intent' KR2.3 is unmeasurable without a price, and pilots are now 5+ weeks in with no conversion signal.
- OKR-Mapper precision below 85% on the live eval would make the auto-narrative unreliable and invalidate the core product promise before any pilot can validate it.

## Decisions needed from operator
- [ ] Has the MVP shipped to production (KR1.1)? If yes, update TRACKER.md now — if no, what is the single blocker and who is unblocking it this week?
- [ ] Did the Product Hunt launch (KR3.4, planned 2026-06-15) execute? If it slipped, what is the new date and what is the prerequisite that must be true before it fires?
- [ ] What is the pilot pricing model — free trial duration, paid tier price point, and conversion trigger — so KR2.3 can be measured and pilots can be given a clear next step?

_Confidence: 0.35_
_Reasoning: The tracker was last updated 2026-05-02, leaving 7 weeks of execution invisible — KR1.1, KR1.2, KR1.3, and KR1.4 were all due between May 12-19 and their current status is unknown, making it impossible to confirm whether the MVP is live or pilots exist. Priorities are ranked by what would cause the most irreversible damage if still unresolved: a missing MVP blocks everything, zero pilots at week 8 of a 17-week cycle is a structural emergency, and an unmeasured mapper precision means the product's core claim is unverified. Confidence is low because the tracker gap means any of these could already be resolved — the operator must confirm current state before acting on this brief._