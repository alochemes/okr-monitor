# 02 — Outreach Scripts

> Three touches. Fewer is too few; more is spam. Goal: **2.5–3.5% reply rate** at Tier 1 → **≥10 booked discovery calls per 50 dials**. The variants below are written so the operator can choose by category (C1–C5, see [`01_target_list.md`](01_target_list.md) §1) without rewriting from scratch.

> **Voice rule (from `config/company.yaml`):** confident, terse, executive-grade. No hype, no emojis, no exclamation marks, no "AI-powered." Plain English. Short sentences. The buyer is a Chief of Staff or Head of Operations — write to a peer, not down to a target.

---

## 1. The shape of a winning cold email

Six lines. Anything more is a wall of text that gets archived.

```
1. Subject line          (≤7 words, lowercase, specific)
2. The hook              (1 sentence — names a thing they did)
3. The observation       (1 sentence — names the pain)
4. What we do            (1 sentence — outcome, not feature)
5. The ask               (1 sentence — 15-min call, named day)
6. The signature         (operator name + role + one URL)
```

If the email is longer than that, cut it.

---

## 2. Subject lines (5 variants, A/B-test by category)

The operator should rotate one per Tier-1 send and track which gets opens. After 50 sends, lock the winner.

| # | Subject line | Best for category | Rationale |
|---|---|---|---|
| **S1** | `friday brief, sourced from your code` | C3 (eng-led) | Concrete artifact (the brief). Concrete source (the code). |
| **S2** | `how to write next week's status without sunday night` | C4, C5 | The pain, named. |
| **S3** | `your okrs, in real time` | C2 | Echoes the wedge. Best for warm CoS who has already heard of us. |
| **S4** | `okr drift before quarter-end` | C1 (newly funded) | Speaks to the board-reporting horizon. |
| **S5** | `[FirstName] — 15 min on the okr-doc gap?` | All categories, fallback | Direct ask. Use sparingly — feels SDR-y. |

**Rules:**
- **No emoji. No `Re:` fakery. No `[urgent]`.** A peer wouldn't do it.
- Lowercase first letter — feels like a person, not a campaign.
- ≤7 words.
- Use S1–S4 over S5 unless you've A/B'd S5 to 3%+ reply.

---

## 3. Email T0 — the cold open

Send Monday 09:00 PT (highest open window for ops audience). One email per account. Personalized to the trigger you found in `01_target_list.md` §2 column "Trigger."

### Template (copy this and fill the bracketed bits)

```
Subject: [pick from §2]

[FirstName] —

[1-sentence hook tied to the trigger.] [E.g. "Saw [CEO]'s clip on
[podcast / post] — the line about the OKR doc not matching what's
actually shipping caught my eye."]

[1-sentence observation that names the pain.] [E.g. "Most ops leaders
I talk to spend Sunday writing the Monday status from memory and
gut, then defend it Wednesday in standup."]

We turn your real work in GitHub + Linear + Slack into a one-page
Friday exec brief naming exactly which KRs are on track, which are
drifting, and which work isn't moving the needle. No new tool for
your team — we just read the work.

Open to 15 minutes [day, time, time-zone]? I'll send you a sample
brief generated against your real OKRs and 30 days of activity, and
walk you through it.

[Operator name]
Founder, OKR Monitor — okrmonitor.com
```

**What goes in the [hook] line** — pick the one that fits the trigger:

| Trigger from list | Hook line |
|---|---|
| Recent funding announce | `"Congrats on the [Series X]. Your board is going to want monthly proof points against the deck — that's the one thing the Friday brief is built to source automatically."` |
| Founder/CEO OKR podcast/post | `"Saw [name]'s [podcast/post title] — the line about [exact quote, ≤10 words] is the exact gap we close."` |
| New CoS hire | `"Saw you started at [Company] [N] weeks ago. The first 90 days is when CoS tools get picked. We're built for the CoS who inherits an OKR doc no one trusts."` |
| Recent layoff / RIF | `"With the team consolidation, the ops bench is thin. The Friday brief is one less report you have to write at 11pm Sunday."` |
| Public job rec for "OKR Program Manager" | `"Saw the [job title] rec — you don't need to hire one. We are the working version of that role's first 6 months of output."` |
| Public OKR doc on careers page | `"Read your public Q[X] OKR doc — most companies' don't make it past the careers page. Yours is well-set; the question is whether the doc still matches what's shipping."` |

