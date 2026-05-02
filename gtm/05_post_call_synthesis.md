# 05 — Post-Call Synthesis

> Every discovery call produces a structured artifact within 60 minutes of call-end. This is non-negotiable — call N+1 is sharper than call N only if call N's lessons are captured before the next call starts. The transcript is not a substitute; the transcript is the input.
>
> The artifact has three jobs: (a) decide what we tell this prospect next, (b) feed the agent loop so the next round of outreach gets sharper, (c) update TRACKER.md so the company has a single source of truth for the pipeline.

---

## 1. The capture template

> Save as `gtm/calls/YYYY-MM-DD_company-slug.md`. (Folder created on first use; one file per call.) The transcript stays in Granola; this file is the operator's judgment on top.

```markdown
---
date: 2026-05-04
company: Acme Devtools
contact:
  name: Riya Patel
  title: Head of Operations
  email: riya@acmedev.com
tier: 1
category: C3
duration_min: 30
recorded: true
disposition: health_check_yes  # health_check_yes | revisit_q3 | no | no_show
---

## TL;DR

[2 sentences. The first names the buyer's pain in their words.
The second names the next step.]

## Verbatim language (from transcript)

- **Noun for the OKR doc:** "the goals doc"
- **Verb for staleness:** "rotting"
- **Drift moment (Q9 of interview guide):** [direct quote, ≤30 words]
- **What the CEO asks them on Monday:** "what shipped against [KR]"
- **Their stack:** GitHub ✓ · Linear ✓ · Slack ✓ · Notion ✓ (4/4)

## The 5-in-5 output (Block 5 of interview guide)

- **Objective they picked:** [their qualitative O statement]
- **3 KRs they wrote in 90 sec:**
  1. [verbatim]
  2. [verbatim]
  3. [verbatim]
- **The one they self-cleaned, before vs after:**
  - Before: [verbatim]
  - After:  [verbatim]
- **Operator note:** [what the cleanup tells us about their KR maturity]

## Pain rank (operator judgment)

- Top-3 priority for them this quarter? **[yes / no / unclear]**
- Did they name a real drift moment unprompted? **[yes / no]**
- Did the 5-in-5 produce a real edit they'll keep? **[yes / no]**
- Stack fit for our integrations (3-of-4 minimum)? **[yes / no]**
- ICP fit overall (rubric in target list §0)? **[yes / no]**

## Anti-signals (the gold)

[Where did they bristle? What did they avoid answering? What
defensive language showed up? These are more valuable than the
positive signals — they're the gaps in the product or the pitch
that have to be addressed.]

- [bullet]
- [bullet]

## Objections raised + how operator handled

| # | Objection (verbatim) | Response | Verdict (resolved / parked / open) |
|---|---|---|---|

## Next step (committed)

- **Action on operator:** [send Health Check intake] [by [date+time]]
- **Action on buyer:** [send OKR doc + integrations list] [by [date]]
- **Brief delivery target:** [date+2 business days]
- **Calendar:** [next call booked? — link / not yet]

## Quotes worth saving (for case-study or copy)

[2-4 verbatim sentences worth lifting. Track these — these are the
lines that become next quarter's homepage headline.]

> "[verbatim]"
> — [name], [title], [company]

## What I'd ask differently next call

[1-3 bullets. Operator self-feedback. The script in interview_guide.md
gets revised when patterns emerge across 5 calls.]
```

---

## 2. The 60-minute discipline

The capture happens **within 60 minutes of call-end**. Not "by end of day." Not "tomorrow morning." Reasons:

1. The verbatim language is fading by minute 90. By tomorrow it's reconstructed (i.e. wrong).
2. The "what I'd ask differently" insight is sharpest right after the call. By tomorrow it's filed under "we always do this."
3. Compounding: if calls 1–5 are captured properly, the script for call 6 is materially better. If 1–5 are skimmed, every call is call 1.

If the next call starts in <60 min — capture in 10 minutes (TL;DR + verbatim language + next step), expand to full template that night.

---

## 3. The feedback loop into the agent system

> Captured calls do **double duty**: they're the operator's pipeline tracking AND the input that makes the agents better. The whole system gets smarter only if both happen.

### 3a. Update the CRM row

Open `gtm/crm.csv` (TBD; for Sprint 0 a Notion table works) and update:

| Column | New value |
|---|---|
| status | `discovery_done` → `health_check_sent` (after we send intake) |
| disposition | match capture front-matter |
| next_action | match capture "Next step" section |
| next_action_date | match same |
| call_artifact_path | `gtm/calls/YYYY-MM-DD_company-slug.md` |

### 3b. Update TRACKER.md §8 (customer pipeline)

When a buyer says "yes, run the Health Check," they enter the design-partner pipeline. Add a row to `TRACKER.md` §8:

```
| Acme Devtools | Riya Patel (Head of Ops) | Health-check-pending | GitHub+Linear+Slack+Notion | "the goals doc is rotting" |
```

When the Health Check ships, status flips to `pilot-pending`. When they sign as a design partner, `active`.

### 3c. Feed the agent loop

The captured artifacts feed three agents:

