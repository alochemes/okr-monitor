# Week of 2026-04-28: Lock the discovery loop, start ingestion plumbing

Sprint 0 starts. The single biggest risk is OKR-Mapper precision (KR1.3) — every other KR depends on it. Front-load the eval set this week.

## Priorities
1. **Run 10 discovery calls by Friday**  
   Owner: `Product/Design` · KR `1.4` · Due `?`  
   _Why:_ ICP isn't truly locked until we hear pain in the buyer's words.
2. **Ship the 200-event labeled eval set for OKR-Mapper**  
   Owner: `AI/Data` · KR `1.3` · Due `?`  
   _Why:_ Build the ruler before building the thing being measured.
3. **GitHub + Linear OAuth working in dev**  
   Owner: `Engineering` · KR `1.1` · Due `?`  
   _Why:_ These two integrations are the demo. Slack/Notion can wait one more day.

## Risks to watch
- DRY_RUN: scope creep on integrations beyond the four MVP sources

## Decisions needed from operator
- [ ] DRY_RUN: confirm Mooncamp is in or out of the v1 OKR import

_Confidence: 0.70_
_Reasoning: DRY_RUN: based on TRACKER.md §2 (KR weights) and §9 (top risk = OKR-Mapper precision)._