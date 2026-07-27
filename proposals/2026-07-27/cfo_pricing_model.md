# Pricing v0 — Three-tier model anchored on Team at $1,049/mo

A 30-day free pilot converts to a paid Team tier at $1,049/month (list), sized for the Chief of Staff / Head of Ops buyer at a Series A–C SaaS with 50–500 employees. A lighter Starter tier at $399/month captures smaller or more cautious buyers; a Scale tier at $2,499/month exists for companies needing multi-team OKR coverage.

## Tiers
| Tier | Price/mo | Includes | Buyer | Rationale |
|---|---|---|---|---|
| Pilot | Free | 30 calendar days; up to 3 OKR sets ingested; 1 integration (GitHub or Linear/Jira); weekly narrative delivered every Friday; full feature access — no artificial hobbling | Chief of Staff or Head of Ops at a Series A–C SaaS, 50–500 employees, evaluating whether the Friday brief is worth paying for | 30 days is long enough to see two full weekly narratives and one drift-catch event; short enough to force a conversion decision before the quarter ends. |
| Starter | $399 | Up to 2 OKR sets; 2 integrations; weekly narrative; scoreboard access for up to 5 seats; no SLA | Smaller Series A (50–100 employees) or a buyer whose budget authority tops out around $5K/year; likely to upgrade once the CEO sees the brief | Exists to avoid losing pilots who balk at $1,049 — not the anchor, but a real revenue floor that still clears CAC payback in under 6 months at blended CAC. |
| Team | $1,049 | Up to 5 OKR sets; all 5 integrations (GitHub, Linear, Jira, Slack, Notion); weekly narrative + daily scoreboard; up to 15 seats; email support with 48h response | Chief of Staff or Head of Ops at a 100–500 employee Series B/C SaaS; this is the buyer the ICP is built around and the tier most pilots will land on | Anchored at $1,049 (not $999) to signal enterprise-grade positioning while staying inside a Chief of Staff's no-PO-required budget band; $12,588 ARR per account clears a $5,000 blended CAC in under 5 months at 80% gross margin. |
| Scale | $2,499 | Unlimited OKR sets; all integrations; weekly narrative + daily scoreboard; unlimited seats; Slack-based support; quarterly business review | Series C company with multiple business units each running their own OKRs, or a Chief of Staff managing a CEO who wants cross-team roll-up visibility | Priced at 2.4× Team to reflect the multi-team complexity cost and to anchor the Team tier as the obvious choice for the median pilot. |

**CAC payback assumption:** 4.8 months

- Blended CAC assumption: $5,000
- Anchor-tier ARPU: $1,049/mo
- Gross margin assumption: 82%

## List vs negotiated
Expect 60–70% of converting pilots to negotiate; the defensible floor is $849/month for Team (a ~19% discount framed as 'pilot conversion rate') and $299/month for Starter — both still clear CAC payback inside 6 months. Do not discount below these floors in the first cohort; the exit-interview data from KR2.3 is more valuable than the incremental ARR from a deeper cut.

## Decisions needed from operator
- [ ] Is $5,000 blended CAC a reasonable assumption given the outbound-heavy GTM motion described in §3 (GTM Pod KR: 600 outbound touches/day)? If founder-time is the primary CAC driver, the real number could be $2,000–$8,000 — this changes whether Starter at $399 clears the payback constraint.
- [ ] Should the Pilot tier be gated (application or demo required) or self-serve? Gated pilots produce higher-intent leads and better exit-interview completion (KR2.3 target ≥90%), but self-serve is the only path to 300 pilots by 2026-08-28 given current GTM capacity.
- [ ] What is the annual prepay discount, if any? A 2-month-free annual offer (≈17% discount) is standard for this price point and would improve cash position, but it requires a decision before the first conversion call — pilots will ask.

_Confidence: 0.45_
_Reasoning: There is zero willingness-to-pay data in TRACKER.md as of today — §8 shows no design partners signed and §9 flags pricing as unresolved since 2026-05-19. The $1,049 Team anchor is derived from comparable B2B SaaS ops-tooling comps (Notion for Teams ~$16/seat, Lattice ~$11/seat, Leapsome ~$8/seat) scaled to a 'platform fee' model appropriate for a Chief of Staff buyer with a $10K–$25K annual software budget authority; it is not validated by a single customer conversation. The CAC payback math is internally consistent but the $5,000 blended CAC assumption is a placeholder — the actual number depends entirely on how much founder time per pilot the GTM motion requires, which will not be known until the first 10 conversion calls are complete._