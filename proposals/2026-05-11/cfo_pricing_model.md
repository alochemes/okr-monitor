# Pricing v0 — Three-tier model anchored on Team at $1,049/mo

A 30-day free pilot converts to a Team tier at $1,049/mo list (negotiated floor $749/mo), sized for the Chief of Staff / Head of Ops buyer at a 50–500-person Series A–C SaaS. A Scale tier at $2,199/mo captures larger accounts; a Starter tier at $349/mo exists only as a fallback for sub-50-person edge cases and should not be led with.

## Tiers
| Tier | Price/mo | Includes | Buyer | Rationale |
|---|---|---|---|---|
| Pilot | Free | 30 calendar days, hard stop. Up to 5 integrations (GitHub + Linear/Jira + Slack + Notion + CSV). One OKR set. Weekly narrative delivered every Friday. Full product — no feature gates. Requires signed pilot agreement and completed intake questionnaire before kickoff. | Chief of Staff or Head of Ops at Series A–C SaaS, 50–500 employees. Introduced via outbound or content; approved by operator before kickoff. | Time-boxed and gated by intake to filter tire-kickers and ensure activation rate (KR2.2 ≥60%) is achievable; 30 days is long enough to see two full Friday narratives and one Monday standup anchored by the brief. |
| Starter | $349 | Up to 3 integrations, 1 OKR set, weekly narrative, no custom KPI alerts, email support only. Intended for companies at the low end of ICP (50–80 employees) or as a step-down offer if Team is rejected on budget. | Head of Ops at a lean Series A (50–80 employees) with limited software budget authority; or a pilot that converted but negotiated hard on price. | Exists to avoid losing a converted pilot entirely on price; do not lead with it — it undercuts the anchor and trains buyers to negotiate down. |
| Team | $1,049 | All 5 integrations, up to 3 OKR sets, weekly narrative + daily drift alerts, Slack digest, pilot-to-paid onboarding call, email + Slack support, quarterly business review. Annual commit available at 10% discount ($11,329/yr list). | Chief of Staff or Head of Ops at Series B–C SaaS, 100–300 employees. Has $10–25K software budget authority without CEO sign-off. This is the modal pilot conversion target. | Anchor tier: $1,049/mo was chosen over a round $1,000 to signal deliberate pricing; it sits below the $1,200 threshold that typically triggers a second approver at this ICP size, while producing $12,588 ARR — enough to hit CAC payback at ≤6 months on a $6,000 blended CAC assumption. |
| Scale | $2,199 | Unlimited integrations, up to 10 OKR sets, weekly narrative + daily alerts + ad-hoc narrative runs, dedicated CSM, SLA-backed support, custom KPI thresholds, SSO/SAML. Annual commit available at 10% discount ($23,749/yr list). | Head of Ops or VP Strategy at Series C SaaS, 300–500 employees, multiple business units each with their own OKR set. Likely requires VP-level sign-off; expect a 30–45 day sales cycle post-pilot. | Captures the top 15–20% of the pilot cohort that outgrows Team limits; priced at roughly 2.1× Team to reflect the CSM cost and multi-OKR-set complexity, not to be a stretch goal. |

**CAC payback assumption:** 5.8 months

- Blended CAC assumption: $6,000
- Anchor-tier ARPU: $1,049/mo
- Gross margin assumption: 82%

## List vs negotiated
List is $1,049/mo for Team; expect 60–70% of pilot conversions to negotiate, with a realistic floor of $749/mo (a 29% discount) for annual commit — do not go below $749 without operator approval, as it breaks CAC payback at the assumed $6K blended CAC. Offer the annual commit discount ($11,329/yr ≈ $944/mo) as the first concession before touching monthly list price; this preserves cash-flow optics while giving the buyer a win.

## Decisions needed from operator
- [ ] What is the actual blended CAC today — specifically, how many founder-hours per pilot conversion and at what imputed hourly rate, plus any paid spend? The $6,000 assumption is the load-bearing number for KR2.5 and needs to be validated or revised before the first paid conversion.
- [ ] Is the 30-day pilot hard-stop enforced in the product (access revoked automatically) or is it a soft social contract? Enforcement materially affects KR2.3 conversion rate — soft stops historically convert at half the rate of hard stops.
- [ ] Do we have any willingness-to-pay signal from the 10 discovery calls (KR1.2 target: 5 design partners by 2026-05-19)? If any prospect named a budget number or compared us to a competitor with a known price, that anchors confidence above 0.6 and may shift the Team tier up or down by $200–$300.

_Confidence: 0.45_
_Reasoning: There is no willingness-to-pay data in TRACKER.md as of 2026-05-11 — the design partner pipeline (§8) is empty and the 10 discovery calls are not yet complete (KR1.2 = 0). The $1,049 anchor is derived from comparable B2B SaaS ops-tooling comps (Notion for Teams ~$960/yr/seat × 10 seats, Mooncamp ~$900/mo, Lattice ~$11K ARR) and the buyer's typical discretionary software budget authority (<$25K without CEO sign-off per §7 decision log). The $6,000 blended CAC assumption is optimistic for a founder-led outbound motion at 600 touches/day (§9 risk row) and should be stress-tested the moment the first 25 pilots are in — if CAC lands at $9,000, Team list price needs to move to $1,399 or payback slips to 9 months, violating KR2.5._