# Budget overview — cycle 2026-04-28 → 2026-08-28

> Hand-prepared by the operator + Claude as the planning-team stand-in, in lieu of running `cfo.pipeline.run(kind="budget_overview")` (that kind is not yet implemented; the live CFO agent currently produces `pricing_model` proposals only). Treat this document as the v0 budget for operator approval before enabling the live API key, agents, or remote Sunday routine.

---

## TL;DR

- **Recommended budget: $30,000 over 4 months** to hit 300 pilots by 2026-08-28.
- The single biggest line item is **GTM ($20.9K = 71% of total)** — primarily paid LinkedIn ($9K) and content production ($3.5K). LLM and infra together are <12% of total.
- **Unit economics at steady state** (300 pilots → 75 paying at Team tier $899/mo): MRR $67K, COGS ~$3.9K/mo, gross margin ~94%. LLM cost is ~2% of revenue.
- **Aggressive floor: $22K** if M2 organic acquisition (Product Hunt + content) outperforms.
- **Comfortable target: $30K.** Recommended.
- **With ad-test latitude: $40K.** Only if early acquisition signals warrant doubling down.

---

## 1. LLM cost model (Anthropic API)

**Pricing reference** (per million tokens, from `core/llm.py`):
| Model | Input | Output | Cached read |
|---|---|---|---|
| haiku-4-5 | $1.00 | $5.00 | $0.10 |
| sonnet-4-6 (default) | $3.00 | $15.00 | $0.30 |
| opus-4-7 (critique only) | $15.00 | $75.00 | $1.50 |

**Caching matters.** The strategy pod's system block (~4,500 tokens of company.yaml + TRACKER.md) gets cached, so calls 2-4 in a single Sunday run cost ~25% of call 1. Same pattern for OKR-Mapper: a stable per-account system block holds the company's KRs and is hit thousands of times per week per account.

### Per-pod monthly LLM run-rate

| Pod | M1 (≤5 pilots) | M2 (~25) | M3 (~75) | M4 (~175) | At 300 pilots |
|---|---|---|---|---|---|
| Strategy (CEO/CPO/CTO/CFO) | $0.20 | $0.20 | $0.20 | $0.20 | $0.20 |
| Product/Design | $5 | $10 | $10 | $10 | $10 |
| Engineering (background only) | $20 | $30 | $40 | $50 | $50 |
| **AI/Data (Mapper + Narrative + Forecast)** | **$10** | **$80** | **$200** | **$450** | **$750** |
| GTM (Demand-Gen + Content + Founder-Sales) | $30 | $80 | $120 | $130 | $130 |
| Customer/Ops | $5 | $30 | $60 | $90 | $105 |
| **LLM total / month** | **$70** | **$230** | **$430** | **$730** | **$1,045** |
| With 30% buffer | $91 | $300 | $560 | $950 | **$1,350** |

**4-month LLM total: ~$1,740** (linear ramp).

**Driver:** OKR-Mapper dominates. Each ingested event (commit, ticket, Slack thread) costs ~$0.0075 effective (incl. re-mapping). At 60 events/wk/pilot, this scales linearly with pilot count. **Optimization lever: swap Haiku for re-mappings of unchanged content → cuts AI/Data pod cost ~50%.**

### Per-step (sprint) LLM forecast

| Sprint | Window | Pilots end-of-sprint | LLM spend |
|---|---|---|---|
| 0 | 04-28 → 05-12 | 0 (build phase) | $40 |
| 1 | 05-13 → 05-26 | 5 design partners | $50 |
| 2 | 05-27 → 06-09 | 25 (M1) | $90 |
| 3 | 06-10 → 06-23 | 50 | $150 |
| 4 | 06-24 → 07-09 | 75 (M2) | $230 |
| 5 | 07-10 → 07-23 | 125 | $350 |
| 6 | 07-24 → 08-09 | 175 (M3) | $480 |
| 7 | 08-10 → 08-28 | 300 (M4) | $750 |
| **Total** | | | **~$2,140** |

(Slight delta from the $1,740 per-month rollup due to mid-month cohort growth.)

---

## 2. Infrastructure & tooling

