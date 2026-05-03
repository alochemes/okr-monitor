# TODAY — 2026-05-02 (Saturday) — end of day

_Sprint 0 day 5 of 14 · 10 days to MVP-or-die deadline (2026-05-12) · 3 days to discovery-call & eval-set deadline (2026-05-05)_

## Today's 3 priorities — all shipped

| # | Priority | Status | What landed |
|---|---|---|---|
| **A** | OKR-Mapper eval set v0 | ✅ done | Framework wired, 50 labeled events covering all 17 KRs, `tests/eval/run_eval.py` writes `REPORT.md`. Live-LLM precision number lands on first paid run. |
| **B** | Discovery-call kit | ✅ done | 5 markdown files in `gtm/`. Operator can dial 2026-05-04 09:00 PT without further prep. |
| **C** | MVP product-app skeleton | ✅ done | `daily_evening.py` writes `web/public/kr_signals.json`; `/app/login` + `/app/dashboard` build green; dashboard SSR-renders 17 KRs at request time. |

## Where we ended

- All 3 priorities complete. `npm run build` passes; new routes are 176 B / 109 kB First Load JS (K10 budget = 200 kB, healthy margin).
- KR1.1 (MVP deployed) ~25% — routes exist, deploy + auth + integrations remain.
- KR1.2 (5 design partners) unblocked — bottleneck now is operator dialing time.
- KR1.3 (mapper precision ≥85%) — framework ready, real number when API runs.
- KR4.2 (auto-narrative) — loop wired; first real narrative on next live LLM run.

---

## Next top 5 priorities (from highest leverage downward)

> **Critical path to 2026-05-12 MVP-or-die.** Each priority moves a specific KR; no nice-to-haves on this list.

| # | Priority | KR moved | Sized | Why this beats the alternatives |
|---|---|---|---|---|
| **P1** | **GitHub integration v0 — read commits → `work_events`** | KR1.1, KR3.0 (eng OKR), enables KR1.3 real eval | 1 day | Without a real source feeding events, the mapper has nothing to map and the dashboard reads zeros. GitHub is the easiest integration (App + webhook) and produces the highest event volume. Unlocks KR1.3's real precision number. |
| **P2** | **Vercel deploy of `/v2` + `/app/*` + custom domain** | KR1.1 directly | 0.5 day | The product CTA points at a URL; without a deploy the operator can't share the link in cold emails. Domain DNS + Vercel project + first deploy is a 2-hour event. |
| **P3** | **Supabase magic-link auth wired to `/app/login` + `/app/dashboard` gate** | KR1.1 | 1 day | The dashboard exists but is unauthenticated. Wiring magic-link makes "sign up for design partner program" mean something concrete. Required before any prospect's eyes touch `/app/dashboard`. |
| **P4** | **Grow eval set 50 → 200 + first live-LLM precision number** | KR1.3 (the load-bearing IP) | 1 day | The whole product fails if the mapper precision is <85%. We have 50 events; need 150 more covering negatives + multi-mapping + the long-tail KRs. Real number runs against funded API. |
| **P5** | **Linear integration v0 — read tickets → `work_events`** | KR1.1, doubles event coverage | 1 day | After GitHub, Linear is the second-highest-volume source. Ships the "GitHub + Linear → Friday brief" demo that the cold emails promise. |

**Total work:** ~4.5 days. Fits inside the 10-day MVP-or-die window with 5 days of slack for discovery-call execution, polish, and bug fixes.

### Out-of-scope for this push (and why)

- **Slack ingestion** — needs DPA work and opt-in flow; saves for Sprint 1 when there's a real customer to negotiate scope with.
- **Notion/Asana OKR-doc parse** — operator can paste OKRs into our intake form for the Health Check; no integration needed for design-partner-zero.
- **Forecasting v2 / P(hit) calibration** — verdict heuristics ship usefulness; calibrated probabilities wait for real data per KR class (per Decision 2026-04-29).
- **Promotion gate (`core/promotion.py`)** — Sprint 0 stays Stage 0. Build the gate when an agent first wants Stage 1.
- **CRM tool** — Notion/Sheet works for Sprint 0–1; revisit when pipeline >25 accounts.

### Sequencing rationale

Doing **P2 (Vercel) before P3 (auth)** because P2 takes 2 hours and unblocks the cold-email link; P3 is the 1-day workstream that requires P2 to be live to test against. **P1 (GitHub) before P4 (eval grow)** because real events validate the mapper on real data, which makes the labeled-set growth choices smarter (label what's actually getting confused, not what we guess will be confused). **P5 (Linear) last** because it's a parallel of P1; once P1 is shipped, P5 is mechanical.

### Definition of done for the 10-day window

- 5 design partners signed (KR1.2)
- Live `https://app.okrmonitor.com/app/dashboard` showing real GitHub + Linear events for the dogfood account (KR1.1)
- Mapper precision ≥85% on 200-event eval (KR1.3)
- One auto-generated weekly narrative shipped to a real human inbox (KR4.2)

---

_Working doc, not a system of record. System of record is `TRACKER.md` §6._

