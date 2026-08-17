# Roadmap pressure test — 11 days to cycle end, 300-pilot gap is existential

With 11 days left in the cycle and KR2.1 (300 pilots) almost certainly far short of target, the only defensible move is to defer all remaining Sprint 0 polish and redirect every hour toward pilot acquisition and retention evidence. The OKR-Mapper eval set must ship to a live-LLM run immediately — without a real precision number, KR1.3 is unverifiable and design-partner NPS (KR1.5) is unanchored.

## Proposed scope changes
- **DEFER** — SOC2-readiness checklist (0/45 items closed, Engineering pod KR)  
  → `post-pilot` · KR impact: `?`  
  _Why:_ SOC2 is a procurement gate for 1,000+ employee companies — our anti-ICP. No design partner in the 50–500 band will block on SOC2 in a pilot phase, and closing 45 items in 11 days is impossible without crowding out work that directly serves KR1.4 and KR2.1.
- **DEFER** — Slack, Notion integrations (2 of the 5 planned integrations)  
  → `Sprint 1` · KR impact: `1.4`  
  _Why:_ GitHub + Linear/Jira alone cover the critical path for KR1.4 (time-to-first-narrative ≤30 min); Slack and Notion add ingestion richness but not the core mapping signal. Deferring two integrations buys ~4–6 engineering days that should go toward hardening the mapper and the Vercel deploy.
- **RESHAPE** — OKR-Mapper eval set: grow from 50 to 200 events AND run against live LLM immediately  
  → `n/a` · KR impact: `1.3`  
  _Why:_ KR1.3 (≥85% precision @ ≥70% recall) is the load-bearing KR for the entire product narrative; the eval framework is done but the precision number is still unknown because dry-run mocks return 0%. With 11 days left this is the highest-leverage unblocked action — operator must flip OKR_MONITOR_DRY_RUN=false and run the eval today.
- **DEFER** — Product Hunt launch (KR3.4, currently scheduled 2026-06-15 — already slipped)  
  → `post-pilot` · KR impact: `?`  
  _Why:_ The launch date has already passed without execution; re-scheduling it inside the final 11 days of the cycle would consume community/PR bandwidth needed for pilot conversion, and launching without a live precision number or NPS data produces a weak story.
- **ADD** — Emergency pilot-count audit: pull actual logged-in accounts from Supabase and surface in daily report  
  → `n/a` · KR impact: `1.2, 2.1, 2.2`  
  _Why:_ The tracker shows 0 design partners and 0 pilots as of the last update (2026-05-02); with 11 days left the operator needs a real number today to decide whether to run a blitz outreach push or declare the 300-pilot KR a miss and focus on NPS evidence for the next cycle pitch.

## Risks if unchanged
- KR1.3 closes the cycle with no real precision number — the product's core claim is unverified and unusable as a design-partner proof point.
- KR2.1 (300 pilots) is almost certainly a hard miss; without an explicit acknowledgment and a revised outreach blitz, the cycle ends with no acquisition evidence to anchor the next funding or GTM narrative.
- Slack/Notion integration work in progress during the final sprint crowds out the Vercel deploy hardening needed for KR1.1 and KR1.4 to be demonstrable to any new partner.

## Decisions needed from operator
- [ ] Will you flip OKR_MONITOR_DRY_RUN=false today and run the 200-event eval against the live LLM — and if the precision is below 85%, is the cycle goal a declared miss or do you want a prompt-tuning sprint in the final 11 days?
- [ ] What is the actual current pilot count in Supabase — and given that number, do you want to run a concentrated outbound blitz for the remaining 11 days or formally scope KR2.1 as a learning milestone rather than a hit?

_Confidence: 0.42_
_Reasoning: The tracker's last update is 2026-05-02 — over three months ago — so all KR current values, pilot counts, and integration statuses are unknown; every recommendation here is driven by the absence of evidence rather than confirmed data. The two highest-confidence calls (eval run and SOC2 defer) are structural: the eval framework is provably done and SOC2 is provably anti-ICP-irrelevant. The pilot-count audit addition is a forced move because no other scope decision is rational without knowing the real number._