| Service | M1 | M2 | M3 | M4 | 4-mo total | Note |
|---|---|---|---|---|---|---|
| Domain (1yr, one-time) | $15 | — | — | — | $15 | |
| Vercel Pro | $20 | $20 | $20 | $20 | $80 | free tier risky once we have customers |
| Supabase Pro | $25 | $25 | $25 | $25 | $100 | |
| Inngest | $0 | $20 | $50 | $100 | $170 | scales with events |
| Nango | $0 | $50 | $100 | $200 | $350 | scales with accounts × integrations |
| PostHog | $0 | $0 | $0 | $20 | $20 | free up to ~1M events |
| Sentry / Axiom | $26 | $26 | $26 | $50 | $128 | |
| Stripe | $0 | $0 | $10 | $30 | $40 | % of revenue, mostly post-pilot |
| Postmark (transactional email) | $15 | $15 | $30 | $50 | $110 | |
| Tooling subs (Notion, Linear, Loom, Apollo, Lemlist, Calendly) | $200 | $200 | $200 | $200 | $800 | |
| **Subtotal** | **$301** | **$356** | **$461** | **$695** | **$1,813** | |

---

## 3. GTM (the elephant — 71% of total spend)

| Item | M1 | M2 | M3 | M4 | 4-mo total | Why |
|---|---|---|---|---|---|---|
| Founder outreach (lunches, intros, swag) | $300 | $200 | $100 | $100 | $700 | warm network costs |
| Apollo/data subscription | (in tooling) | | | | | |
| LinkedIn ads (test → scale) | $0 | $1,500 | $2,500 | $5,000 | $9,000 | hypothesis-tested by cohort, not blown in M4 |
| Product Hunt assets (video + design) | $0 | $1,000 | $0 | $0 | $1,000 | M2 launch |
| Content production (designer/editor freelance) | $0 | $500 | $1,500 | $1,500 | $3,500 | only after we know what works |
| Podcast tour (mics, post-prod, fees) | $0 | $200 | $200 | $200 | $600 | |
| Community sponsorships (Chief of Staff Network etc.) | $0 | $0 | $1,000 | $2,000 | $3,000 | |
| Referral program incentives | $0 | $0 | $500 | $2,000 | $2,500 | unlock once 50+ pilots seed referrals |
| Free swag / dinners for pilot champions | $150 | $150 | $150 | $150 | $600 | retention is acquisition |
| **Subtotal** | **$450** | **$3,550** | **$5,950** | **$10,950** | **$20,900** | |

**Note on the LinkedIn ad budget:** original plan called for "$15K LinkedIn test in M4." This proposal trims to $9K spread M2-M4 because we should test by ICP segment (Series A vs. B vs. C; eng-led vs. RevOps-led) BEFORE concentrating spend. If M2 paid ROAS is bad, M3 and M4 LinkedIn lines collapse to $1K each → save $5.5K.

---

## 4. Cumulative spend by pod (4-month total)

| Pod | LLM | Infra/tools attributable | GTM | Total | % of $30K |
|---|---|---|---|---|---|
| Strategy | $1 | — | — | $1 | 0.0% |
| Product/Design | $35 | $50 (Figma etc.) | — | $85 | 0.3% |
| Engineering | $140 | $623 (Vercel, Supabase, Inngest, Sentry) | — | $763 | 2.6% |
| AI/Data | **$1,400** | $20 (PostHog) | — | $1,420 | 4.8% |
| GTM | $360 | $920 (Apollo/Lemlist/Postmark) | $20,900 | **$22,180** | **75.5%** |
| Customer/Ops | $200 | — | — | $200 | 0.7% |
| **Subtotal** | **$2,136** | **$1,613** | **$20,900** | **$24,649** | 84% |
| 20% contingency | | | | $4,930 | 17% |
| **Grand total** | | | | **$29,579** | **100%** |

Headline: **GTM is 3× everything else combined.** If you have to defend the budget to a partner or spouse, that's the number that gets attacked. Be ready to show what each $1K of paid acquisition is supposed to buy in pilots.

---

## 5. Per-sprint cash budget

| Sprint | Window | Goal | LLM | Infra | GTM | Sprint spend | Cumulative |
|---|---|---|---|---|---|---|---|
| 0 | 04-28 → 05-12 | MVP live, 5 design partners | $40 | $200 | $200 | **$440** | $440 |
| 1 | 05-13 → 05-26 | NPS measured, first case study | $50 | $150 | $250 | **$450** | $890 |
| 2 | 05-27 → 06-09 | 25 pilots (M1) | $90 | $200 | $1,800 | **$2,090** | $2,980 |
| 3 | 06-10 → 06-23 | PH launch + first paid tests | $150 | $200 | $2,800 | **$3,150** | $6,130 |
| 4 | 06-24 → 07-09 | 75 pilots (M2) | $230 | $250 | $3,200 | **$3,680** | $9,810 |
| 5 | 07-10 → 07-23 | Content engine | $350 | $250 | $3,500 | **$4,100** | $13,910 |
| 6 | 07-24 → 08-09 | 175 pilots (M3) | $480 | $300 | $4,200 | **$4,980** | $18,890 |
| 7 | 08-10 → 08-28 | 300 pilots (M4) — final push | $750 | $400 | $4,950 | **$6,100** | **$24,990** |
| Contingency 20% | | | | | | $4,998 | **$29,988** |

