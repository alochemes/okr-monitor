# Onboarding video — script & production guide

> **Format:** screen-recorded explainer with founder voice-over.
> **Runtime target:** 5–6 minutes.
> **Tools:** Loom (one-take, fastest) OR OBS Studio + Descript (more polished).
> **Use cases:** internal onboarding for a new hire, sent as a follow-up to a discovery call, embedded on the landing page below the fold once it exists.

---

## Pre-recording checklist (~10 minutes setup)

### Have these open and arranged before you start

Three windows / tabs visible from the recording surface:

| Window | What's on screen | Why |
|---|---|---|
| **Tab 1 — landing page** | `http://localhost:3000` (or live Vercel URL) | Hero + memo asset for Section 1 |
| **Tab 2 — code editor** (Cursor / VS Code) | `TRACKER.md` open in left pane, `agents/_proposal.py` in right pane | "Behind the scenes" reveal |
| **Tab 3 — terminal** | Inside `C:/Users/aloch/okr-monitor/` | For running the live commands |
| **Tab 4 (overlay)** | A blank Notion page named "Onboarding video" with the URL of [`notion/00_MASTER_INDEX.md`](../00_MASTER_INDEX.md) handy | Show the KB exists |

Optional but recommended:
- Increase font size in the editor and terminal to ~16pt minimum (Loom captures look small otherwise)
- Close Slack, mail, anything that might notification-ping mid-recording
- Have the [`notion/02_product/03_team_and_workflow_diagrams.md`](../02_product/03_team_and_workflow_diagrams.md) page open in another browser tab in case you want to show the Mermaid diagrams

### Pre-warm the data so the demo isn't empty

Run these once before recording so screens have content (not blank):

```bash
cd C:/Users/aloch/okr-monitor
python scripts/init_db.py                                        # if needed
OKR_MONITOR_DRY_RUN=true python scripts/sunday_evening.py        # populates proposals/
OKR_MONITOR_DRY_RUN=true python scripts/daily_evening.py --no-email  # populates reports/
```

Now `proposals/<today>/` and `reports/daily/<today>/` have artifacts to point at.

---

## The script (read aloud, voice-over)

> **Format key:**
> - **`[SCREEN: ...]`** — what's visible during this segment
> - *"..."* — what you say
> - **`[CUT]`** — moment to switch screens, lasts ~0.5s

---

### 0:00 – 0:20 · Cold open

**`[SCREEN: Tab 1 — landing page hero, with the printed memo asset visible]`**

> *"This is the Friday brief OKR Monitor wrote about a mid-size SaaS company. Three of seven Key Results at risk this quarter. Engineering shipped 80% of work against KR-1. Customer Success shipped zero against KR-3. The recommendation: reallocate or restate."*

> *"The brief is one page. It writes itself every Friday at 9 AM. It cites the actual commits and tickets that moved the needle, and the ones that didn't. It exists because by the time most companies run their quarterly post-mortem, the answer to "what went wrong" is already three months stale."*

> *"My name is Andrew. I'm building OKR Monitor. Let me show you how it works."*

---

### 0:20 – 1:10 · The problem we solve

**`[CUT to TAB 1, scroll down to the "02 / The Autopsy" section]`**

> *"Most companies have two completely separate documents. There's the OKR doc — usually in Notion, set in January, reviewed maybe once a quarter. And there's the work — commits in GitHub, tickets in Linear, conversations in Slack. The OKR doc says one thing. The work says another. The gap between them is invisible until quarter-end, when it's too late to do anything about it."*

**`[SCREEN: bring up the field-note quote: "Every Monday I spend an hour playing telephone..."]`**

> *"This quote is from a real Chief of Staff at a Series B fintech. Anonymous, but real. They spend an hour every Monday DMing five people to find out if their OKRs are still on track. That's the problem we solve. We replace the telephone game with a one-page reading."*

---

### 1:10 – 2:30 · How it works

**`[CUT to Tab 1, scroll to the "03 / The Mechanism" section showing Connect → Map → Narrate]`**

> *"Three steps. Step one — Connect. You point us at the systems where work already happens. GitHub, Linear or Jira, Slack, Notion. OAuth, minimum scopes, no new process for your team."*

**`[CUT to Tab 3 — terminal]`**

```
python -m cli.status
```

