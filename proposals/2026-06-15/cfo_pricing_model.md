# Pricing v0 — Three-tier model anchored on Team at $1,049/mo

A 30-day free pilot converts to a paid Team tier at $1,049/mo (list) or $849/mo (negotiated first year), sized for the Chief of Staff / Head of Ops buyer at a 50–500-person Series A–C SaaS. A Scale tier at $2,199/mo captures larger accounts; a Starter tier at $399/mo exists only as a fallback to prevent churn, not as the primary landing zone.

## Tiers
| Tier | Price/mo | Includes | Buyer | Rationale |
|---|---|---|---|---|
| Pilot | Free | 30 days hard cap; up to 3 OKR sets ingested; 1 integration (GitHub or Linear/Jira); weekly narrative delivered every Friday; full feature access with no artificial hobbling | Chief of Staff or Head of Ops at Series A–C SaaS, 50–500 employees — evaluating before any budget conversation | 30-day hard cap creates urgency for KR2.3 conversion without feeling predatory; full feature access means the 'magic moment' (Friday narrative) lands before the clock expires. |
| Starter | $399 | Up to 2 OKR sets; 2 integrations; weekly narrative; no Slack digest; no custom KPI layer; 1 seat (buyer only) | Pilot account that genuinely cannot clear $1K/mo budget — Series A companies with <60 employees or constrained ops budgets; use as a save, not a target | Exists to prevent a 'loved it, can't afford it' churn; priced at $399 to stay above the 'free tool' mental category while remaining under typical $500 no-PO-needed thresholds. |
| Team | $1,049 | Up to 8 OKR sets; all 5 integrations (GitHub, Linear, Jira, Slack, Notion); weekly narrative + Friday Slack digest; KPI layer; 3 seats; quarterly business review support | Primary landing tier — Chief of Staff or Head of Ops at 80–300-person Series B/C SaaS with a $10K–$50K annual software budget line; this is the account that hits CAC payback | $1,049 is below the $1,200 psychological ceiling for monthly SaaS without a VP approval, lands at ~$12,600 ARR which is defensible against a $5K–$6K blended CAC, and the odd number signals cost-basis pricing rather than round-number guessing. |
| Scale | $2,199 | Unlimited OKR sets; all integrations; weekly + daily narrative; dedicated onboarding; 10 seats; SLA 99.9%; custom KPI definitions; Slack channel with OKR Monitor team | Series C companies 200–500 employees, or any account where the Head of Ops is running 3+ business units against OKRs and needs daily drift signals, not just weekly | 2× the Team price reflects the step-change in ingestion volume and support cost, not a feature-gate game; positions us to capture larger ARR without a custom enterprise motion. |

**CAC payback assumption:** 5.1 months

- Blended CAC assumption: $4,500
- Anchor-tier ARPU: $1,049/mo
- Gross margin assumption: 84%

## List vs negotiated
List is $1,049/mo (Team); expect 75–80% of pilot-to-paid conversions to negotiate to $849/mo for the first 12 months ('pilot alumni rate'), which still yields $10,188 ARR and a 5.3-month payback at the assumed CAC — inside KR2.5. Do not discount below $799/mo without operator approval; below that, the payback math breaks at any CAC above $4K.

## Decisions needed from operator
- [ ] Is $4,500 a defensible blended CAC assumption given the current outbound-heavy acquisition motion, or do we have early data from the first 25 pilots (KR2.1 target: 25 by 2026-06-09) that should replace this estimate?
- [ ] Should the Starter tier exist at all, or does a $399 fallback undermine the Team anchor by giving buyers a negotiating floor to push toward?
- [ ] What is the pilot exit interview data (KR2.3 proxy) telling us about willingness-to-pay — specifically, are objections price-based or value-based, and does the $1,049 anchor need to move before we hit the 300-pilot milestone?

_Confidence: 0.45_
_Reasoning: There is no willingness-to-pay data in TRACKER.md as of today — the customer pipeline (§8) shows zero named accounts, KR2.3 is at n/a, and the pilot exit interview process has not yet fired. The $1,049 anchor is derived from comparable B2B SaaS ops-tooling comps (Notion Business ~$960/yr per seat, Mooncamp ~$900/yr, Lattice ~$11K ARR for similar buyer) and the constraint that the Chief of Staff buyer typically has unilateral authority up to ~$1,200/mo without a VP sign-off. The CAC assumption of $4,500 is a placeholder based on a founder-led outbound motion at ~3% reply rate and ~15% demo-to-pilot conversion; it must be replaced with real data from the first paying cohort before KR2.5 can be declared on track._