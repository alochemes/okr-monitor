# Roadmap pressure test — Sprint 0 is 55 days overdue; rebase now

The MVP deadline (2026-05-12) passed 55 days ago with KR1.1 at ~25% and zero design partners signed, meaning KR1.2, KR1.3, KR1.4, and KR1.5 are all effectively blocked. The single highest-leverage move is to declare a hard 7-day 'ship-or-stop' sprint focused exclusively on Vercel deploy + Supabase auth + one live integration (GitHub), deferring everything else until a design partner can log in.

## Proposed scope changes
- **RESHAPE** — Sprint 0 MVP scope — collapse to: Vercel deploy, Supabase magic-link auth, GitHub integration only, dashboard reading live kr_signals.json  
  → `n/a` · KR impact: `1.1, 1.4`  
  _Why:_ KR1.1 (MVP live) is the prerequisite for every other O1 KR. The current scope includes 5 integrations (GitHub + Linear + Jira + Slack + Notion); shipping one live integration with real data is sufficient to start the clock on KR1.4 (time-to-first-narrative ≤30 min) and unblock design-partner onboarding for KR1.2.
- **DEFER** — Linear, Jira, Slack, and Notion integrations  
  → `Sprint 1` · KR impact: `1.4`  
  _Why:_ All four are listed as Sprint 0 engineering KRs but none are required for a design partner to experience the core narrative loop; GitHub alone produces enough commit-level work events to demonstrate KR1.3 mapper precision and generate a meaningful narrative. Deferring four OAuth integrations removes the highest-variance engineering risk from the critical path.
- **DEFER** — OKR-Mapper eval set grow-out from 50 to 200 events (KR1.3 milestone 2026-05-05)  
  → `Sprint 1` · KR impact: `1.3`  
  _Why:_ The eval framework is wired and 50 events are labeled; the 200-event target was due 2026-05-05 and is already 62 days late. Growing to 200 events before the first live integration produces real data is premature — real GitHub events from design partners will be higher-signal labels than synthetic ones. Defer the grow-out until 2 design partners are live and contributing real events.
- **DEFER** — Product Hunt launch (KR3.4, targeted 2026-06-15)  
  → `post-pilot` · KR impact: `1.2`  
  _Why:_ The launch date has already passed (2026-06-15) with zero design partners onboarded and no live product; launching now without social proof or a working product risks burning the one-shot PH opportunity. Defer until KR1.2 (5 active design partners) and KR1.5 (NPS ≥50) are met — a launch with testimonials converts at 3–5× the rate of a cold launch.
- **ADD** — Weekly operator checkpoint: if zero design partners are logged in by 2026-07-13, pause GTM spend and run a kill-or-pivot decision  
  → `n/a` · KR impact: `1.2, 2.1`  
  _Why:_ The tracker has no forcing function to surface a go/no-go decision; with 53 days left in the cycle and KR2.1 requiring 300 pilots by 2026-08-28, the compounding math is now nearly impossible (≈6 pilots/day required from a standing start). A hard checkpoint in 7 days converts the current drift into an explicit decision rather than a silent slip.

## Risks if unchanged
- With 53 days left in the cycle and KR2.1 at 0/300 pilots, the 300-pilot target is mathematically unreachable without a live product and active GTM — every week of further delay makes the end-of-cycle OKR review a post-mortem rather than a retrospective.
- The dogfood gate in §10 (two consecutive Fridays of useful auto-narrative before showing any design partner) cannot be satisfied without a live LLM integration and at least one real data source; this gate is currently blocking KR1.2 with no bypass defined.
- The High-severity Anthropic balance risk (§9) was logged at $0 balance on 2026-04-29; if this was never resolved, every agent run is still in dry-run and KR1.3 precision is still unmeasured — the entire AI/Data pod's output is unvalidated.

## Decisions needed from operator
- [ ] Has the Anthropic API balance been topped up and have any real (non-dry-run) LLM calls succeeded since 2026-04-29? If not, this is the single highest-priority unblock before any other scope decision matters.
- [ ] Given that the 300-pilot target (KR2.1) now requires roughly 6 new pilots per day for the remaining 53 days with zero currently onboarded, is the operator willing to restate the cycle target to a number achievable from a standing start, or hold the target and accept that O2 will be missed?

_Confidence: 0.42_
_Reasoning: The tracker's last update is 2026-05-02 (65 days ago as of today), so all recommendations are inferred from the last known state — there is no design-partner feedback, no live precision number from KR1.3, and no confirmation that the Anthropic billing block was resolved. The scope-collapse and defer recommendations are high-confidence because the critical-path logic is structural (no auth = no design partners = no NPS = no pilots), but the kill-or-pivot checkpoint confidence is lower because the operator may have shipped work not yet reflected in the tracker._