# 60-day pilot kickoff playbook

> The standard playbook for every pilot. Customized per-customer by the `onboarding` agent before the kickoff call.

---

## Day -3 to Day 0 — pre-kickoff

| Day | What happens | Owner |
|---|---|---|
| -3 | Customer signs the pilot agreement (DPA + 60-day terms). | Operator |
| -2 | Customer sends the 5-item kickoff packet (OKR doc link, GitHub org, Linear/Jira workspace, Slack channel names, quarter-end date). | Customer |
| -1 | We run [KB mining](02_kb_mining_during_onboarding.md) and generate the sample OKR Health Check. | Operator |
| 0 | **Kickoff call** — 45 min. Agenda below. | Both |

---

## Kickoff call agenda (45 min)

| Window | Topic | Decision point |
|---|---|---|
| 0:00–0:05 | Intros, restate the pilot ask, confirm 60-day duration. | — |
| 0:05–0:15 | Walk the OKR Health Check we generated against their data. Flag any KRs missing baseline/target/date. | Cleanup commitment. |
| 0:15–0:25 | Walk the weekly cadence (Friday brief + Monday standup). Show what changes (almost nothing). | Brief delivery time confirmed. |
| 0:25–0:35 | Confirm recipients + Slack delivery channel. | Recipient list signed. |
| 0:35–0:45 | First-week milestones (see below) + open Qs. | First-week plan signed. |

**Customer leaves the call with:** a sample brief on their data, a cleaned-up OKR doc commitment for end of week 1, and a milestone plan for the next 60 days.

---

## First-value moment

Specific to each pilot, but always one of:

- "I forwarded the brief to the CEO without editing it." (the screenshot moment)
- "I cancelled my Monday status meeting." (the time moment)
- "We restated KR-X in week 3 because the brief made the drift visible." (the action moment)

The `onboarding` agent identifies which of the three is most likely for a given pilot based on their context (team size, OKR maturity, current standup format) and tailors the kickoff to set up that specific moment.

---

## First-week milestones (Days 1–7)

| Day | Milestone | Observable signal in our telemetry |
|---|---|---|
| D+1 | All integrations connected (GitHub, Linear/Jira, Slack, Notion). | `integrations_connected = 4/4` in tenant settings. |
| D+2 | OKR doc cleanup complete (baselines + targets + dates filled in). | `kr_signals` shows `target_numeric IS NOT NULL` for ≥80% of KRs. |
| D+3 | Customer reads the first daily 7 PM brief. | Email open + dashboard view event. |
| D+5 | First Friday brief lands in inbox + recipients' inboxes. | `narrative` row written + email send_status = sent. |
| D+7 | Customer attends a 15-min "first brief retro" call with us — what landed, what didn't. | Calendar event held. |

**If any milestone slips by 2+ days, the `pilot_pm` agent flags it as `at_risk` in the Thursday review.**

---

## Day-7 retro (15 min)

Single agenda item: **"Did the brief give you something you didn't already know?"**

If **yes** — what specifically? (Capture verbatim — these become the testimonial bank.)
If **no** — diagnose: was it the OKR doc (not measurable), the integrations (not enough signal), or the model (mappings wrong)? Decide which.

We ask the customer to forward the brief to one peer in their network. Not a referral ask — a "tell me what they said" ask. The peer's first reaction is the most honest signal we get.

---

## Days 8–28 — soak window

Mostly hands-off. Brief lands every Friday. Daily 7 PM digest lands.

We monitor in our telemetry:
- Weekly brief read rate (target: ≥80%).
- Monday standup attendance (we ask in week 4: "did you keep doing it?").
- Slack reactions to the brief in `#general` (qualitative signal).
- Any in-product feedback messages.

We **do not** push for expansion in this window. The pilot is real, the brief is honest, that's the work.

---

## Day 28 check-in (30 min)

Agenda:

1. **Review the trailing 4 briefs together.** Which verdicts were right, which were off, which surprised?
2. **What changed in their behavior?** Cancelled meetings? Restated KRs? New decisions made?
3. **Who else inside their company is reading the brief now?** (Tracks viral coefficient.)
4. **What's the one thing they wish the brief did?** (Single highest-priority feature ask.)

Outcome: a structured note added to the customer's pilot record. The `pilot_pm` agent reads this in week 5 and starts setting up the day-60 conversation.

---

## Day 56 — the day-60 setup call (20 min)

Single agenda: "What does the next 90 days look like?"

We name three options:

| Option | What it means | When to recommend |
|---|---|---|
| **Convert** | Move to the Team tier ($899/mo). | Customer has cancelled their Monday status meeting and the brief is forwarded weekly to their CEO. |
| **Extend** | 30 more days at $0 because something is unresolved (integration broken, KR doc still messy, missed key person on summer leave). | The product is working but the customer hasn't had a chance to react to it. |
| **Off-ramp** | Decline the pilot. We turn off the integrations within 24 hrs. We ask for one specific reason and add it to the rolling "wrong-fit signals" doc. | Customer is wrong-fit, or the product hasn't moved their behavior. |

**There is no soft sell.** If the customer is unsure between convert and extend, we recommend extend. If they're unsure between extend and off-ramp, we recommend off-ramp. Pre-launch, we'd rather have 25 great pilots than 50 lukewarm ones.

---

## Day 60 — decision

Customer signs the next-step doc (Convert / Extend / Off-ramp).

For Convert pilots:
- Card on file via Stripe.
- Move to Team tier (or up if scope warrants).
- Permanent dashboard access.
- Continued support, but reduced touch (we step out; the product carries it).

For Extend pilots:
- New 30-day end date.
- One named reason in the doc.
- Same review at Day 90.

For Off-ramp pilots:
- Integrations disabled, data preserved for 30 days then deleted.
- Single thank-you email.
- Reason logged in our wrong-fit signals doc.

---

## Pilot health monitoring throughout

The `pilot_pm` agent runs every Thursday and emits a `pilot_milestone_review` proposal that classifies every active pilot:

- `on_track` — meeting milestones, reading briefs, integrations healthy
- `at_risk` — gap of ≥10 days in any signal; intervention proposed
- `dormant` — silent ≥21 days; breakup email drafted
- `converting` — actively asking about pricing or expansion

The review hits the operator's queue (`python -m cli.review`). The operator approves the proposed interventions or edits them.

---

## Pre-launch caveat

Until we have any pilots running, this playbook is a **template** that the `onboarding` agent generates per-customer in dry-run mode. The first real pilot kickoff (target: 2026-05-19) will produce the first real customized version. Iterate from there.
