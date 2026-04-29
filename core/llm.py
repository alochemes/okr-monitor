"""Anthropic client wrapper. All model calls go through here so token
accounting, audit, and prompt caching live in one place.

Caching strategy: the system prompt is the cacheable surface. We pin
`cache_control: ephemeral` on the system block so repeated calls in the same
~5-minute window read the prompt from cache. The user message varies per
call and is not cached. For the strategy pod this matters: the system block
includes company.yaml + the full TRACKER.md, so caching is a 90%+ cost
reduction when running CEO/CPO/CTO/CFO back-to-back.

Model picks (see CLAUDE.md):
- claude-haiku-4-5-20251001  → cheap summarization, light filtering
- claude-sonnet-4-6          → strategy proposals, default workhorse
- claude-opus-4-7            → critique, edge cases, board-prep level work
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any

from core import audit, limits


# Token-cost table in USD per million tokens. Update when pricing changes.
_PRICE = {
    "claude-haiku-4-5-20251001":  {"in": 1.00, "out": 5.00,  "cache_read": 0.10},
    "claude-sonnet-4-6":          {"in": 3.00, "out": 15.00, "cache_read": 0.30},
    "claude-opus-4-7":            {"in": 15.00, "out": 75.00, "cache_read": 1.50},
}


@dataclass
class LLMResult:
    text: str
    model: str
    tokens_in: int
    tokens_out: int
    cache_read_tokens: int
    cost_usd: float
    raw: dict[str, Any]

    def parse_json(self) -> dict[str, Any]:
        """Parse the model output as JSON. Tolerates code fences and trailing
        prose. Returns {} on failure (the caller decides if that's fatal)."""
        return _extract_json(self.text)


def _extract_json(text: str) -> dict[str, Any]:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fenced:
        candidate = fenced.group(1)
    else:
        m = re.search(r"\{.*\}", text, re.S)
        candidate = m.group(0) if m else ""
    if not candidate:
        return {}
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return {}


def _is_dry_run() -> bool:
    return os.environ.get("OKR_MONITOR_DRY_RUN", "true").lower() == "true"


def _price(model: str, tokens_in: int, tokens_out: int, cache_read: int) -> float:
    p = _PRICE.get(model)
    if not p:
        return 0.0
    return (
        (tokens_in - cache_read) * p["in"] / 1_000_000
        + cache_read * p["cache_read"] / 1_000_000
        + tokens_out * p["out"] / 1_000_000
    )


def complete(
    *,
    system: str,
    user: str,
    model: str,
    max_tokens: int = 2048,
    temperature: float = 0.4,
    run_id: str | None = None,
    agent: str = "unknown",
    action: str = "llm.complete",
    cache_system: bool = True,
    mock_response: str | None = None,
) -> LLMResult:
    """Make one Claude call. In dry-run mode, returns `mock_response` (or a
    stub envelope) without contacting the API."""
    if _is_dry_run():
        text = mock_response if mock_response is not None else _default_mock(action)
        result = LLMResult(
            text=text, model=f"{model}::DRY_RUN",
            tokens_in=len(system) // 4 + len(user) // 4,
            tokens_out=len(text) // 4,
            cache_read_tokens=0, cost_usd=0.0, raw={"dry_run": True},
        )
        audit.emit(run_id=run_id, agent=agent, action=action, model=result.model,
                   tokens_in=result.tokens_in, tokens_out=result.tokens_out,
                   cost_usd=0.0, payload={"dry_run": True})
        return result

    # Daily LLM circuit breaker — check before spending. Raises
    # limits.CircuitBreakerOpen if today's cap has been reached. Caller
    # decides whether to fail loud or fall back to dry-run.
    try:
        limits.check_or_raise()
    except limits.CircuitBreakerOpen as exc:
        audit.emit(
            run_id=run_id, agent=agent, action=f"{action}.circuit_breaker_open",
            severity="alert", payload={"reason": str(exc)},
        )
        raise

    from anthropic import Anthropic

    client = Anthropic()
    system_block: list[dict[str, Any]] = [{"type": "text", "text": system}]
    if cache_system:
        system_block[0]["cache_control"] = {"type": "ephemeral"}

    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_block,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(
        block.text for block in resp.content if getattr(block, "type", None) == "text"
    )
    usage = resp.usage
    tokens_in = getattr(usage, "input_tokens", 0) or 0
    tokens_out = getattr(usage, "output_tokens", 0) or 0
    cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
    cost = _price(model, tokens_in, tokens_out, cache_read)

    # Record spend toward today's circuit-breaker cap before returning.
    limits.record_spend(cost)

    audit.emit(
        run_id=run_id, agent=agent, action=action, model=model,
        tokens_in=tokens_in, tokens_out=tokens_out, cost_usd=cost,
        payload={"cache_read_tokens": cache_read,
                 "stop_reason": getattr(resp, "stop_reason", None),
                 "daily_spent_usd_after": round(limits.spent_today(), 4),
                 "daily_cap_usd": limits.daily_cap_usd()},
    )
    return LLMResult(
        text=text, model=model, tokens_in=tokens_in, tokens_out=tokens_out,
        cache_read_tokens=cache_read, cost_usd=cost,
        raw={"id": resp.id, "stop_reason": getattr(resp, "stop_reason", None)},
    )


def _default_mock(action: str) -> str:
    """Canned proposals by action so dry-run pipelines produce sensible JSON.
    Each strategy agent's pipeline keys off its action verb."""
    if "weekly_priorities" in action:
        return json.dumps({
            "title": "Week of 2026-04-28: Lock the discovery loop, start ingestion plumbing",
            "summary": "Sprint 0 starts. The single biggest risk is OKR-Mapper precision (KR1.3) — every other KR depends on it. Front-load the eval set this week.",
            "priorities": [
                {"rank": 1, "what": "Run 10 discovery calls by Friday", "owner_pod": "Product/Design", "kr": "1.4", "why": "ICP isn't truly locked until we hear pain in the buyer's words."},
                {"rank": 2, "what": "Ship the 200-event labeled eval set for OKR-Mapper", "owner_pod": "AI/Data", "kr": "1.3", "why": "Build the ruler before building the thing being measured."},
                {"rank": 3, "what": "GitHub + Linear OAuth working in dev", "owner_pod": "Engineering", "kr": "1.1", "why": "These two integrations are the demo. Slack/Notion can wait one more day."}
            ],
            "risks_to_watch": ["DRY_RUN: scope creep on integrations beyond the four MVP sources"],
            "decisions_needed_from_operator": ["DRY_RUN: confirm Mooncamp is in or out of the v1 OKR import"],
            "confidence": 0.7,
            "reasoning": "DRY_RUN: based on TRACKER.md §2 (KR weights) and §9 (top risk = OKR-Mapper precision)."
        })
    if "roadmap_review" in action:
        return json.dumps({
            "title": "Roadmap pressure test — Sprint 0 scope still fits in 14 days",
            "summary": "Current MVP scope is achievable but tight. Two items are at risk: forecasting and Notion ingestion. Recommend deferring forecasting to Sprint 1.",
            "scope_changes": [
                {"action": "defer", "item": "Forecasting agent (Monte Carlo)", "to": "Sprint 1", "why": "DRY_RUN: not on the demo critical path; narrative + drift score is the wow."},
                {"action": "keep", "item": "Notion OKR import", "why": "DRY_RUN: 60% of ICP keeps OKRs in Notion."}
            ],
            "confidence": 0.65,
            "reasoning": "DRY_RUN: stub."
        })
    if "architecture_review" in action:
        return json.dumps({
            "title": "Architecture check — 3 risks flagged",
            "summary": "Stack choice is sound. Three risks: integration auth scope, LLM cost on long-tail accounts, and ingestion idempotency.",
            "risks": [
                {"area": "integrations", "risk": "DRY_RUN: GitHub App scopes default too broad", "mitigation": "request only repo:read + metadata"},
                {"area": "cost", "risk": "DRY_RUN: large customers may 10x token spend", "mitigation": "cap re-mapping frequency and use Haiku for relinks"},
                {"area": "data", "risk": "DRY_RUN: webhook retries could double-insert events", "mitigation": "idempotency key on (source, source_event_id)"}
            ],
            "confidence": 0.75,
            "reasoning": "DRY_RUN: stub."
        })
    if "pricing_model" in action or "unit_economics" in action:
        return json.dumps({
            "title": "Pricing v0 proposal — three tiers, anchor on Team",
            "summary": "Recommend $0 pilot for 60 days, then Starter $299/mo (≤10 contributors), Team $899/mo (≤50), Scale $2,499/mo (≤200). Anchor pricing conversation on Team.",
            "tiers": [
                {"name": "Pilot", "price_usd": 0, "duration": "60 days", "limits": "any size"},
                {"name": "Starter", "price_usd": 299, "limits": "≤10 contributors, 2 integrations"},
                {"name": "Team", "price_usd": 899, "limits": "≤50 contributors, all integrations"},
                {"name": "Scale", "price_usd": 2499, "limits": "≤200 contributors, SSO, audit log"}
            ],
            "cac_payback_assumption_months": 5.5,
            "confidence": 0.55,
            "reasoning": "DRY_RUN: stub. Real pricing needs willingness-to-pay signal from the 10 discovery calls."
        })
    return "{}"
