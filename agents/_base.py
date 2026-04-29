"""Shared scaffolding for strategy-pod agents.

Each agent calls one LLM with:
- a stable system prompt (its role + company.yaml + TRACKER.md) — cached
- a user message naming the specific question for this run

This module assembles the system block and snapshots the tracker so we can
later replay any proposal against the exact tracker state it reasoned over.
"""

from __future__ import annotations

import yaml

from core import audit, config, store, tracker


_SYSTEM_TEMPLATE = """\
{agent_prompt}

---

## Company identity (do not restate; absorb)

```yaml
{company_yaml}```

---

## Live state — TRACKER.md (the single source of truth)

This is the canonical tracker for the company. Reason over it. KR IDs (e.g.
"KR1.3") refer to specific cells in §2. Quote them by ID when justifying
your proposal.

```markdown
{tracker_md}```
"""


def build_system_prompt(*, agent_prompt_md: str) -> str:
    """Compose the cacheable system block. The output is intentionally large
    and stable — that's what makes prompt caching pay off across the four
    strategy agents in one run."""
    return _SYSTEM_TEMPLATE.format(
        agent_prompt=agent_prompt_md.strip(),
        company_yaml=yaml.safe_dump(config.company(), sort_keys=False),
        tracker_md=tracker.load_text(reload=True),
    )


def snapshot_tracker(*, run_id: str, agent: str) -> tuple[str, bool]:
    """Record the exact tracker contents this run is reasoning over. Returns
    (snapshot_id, was_new). Idempotent on content."""
    content = tracker.load_text(reload=True)
    sid, was_new = store.upsert_tracker_snapshot(content)
    audit.emit(
        run_id=run_id, agent=agent, action="tracker.snapshot",
        payload={"snapshot_id": sid, "was_new_content": was_new},
    )
    return sid, was_new
