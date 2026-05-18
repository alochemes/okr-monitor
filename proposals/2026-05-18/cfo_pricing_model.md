# Pricing v0 — Three-tier model anchored on $899/mo Team tier

A 30-day free pilot converts to a paid Team tier at $899/mo (list) or $749/mo (negotiated), sized for the Chief of Staff / Head of Ops buyer at a 50–500-person Series A–C SaaS. CAC payback at the anchor tier clears the ≤6-month KR2.5 constraint under conservative blended-CAC assumptions.

## Tiers
| Tier | Price/mo | Includes | Buyer | Rationale |
|---|---|---|---|---|
| Pilot | Free | 30 days, hard stop. Up to 5 OKRs tracked, 3 integrations (GitHub + one ticket source + Slack), 1 seat (buyer persona only), weekly narrative delivered every Friday. No credit card required at signup; card collected at day 21 to reduce conversion friction at day 30. | Chief of Staff or Head of Ops at a Series A–C SaaS, 50–500 employees, evaluating whether the Friday brief is worth paying for. | Time-boxed free removes the 'just another tool' objection and creates a natural conversion event at day 30 without requiring a sales call to close. |
| Team | $899 | Annual contract (billed monthly or annually at 10% discount = $9,711/yr). Up to 15 OKRs, all 5 integrations (GitHub, Linear/Jira, Slack, Notion/CSV), 5 seats, weekly narrative + live scoreboard, email support with 24h SLA. | Same Chief of Staff / Head of Ops buyer who ran the pilot; this is the tier 90%+ of pilot conversions will land on. Budget authority for tools under $15K/yr is typically within their discretion at Series A–C. | $899/mo sits below the $1K/mo psychological threshold that triggers procurement review at most Series A–C companies, while generating enough ARPU to clear CAC payback in under 6 months at a blended CAC of $3,800. |
| Scale | $2,249 | Annual contract only (no monthly option). Unlimited OKRs, unlimited integrations, up to 25 seats, dedicated onboarding (2 live sessions), Slack-channel support, quarterly business review, custom CSV/export for board reporting. | Series B–C companies with multiple business units or a VP of Ops who needs to roll up OKR health across 3+ teams; also the upgrade path when a Team customer grows past 15 OKRs or 5 seats. | $2,249/mo is priced at 2.5× Team to reflect the dedicated onboarding and multi-team surface area, not to be the primary conversion target — it exists to capture upside from larger pilots and to anchor Team as the obvious choice. |

**CAC payback assumption:** 4.2 months

- Blended CAC assumption: $3,800
- Anchor-tier ARPU: $899/mo
- Gross margin assumption: 82%

## List vs negotiated
List price for Team is $899/mo; expect 75–80% of pilot-to-paid conversions to negotiate to $749/mo (first-year discount framed as 'design partner rate') — this is the number the founder should have in their back pocket before the day-28 conversion call. At $749/mo the CAC payback extends to ~5.1 months, still inside the KR2.5 ceiling. Do not discount below $699/mo without operator approval; below that level the payback math breaks at the assumed blended CAC.

## Decisions needed from operator
- [ ] Is $3,800 blended CAC a defensible assumption? The GTM pod is targeting 600 outbound touches/day — if founder-time is costed at $0 and only tooling spend is counted, CAC could be as low as $400; if founder-time is fully loaded at $150/hr and average 25 touches per booked demo, blended CAC is closer to $6,200, which breaks the payback math at $749/mo. Which CAC definition should KR2.5 use?
- [ ] Should the Pilot tier collect a credit card at day 21 (reduces conversion friction, increases opt-out anxiety) or remain fully no-card-required through day 30 (cleaner trust signal for a product asking for GitHub/Slack OAuth access)?
- [ ] Is annual-only for Scale the right constraint, or should monthly-at-premium ($2,699/mo) be offered to avoid losing larger pilots who won't sign an annual contract before seeing a second quarter of data?

_Confidence: 0.45_
_Reasoning: No willingness-to-pay data exists as of 2026-05-18 — KR1.2 (5 design partners) is not yet met and KR2.3/KR2.5 have no current values. The $899 anchor is derived from comparable B2B SaaS ops-intelligence tools (Notion, Coda, Loom at team tier; OKR-specific tools like Perdoo and Quantive at $600–$1,200/mo for similar seat counts) and from the buyer's typical discretionary budget ceiling (~$15K/yr without procurement). The CAC payback math is internally consistent but the blended CAC assumption of $3,800 is a placeholder — the first 10 pilot conversion calls will either validate or break it, and pricing should be revisited at the Sprint 1 close (2026-05-26) once exit-interview data from the first converting pilots is available._