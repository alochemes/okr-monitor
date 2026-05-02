# 03 — Interview Guide (30-min discovery call)

> The call that turns a reply into a design-partner candidate. **30 minutes**, not 60. Operator runs solo for the first 10 calls; pair-runs after that as the founder_sales agent gets promoted.
>
> The framework this guide is built on lives in [`notion/03_playbooks/01_customer_okr_kpi_framework.md`](../notion/03_playbooks/01_customer_okr_kpi_framework.md). The 5-in-5 exercise (§4 of that playbook) is the closer for the call — it's what gets the prospect to choose us before the call ends.

---

## 1. The goal of this call (be ruthless)

We are NOT here to demo. We are here to answer **three questions** with hard evidence:

1. **Is this a real ICP fit?** (ICP rubric, [`01_target_list.md`](01_target_list.md) §0)
2. **Is the OKR pain real and ranked top-3 for the buyer this quarter?** If it isn't, no amount of product pitch saves the deal.
3. **Will they say yes to the OKR Health Check on this call?** (The Health Check is the design-partner intake. See `notion/03_playbooks/04_pilot_intake_questionnaire.md`.)

Anything else (pricing, integrations roadmap, security review) is for the second call.

> **Anti-goal:** convincing them. Real demand survives a 30-min Q&A pointed at the pain. Manufactured demand doesn't. Believe the call.

---

## 2. Time budget (with the clock)

| Min | Block | Buyer talks ≥ | Operator's job |
|---|---|---|---|
| 0–2 | Intro + agenda | — | Set frame: "30 min, no demo, just questions about how OKRs work at [Company]." |
| 2–8 | Their context (current state) | 80% | Listen. Ask follow-ups; don't pitch. |
| 8–14 | The OKR/work gap (the pain) | 70% | Probe for the specific story. |
| 14–18 | What they tried | 60% | Map their stack and prior attempts. |
| 18–24 | The 5-in-5 micro-exercise (live, on one O) | 50/50 | Run the exercise; this is the magic moment. |
| 24–28 | The ask (Health Check intake) | 30% | Close on the next step. |
| 28–30 | Wrap | — | Confirm what they'll send + when they'll see the brief. |

**Strict timer.** The operator opens the call with "I've got 30 min on my side, you?" — anchors the box. If buyer wants more, schedule call #2 instead of running long.

---

## 3. Block-by-block

### Block 1 (0–2 min) — Intro + agenda

```
"Thanks for the time. 30 min, no demo. I'm going to ask about how
OKRs work at [Company] today, then run a 5-min exercise on one of
your Os, then suggest a next step. Sound good?"
```

**Watch for:** they say yes; they push for a demo; they say "I'm 15 min not 30." If 15 — restate the agenda and skip Block 4 (the prior-attempts probe). Keep Block 5 (5-in-5).

### Block 2 (2–8 min) — Current state

> Open-ended; operator says ≤30 words total. Their words are the asset.

Ask in this order. Do NOT skip ahead — the answers compound.

```
1. "Walk me through how you set OKRs last quarter. Who owned the doc?"
2. "When was the last time someone read it after week 1?"
3. "How does the team know what's on track this Wednesday?"
4. "What does the CEO ask you on Monday?"
5. "What part of that question do you actually have a good answer to?"
```

**The capture:** in the call notes (Otter / Granola / Fathom auto-transcribed), star the verbatim phrasings of:
- the **noun** they use for the doc ("our OKRs," "the goals doc," "the Notion thing").
- the **verb** they use for staleness ("rotting," "drifting," "out of date," "fictional").
- the **moment** when the gap last caused real pain (specific story).

Those three become the language we use in the rest of the call AND in the post-call follow-up email. Buyers buy when their words are echoed back.

### Block 3 (8–14 min) — The OKR/work gap

> The pain — narrowed from "OKRs are hard" to "this specific Sunday I spent 3 hours reconstructing what shipped against KR-1.2."