**Rules for the hook:**
- Quote the actual artifact. "Saw your post" is generic. "Saw the line about the OKR-doc gap in the Acquired clip at 14:32" is not.
- Never invent a quote. If you can't find a real one, switch to the trigger that has evidence.
- Never compliment for the sake of complimenting. "Loved your blog!" is filler.

---

## 4. LinkedIn DM T2 — 48 hours after T0

Send if T0 got no reply. **Do NOT** send if T0 got a reply (positive or negative) — wait for the back-and-forth to play out.

LinkedIn allows ~300 chars before "show more"; the message must work inside that.

### Template (3 variants — pick by category)

**V1 — for C3 (eng-led):**
```
[FirstName] — sent a note to [email] about a Friday OKR brief sourced from
your GitHub + Linear. Worth 15 min? I'll bring a sample brief on your real
data so you can judge before you commit. Either way, no follow-up beyond
this — I'm not running a sequence.
```

**V2 — for C2/C4 (CoS-heavy):**
```
[FirstName] — congrats on the [trigger]. We turn the work in your tools
into a Friday OKR brief — the report you'd have to write yourself otherwise.
15 min, I'll send a brief on your real OKRs first. No follow-up after this
unless you want it.
```

**V3 — for C5 (post-RIF):**
```
[FirstName] — when ops gets thin, the Friday status is the first thing that
slips. We write that brief, sourced from your code and tickets, so the CEO
sees the same picture you do. 15 min if useful. If not, no follow-up.
```

**Rule:** the closing line "no follow-up beyond this / unless you want it" is non-negotiable. Tier-1 buyers reciprocate restraint.

---

## 5. Email T4 — the founder-direct, 96 hours after T0

Only sent if T0 + T2 got no reply at all (no bounce, no out-of-office, no human reply). Goes to the founder/CEO with the **Chief of Staff cc'd**, not vice versa.

The cc is the move — the CoS now knows their CEO got the email, and the CoS is the natural one to handle it. This works because the brief is genuinely a thing the CEO would want; we're not weaponizing the CEO against the CoS, we're routing through the doorman.

### Template

```
Subject: [pick from §2 — usually S1 or S4]

[CEO FirstName] (cc [CoS FirstName]) —

Two notes back to [CoS FirstName] last week didn't land — sending
this one straight to you in case the topic is yours, not theirs.

We make a one-page Friday brief naming which OKRs are on track, which
are drifting, and which work isn't moving the needle — sourced from
your team's actual GitHub, Linear, Slack, Notion. The thing it
replaces is the email you write your board on Sunday.

Happy to generate a brief on [Company]'s real Q2 OKRs and 30 days of
activity, and walk [CoS FirstName] through it. 15 minutes.

[Operator name]
Founder, OKR Monitor — okrmonitor.com
```

**Rules:**
- Never cold the CEO without the CoS already in the loop. That's a different play (and a worse one).
- Never send T4 if T0 or T2 got *any* response, even "not now."
- T4 is one shot. No follow-up to T4. After T4 with no reply → mark `dead` and stop.

---

## 6. Reply handling

The operator triages every reply within 6 hours during business days. The 6-hour SLA matters: this audience checks email in bursts, and a reply that sits 24 hours feels like an outbound campaign, not a peer conversation.

### Reply types and the playbook

| Reply shape | Move | Time |
|---|---|---|
| **"Send the sample brief first"** | Generate the OKR Health Check (see playbook `notion/03_playbooks/04_pilot_intake_questionnaire.md`). Send within 48h, with a Calendly link inside. | 48h SLA |
| **"Yes, book 15 min"** | Send Calendly link with 3 specific time slots; do not make them open the picker. | 1h SLA |
| **"Not now / try in [Q]"** | Acknowledge, file in CRM with a re-touch date 14 days before that quarter starts. | 1h SLA |
| **"Wrong person — talk to [Y]"** | Thank, ask for an intro line, then send T0 to Y with the referral baked in. | 4h SLA |
| **"What is this exactly?"** | Reply with two sentences + the okrmonitor.com/v2 link. **Never** send a deck. | 4h SLA |
| **"Take me off your list"** | Acknowledge in one sentence. Mark `dead`. Do not reply twice. | 1h SLA |
| **Anything that looks like genuine pushback** | Reply with a real answer to the objection. The 5 most common objections are pre-answered in §7. | 4h SLA |

### Sample brief request — the response

