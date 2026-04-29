# Knowledge-base mining during onboarding

> How we mine a customer's existing knowledge base (Notion, Confluence, Google Drive) to bootstrap their OKR Monitor instance on day one.
>
> **Status:** internal playbook. Manual for the first 10 pilots; automated thereafter via a `kb_miner` agent (planned).

---

## Why we do this

A pilot's first impression is set by what they see in the first 30 minutes. If they connect their tools and see *empty* dashboards, the product feels theoretical. If they see their **own** OKRs already mapped to their **own** recent commits and tickets, the product feels inevitable.

Knowledge-base mining is the bridge — we walk into pilot day 1 with their KRs already imported, their last 30 days of work already mapped, and a draft Friday brief already generated. They get to react to a real artifact, not a blank page.

---

## What counts as a "knowledge base"

Anything that documents the *strategy* of how the company wants to operate, distinct from the *execution* (which lives in code/tickets/conversations). Common surfaces:

| Surface | What we look for |
|---|---|
| Notion workspace | Quarterly plans, OKR pages, team OKR pages, project pages, retros |
| Confluence | Same — quarterly plans, project briefs |
| Google Docs / Drive | OKR docs, board updates, all-hands decks, project briefs |
| GitHub `/docs` | RFCs, architecture decision records (ADRs), team READMEs |
| Coda | OKR + project docs |
| Mooncamp / Lattice / 15Five / Workboard | Direct OKR sources — easiest case |

We do **not** mine: HR docs, compensation, individual performance reviews, customer-confidential data, anything tagged `#confidential` or in a private personal folder.

---

## The 4-step mining process

### Step 1 — Discovery (operator-led, ≤30 min)

Operator (us) joins a 30-min call with the customer's CoS / Head of Ops.

The single ask: **"Walk me through where your OKRs live and where work updates happen — show me the actual pages."**

We screen-share their workspace and take notes on:

| Question | Why it matters |
|---|---|
| Which Notion page is the canonical OKR doc this quarter? | Source of KRs. |
| Are there team-level OKR pages that roll up? | Whether to mine them too. |
| Where do projects live? Per-team Notion subpages? Linear projects? | Source of work-event-to-KR linkage hints. |
| Is there a shared "weekly update" or "Friday note" already? | Tells us the format the customer expects. |
| Who has edit rights? Who has view rights? | OAuth scope — we ask for view-only on the right pages. |

Output: a one-page mining plan with named source pages and access requirements.

### Step 2 — Connection (customer-led, ≤15 min)

Customer connects Notion (and optionally Google Drive, Confluence) via OAuth. We default to **page-level access** — no workspace-wide tokens.

For the first 10 pilots we do this manually:
- Customer shares the specific Notion pages with our `okr-monitor@<their-workspace>.notion.site` integration user.
- We scrape via the Notion API on those specific pages only.
- Audit log records every page we touched.

Once the `kb_miner` agent ships, this becomes a one-click OAuth flow.

### Step 3 — Extraction (us, ≤2 hours)

We pull from each source page:

#### From the OKR doc:

For each Objective:
- Objective text (cleaned of formatting noise)
- Owner (if listed)
- Set-date and review-date

For each KR under each Objective:
- KR text
- Baseline (if explicit)
- Target (if explicit)
- Due date (if explicit)
- Owner (if listed)
- Current value (if recorded)

We **flag** any KR that's missing baseline, target, or due date. Those go into a "needs-cleanup" list we walk through with the customer in the kickoff call (using the OKR framework playbook).

#### From project pages:

- Project title, owner, status
- Linked KRs (if explicit)
- Last-updated date — anything stale >30 days gets noted as "possibly orphaned"

#### From the weekly-update doc (if it exists):

- The customer's existing format and tone — we mirror it in our brief styling so it feels familiar.

### Step 4 — Pre-population (us, automated)

We import everything into the customer's OKR Monitor tenant:

```
notion_kr → kr_signals row (target_raw, target_numeric if parseable, due_date, current_numeric)
notion_project_page → work_event row (source: "notion_project", kind: "project_status")
notion_weekly_update → work_event row (source: "notion_doc", kind: "weekly_note")
```

Then run the OKR-Mapper across the imported `work_events` so the customer's KRs already have **30 days of recent activity already mapped** when they log in.

Then run the Narrative agent to generate a sample Friday brief against the imported KRs + mappings. This is what they see at pilot kickoff (Step 5 below).

---

## Step 5 — The kickoff call

A 45-minute call. Agenda:

| Window | Topic | Decision point |
|---|---|---|
| 0:00–0:05 | Intros + restate the pilot ask | — |
| 0:05–0:15 | Walk through the **OKR Health Check** — the sample brief we generated against their data. We flag the KRs that need cleanup (missing baseline / target / due date) and the work that didn't map to any KR (orphan signal). | Customer agrees to clean up flagged KRs by end of week 1. |
| 0:15–0:30 | Walk the canonical OKR Monitor weekly cadence (Friday brief, Monday standup). Show what changes vs. their current process (almost nothing — they keep their OKR doc and tools). | Customer confirms Friday 9 AM their time as the brief delivery slot. |
| 0:30–0:40 | Decide who else gets the brief — usually CEO + 1–2 leaders. | Customer names recipients. |
| 0:40–0:45 | Open Qs + first-week milestones (see [Pilot Kickoff playbook](03_pilot_kickoff_60_days.md)). | First-week milestone list signed. |

Outcome: pilot is live, the customer's first real Friday brief lands 3–7 days after this call.

---

## What we do NOT mine

We're conservative about scope to keep trust intact and avoid surprise:

- ❌ HR / people pages
- ❌ Compensation
- ❌ Individual performance reviews
- ❌ Customer-confidential data (named customers in support tickets unless customer opt-in)
- ❌ Slack DMs (only public + opted-in private channels)
- ❌ Anything in a Notion page tagged `#confidential` or in a `Confidential/` parent
- ❌ Personal task pages (Notion "My tasks", individual journals)

The `kb_miner` agent's first prompt rule: **when in doubt, skip and surface to operator**. False negatives (skipped a relevant page) are easy to fix; false positives (mined a sensitive page) destroy trust irrecoverably.

---

## What we tell the customer about data residency

Verbatim copy for the pilot agreement:

> Your data — including your OKR text, project pages, commits, tickets, and indexed Slack messages — is stored in your dedicated tenant database. We do not use your data to train any model. Anthropic's API (which we use for the OKR-Mapper and Narrative agents) is configured with prompt-data-used-for-training off; this is verifiable in your account's audit log on request. We retain raw data for 13 months for trend computation, then aggregate and discard.

If a pilot pushes back on any of this in the kickoff, escalate to the operator before agreeing to a workaround.

---

## When the `kb_miner` agent ships (planned)

The manual mining process becomes:

```
1. Customer connects Notion via one-click OAuth.
2. Customer selects the parent page or workspace section to mine.
3. kb_miner agent crawls — depth-bounded, scope-bounded — and emits a mining_plan proposal.
4. Operator reviews the proposal (Stage 0): which pages were chosen, what got flagged for cleanup.
5. Operator approves; mining executes; OKR-Mapper sweeps; sample brief generates.
6. Total time: 30 minutes from OAuth click to first brief.
```

The kb_miner is on the agent roadmap as a Stage 0 → Stage 1 promotion candidate (it's read-only, output is a proposal, easy to gate). See `agents/integrations_engineer/prompts/integration_design.md` for the connector spec.
