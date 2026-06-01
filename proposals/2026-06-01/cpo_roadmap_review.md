# Roadmap pressure test — MVP 3 weeks late, zero design partners, critical path exposed

The MVP deadline (2026-05-12) has slipped by ~3 weeks with no design partners onboarded and no live LLM eval number — defer everything not on the path to a working demo with real data and reschedule KR1.2/1.4 targets accordingly. The single highest-leverage move is forcing a live OKR-Mapper precision run this week, because without a real KR1.3 number the entire narrative quality claim is unverifiable and no design partner will stay.

## Proposed scope changes
- **DEFER** — Product Hunt launch (2026-06-15 milestone)  
  → `Sprint 2` · KR impact: `2.1, 3.4`  
  _Why:_ Launching on Product Hunt with zero design-partner validation and an unverified KR1.3 precision number risks a permanent reputation hit with the exact ICP audience we need. KR1.2 (5 active design partners) is the prerequisite gate; that target is already 2 weeks late.
- **DEFER** — Full 5-integration suite (GitHub + Linear + Jira + Slack + Notion) for MVP  
  → `Sprint 1` · KR impact: `1.4`  
  _Why:_ KR1.4 (time-to-first-narrative ≤30 min) requires exactly one working integration to demo the magic moment — GitHub alone covers the critical path. Shipping all five integrations before a single design partner has validated the core loop is scope that cannot be recovered if it slips further.
- **RESHAPE** — OKR-Mapper eval set: grow from 50 to 200 labeled events  
  → `n/a` · KR impact: `1.3`  
  _Why:_ The 200-event target was scoped for 2026-05-05 and is still unmet; the framework exists but the dataset does not. Reshape the goal: ship 100 events with a live-LLM precision run by 2026-06-05 to get a real KR1.3 number this week, then grow to 200 in Sprint 1 — a real 60% precision number now is more useful than a perfect 200-event set two weeks from now.
- **DEFER** — SOC2-readiness checklist (0/45 items, Engineering pod KR)  
  → `post-pilot` · KR impact: `1.1`  
  _Why:_ Zero design partners are blocked on SOC2 today; Series A–C buyers at pilot stage accept a DPA and a security one-pager. Closing 45 checklist items before the product has a single active user is the definition of premature compliance spend.
- **ADD** — Hardcoded demo-mode data path in the dashboard for design-partner first session  
  → `n/a` · KR impact: `1.4, 1.2`  
  _Why:_ KR1.4 (≤30 min to first narrative) will fail for every new account until integrations are stable and OAuth is wired — a seeded demo dataset lets the operator run a design-partner session today without waiting for live ingestion, directly protecting KR1.2 (5 partners by a rescheduled target).

## Risks if unchanged
- Product Hunt fires on 2026-06-15 with no design-partner proof points and an unverified mapper precision number, permanently poisoning the ICP audience we need for KR2.1.
- Attempting all five integrations in parallel with no design-partner feedback means the first real precision signal on KR1.3 arrives after the pilot window has already started, making narrative quality a known unknown throughout Sprint 1.
- Without a demo-mode fallback, every design-partner first session depends on a live OAuth + ingestion pipeline that has never been tested with a real external account, making KR1.4 (≤30 min) structurally unachievable in the near term.

## Decisions needed from operator
- [ ] Which single integration (GitHub is the recommendation) ships as the MVP demo path, and are you willing to explicitly defer the other four to Sprint 1 so engineering focus is not split?
- [ ] Will you run OKR_MONITOR_DRY_RUN=false against the current 50-event eval set this week to get a real KR1.3 precision number, even if it comes back below 85% — because an honest low number is a better input to Sprint 1 scoping than continued uncertainty?

_Confidence: 0.62_
_Reasoning: The tracker shows the MVP deadline missed by ~3 weeks, KR1.2/1.3/1.4 all at zero, and no design-partner feedback wired in — the evidence for urgency is strong. Confidence is capped at 0.62 because there is no external signal: no discovery-call synthesis from ux_researcher, no design-partner reactions, and no live precision number from the OKR-Mapper, so the relative priority of mapper quality vs. integration breadth vs. onboarding UX is inferred from first principles rather than observed customer behavior._