| Agent | What it consumes | What it produces |
|---|---|---|
| **`founder_sales`** | Last 5 capture files | Refreshed outreach drafts using the new verbatim language. Operator approves before send. |
| **`ux_researcher`** | All capture files (rolling 30 days) | Discovery synthesis — JTBD clusters, anti-signal heatmap, frequency of named pains. Becomes the input to copy revisions and roadmap. |
| **`copywriter`** | The "Quotes worth saving" sections, all calls | New homepage / cold-email subject-line variants grounded in real customer language. |

Until those agent runs are wired into a cron, the operator triggers them manually after every 5th call:

```bash
python scripts/run_ux_researcher.py
python scripts/run_founder_sales.py
python scripts/run_copywriter.py
```

The agents read `gtm/calls/*.md` directly. They do **not** parse the transcripts — the operator's judgment in the structured fields is the input.

---

## 4. Five-call retro (Friday cadence)

Every Friday during Sprint 0 + Sprint 1, the operator runs a 30-min retro on the last 5 calls.

### Retro template (write to `gtm/retros/YYYY-MM-DD_5call.md`)

```markdown
# 5-call retro — week of [Monday-Friday]

## Calls
1. [link to capture]
2. [link to capture]
3. [link to capture]
4. [link to capture]
5. [link to capture]

## Funnel ratios
- Booked → discovery: [N/N]
- Discovery → Health Check yes: [N/5]
- Stack fit (3-of-4 or better): [N/5]
- Drift moment named unprompted: [N/5]
- Pain ranked top-3: [N/5]

## Patterns

### Repeated language (≥3 calls)
- [verbatim phrase]
- [verbatim phrase]

### Repeated objections (≥2 calls)
- [objection] — current handling [link to script]

### Repeated anti-signals (≥2 calls)
- [bullet]

## Script edits to commit

- [interview_guide §X edit]
- [outreach_scripts §Y edit]
- [target_list §Z edit]

## Operator note to self

[1-3 sentences. The hardest call this week and what was learned.]
```

The script edits get **committed to the repo** — not just noted. After 20 calls, the discovery script is materially better than the day-1 draft.

---

## 5. The "kill list" — calls that don't go to design partner

Half of well-run discovery calls end without a Health Check yes, and that's healthy. The capture for those calls is **especially** valuable because they tell us what the product/positioning is missing.

### When the disposition is `no` or `revisit_q3`, capture this extra section:

```markdown
## Why not now (be honest)

- The actual reason (in their words): [verbatim]
- Operator interpretation: [bullet]
- Is this a "we have the wrong product" signal or a "wrong quarter for them" signal? [pick]
- If wrong product: what would have flipped it?
- If wrong quarter: re-touch trigger date: [date]
```

After 5 `no` calls, look for the pattern. If 4-of-5 are "wrong product" reasons that point at the same gap, that's a Sprint-1 backlog item, not a closing problem.

---

## 6. Anti-patterns

| Don't | Why | Do instead |
|---|---|---|
| Treat the transcript as the artifact | Transcripts are unstructured; agents and ops-future-you need structured. | Fill the template even if the transcript is perfect. |
| Skip the "what I'd ask differently" section | This is the call-1-vs-call-20 lever; skipping it means the script never improves. | Force a bullet, even if it's "nothing." Saying "nothing" 5 times in a row is itself a signal that you've stopped paying attention. |
| Capture only the wins | The kill-list captures are where the product fixes come from. | Capture the no's with the same rigor as the yeses. |
| Wait until end-of-day to capture | Memory is already reconstructed by then. | 60-min discipline. |
| Embellish quotes | "Saved" quotes get reused in cold emails; if they're not verbatim, the buyer notices the next call. | Copy from the transcript, character-exact. |

---

## 7. What good looks like (after 20 calls)

- 20 capture files in `gtm/calls/`. Every one with all sections filled.
- 4 retro files in `gtm/retros/`. Each ending in committed script edits.
- The `ux_researcher` agent's discovery-synthesis output names 3–5 JTBD clusters with confidence ≥0.7, evidence pulled from ≥3 calls each.
- The `founder_sales` agent's outreach drafts use language from the capture files (not the operator's drafts) — verifiable by quoting.
- TRACKER.md §8 has 5+ named design-partner candidates, status across the funnel.
- The Friday brief on our own dogfood KRs (KR1.2 design partners) starts moving from `🔴 Not started` to `active`.

---

## 8. Linkage

- Source of bookings: [`02_outreach_scripts.md`](02_outreach_scripts.md).
- The call this synthesizes: [`03_interview_guide.md`](03_interview_guide.md).
- Calendaring + intake handoff: [`04_calendaring.md`](04_calendaring.md).
- Customer-facing framework referenced in the call: [`notion/03_playbooks/01_customer_okr_kpi_framework.md`](../notion/03_playbooks/01_customer_okr_kpi_framework.md).
- Pilot intake form (Health Check trigger): [`notion/03_playbooks/04_pilot_intake_questionnaire.md`](../notion/03_playbooks/04_pilot_intake_questionnaire.md).
- The agents that consume captures: [`agents/ux_researcher/`](../agents/ux_researcher/), [`agents/founder_sales/`](../agents/founder_sales/), [`agents/copywriter/`](../agents/copywriter/).
- KR moved by this work: TRACKER.md KR1.2 (5 active design partners by 2026-05-19) and KR4.3 (dogfood-discovered gaps → backlog within 24h).
