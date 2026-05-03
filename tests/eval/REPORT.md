# OKR-Mapper eval — REPORT

_Last run: 2026-05-02 19:58 UTC · model: `claude-sonnet-4-6::DRY_RUN` · **DRY_RUN** · $0.0000 · 0.1s_

## Headline

- **Precision: 3.0%** 🔴 (target ≥85%)
- **Recall:    3.1%** 🔴 (target ≥70%)
- F1:         0.031
- Negatives correctly classified: 0/31 (0%)

## Counts

- Examples: **200**  (negatives: 31 · multi-mapping: 21)
- KRs covered: 17 / 17
- TP: 6 · FP: 194 · FN: 186

## Per-KR breakdown

| KR | TP | FP | FN | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| **1.1** | 0 | 0 | 13 | 0.0% | 0.0% |
| **1.2** | 0 | 0 | 12 | 0.0% | 0.0% |
| **1.3** | 0 | 0 | 13 | 0.0% | 0.0% |
| **1.4** | 0 | 0 | 9 | 0.0% | 0.0% |
| **1.5** | 0 | 0 | 9 | 0.0% | 0.0% |
| **2.1** | 0 | 0 | 19 | 0.0% | 0.0% |
| **2.2** | 0 | 0 | 10 | 0.0% | 0.0% |
| **2.3** | 0 | 0 | 10 | 0.0% | 0.0% |
| **2.4** | 0 | 0 | 14 | 0.0% | 0.0% |
| **2.5** | 0 | 0 | 6 | 0.0% | 0.0% |
| **3.1** | 0 | 0 | 16 | 0.0% | 0.0% |
| **3.2** | 0 | 0 | 14 | 0.0% | 0.0% |
| **3.3** | 0 | 0 | 11 | 0.0% | 0.0% |
| **3.4** | 0 | 0 | 9 | 0.0% | 0.0% |
| **4.1** | 6 | 194 | 0 | 3.0% | 100.0% |
| **4.2** | 0 | 0 | 10 | 0.0% | 0.0% |
| **4.3** | 0 | 0 | 11 | 0.0% | 0.0% |

## Failures

- `ev_001` — **true: 1.1** vs **pred: 4.1**  
  _Set up Vercel project for product app_
- `ev_002` — **true: 1.1** vs **pred: 4.1**  
  _Deploy MVP v0 to staging at app.okrmonitor.com_
- `ev_003` — **true: 1.1** vs **pred: 4.1**  
  _Configure custom domain DNS for production_
- `ev_004` — **true: 1.1** vs **pred: 4.1**  
  _Production deploy went green at 14:32 UTC_
- `ev_005` — **true: 1.2** vs **pred: 4.1**  
  _Kickoff call with Acme Corp scheduled for 2026-05-14_
- `ev_006` — **true: 1.2** vs **pred: 4.1**  
  _Beta Co signed pilot agreement_
- `ev_007` — **true: 1.2** vs **pred: 4.1**  
  _Charlie Inc onboarded — read first narrative this morning_
- `ev_008` — **true: 1.3** vs **pred: 4.1**  
  _Improve mapper prompt for Slack threads_
- `ev_009` — **true: 1.3** vs **pred: 4.1**  
  _Drop mapper confidence floor of 0.5 across pipeline_
- `ev_010` — **true: 1.3** vs **pred: 4.1**  
  _Hand-labeled 50 more events for OKR-Mapper eval set_
- `ev_011` — **true: 1.3** vs **pred: 4.1**  
  _Add prompt cache key to mapper system block_
- `ev_012` — **true: 1.4** vs **pred: 4.1**  
  _Reduce narrative tokens from 8K to 4K via per-KR slicing_
- `ev_013` — **true: 1.4** vs **pred: 4.1**  
  _First narrative for new account in 22 minutes_
- `ev_014` — **true: 1.5** vs **pred: 4.1**  
  _Sent NPS survey to all 5 design partners_
- `ev_015` — **true: 1.5** vs **pred: 4.1**  
  _Acme rated us 9/10 on first NPS pulse_
- `ev_016` — **true: 2.1** vs **pred: 4.1**  
  _New pilot signup: Echo Inc._
- `ev_017` — **true: 2.1** vs **pred: 4.1**  
  _Pilot count crossed 25 (M1 milestone hit)_
- `ev_018` — **true: 2.2** vs **pred: 4.1**  
  _Beta Co read 4th weekly narrative this week_
- `ev_019` — **true: 2.3** vs **pred: 4.1**  
  _Acme: pilot-to-paid kickoff call booked for 2026-06-01_
- `ev_020` — **true: 2.4** vs **pred: 4.1**  
  _Started Reddit r/SaaS growth experiment as 4th channel_
- `ev_021` — **true: 2.4** vs **pred: 4.1**  
  _Outbound channel hit 32 pilots this month_
- `ev_022` — **true: 2.5** vs **pred: 4.1**  
  _First cohort blended CAC computed: $480, payback 5.3mo_
- `ev_023` — **true: 3.1** vs **pred: 4.1**  
  _Published 'State of OKR Execution Q2 2026' benchmark post_
- `ev_024` — **true: 3.1** vs **pred: 4.1**  
  _Drafted benchmark post on KR drift in B2B SaaS_
- `ev_025` — **true: 3.2** vs **pred: 4.1**  
  _LinkedIn post 'Why monthly check-ins are too late' — 487 reactions_
- `ev_026` — **true: 3.2** vs **pred: 4.1**  
  _Hit 1,000 LinkedIn followers milestone_
- `ev_027` — **true: 3.3** vs **pred: 4.1**  
  _Booked SaaStr Founder Stories podcast for 2026-05-22_
- `ev_028` — **true: 3.3** vs **pred: 4.1**  
  _Recorded 'B2B Banter' episode on operational visibility_
- `ev_029` — **true: 3.4** vs **pred: 4.1**  
  _Drafted Product Hunt launch hero asset and copy_
- `ev_030` — **true: 3.4** vs **pred: 4.1**  
  _Submitted Product Hunt scheduled launch for 2026-06-15_

_…and 164 more — see `tests/eval/last_run.json` for full detail._

## How to improve precision

- The largest FP cluster is your tightest leverage point. Read the miss list, find the common shape (e.g. "docs PRs are mapping to KR1.4"), and add one explicit example to `agents/okr_mapper/prompts/map_event.md`.
- The confidence floor (0.5) is enforced in code. To tighten precision at the cost of recall, raise the floor in `agents/okr_mapper/pipeline.py:_map_one` and `predict_mappings`.
- Re-run after each change: `OKR_MONITOR_DRY_RUN=false python -m tests.eval.run_eval`.

## Schedule

- **2026-05-05 (Sprint 0 milestone):** 200-event labeled set + first precision number ≥85%. Today's run is on **50** events — grow toward 200 by adding entries to `tests/eval/dataset.py`.