**Spend curve:** ~$1K in Sprints 0-1 (build + design partners), $2-3K in Sprint 2 (acquisition starts), then $3-6K per sprint as paid acquisition ramps. **75% of spend is in the back half (Sprints 4-7).**

---

## 6. Operating cost at steady state (post-cycle)

If you hit 300 pilots and convert 25% (= 75 paying) on the Team tier ($899/mo):

| Line | Monthly | Notes |
|---|---|---|
| MRR | $67,425 | 75 × $899 |
| LLM (Anthropic) | $1,350 | scales linearly w/ accounts |
| Infrastructure | $1,500 | Vercel/Supabase/Inngest/Nango at scale |
| Tooling subscriptions | $300 | |
| Stripe fees | $2,000 | ~3% of MRR |
| Email/observability | $200 | |
| **COGS subtotal** | **$5,350** | |
| **Gross margin** | **92%** | excellent for a thin-AI vertical SaaS |
| ARR run-rate | **$809,100** | |

**Cash-flow inflection:** if 25% of pilots convert at end of cycle (i.e. ~Sept-Oct 2026), you become roughly cash-flow neutral on operating costs by Sprint 8 (post-cycle). The $30K budget is what buys you that inflection.

---

## 7. Where to throttle if cash is tight

In priority order (cut top first):

1. **LinkedIn ads M3-M4** — if M2 paid CAC > $400, cut M3 to $1K and M4 to $1K. **Saves $5,500.**
2. **Community sponsorships M4** — defer if referral motion is working. **Saves $2,000.**
3. **Content freelance** — ship content yourself in Sprint 4-5 if you have bandwidth. **Saves $1,000-$3,000.**
4. **Apollo subscription** — defer to M2 once outbound starts. **Saves $300.**
5. **Vercel/Supabase Pro tiers** — stay on free in Sprint 0-1 if you can stomach the limits. **Saves $90.**

Aggressive cuts get you to **$22K floor** without changing the pilot target.

---

## 8. Where NOT to cut

- **AI/Data LLM spend** — this IS the product. Cutting it = cutting product quality. Instead: enforce a per-account daily LLM cap as a circuit breaker (alert when any account spikes >10× median).
- **Sentry/observability** — you cannot debug at 50+ pilots without it.
- **Postmark** — transactional email reliability is the difference between a working product and an embarrassing one.
- **Free swag / dinners for pilot champions** — small line, outsized retention impact.

---

## 9. Decisions needed from operator

- [ ] **Approve $30,000 budget for the cycle** (or specify a different cap).
- [ ] **Approve Anthropic API key activation** — currently in `.env`, dry-run was on. With this budget approved, flip `OKR_MONITOR_DRY_RUN=false` and the Sprint 0 LLM forecast ($40 across 14 days) starts billing.
- [ ] **Confirm GTM allocation shape** — is the $20.9K GTM line acceptable, or do you want a more conservative $10K and accept slower pilot acquisition?
- [ ] **Daily LLM cost circuit breaker threshold** — recommend $50/day overall hard cap during Sprint 0-1, raised to $100/day in Sprint 2+. Per-account cap recommended at 10× the median account spend.
- [ ] **GitHub repo init + remote routine creation** — paused pending budget approval. Routine itself costs $0 (it runs for ~2 minutes/week using Claude Code's own infrastructure). The Sunday spend is the strategy-pod LLM cost: ~$0.04/run = $0.17/month.

---

## 10. Confidence

**0.65.** The infrastructure and LLM numbers are well-grounded (real pricing, actual measured token counts from the smoke test). The GTM numbers are the wide error bars — paid CAC for B2B SaaS at this stage varies 3-5× depending on ICP fit. The model assumes 25% pilot→paid conversion at the Team tier, which is itself a hypothesis (KR2.3) — if it lands at 15%, ARR drops to $485K and gross margin remains healthy but cash-neutrality slips a quarter.

The main missing input is willingness-to-pay signal from the 10 discovery calls (KR1.4) — once those land in Sprint 0, the CFO agent should re-run pricing and this budget should be revised against actual buyer feedback.
