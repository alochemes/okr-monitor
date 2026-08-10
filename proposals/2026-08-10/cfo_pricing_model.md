# Pricing v0 — Three-tier model anchored on $1,049/mo Team

A 30-day free pilot converts to a paid Team tier at $1,049/mo (list) or $849/mo (negotiated), sized for the Chief of Staff / Head of Ops buyer at a 50–500-person Series A–C SaaS. CAC payback at the anchor tier clears 6 months under conservative blended-CAC assumptions, but confidence is low without willingness-to-pay data from the 300-pilot cohort.

## Tiers
| Tier | Price/mo | Includes | Buyer | Rationale |
|---|---|---|---|---|
| Pilot | Free | 30 days, 1 workspace, up to 3 integrations (GitHub + 1 ticket tool + Notion/CSV), weekly narrative enabled, operator-assisted onboarding included. Hard stop at day 30 — no auto-extend. | Chief of Staff or Head of Ops at a Series A–C SaaS evaluating OKR drift tooling. No procurement approval needed at $0. | Time-boxed free pilot is the standard B2B SaaS motion for a product whose value is only visible after 2–3 weekly narratives land; 30 days is enough for 4 narratives without giving away a full quarter. |
| Team | $1,049 | 1 workspace, unlimited OKRs, all 5 integrations (GitHub, Linear/Jira, Slack, Notion/CSV), weekly narrative + live scoreboard, up to 25 OKR owners tracked, email support SLA 24h. | Chief of Staff or Head of Ops at a 50–200-person Series A–B SaaS. This is the pilot-conversion tier — the one most pilots land on. Budget authority typically $10K–$50K/yr for ops tooling; $1,049/mo ($12,588/yr) sits comfortably inside that envelope. | $1,049 is $12,588 annualized — below the $15K threshold that typically triggers a second approver at this company size, while delivering enough margin to clear CAC payback in under 6 months at a blended CAC of $4,200. |
| Scale | $2,349 | Up to 3 workspaces (divisions/BUs), unlimited OKR owners, all integrations, weekly + ad-hoc narrative runs, Slack-native digest, dedicated onboarding CSM for 60 days, priority support SLA 4h. | Head of Ops or VP Strategy at a 200–500-person Series B–C SaaS with multiple product lines or business units running separate OKR cycles. Requires a second approver but still below $30K/yr procurement threshold. | $2,349/mo ($28,188/yr) is priced at a 2.24× multiple of Team — justified by multi-workspace complexity and the CSM cost — and creates a credible upsell path without requiring a custom enterprise contract. |

**CAC payback assumption:** 4.8 months

- Blended CAC assumption: $4,200
- Anchor-tier ARPU: $1,049/mo
- Gross margin assumption: 83%

## List vs negotiated
List price for Team is $1,049/mo; expect 75–80% of pilot conversions to negotiate to $849/mo (annual prepay framing: '$849/mo billed $10,188 upfront'). The annual prepay offer should be the default conversion ask — it improves CAC payback to ~4.2 months at the negotiated rate while giving the buyer a 19% discount they can show their CFO. Never discount below $749/mo; below that, gross margin compresses to a point where CAC payback exceeds 6 months even at low blended CAC.

## Decisions needed from operator
- [ ] Do any of the 300-pilot cohort conversations reveal a willingness-to-pay anchor — either a number they named, a competing tool they pay for, or a budget they mentioned? That single data point moves confidence from 0.45 to 0.7+.
- [ ] Should the annual prepay discount (list $12,588 → $10,188) be the default conversion offer, or do you want to hold list monthly and only offer annual when the pilot asks about cost?
- [ ] Is a 30-day pilot hard stop operationally enforceable today (i.e., can the product gate access at day 30), or do we need a softer 'pilot extended by mutual agreement' clause while the access-gating feature is built?

_Confidence: 0.45_
_Reasoning: There is no willingness-to-pay data in TRACKER.md — §8 shows zero signed design partners as of the last update, and §9 explicitly flags pricing as unresolved with a 2026-05-19 deadline that has now passed. The $1,049 anchor is derived from comparable B2B SaaS ops-tooling comps (Notion for Teams ~$960/yr, Mooncamp ~$9/user/mo, Lattice ~$11/user/mo) and the buyer's typical software budget authority, not from a stated price in a customer conversation. The CAC payback math assumes a $4,200 blended CAC — plausible for a founder-led outbound motion at 600 touches/day with a ~1.5% demo-to-pilot rate and a $300 fully-loaded cost per demo — but this number must be validated against the actual GTM spend once the pilot cohort data is available from KR2.4 and KR2.5 tracking._