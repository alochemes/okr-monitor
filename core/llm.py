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
    if "map_event" in action:
        # Stub mapping that ties any event to KR4.1 (dogfood) — useful for
        # exercising the end-to-end flow in dry-run.
        return json.dumps({
            "mappings": [
                {"kr_id": "4.1", "confidence": 0.85,
                 "reasoning": "DRY_RUN: stub maps every event to KR4.1 to exercise the dogfood loop."}
            ]
        })
    if "weekly_narrative" in action:
        return json.dumps({
            "title": "DRY_RUN: weekly narrative stub",
            "verdict_summary": "DRY_RUN: cannot judge real progress without live model output.",
            "kr_verdicts": [
                {"kr_id": "4.1", "verdict": "on_track",
                 "narrative": "DRY_RUN: stub narrative — every event mapped to this KR.",
                 "events_count": 0}
            ],
            "alignment_score_pct": 0,
            "alignment_commentary": "DRY_RUN.",
            "what_to_do_next_week": "DRY_RUN: enable live LLM and re-run narrative.",
            "confidence": 0.1,
            "reasoning": "DRY_RUN."
        })
    if "user_stories" in action:
        return json.dumps({
            "title": "DRY_RUN: Sprint 0 stories — top 5 stub",
            "summary": "DRY_RUN stub — real sprint stories require live model.",
            "stories": [{"as_a": "operator", "i_want": "real LLM output",
                         "so_that": "I can review actual proposals", "kr": "1.1",
                         "acceptance": ["DRY_RUN", "DRY_RUN"]}],
            "stories_cut": ["DRY_RUN"], "decisions_needed_from_operator": [],
            "confidence": 0.1, "reasoning": "DRY_RUN."
        })
    if "discovery_synthesis" in action:
        return json.dumps({
            "title": "DRY_RUN: discovery synthesis stub",
            "summary": "DRY_RUN stub — real synthesis requires call notes.",
            "jtbd_clusters": [{"job": "DRY_RUN cluster", "frequency": 0.0,
                               "intensity": 0.0, "evidence": ["DRY_RUN"]}],
            "anti_signals": ["DRY_RUN anti-signal"], "icp_refinements": [],
            "decisions_needed_from_operator": [], "confidence": 0.1,
            "reasoning": "DRY_RUN."
        })
    if "copy_draft" in action:
        return json.dumps({
            "title": "DRY_RUN: copy draft stub",
            "summary": "DRY_RUN — 3 stub variants.",
            "variants": [
                {"id": "A", "angle": "stub", "text": "DRY_RUN headline A",
                 "rationale": "DRY_RUN."},
                {"id": "B", "angle": "stub", "text": "DRY_RUN headline B",
                 "rationale": "DRY_RUN."},
                {"id": "C", "angle": "stub", "text": "DRY_RUN headline C",
                 "rationale": "DRY_RUN."}
            ],
            "operator_pick_recommended": "A", "confidence": 0.1,
            "reasoning": "DRY_RUN."
        })
    if "outreach_drafts" in action:
        return json.dumps({
            "title": "DRY_RUN: 5 outreach drafts (templates) stub",
            "summary": "DRY_RUN — generic templates.",
            "drafts": [{"persona": "Chief of Staff at {company}",
                        "artifact_hook": "{recent_artifact}",
                        "subject": "DRY_RUN subject",
                        "body": "DRY_RUN body with {placeholder}.",
                        "rationale": "DRY_RUN."}],
            "follow_up_cadence_suggested": "T+3, T+7, T+14",
            "expected_reply_rate_pct": 0.0, "confidence": 0.1,
            "reasoning": "DRY_RUN."
        })
    if "cold_sequence" in action:
        return json.dumps({
            "title": "DRY_RUN: 5-touch cold sequence stub",
            "summary": "DRY_RUN — stub sequence.",
            "segment": {"persona": "DRY_RUN", "company_archetype": "DRY_RUN",
                        "trigger_event": "DRY_RUN"},
            "touches": [{"n": 1, "day": 1, "channel": "email",
                         "subject_or_opening": "DRY_RUN subject",
                         "body": "DRY_RUN body.", "thesis": "DRY_RUN."}],
            "expected_reply_rate_pct": 0.0, "confidence": 0.1,
            "reasoning": "DRY_RUN."
        })
    if "blog_post_draft" in action:
        return json.dumps({
            "title": "DRY_RUN: blog post draft stub",
            "summary": "DRY_RUN — stub post.",
            "outline": ["DRY_RUN section 1", "DRY_RUN section 2"],
            "first_draft_md": "DRY_RUN body.",
            "anchor_stat": "DRY_RUN", "named_anti_pattern": "DRY_RUN",
            "proprietary_frame": "DRY_RUN",
            "social_pull_quote": "DRY_RUN pull quote",
            "seo_keywords": ["DRY_RUN"], "target_word_count": 900,
            "actual_word_count": 0, "confidence": 0.1, "reasoning": "DRY_RUN."
        })
    if "pilot_milestone_review" in action:
        return json.dumps({
            "title": "DRY_RUN: pilot health stub (no pilots yet)",
            "summary": "DRY_RUN — 0 pilots, template review.",
            "pilots_on_track": [], "pilots_at_risk": [],
            "pilots_dormant": [], "pilots_converting": [],
            "decisions_needed_from_operator": [
                "DRY_RUN: confirm pilot intake form schema before week 1 design partner."
            ],
            "confidence": 0.2, "reasoning": "DRY_RUN — 0 active pilots."
        })
    if "onboarding_playbook" in action:
        return json.dumps({
            "title": "DRY_RUN: onboarding playbook v1 stub",
            "summary": "DRY_RUN — generic playbook for default ICP.",
            "pilot_context": {"company": "DRY_RUN Co", "size": "200",
                              "okr_tool": "Notion",
                              "integrations": ["GitHub", "Linear", "Slack"],
                              "stated_goal": "DRY_RUN goal"},
            "kickoff_agenda": [{"window": "0:00-0:05", "topic": "intros",
                                "decision_point": None}],
            "first_value_moment": "DRY_RUN: first auto-narrative read within 30 min.",
            "first_week_milestones": [{"day": "D+1",
                                       "milestone": "DRY_RUN milestone",
                                       "observable_signal": "DRY_RUN signal"}],
            "day_30_check_in": {"agenda": ["DRY_RUN"],
                                "success_criteria": ["DRY_RUN"]},
            "day_60_decision": {"options": ["convert", "extend", "off-ramp"],
                                "criteria": "DRY_RUN."},
            "confidence": 0.3, "reasoning": "DRY_RUN."
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