```
6. "Last quarter, did any KR end the quarter scored differently than
    you'd have predicted at week 4?" 
   → If yes: "What happened?"
   → If no: "What's the score-vs-prediction gap typically like?"

7. "Right now, name a KR you couldn't tell me the current value of
    in 60 seconds."
   → Sit in the silence. Let them name it.

8. "When that's hard to answer, where do you go to find out?"
   → They will name 2–3 tools. Note them.

9. "Is there a moment in the quarter where a KR has clearly drifted
    but no one says it out loud yet?"
   → If yes: "How does that get surfaced?"
```

**The buyer's answer to Q9 is the load-bearing one.** If they can't name a specific drift moment, the OKR pain isn't ranked high enough — they're a future customer, not a Q2 customer. Don't push; close politely.

### Block 4 (14–18 min) — What they've tried

> Map their stack and their prior attempts. This is where demos die for the wrong reason — operator stops listening to pitch a feature. **Don't.**

```
10. "How are you tracking goals today — Notion / Asana / Mooncamp / Excel /
     in someone's head?"
11. "Have you tried any tool to bridge the OKR doc to the work?
     What happened?"
12. "Where does the team actually live? GitHub + Linear + Slack +
     Notion — which 3 of those are the daily-life tools?"
```

**Capture:** their answer to Q12 is what we use to estimate integration effort. If 4-of-4, they're a perfect fit. If 2-of-4 with the missing two being Linear/GitHub, demur — we won't have the data to map.

### Block 5 (18–24 min) — The 5-in-5 micro-exercise (live)

> This is the close. Done well, the prospect feels the product before we ship a single feature for them.

The full exercise is documented in [`notion/03_playbooks/01_customer_okr_kpi_framework.md`](../notion/03_playbooks/01_customer_okr_kpi_framework.md) §4. The compressed call version:

```
Operator (min 18):
"Pick one of your current Objectives. The one you trust least.
 Now, 90 seconds — write 3 KRs for it. Don't think — write."

[silence; share the screen if possible]

Operator (min 19:30):
"Read them to me."

[buyer reads]

Operator (min 21):
"On the rubric — numeric, observable in a system you already have,
 outcome-not-vanity — which of these 3 holds up?"

[discussion — buyer self-edits in real time]

Operator (min 23):
"That edit you just made — the change from 'improve onboarding' to
 'reduce time-to-first-value from 18 min to 4 min' — that's the cleanup
 we do with every pilot in week 1. Good KRs are the ruler before our
 brief means anything."
```

**What this does:**
- Demonstrates competence without slide-ware.
- Gives the buyer a take-home (their cleaner KR).
- Frames the next step ("the cleanup we do with every pilot").
- Earns 6 minutes of attention they wouldn't have given a demo.

### Block 6 (24–28 min) — The ask

```
"Two next steps, depending on what you want.

 Option A — fast: I generate an OKR Health Check for [Company].
   You send me your current OKR doc + 30 days of GitHub + Linear
   + Slack history. Two business days later you get back a sample
   Friday brief on your real data, plus a flagged-cleanup list for
   the OKR doc itself.

 Option B — slow: we do another call in 2 weeks once you've thought
   about it.

 The Health Check is free and the cleanup list is yours regardless
 of whether we keep working together. Which makes sense?"
```

**Almost everyone says A.** The few who say B are not in this quarter; treat as a recycled lead.

### Block 7 (28–30 min) — Wrap

```
"Three things — confirming.

 1. I'll send a 1-line follow-up tonight with the intake link.
 2. You send me [the OKR doc + integrations list] by [day].
 3. You'll have a brief on your real data by [day +2 business days].

 Anything you'd want me to ask you that I didn't?"
```

That last question often surfaces the real objection. Take it seriously.

---

## 4. The call notes — what the operator captures

> The transcription tool (Granola / Fathom / Otter) records everything. The operator's job in the next 10 minutes after the call is to fill in this template manually — auto-transcripts don't surface judgment.

