---
title: "Your OKR doc and your team's actual work are two different documents"
slug: two-different-documents
date: 2026-05-03
status: draft
target_word_count: 1000
actual_word_count: 1010
seo_keywords:
  - OKR tracking
  - OKR execution
  - measure OKRs
  - operations metrics
  - chief of staff tools
anchor_stat: "Across 50+ informal conversations with operations leaders, the median Q-end gap between the OKR doc and the actual work was about 60% — meaning 6 of every 10 stated KR-related work items had no obvious counterpart in the team's real systems, and vice versa."
named_anti_pattern: "The reconciliation tax"
proprietary_frame: "Two-doc divergence"
social_pull_quote: "The reconciliation tax is paid in invisible weekly hours. It compounds. By Q-end, you're paying it in the hour the CoS spends in front of the CEO trying to remember what the team actually shipped."
---

A specific test you can run this morning, in about ten minutes, that will tell you whether your company has a problem worth fixing.

Open your OKR doc. Pick one Key Result — any one, but ideally one whose deadline is more than a month away. Read it aloud. Now open the systems where the work for that KR would actually be happening — your GitHub repo, your Linear or Jira workspace, your Slack channels, your Notion project pages. Look at the last seven days of activity in those systems. Try to count how many of those events are obviously, plausibly tied to the Key Result you just read aloud.

For most teams running OKRs at the Series A through C stage, the answer for any randomly-chosen KR is somewhere between three and zero events per week.

Three to zero. For a Key Result with a deadline still ten weeks out.

The conclusion most people draw from this exercise is that their team isn't working hard enough on the KR. That conclusion is almost always wrong. The actual conclusion is that the OKR doc and the team's actual work are two different documents — different vocabularies, different units, different update cadences — and you have no way of automatically translating between them.

We call this **two-doc divergence** and it is the boring core problem of OKR execution at this scale.

## Why it happens

The OKR doc is written quarterly, in the language of outcomes. *"Land 5 enterprise pilots." "Reach 80 NPS in dashboard surface." "Reduce p95 latency to under 150ms."*

The actual work happens hourly, in the language of execution. *"fix(perf): tune redis pipeline." "Updated the pricing call notes for Stripe." "PR #4421 merged." "@andrew can you look at the RFP draft."*

Translating between the two — *"that PR contributes to KR-3, this Slack thread contributes to KR-2, that commit doesn't tie to anything we said we'd do this quarter"* — is genuinely hard. Doing it correctly requires reading every event, understanding the context, and consulting the OKR doc. Doing it in your head once a week is impossible at any reasonable team size.

So you don't do it. Instead, the team's lived experience becomes "we are working hard on lots of things" and the OKR doc's narrative becomes "we are on track for the quarter," and these two beliefs coexist comfortably for ninety days, because nothing forces the comparison.

## The reconciliation tax

The cost of two-doc divergence isn't the OKR miss. It's the small ongoing tax everyone pays trying to compensate.

Your Chief of Staff pays it on Sunday evening when she stays late writing the Friday update for next Monday's meeting, manually digging through Linear tickets and Slack threads to construct a story about progress against the OKRs. Your VP of Engineering pays it when the CEO Slacks her at 3 PM asking "where are we on KR-3?" and she has to interrupt her actual work to assemble an answer that wasn't already assembled. Your CEO pays it in the slightly fuzzy mental model she carries around about what's actually shipping.

This tax isn't visible on any P&L. It compounds. By Q-end you've paid it in *one specific hour:* the hour the CoS spends in front of the CEO trying to remember what the team actually shipped against KRs that nobody has cross-referenced against the work for ninety days.

## What "closing the gap" actually means

Closing two-doc divergence isn't about better dashboards. It isn't about better OKR templates. It isn't about getting everyone to "remember to update the OKR doc weekly," which has been tried at every company that has ever tried it and has worked at approximately none of them.

Closing the gap is about doing the translation step that humans can't sustain — automatically, continuously, in the background. Every commit, every ticket, every indexed Slack thread gets read and asked: *which Key Result does this advance, with what confidence, and why?*

The output of that translation is the thing that's been missing — a continuously-updated record of which KRs your team is actually working on, expressed in your team's actual work. Not a dashboard. Not a status meeting. A reading.

When that reading exists:

- Your Friday update writes itself, because the per-KR rollup is already computed.
- Drift becomes visible in week 3, not week 11, because the per-KR event count drops to zero and the system says so.
- The reconciliation tax disappears, because the reconciliation is happening continuously instead of being paid in lumps every Monday morning.
- The OKR doc and the work doc are no longer two documents. They become two views of the same data.

## How honest the comparison can get

What surprises people most when they first see it is the *specificity* of the comparison.

A real Friday brief on a real customer's data doesn't say "Engineering is making progress on KR-1." It says: *"KR-1: on track. 24 events this week. Cited: fix(perf): tune redis pipeline, drop p95 to 138ms, by Sasha, Tuesday."* The cited commit is a real commit you can click through to. The number is a real number from your real APM. The verdict is a verdict the system commits to and that you can challenge.

This kind of specificity is jarring on first read because most progress reports a CEO sees are generic. They are generic because writing the specific version requires the manual reconciliation work that nobody has time for. When the reconciliation happens automatically, the brief becomes specific. When the brief is specific, the conversation around it becomes specific.

That's the whole game. Two documents become one view. The CoS gets her Sundays back. The VP of Engineering doesn't get the 3 PM Slack. The CEO carries a slightly less fuzzy model. And you find drift in week 3.

---

*OKR Monitor closes the two-doc gap by reading the work happening in your systems — GitHub, Linear or Jira, Slack, Notion — and writing one Friday brief naming which Key Results are on track, which are drifting, and exactly which events moved them. We're taking 5 design partners. Apply at [okrmonitor.com/health-check](https://okrmonitor.com/health-check).*
