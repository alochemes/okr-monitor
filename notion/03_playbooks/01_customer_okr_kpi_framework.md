# Customer OKR + KPI Framework

> **Audience:** the Chief of Staff or Head of Operations at a pilot company. Pre-pilot, pilot kickoff, and pilot week 1.
>
> **Purpose:** about half of pilots arrive with OKRs that aren't measurable yet — vague verbs, no baseline, KRs that are really task lists. Before our product can find drift, the OKRs themselves have to be in good shape. This playbook is the cleanup pass we walk customers through in the kickoff call.
>
> **Time to apply:** 90 minutes for a first draft, then iterate weekly for the first three weeks.

---

## 1. The OKR vs KPI distinction (no, they're not the same)

Most teams conflate these. The difference matters because the right tool depends on which one you're talking about.

| | **OKR** | **KPI** |
|---|---|---|
| Purpose | Drive change | Maintain a state |
| Time horizon | One quarter or one year | Continuous |
| Cadence | Set quarterly, reviewed weekly | Reviewed continuously |
| Aspiration | Ambitious — 60–70% achievement is success | Operational — should always be in green |
| Example | "Land 5 enterprise pilots by EOQ" | "Uptime ≥99.95% rolling 30d" |
| What we monitor | OKRs (drift detection) | KPIs (alerts on threshold breach) |

**OKR Monitor cares about OKRs first.** Your KPIs probably already have alerting. Your OKRs probably don't.

---

## 2. How to write a good Objective

Five rules. If your O fails any of them, rewrite it.

1. **Qualitative.** No numbers in the Objective itself; numbers belong in the KRs.
2. **Ambitious.** If you're 80% sure you'll hit it, it's not an Objective — it's a project. Aim for 50–60% confident.
3. **Inspirational, not instructional.** "Become the OKR-execution standard for ops leaders" beats "Improve OKR tracking."
4. **Time-bound.** Single quarter (or single year for company-level Os).
5. **Outcome, not activity.** "Customers can answer 'are we on track?' in 60 seconds" — not "Build a dashboard."

### Examples

| ❌ Bad | ✅ Better | Why |
|---|---|---|
| Increase revenue by 30% | Become the default tool for ops-led teams running OKRs | The bad one is a number disguised as an objective. The good one is the qualitative outcome that drives the number. |
| Improve customer satisfaction | Customers describe us as "the most honest report they get all week" | Generic vs. specific narrative outcome. |
| Build dashboard v2 | Operators ground every Monday standup in our brief, not vibes | Activity vs. outcome. |
| Hire 5 engineers | Engineering ships every Sprint goal without slipping | The hires are an input; the outcome is shipping. |

---

## 3. How to write a good Key Result

Six rules.

1. **Numeric.** A KR has a number, a unit, and a deadline. No exceptions.
2. **Observable in a system you already have.** If measuring it requires a new survey or a new tool, you'll stop measuring it by week 4.
3. **Outcome metric, not vanity metric.** Pageviews ≠ outcome. Activations ≠ outcome until you define what "activation" means.
4. **One KR = one number.** Compound KRs ("ship X **and** improve Y by 20%") fail because half-success looks like full-failure.
5. **At most 5 KRs per Objective.** More than 5 = you're really listing tasks. Cut.
6. **At most 5 Objectives per company per quarter.** Same reason.

### The KR shape

> [Verb][Metric] from [Baseline] to [Target] by [Date].

Examples:
- Increase pilot-to-paid conversion from 0% to 25% by 2026-08-28.
- Reduce p95 API latency from 320ms to 150ms by 2026-06-30.
- Raise NPS from 12 to 50 (5 design partners) by 2026-05-26.

### Anti-patterns that look like KRs but aren't

| Looks like a KR | What's wrong | Fix |
|---|---|---|
| "Ship feature X" | This is a task. Where's the number? | "X used by ≥30% of weekly actives within 14 days of ship." |
| "Improve onboarding" | No baseline, no target. | "Reduce signup-to-first-value from 18 min to 4 min by EOQ." |
| "100% of customers respond to NPS" | A 100% target is almost always a process metric, not an outcome. | "NPS sample of ≥40 customers/quarter; median NPS ≥50." |
| "Hit revenue target" | Vague + no number. | "ARR from $480k to $720k by EOQ." |
| "Maintain quality" | This is a KPI, not a KR. | Move it to your KPI dashboard. |

---

## 4. The 5-in-5 exercise (use this in the kickoff call)