Template lives in [`05_post_call_synthesis.md`](05_post_call_synthesis.md). Quick reference here:

| Capture slot | Why |
|---|---|
| **Verbatim noun for the OKR doc** | Used in follow-up email + future outreach |
| **Verbatim verb for staleness** | Same |
| **Specific drift story** (Q9) | The proof we have product-market fit if it appears in 5/10 calls |
| **Their stack (4-of-4? 3-of-4? 2-of-4?)** | Integration effort estimate |
| **The KR they self-cleaned in 5-in-5** | The opening line of the Health Check report |
| **A/B/C decision (Health Check / 2-week / no)** | Pipeline status |
| **Anti-signals** (places they bristled, defensive language, deflections) | More valuable than the positive signals — they're what the product has to address |

---

## 5. Anti-patterns to avoid

| Don't | Why | Do instead |
|---|---|---|
| Run a demo screenshare | Demos lose the buyer who is evaluating fit, not features. | Run the 5-in-5. They feel the product. |
| Pitch the brief before they describe their pain | The brief sounds generic without their language attached. | Listen first. The brief description writes itself once you have their nouns. |
| Ask "what's your budget?" | Premature; lowers the conversation to vendor. | Ask "what would it take to get this on next quarter's tooling list?" only on call 2. |
| Promise integrations we don't have | We'll lose them at week 2 of the pilot. | Be honest: "Slack + Linear today; Jira in 2 weeks; Notion in 4." |
| Skip the agenda set in min 0–2 | The clock drifts; you exit at 38 min having pitched, not closed. | Anchor the box. |
| Send a "thanks for the time" deck after | The deck is the email of "we couldn't close on the call." | Send the intake form link only. |

---

## 6. Variants — adapting the script

| Buyer profile | Adjustment |
|---|---|
| Buyer is the **CEO** (skipped the CoS) | Cut Block 4 (what they tried) by half. CEOs care less about prior tooling. Spend the time on Block 3 (the gap). |
| Buyer is a **CFO** | Add 60 seconds at end of Block 6 on what gets reported to the board and how the brief plugs in. |
| Buyer is a **VP Eng / CTO** | Run Block 5 against an engineering-pod O, not a company O. |
| Call is **15 min** | Drop Block 4 entirely. Block 5 stays — it's the close. |
| Call is **60 min** (rare; only if they ask) | Don't fill the 60. Run the 30-min playbook, then ask "what'd I not ask that you wanted me to?" — let them lead. |

---

## 7. Calibration — track these every 5 calls

The operator runs a 5-call retro every Friday until the ratio is steady.

| Metric | Target after first 5 calls | Target after first 20 |
|---|---|---|
| Discovery → Health Check yes | ≥60% | ≥75% |
| Health Check → "this is useful" verbatim | n/a (no Health Checks shipped yet) | ≥80% |
| Drift-story present in Q9 answer | ≥50% | ≥70% |
| Calls where 5-in-5 produced a real edit | ≥60% | ≥80% |
| Buyer mentions a competitor we lose to | record verbatim — track quarterly | same |

If discovery → Health Check yes is below 60% after 5 calls, the bug is **the script**, not the targets. Re-read this file before the next 5.

---

## 8. Linkage

- Reach this script via a reply to one of the templates in [`02_outreach_scripts.md`](02_outreach_scripts.md).
- Calendly setup, time slot rules, intake handoff → [`04_calendaring.md`](04_calendaring.md).
- After the call, the capture template → [`05_post_call_synthesis.md`](05_post_call_synthesis.md).
- The 5-in-5 framework lives in [`notion/03_playbooks/01_customer_okr_kpi_framework.md`](../notion/03_playbooks/01_customer_okr_kpi_framework.md) §4.
- The Health Check intake itself: [`notion/03_playbooks/04_pilot_intake_questionnaire.md`](../notion/03_playbooks/04_pilot_intake_questionnaire.md).