**`[Output renders — KR scoreboard table]`**

> *"Step two — Map. An agent we call OKR-Mapper reads every commit, every ticket, every Slack thread, and decides which Key Result it advances. Confident mappings only — anything below 0.5 confidence is dropped, not faked. We measure ourselves at 85% precision and 70% recall, and we publish that number."*

**`[CUT to Tab 2 — open `agents/okr_mapper/prompts/map_event.md` and scroll]`**

> *"Here's the actual prompt. Notice the calibration rubric — 0.9 means the event explicitly references the KR by ID. 0.5 means a plausible link with reasoning. Below that, we don't return a mapping. Confident wrong is worse than no answer."*

**`[CUT to Tab 1 — scroll to "Sample Friday brief"]`**

> *"Step three — Narrate. Every Friday at 9 AM, an agent called Narrative writes the brief. Verdict per KR. Cited events. One paragraph at the bottom telling you what to do Monday morning. It's not a dashboard — it's a reading."*

---

### 2:30 – 3:30 · What you actually get

**`[CUT to Tab 3 — terminal]`**

```
python -m cli.review --list
```

**`[Output — list of pending proposals]`**

> *"Every agent emits a proposal that lands in this queue. The CEO agent proposes weekly priorities. The CFO projects 14 days of cost. The Pilot-PM scores every active pilot. I review them every morning — about ten minutes. I approve, edit, or reject. The system measures how much I edit each proposal and uses that as a trust signal."*

**`[CUT to Tab 2 — open `reports/daily/<today>/OWNER_FINANCE_REPORT.md`]`**

> *"And every day at 7 PM, this lands in my inbox. Top of the page — the live KPI dashboard. Then four sections. CEO synopsis: today versus what the sprint plan implied should ship. Product roadmap. CFO 14-day cost projection. Growth metrics. The whole thing is generated automatically by GitHub Actions — runs on a cron, commits the report back to the repo, sends the email."*

**`[CUT to Tab 3 — terminal]`**

```
python -m cli.kpis
```

**`[Output — operational KPI table]`**

> *"This is the operational layer. Ten KPIs that should always be green. If any go red, the daily report alerts me. Right now seven are green, two are unknown — the two requiring manual data entry — and one is amber. I know exactly what's wrong without opening a database."*

---

### 3:30 – 4:30 · Behind the scenes

**`[CUT to browser — open `notion/02_product/03_team_and_workflow_diagrams.md` rendered]`**

> *"The whole company runs as a 30-agent team across six pods. Strategy. Product and Design. Engineering. AI/Data. Go-to-market. Customer and Operations. Every agent has a single job, a focused prompt, a structured output."*

**`[Hover or scroll to the data-flow diagram]`**

> *"This is the data flow. Work events come in from sources. The OKR-Mapper classifies them. Signals-Analyst computes rolling counts — pure compute, no LLM. Forecasting compares pace required against pace observed and emits a verdict. Narrative writes the story. Every step is auditable."*

**`[CUT to Tab 2 — open `TRACKER.md`]`**

> *"And this — TRACKER.md — is the single source of truth. Our OKRs, our KPIs, the agent roster, every consequential decision with rationale, every risk with severity. It's checked into git. Every agent's prompt embeds it. When I change the OKR text, the next mapper sweep re-maps the last 30 days against the new wording. There's no save-and-forget."*

---

### 4:30 – 5:30 · The real wedge

**`[CUT to browser — open `notion/03_playbooks/01_customer_okr_kpi_framework.md`]`**

> *"Here's the part most teams get wrong. Most pilots arrive with OKRs that aren't measurable. Vague verbs. No baseline. Key Results that are really task lists. Before any product can find drift, the OKRs themselves have to be in good shape."*

> *"So the actual deliverable we lead with isn't the agents. It's this — a 12-section OKR and KPI framework playbook we walk every customer through. The 5-in-5 exercise. The six rules for a good Key Result. A worked example. Templates. The agents are the delivery mechanism that makes the cleanup stick. The framework is the wedge."*

**`[CUT to browser — open `notion/03_playbooks/04_pilot_intake_questionnaire.md`]`**

> *"Before a pilot kickoff, the customer fills this out — about fifteen minutes. We use their answers to generate this — a customized OKR Health Check brief that we send back within two business days. Their real KRs reviewed against our rubric, their real recent work mocked into a sample Friday brief, a customized 45-minute kickoff agenda."*

