# Roadmap pressure test — MVP deadline passed; design-partner clock now critical

The 2026-05-12 MVP deadline has passed with KR1.1 at ~25% and zero design partners onboarded; the single most consequential move is to collapse all remaining Sprint 0 engineering scope into a shippable demo slice (one live integration + auth + Vercel deploy) within the next 7 days to salvage KR1.2 and KR1.4 before the NPS measurement date of 2026-05-26. Everything that does not put a working product in front of a design partner this week is a deferral candidate.

## Proposed scope changes
- **RESHAPE** — Integration scope: ship exactly ONE integration (GitHub) end-to-end before touching Linear, Jira, Slack, or Notion  
  → `Sprint 1` · KR impact: `1.1, 1.3, 1.4`  
  _Why:_ KR1.4 (time-to-first-narrative ≤30 min) only requires one live data source to demonstrate the magic moment; shipping all five integrations in parallel fragments engineering attention and is the most likely reason KR1.1 is still at 25%. Defer Linear/Jira/Slack/Notion to Sprint 1 — GitHub alone covers the demo critical path and satisfies the OKR-Mapper eval set (KR1.3) with real commit events.
- **DEFER** — SOC2-readiness checklist (0/45 items) and DPA template  
  → `Sprint 2` · KR impact: `1.1`  
  _Why:_ Zero design partners are onboarded yet, so no customer data is at risk today; the High privacy risk (Slack ingestion) is moot until Slack integration ships, which is already deferred. Pulling security work off the Sprint 1 critical path recovers meaningful engineering bandwidth for auth + Vercel deploy, which are the actual blockers on KR1.1.
- **DEFER** — Forecasting agent P(hit) calibration and Brier-score target (AI/Data pod KR: ≤0.15)  
  → `post-pilot` · KR impact: `1.3, 1.4`  
  _Why:_ The decision log already notes P(hit) is deferred pending real per-KR conversion data; the tracker still lists it as an active pod KR, which creates false sprint pressure. Explicitly deferring it post-pilot removes it from the Sprint 1 review surface and lets the AI/Data pod focus entirely on OKR-Mapper precision (KR1.3), which is the load-bearing demo metric.
- **DEFER** — Product Hunt launch (KR3.4, currently 2026-06-15)  
  → `Sprint 2` · KR impact: `1.2`  
  _Why:_ Launching on Product Hunt with zero active design partners and an unvalidated NPS produces a one-day traffic spike with no retention story and risks a public credibility hit; KR1.2 (5 design partners logging in ≥3×/week) is the prerequisite signal that makes a PH launch defensible. Pushing to late June or early July preserves the option without burning it.
- **ADD** — Hardcoded 'demo account' with synthetic but realistic data pre-loaded, bypassing live integration setup for the first 30-minute design-partner session  
  → `Sprint 1` · KR impact: `1.4, 1.2`  
  _Why:_ KR1.4 measures time-to-first-narrative at p90 for new accounts; if a design partner must complete OAuth + webhook setup before seeing any output, that clock will exceed 30 minutes on every first session. A pre-seeded demo account lets the operator show the narrative in under 5 minutes, then walk the partner through connecting their own GitHub — this is a forced move given the current onboarding gap and the absence of any design-partner feedback to validate the live-setup flow.

## Risks if unchanged
- KR1.2 (5 design partners by 2026-05-19) is already missed; without collapsing integration scope to one source, KR1.4 and KR1.5 will also miss their 2026-05-26 dates with no design partners to measure against.
- Attempting all five integrations in Sprint 1 while auth and Vercel deploy are still open creates a high probability of shipping nothing fully — the same failure mode that caused the Sprint 0 slip.
- Product Hunt on 2026-06-15 with zero validated design partners and an unmeasured NPS converts a GTM milestone into a reputational liability that is hard to undo.

## Decisions needed from operator
- [ ] Will you accept a demo-account shortcut (synthetic pre-loaded data) as the mechanism for the first design-partner session, or is a live integration required before any partner sees the product?
- [ ] Given that the 2026-05-12 MVP deadline has passed, should the Sprint 1 goal be redefined as 'one design partner reads their first auto-narrative' rather than '5 design partners onboarded,' to create a tighter, achievable gate before scaling outreach?

_Confidence: 0.62_
_Reasoning: The tracker provides clear evidence of the MVP slip (KR1.1 at ~25% as of Day 5, no update since 2026-05-02) and zero design partners, which makes the critical-path analysis straightforward. Confidence is limited by two gaps: no design-partner feedback has been collected (the tracker explicitly flags this), so the demo critical path is inferred from the product's own KRs rather than observed user behavior; and the tracker has not been updated since 2026-05-02, meaning up to 23 days of engineering progress may exist that is not reflected here — if integrations or auth have shipped since then, several of these recommendations may already be resolved._