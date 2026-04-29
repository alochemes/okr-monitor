# Architecture check — 3 risks flagged

Stack choice is sound. Three risks: integration auth scope, LLM cost on long-tail accounts, and ingestion idempotency.

## Risks
- **[?]** `integrations` — DRY_RUN: GitHub App scopes default too broad  
  → _Mitigation:_ request only repo:read + metadata (`?`)
- **[?]** `cost` — DRY_RUN: large customers may 10x token spend  
  → _Mitigation:_ cap re-mapping frequency and use Haiku for relinks (`?`)
- **[?]** `data` — DRY_RUN: webhook retries could double-insert events  
  → _Mitigation:_ idempotency key on (source, source_event_id) (`?`)

_Confidence: 0.75_
_Reasoning: DRY_RUN: stub._