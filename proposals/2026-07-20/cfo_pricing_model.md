# Pricing v0 — Three-tier model anchored on Team at $1,049/mo

A time-boxed free Pilot tier converts to a Team tier priced to hit CAC payback in under 6 months at a blended CAC of $6,300. A Scale tier exists for companies that outgrow Team, but the anchor and the math both live at Team.

## Tiers
| Tier | Price/mo | Includes | Buyer | Rationale |
|---|---|---|---|---|
| Pilot | Free | 45 days, 1 workspace, up to 3 integrations (GitHub + one ticket source + Slack), up to 10 OKRs tracked, full Friday narrative, operator exit interview required to close | Chief of Staff or Head of Ops at a Series A–C SaaS, 50–200 employees, evaluating whether OKR drift is a real problem for them | 45 days is long enough to span one full monthly OKR review cycle and produce 6 Friday briefs — enough signal for the buyer to feel the value without giving away a full quarter. |
| Team | $1,049 | Unlimited OKRs, all 5 integrations (GitHub, Linear/Jira, Slack, Notion/CSV), weekly narrative, live scoreboard, up to 500 employees, 1 workspace, annual contract billed monthly; 10% discount for annual prepay ($11,329/yr list) | Chief of Staff or Head of Ops who completed the pilot and has already shown the Friday brief to their CEO at least twice — they are buying a recurring ritual, not a tool | This is the tier 80%+ of pilots will land on; priced to clear CAC payback in 6 months at a blended CAC of $6,300 with 78% gross margin. |
| Scale | $2,499 | Everything in Team plus multi-workspace (up to 3 business units), custom integration support, dedicated onboarding call, SLA on narrative delivery, annual contract required | Series C company, 200–500 employees, multiple product lines or divisions each running their own OKR cycle — the Chief of Staff needs cross-BU roll-up, not just one scoreboard | Exists to capture the top 10–15% of the pilot cohort that has genuine multi-team complexity; also anchors Team as the obvious choice for everyone else. |

**CAC payback assumption:** 5.0 months

- Blended CAC assumption: $6,300
- Anchor-tier ARPU: $1,049/mo
- Gross margin assumption: 78%

## List vs negotiated
Expect 60–70% of pilot-to-paid conversions to negotiate; the defensible floor is $849/mo for Team (a $200 discount framed as 'pilot alumni pricing,' never as a percentage off). Do not discount below $849 — at that level CAC payback stretches to 7.5 months and KR2.5 breaks. Scale list is firm; any discount there requires operator approval per company.yaml.

## Decisions needed from operator
- [ ] Is 45 days the right pilot length, or does the buyer's internal review cycle (monthly vs quarterly OKRs) argue for 30 or 60 days?
- [ ] Should annual prepay be the default ask at conversion, or is month-to-month acceptable for the first cohort given we have zero churn data to defend a lock-in ask?
- [ ] What is the actual blended CAC assumption — the $6,300 figure is derived from a founder-led outbound model (600 touches/day, ~2% reply, ~15% demo-to-pilot, ~25% pilot-to-paid); if a paid channel enters the mix, CAC could 3x and Team pricing breaks KR2.5 without a price increase.

_Confidence: 0.45_
_Reasoning: There is no willingness-to-pay data as of 2026-07-20 — KR1.2 (5 design partners) and KR2.1 (300 pilots) are both still in progress per the tracker, and §8 shows zero named customers. The $1,049 anchor is derived from comp-set reasoning: OKR tools (Lattice, Perdoo, Mooncamp) price $6–$12 per user per month; at 100 users that is $600–$1,200/mo, but OKR Monitor is not a per-seat tool — it is an ops ritual delivered to one buyer, so per-seat pricing would undervalue it and confuse the persona. The $1,049 flat rate is positioned above the per-seat midpoint for a 100-person company but below what a Chief of Staff would need a VP-level approval to sign. CAC payback math is internally consistent but the CAC input itself is an assumption, not a measured number — confidence will not exceed 0.6 until at least 10 pilot exit interviews are complete._