```
[FirstName] — yes. To generate a brief on [Company]'s real OKRs I need
five things, listed here:
https://okrmonitor.com/v2  (the form is on the page).

Two business days from when those land, you get back:
  1. A Friday-style brief on [Company] (1 page).
  2. A flagged-cleanup list of any KRs we'd recommend tightening
     before the brief is reliable.

If the brief reads like nonsense, that's our problem and we say so.

I've blocked these slots in case the brief lands well — [3 slots]. 
Calendly: [link]. No commitment until you've read the brief.

[Operator]
```

---

## 7. Pre-answered objections (paste-able, edit per reply)

These are the 5 objections we expect to see most. The operator should keep them in a snippet manager (e.g. TextExpander) so the response goes out in 30 seconds.

### O1 — "We already use [Mooncamp / Ally.io / Lattice OKRs]."

```
Right — those are good places to type the OKR doc. None of them read your
GitHub, Linear, or Slack to tell you which KRs are actually drifting.
We're a layer on top, not a replacement. The brief reads like the email
your CoS would write if they had time to read every commit.
```

### O2 — "We just don't have time to look at another tool."

```
Then this is the right one. There is nothing to log into. We email a
one-page brief on Fridays. You read it in 5 minutes Monday morning.
That's the entire interaction — for the whole company, every week.
```

### O3 — "Our OKRs aren't great — wouldn't be a good test."

```
That's actually the best test. Half our pilots arrive with OKRs that
aren't measurable yet. We make the cleanup pass with you in week 1
(the 5-in-5 exercise). The brief gets honest the week after.
```

### O4 — "Privacy / Slack ingestion concern."

```
Default: only public channels, plus opted-in private channels. Data stays
in your tenant. We never train on it. DPA template ready to send today
if useful.
```

### O5 — "What's the price?"

```
Free during the design-partner cohort (5 spots, currently filling).
You give us a real Q's-worth of feedback; we give you the product
plus a written case study with your sign-off. Pricing locks at end of
Sprint 0 — design partners are grandfathered.
```

---

## 8. Volumes and pacing

| Cadence | Volume | Channel mix |
|---|---|---|
| Per business day, week 1 (2026-05-04 → 2026-05-08) | 10 T0 emails (Tier 1) + 5 T2 LinkedIn DMs (echo of last week's T0) | 100% personalized |
| Per business day, week 2 onward | 15 T0 + 10 T2 + 3 T4 | Same |
| Reply triage | 6h SLA | Operator |

**Daily floor and ceiling:**
- **Floor:** 10 personalized touches by 11:00 PT or the day is on fire.
- **Ceiling:** 25/day. Beyond that, quality drops and reply rate halves. Better to add a second operator than push past 25.

---

## 9. What goes wrong (and how to know)

> Reply rate is the steering wheel. Watch it weekly.

| Symptom | Probable cause | Fix |
|---|---|---|
| Reply rate <1% | Subject line generic OR opener line generic | Switch to S1; tighten hook to a real artifact quote. |
| Reply rate 1–2% | Pain not crisp enough in line 3 | Rewrite line 3 to name a specific Sunday-night activity the buyer does manually. |
| Reply rate 2–3% | Working — keep tuning the close | A/B the call slot wording. "15 min" vs "20 min" vs "Tue 2pm or Wed 11am?" |
| Reply rate >4% | Something is wrong (wrong personalization detection, or you're hitting a list that's already warm) | Check unsubscribe / spam complaint rate. If clean, accept it. |
| Reply rate at Tier 1 ≥ Tier 2/3 | Healthy — Tier 1 effort is the leverage point | Keep the Tier-1 prep ritual to 5–10 min/account. |
| Reply rate at Tier 1 < Tier 2/3 | Tier 1 angles are bad (you cherry-picked weak triggers) | Re-do Tier 1; swap in 5 from Tier 2 with stronger triggers. |

---

## 10. Linkage

- The targets these scripts run against → [`01_target_list.md`](01_target_list.md).
- What happens after the reply → 30-min discovery template in [`03_interview_guide.md`](03_interview_guide.md).
- Calendly + intake handoff → [`04_calendaring.md`](04_calendaring.md).
- After the call → capture rules in [`05_post_call_synthesis.md`](05_post_call_synthesis.md).
- Future state: the `founder_sales` and `demand_gen` agents draft these messages and the operator approves before send. Until those agents have ≥85% approval rate (per the promotion gate), the operator writes them by hand using these templates.