---

### 5:30 – 6:00 · Where we are and what's next

**`[CUT to Tab 2 — TRACKER.md, scroll to KR4.1 line]`**

> *"As of today — the full thirty-agent organization is online. Two GitHub Actions workflows fire on cron. Nine math tests pass. The marketing landing page is built. We're ten days from MVP target and four months from the goal of three hundred pilots."*

**`[CUT to Tab 1 — landing page CTA]`**

> *"We're taking five design partners over the next two weeks. If you're a Chief of Staff or Head of Operations at a Series A through C SaaS company and your Monday standup is the autopsy — apply at okrmonitor.com. We do a real OKR Health Check on your real data, no slides, no demo to sit through. You read the brief, you tell us what's wrong, we fix it together."*

> *"Thanks for watching."*

**`[FADE to brand wordmark — Fraunces serif "OKR Monitor", paper background, persimmon dot]`**

---

## Suggested cut-down versions

If you need shorter versions for specific contexts:

| Audience | Cut to | What to drop |
|---|---|---|
| **2-min ad** for LinkedIn / Twitter | 0:00–0:20 (cold open) + 1:10–2:30 (how it works) + 5:30–end (CTA) | Skip "behind the scenes" entirely |
| **3-min discovery follow-up** | 0:00–3:30 + 5:30–end | Skip the framework wedge section |
| **45-sec teaser** | 0:00–0:20 + the CTA | Just the brief example + the ask |

Record the full 6-min version once. Cut down in Descript or your editor of choice.

---

## Voice + tone notes

- Pace: slower than feels natural. Rough rule — read each line, breathe, then read the next.
- Posture: speak as if explaining to one specific person who's smart but skeptical. Not to a crowd.
- Language: zero hype. No "AI-powered." No "revolutionary." Don't use the word "delight" as a verb. Stick to specifics — numbers, KR IDs, real examples.
- Rest: pause for a full beat before "What you actually get" (2:30) and "The real wedge" (4:30). These are the chapter breaks the viewer feels.

If you stumble, restart from the nearest chapter break — don't try to recover mid-sentence. Loom keeps the take simple; you can re-record one segment without redoing the whole thing.

---

## After recording

| Step | Tool | Output |
|---|---|---|
| 1 | Loom (auto) or Descript | Editable transcript |
| 2 | Edit out long pauses, fix obvious flubs, trim head + tail | Clean cut, ~5:30–6:00 final |
| 3 | Optional: add chapter markers at the times listed above | Better navigation |
| 4 | Generate auto-captions, proofread for "OKR" / "KR" capitalization | Accessible |
| 5 | Upload as unlisted to YouTube **and** keep the Loom link | YouTube for embed quality, Loom for view analytics |
| 6 | Add the YouTube embed to `web/app/page.tsx` below the hero, OR add a new section "Watch the 5-min walkthrough" with a thumbnail link | Live on landing page |
| 7 | Send the link to the next 5 cold-outreach recipients in place of a calendar invite | Lower-friction follow-up |

---

## Production cost estimate

- **Bare-minimum (Loom only):** $0, ~30 minutes including takes + the pre-warm
- **Polished (Descript + light edit):** Descript free tier OK for a single video; ~2 hours total
- **Premium (with motion graphics + B-roll):** Hire a freelancer through Onlogo or Upwork, $400–$1,200, 3–5 day turnaround

Recommend the bare-minimum first. Watch it back, decide if you need polish. The voice + content matter 10× more than the production value at this stage.

---

## Things you might want for later (don't block on these)

- A two-minute version recorded entirely on Loom for cold outbound. Lower production but with you on camera (picture-in-picture) — cold-email reply rates jump when there's a face.
- A "watch us build" series — record yourself running `python scripts/run_strategy_pod.py` for real, narrating the proposals as they come back. Posted as a weekly YouTube series. Builds authority + credibility for KR3 (voice / credibility).
- A "behind the scenes" demo specifically for technical buyers — open the repo, walk through `agents/okr_mapper/pipeline.py`, show the prompt, show the audit log. Ten minutes. For VPEs and CTOs.

These come **after** the first onboarding video lands and you have data on whether it converts.