We do this exercise live in pilot kickoffs. It surfaces the real KRs faster than any framework discussion.

**Setup:** the operator picks one Objective. Everyone gets a blank doc.

**Round 1 — 5 minutes.** Each person writes 5 candidate KRs for that Objective. No editing, no debating, no looking at others' drafts. Fast and rough.

**Round 2 — 10 minutes.** Read aloud. Cluster duplicates. The room produces 8–15 unique candidates.

**Round 3 — 5 minutes.** Vote — each person picks their top 3. Tally.

**Round 4 — pick.** Take the top 3 by vote. Pressure-test each against the 6 rules above. If a top-voted KR fails a rule, fix it on the spot or drop it.

**Output:** 3–5 KRs per Objective, written in the canonical shape, voted into the room.

This works because writing 5 in 5 minutes forces you past the safe ones to the real ones.

---

## 5. Cascading vs non-cascading

Most OKR consultants will tell you to cascade — every team's KRs roll up to the company KRs.

**We recommend non-cascading at your stage** (Series A–C, 50–500 people).

| Cascading | Non-cascading |
|---|---|
| Team Os derive from company Os; team KRs derive from team Os. | Each team writes Os and KRs that *contribute to* the company Os, but doesn't have to mirror them. |
| Forces alignment. | Forces ownership. |
| Looks neat in a deck. | Reflects how teams actually work. |
| Encourages "fake" team KRs (created to satisfy the cascade). | Encourages teams to commit to outcomes they actually believe they can move. |

The trade-off: non-cascading means cross-team contributions to a company OKR are less visible *in the doc*. **OKR Monitor solves exactly this** — by mapping every commit, ticket, and conversation to a KR (regardless of team), the brief makes cross-team contributions visible without forcing them into the doc structure.

If you have a strong reason to cascade (PE-backed, board mandate, very large company), cascade. Otherwise, don't.

---

## 6. Cadence — set quarterly, review weekly

**Quarterly:** set 3–5 Os and ≤5 KRs each.

**Weekly (Friday):** read the OKR Monitor brief. ~5 min.

**Weekly (Monday standup):** 15 min, structured by the brief:
- Spend ~5 min on each KR rated `drifting` or `off`.
- Skip the green ones unless someone has news.
- End with 1–3 named decisions that come out of the discussion.

**Quarterly retro:** score each KR (0.0–1.0). Honest scoring is the most valuable input for next quarter's targets. If you're consistently scoring 0.85+, your KRs are too easy.

**What we recommend cutting:** mid-quarter "pulse checks" longer than 30 minutes, OKR doc-reviews longer than 30 minutes, status reports that take more than 15 min to write.

---

## 7. Setting baselines and targets

Two-step process:

### Step 1 — establish baseline

Pull the current value of the metric from your existing tools. **Do not skip this** — a KR without a baseline is just a target without context.

| Metric type | Where to pull baseline |
|---|---|
| Revenue / pipeline | Stripe, your CRM |
| Conversion rates | PostHog, Mixpanel, Amplitude |
| System metrics | Datadog, Grafana, your APM |
| NPS / CSAT | Survey tool of choice |
| Engineering throughput | GitHub Insights, Linear analytics |

### Step 2 — set the target

Use one of these patterns:

- **2× current.** Aggressive. Use when you have an obvious lever to pull.
- **+50% of current.** Stretch. Use when you don't have an obvious lever.
- **+20% of current.** Conservative. Use when the metric is already mature and you're just trying to maintain a healthy growth rate.
- **Industry P75.** External anchor. Use when you don't trust internal estimates.

**Avoid:** round numbers without rationale. "100 pilots" because it's a round number is worse than "75 pilots" because that's what your funnel can support.

---

## 8. Connecting OKRs to actual work (this is where we come in)

The reason teams stop trusting OKRs is the gap between what's in the OKR doc and what's actually happening in the team's tools. By Q-end, that gap is the size of a quarter — too late to act.

**OKR Monitor closes the gap by reading the work directly:**

- Every commit you push gets classified against a KR with confidence ≥0.5 — or dropped if no honest tie exists.
- Every ticket you close, same.
- Every Slack thread in opted-in channels, same.
- Every Notion page update on linked project pages, same.

When KR-3 has zero events in 14 days, you know *in week 3* — not in week 11.

You don't change how your team works. We just make the work visible against your goals.

---

## 9. A worked example

**Company:** mid-size SaaS, 220 employees, Series B.

