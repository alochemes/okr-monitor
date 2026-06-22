# Roadmap pressure test — MVP 41 days late; demo path is the only path now

The MVP deadline (2026-05-12) has passed by 41 days with KR1.1 at ~25% and zero design partners (KR1.2 = 0 vs target 5 by 2026-05-19); the entire O1 critical path must be collapsed to a single shippable demo loop this week. Defer all integrations beyond GitHub and all SOC2 work until Sprint 2 — the only thing that matters now is one live account seeing a narrative in under 30 minutes.

## Proposed scope changes
- **DEFER** — Linear, Jira, Slack, and Notion integrations (3 of 5 planned integrations)  
  → `Sprint 2` · KR impact: `1.1, 1.4`  
  _Why:_ GitHub alone is sufficient to generate a narrative for a design partner demo; shipping four OAuth integrations before a single partner is live adds 1–2 weeks of integration-engineer time with zero KR1.4 payoff until KR1.2 > 0.
- **DEFER** — SOC2-readiness checklist (0/45 items, Engineering pod KR)  
  → `Sprint 2` · KR impact: `1.1`  
  _Why:_ No design partner at Series A–C will block a free pilot on SOC2 status; starting this work now consumes platform and security agent cycles that are on the KR1.1 critical path.
- **RESHAPE** — OKR-Mapper eval set: grow from 50 to 200 labeled events  
  → `Sprint 1` · KR impact: `1.3`  
  _Why:_ The framework is done and the 50-event set exists; the 200-event milestone (KR1.3, originally due 2026-05-05) is already 47 days late — completing it is a 1-day task that should be the next AI-Eng action, not a multi-sprint project, but it must not block the Vercel deploy.
- **DEFER** — Product Hunt launch (KR3.4, planned 2026-06-15)  
  → `post-pilot` · KR impact: `1.2, 3.4`  
  _Why:_ The launch date has already passed with no product live; relaunching without active design partners producing real narratives will yield a weak result and burn the one-shot PH window — defer until KR1.2 ≥ 3 and KR1.5 is measurable.
- **ADD** — Hardcoded demo account: pre-seeded GitHub events → OKR mappings → narrative, bypassing live OAuth for the first design partner session  
  → `Sprint 1` · KR impact: `1.4, 1.2`  
  _Why:_ KR1.4 (time-to-first-narrative ≤30 min) cannot be measured until a partner sees a narrative; a demo-mode account with fixture data lets the operator run the first 5 discovery-to-demo calls this week without waiting for Supabase auth and live webhook wiring to be production-ready.

## Risks if unchanged
- KR2.1 (300 pilots by 2026-08-28) requires ~4.5 pilots/day from today with zero pilots currently — every additional week without a shippable demo makes this target mathematically unreachable.
- KR1.3 precision is still unmeasured (dry-run only); if the first live eval comes back below 85%, the narrative is broken and design partners churn before NPS is measurable (KR1.5).
- The 2026-06-09 milestone of 25 cumulative pilots has already passed at 0 — without an explicit scope collapse and public acknowledgment of the slip, Sprint 1 planning will anchor to the original calendar and repeat the same miss.

## Decisions needed from operator
- [ ] Will you accept a demo-mode account with fixture data as the gate for the first design partner call, or do you require live GitHub OAuth to be wired before any external demo?
- [ ] Given that the 2026-06-15 Product Hunt date has passed, should KR3.4 be formally removed from this cycle's OKRs and replaced with a measurable interim KR (e.g., 3 design partners producing weekly narratives by 2026-07-09)?

_Confidence: 0.52_
_Reasoning: The tracker is detailed through Day 5 (2026-05-02) but goes silent after that — there is no sprint log entry for the 51 days between then and today, so the actual state of Vercel deploy, Supabase auth, and GitHub integration is unknown and could be further along than the 25% KR1.1 estimate recorded on Day 5. The zero design-partner count is the hardest signal: KR1.2 was due 2026-05-19 and no pipeline entries exist in §8, which is strong evidence the demo is not yet showable. Confidence would rise significantly with a current KR1.1 percentage and one confirmed design-partner conversation._