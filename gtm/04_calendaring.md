# 04 — Calendaring

> The handoff between "buyer replied yes" and "operator runs the discovery call." Sloppy calendaring kills 1 in 5 booked meetings — wrong time zone, no agenda, surprise dial-in. Get this right once and never touch it.

---

## 1. The principle

The buyer's experience between the reply email and the call should be **two clicks max**. One to pick a time. One to add the calendar invite.

If we send a Calendly link with 12 slots and ask them to pick a time + fill out a form + answer a screener, half drop off. We are competing with their inbox, not with another OKR tool.

---

## 2. Calendly setup (one-time, do this once)

> The operator owns one event type. Don't proliferate. If we add more event types later (e.g. Health Check review, mid-pilot check-in) they each get their own page.

### The event type: `okr-monitor-discovery`

| Setting | Value | Why |
|---|---|---|
| **Name** | `OKR Monitor — discovery` | Buyer sees this; clean name signals the company. |
| **URL** | `calendly.com/andrew-okrmonitor/discovery` | Stable. Don't rename — the URL is in 50 cold emails. |
| **Length** | 30 min | Matches [`03_interview_guide.md`](03_interview_guide.md) §2. |
| **Date range** | Next 14 days, rolling | Beyond 14 days, the lead cools. |
| **Time zone** | Auto-detect (showing buyer's local) | They never do TZ math. |
| **Buffer** | 10 min before, 10 min after | Operator needs the buffer to do call-prep + post-call capture. |
| **Daily limit** | 4 calls/day | Past 4 the operator can't hold a 30-min listening posture. |
| **Min notice** | 4 hours | Lets the operator do 5–10 min of pre-call research. |
| **Available hours** | Mon–Thu 09:00–16:00 PT, Fri 09:00–12:00 PT | Buyer audience is US-East-heavy; our 09:00 PT = their noon. |
| **Friday afternoons** | Closed | Friday afternoons are for the brief and the weekly retro, not new calls. |
| **Weekend** | Closed | Don't be that founder. |

### The booking page

- **Headline:** `30 min — OKR Monitor discovery`
- **Subhead:** `No demo. We discuss how OKRs work at your company today, and whether a Friday brief sourced from your real GitHub + Linear + Slack would help.`
- **Photo:** real photo of the operator. (Avatar = SDR. Real face = founder.)
- **Form fields** (don't ask more than these — every extra field is a 5% drop):
  1. Name (required)
  2. Work email (required)
  3. Company (required)
  4. `What's the OKR question keeping you up?` — one open-ended (optional, but most fill it; gold for call prep)

That's four fields. Resist the temptation to add headcount, role, etc. — we have that from `01_target_list.md` and LinkedIn.

### Confirmation email (auto-sent by Calendly)

```
Subject: confirmed — 30 min, [day] [time] [tz], OKR Monitor discovery

Thanks for booking. The agenda:

 1. 5 min — how OKRs work at [Company] today.
 2. 15 min — the OKR-doc-vs-actual-work gap.
 3. 5 min — a 5-in-5 micro-exercise on one of your Os.
 4. 5 min — a possible next step (we'll pick on the call).

Optional: if you want me to come in already familiar, send me your
current OKR doc (Notion / Asana / Mooncamp / CSV) ahead of time.
Same email address as this thread. No pressure.

Dial-in is in the calendar invite. Reply if anything changes.

Andrew
Founder, OKR Monitor — okrmonitor.com
```

**What this confirmation does** that the default doesn't:
- Restates the agenda (so they show up not expecting a demo).
- Offers an asynchronous prep path (sending the OKR doc) — half do, and call quality is 2× better when they do.
- Personal closer (single name) — feels like a peer, not a vendor.

---

## 3. The reply that contains the Calendly link

When a cold-outreach reply opens the door, the operator's response is **always** this short:

```
[FirstName] —

Yes — three slots that work on my side:

  · [Day] [time] [tz]
  · [Day] [time] [tz]
  · [Day] [time] [tz]

If none fit, the picker is here: calendly.com/andrew-okrmonitor/discovery
(I keep it open for the next two weeks.)

Andrew
```

**Rules:**
- **Three concrete slots first**, link as fallback. Many buyers pick a slot rather than open the link — saves them 30 seconds.
- Slots are 09:00 / 11:00 / 14:00 buyer-local. Auto-pick from their inferred TZ if known; else PT.
- If there's no inferred TZ, give 3 PT slots and trust Calendly to do the math if they need a different one.

---

## 4. Email handoff to call (T-24h, T-1h)

Buyers no-show when the booking is >5 days out and they didn't confirm. Two automated touches close that gap. Both go from the operator's address (not Calendly's domain) so they show up in the same thread as the original conversation.

### T-24h (the day before)

```
[FirstName] — confirming our 30 min tomorrow at [time] [tz]. Dial-in:
[Zoom / Meet link]. If you want me to look at anything specific, send
it now and I'll come prepared.
```

### T-1h (one hour before)

> Skip this for warm referrals; it's overkill for friends-of-friends. Send for cold-sourced bookings.

```
[FirstName] — see you in an hour. Same dial-in: [link]. If something
just blew up on your side, reply "later" and we'll re-book; no
explanation needed.
```

The "no explanation needed" line is the move — it makes rescheduling cheap and reduces no-shows. People who can't make it but feel awkward telling you don't show; remove the awkwardness, you get the reschedule instead of the silence.

---

## 5. Conferencing — Zoom or Google Meet?

| Use | Tool |
|---|---|
| Default | **Google Meet** (auto-created from operator's Calendar) |
| Buyer requests Zoom | Use Zoom (their preference always wins) |
| Buyer is on Microsoft Teams | Send a Meet link anyway — 99% of buyers can join Meet from a browser. Don't install Teams. |
| Recording | **Granola** (auto-records, attaches transcript to calendar event) |

Granola is the operator's default note-taker because it works on every conferencing tool, doesn't show up as a bot in the call, and produces clean transcripts that feed straight into the post-call capture template ([`05_post_call_synthesis.md`](05_post_call_synthesis.md)).

> **Disclosure rule:** the operator says, in the first 30 seconds of every call, "I record these for my own notes — let me know if that's a problem." This is not optional. Two-party consent states (CA, FL, IL, MA, MD, NH, PA, WA) make it legal exposure if we don't.

---

## 6. The intake handoff (post-call)

When the call ends with "yes, do the Health Check" (which is the goal — see [`03_interview_guide.md`](03_interview_guide.md) §3, Block 6), the operator sends this within 4 hours of call-end.

```
Subject: re: 30 min — next step (OKR Health Check intake)

[FirstName] —

Good call. As promised, the intake — five things to send me, in
this 15-min form:

  https://okrmonitor.com/v2  (the form is on the page)

What you'll get back, two business days from receipt:

  1. A Friday-style brief on [Company] (1 page).
  2. A flagged-cleanup list of any KRs we'd recommend tightening
     before the brief is reliable.

If anything in the brief reads wrong to you, that's our problem,
not yours, and we'll say so in writing.

Andrew
```

**The form they fill out** is the [pilot intake questionnaire](../notion/03_playbooks/04_pilot_intake_questionnaire.md). 30 questions; takes them 15 min if they have the OKR doc handy.

When the form returns, the operator runs the OKR Health Check via `python scripts/run_okr_health_check.py` — output goes to `data/health_checks/<account_slug>/HEALTH_CHECK.md` (and `.json`). Dogfooded reference output is in [`data/health_checks/example_acme/`](../data/health_checks/example_acme/).

---

## 7. No-show handling

If they don't dial in by min 5:

1. **Min 5:** operator sends a Slack-tone reply in the email thread:  
   `"Looks like we missed each other — happy to reschedule, no harm done. Same Calendly link: calendly.com/andrew-okrmonitor/discovery."`
2. **Min 30:** mark `no_show_1` in the CRM. Wait for them to re-book.
3. **+7 days:** if no rebook, send one more touch:  
   `"[FirstName] — circling back; if it's not the right quarter, totally fair. Want me to set a reminder for [Q+1]?"`
4. **+14 days:** mark `dead`.

> Never punish a no-show. The buyer was probably running into a meeting; making them feel bad about it costs the reschedule. Make rebooking the path of least resistance.

---

## 8. Things that break (and the fix)

| Symptom | Cause | Fix |
|---|---|---|
| Buyer books a Friday afternoon slot | Wrong availability config | Re-check §2; Friday afternoons must be closed. |
| Buyer says "the link 404'd" | Calendly URL changed (someone renamed the event type) | Don't rename. Ever. The URL is referenced in 50 emails. |
| 4-of-5 calls on a given day at the same hour | Slot pressure too high; operator can't think between calls | Lower daily limit from 4 to 3 in §2. |
| Buyer joins from phone, can't share screen for 5-in-5 | Phone-joiners can't drive Block 5 | Operator drives the screen instead — share a blank doc, type for them. |
| Buyer dials in 10 min late | Habitual; their assistant booked it | Skip Block 4 (what they tried), still run Block 5. |
| Buyer brings a +1 (CFO, CTO) | They're internal-selling already; great signal | Skip Block 1 niceties; jump to Block 2 with both addressed. |

---

## 9. Volume math (sanity-check the funnel)

| Stage | Conversion (target after first 20 calls) | Volume to feed 5 design partners |
|---|---|---|
| T0 sent | — | 50 (Tier 1) |
| Reply | 5–8% | 3–4 |
| Discovery booked | 80% of replies | 3 |
| Discovery → Health Check yes | 75% of discoveries | 2 |
| Health Check → design-partner yes | 80% of Health Checks | 1.6 |

So **50 well-targeted T0 emails → ~1.6 design partners**. To land 5 design partners by 2026-05-19 we need **~150 T0 emails sent**, or another way to think of it: Tier 1 (10) + 75% of Tier 2 (15) + a steady Tier 3 trickle.

This is why §1 of [`01_target_list.md`](01_target_list.md) gives 50 named accounts and §3–§4 give the next 30 — the funnel math demands it.

---

## 10. Linkage

- Outbound that sources these bookings: [`02_outreach_scripts.md`](02_outreach_scripts.md).
- Discovery-call playbook itself: [`03_interview_guide.md`](03_interview_guide.md).
- Post-call capture: [`05_post_call_synthesis.md`](05_post_call_synthesis.md).
- Health Check intake: [`notion/03_playbooks/04_pilot_intake_questionnaire.md`](../notion/03_playbooks/04_pilot_intake_questionnaire.md).
- Generated Health Check artifact: `data/health_checks/<account_slug>/HEALTH_CHECK.md`.