**Q3 2026 Objectives (set in early July):**

### O1: Become the default tool ops leaders share with each other.

| KR | Baseline | Target | Date |
|---|---|---|---|
| KR-1.1 | NPS = 12 (small sample) | NPS ≥50 from ≥40 customers | 2026-08-28 |
| KR-1.2 | 0 inbound referrals | 25 inbound referrals (last-touch attribution) | 2026-08-28 |
| KR-1.3 | 0 unprompted mentions in CoS Slack communities | ≥10 unprompted mentions | 2026-08-28 |

### O2: Make the Friday brief the most honest report a CEO gets all week.

| KR | Baseline | Target | Date |
|---|---|---|---|
| KR-2.1 | 65% precision @ 50% recall (mapper) | ≥85% precision @ ≥70% recall | 2026-08-28 |
| KR-2.2 | 40% of customers read the brief | ≥80% of customers read the brief | 2026-08-28 |
| KR-2.3 | Anecdotal "this is great" | ≥3 customers screenshot the brief into their CEO Slack | 2026-08-28 |

### O3: Reach pilot →paid product-market fit signal.

| KR | Baseline | Target | Date |
|---|---|---|---|
| KR-3.1 | 5 pilots, $0 paid | 75 pilots, $20k MRR | 2026-08-28 |
| KR-3.2 | 0% pilot →paid conversion | ≥25% pilot→paid intent at end of pilot | 2026-08-28 |
| KR-3.3 | CAC unmeasured | CAC payback ≤6 months on first paying cohort | 2026-08-28 |

Notice:
- 3 Objectives. 9 KRs total. Tight.
- Every KR has baseline + target + date.
- Os are qualitative; KRs are numeric.
- O1 is about reputation. O2 is about product quality. O3 is about commercial outcome. They reinforce each other but don't overlap.

---

## 10. Templates you can copy

### A. The blank OKR doc (one quarter)

```
Q[N] [YEAR] OKRs

OWNER: [Chief of Staff name]
SET: [Date]
REVIEWED WEEKLY: Fridays via OKR Monitor brief
RETRO: [End of quarter date]

---

O1: [Qualitative outcome statement, ≤15 words]
   KR-1.1  [Verb] [metric] from [baseline] to [target] by [date]
   KR-1.2  ...
   KR-1.3  ...

O2: ...
   KR-2.1  ...
   KR-2.2  ...

O3: ...
   KR-3.1  ...
   KR-3.2  ...
```

### B. The blank Objective worksheet (use during 5-in-5)

```
OBJECTIVE: ____________________________________________

(qualitative? ambitious? time-bound? outcome-not-activity?)

CANDIDATE KRs:
1. _______________________________________________________
2. _______________________________________________________
3. _______________________________________________________
4. _______________________________________________________
5. _______________________________________________________

VOTE: pick top 3.

Final KRs (in canonical shape):
KR-1: [Verb] [metric] from [baseline] to [target] by [date]
KR-2: ...
KR-3: ...
```

---

## 11. Common questions

**"Should engineers have their own KRs?"**
Yes — at the team level, not the individual level. Individual OKRs become performance reviews in disguise and degrade quickly.

**"What if a KR turns out to be wrong mid-quarter?"**
Restate it explicitly. Write a one-paragraph "we are restating KR-X to Y because Z" in the OKR doc. Don't silently change it. The audit trail matters more than the number.

**"How do we reconcile OKRs with our roadmap?"**
The roadmap is *how*; OKRs are *what for*. If a roadmap item doesn't move a KR, ask why it's on the roadmap. If a KR has no roadmap item, ask why it's a KR.

**"Do we share OKRs with the whole company?"**
Yes. Public by default. Private OKRs become political. The Friday brief is shared in `#general` (or your equivalent) — public accountability is the point.

---

## 12. What you give us at pilot kickoff

To start mining your knowledge base on day one, send us:

1. **Your current OKR doc** (Notion link, Asana board, Mooncamp doc, or CSV).
2. **The team Slack workspace** — at minimum, names of the 3–5 channels you'd want indexed.
3. **The GitHub org** + the repo names that map to the goals.
4. **Linear or Jira workspace** + the project names that map to the goals.
5. **The deadline** — when does the current quarter end?

Within 2 business days of receiving these, you get your first **OKR Health Check** — a sample brief generated against your real OKRs and 30 days of recent work, plus a list of any cleanup we recommend on the OKR doc itself before the pilot officially begins.
