# Pricing v0 — Three-tier model anchored on Team at $1,049/mo

A 30-day free pilot converts to a paid Team tier at $1,049/mo (list), sized for the Chief of Staff / Head of Ops buyer at a Series A–C SaaS with 50–500 employees. A Scale tier at $2,299/mo captures larger accounts; a Starter tier at $399/mo exists only as a fallback for sub-50-employee edge cases that clear the ICP bar on integrations.

## Tiers
| Tier | Price/mo | Includes | Buyer | Rationale |
|---|---|---|---|---|
| Pilot | Free | 30 days, hard cap. Up to 5 OKRs ingested, 3 integrations (any of GitHub / Linear / Jira / Notion / Slack), 1 seat (buyer persona only), weekly narrative delivered every Friday. No credit card required at signup; card collected on day 21 for conversion. | Chief of Staff or Head of Ops at a Series A–C SaaS, 50–500 employees, evaluating whether the Friday brief is worth paying for. | 30 days is long enough to receive 4 Friday briefs — the minimum sample for a buyer to form a real opinion — and short enough to create urgency before the quarter-end review cycle. |
| Starter | $399 | Up to 10 OKRs, 3 integrations, 3 seats, weekly narrative, email support. Annual prepay option at $3,829 (~20% discount, equivalent to $319/mo). | Series A edge case: 30–60 employees, tight budget, CoS is also the operator. Exists to avoid losing a willing-to-pay pilot on pure price grounds. | Priced below the Team anchor to give the sales conversation a floor, not a ceiling — most pilots should be steered toward Team. |
| Team | $1,049 | Up to 25 OKRs, all 5 integrations (GitHub + Linear/Jira + Slack + Notion), 10 seats, weekly narrative + Monday brief, Slack digest, pilot-PM onboarding call, email + Slack support. Annual prepay at $10,070 (~20% discount, equivalent to $839/mo). | Primary ICP: Chief of Staff or Head of Ops at a 50–300 employee Series A–C SaaS. This is the tier the product is built for and where the CAC payback math closes. | $1,049 sits below the ~$1,200/mo mental threshold most CoS buyers have for 'needs a procurement cycle' while clearing the CAC payback constraint at a blended CAC of $4,800. |
| Scale | $2,299 | Unlimited OKRs, all integrations, unlimited seats, weekly narrative + Monday brief + ad-hoc on-demand narrative runs (up to 4/mo), dedicated onboarding, quarterly business review, SLA 99.9% uptime. Annual prepay at $22,070 (~20% discount, equivalent to $1,839/mo). | Series B–C, 200–500 employees, multiple business units each with their own OKR tree, VP of Ops or COO as economic buyer. | Anchors the value ceiling and makes Team look like the obvious choice for most pilots; also captures the real revenue upside from larger accounts without a custom-quote motion. |

**CAC payback assumption:** 4.6 months

- Blended CAC assumption: $4,800
- Anchor-tier ARPU: $1,049/mo
- Gross margin assumption: 82%

## List vs negotiated
Expect 60–70% of converting pilots to negotiate; the defensible landing zone is $849–$949/mo on Team (a 10–19% discount) in exchange for an annual prepay commitment — this still clears the CAC payback at 5.7 months. Do not discount below $799/mo on monthly billing; that breaks the payback math. Starter is already the floor — do not create a fourth tier in the field.

## Decisions needed from operator
- [ ] Is $4,800 blended CAC realistic given the current outbound-heavy acquisition motion, or should we model higher (e.g., $7,200) and reprice the anchor tier upward before the first conversion conversation?
- [ ] Should the Pilot hard-stop at 30 days with a credit-card gate on day 21, or do we allow a one-time 14-day extension for accounts that have activated (read ≥1 narrative) but haven't made a decision — risking KR2.3 dilution?
- [ ] Do we offer a nonprofit / early-stage discount (e.g., 40% off Team for seed-stage companies that clear the integration bar) to accelerate the first 25 paid conversions, or does that poison the pricing anchor before we have willingness-to-pay data?

_Confidence: 0.45_
_Reasoning: There is no willingness-to-pay data as of 2026-06-22: KR2.3 and KR2.5 are both 'not started,' the customer pipeline in §8 shows zero named accounts, and no discovery interviews are logged as complete. The $1,049 anchor is derived from comparable B2B SaaS ops-tooling comps (Notion for Teams ~$960/yr/seat, Mooncamp ~$900/yr, Lattice ~$11/seat/mo) scaled to a per-account model appropriate for a CoS buyer with sub-$25K annual software authority, then back-solved against the ≤6-month CAC payback constraint at an assumed $4,800 blended CAC — that CAC assumption is itself unvalidated. The first 10 pilot exit interviews (targeting KR2.3) are the single most important input to Pricing v1; this model should be treated as a negotiating hypothesis, not a settled price._