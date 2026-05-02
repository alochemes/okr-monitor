# OKR-Mapper eval — REPORT

_Last run: 2026-05-02 19:17 UTC · model: `claude-sonnet-4-6::DRY_RUN` · **DRY_RUN** · $0.0000 · 0.0s_

## Headline

- **Precision: 0.0%** 🔴 (target ≥85%)
- **Recall:    0.0%** 🔴 (target ≥70%)
- F1:         0.000
- Negatives correctly classified: 0/0 (0%)

## Counts

- Examples: **50**  (negatives: 10 · multi-mapping: 4)
- KRs covered: 17 / 17
- TP: 0 · FP: 5 · FN: 5

## Per-KR breakdown

| KR | TP | FP | FN | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| **1.1** | 0 | 0 | 4 | 0.0% | 0.0% |
| **1.2** | 0 | 0 | 1 | 0.0% | 0.0% |
| **4.1** | 0 | 5 | 0 | 0.0% | 0.0% |

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

## How to improve precision

- The largest FP cluster is your tightest leverage point. Read the miss list, find the common shape (e.g. "docs PRs are mapping to KR1.4"), and add one explicit example to `agents/okr_mapper/prompts/map_event.md`.
- The confidence floor (0.5) is enforced in code. To tighten precision at the cost of recall, raise the floor in `agents/okr_mapper/pipeline.py:_map_one` and `predict_mappings`.
- Re-run after each change: `OKR_MONITOR_DRY_RUN=false python -m tests.eval.run_eval`.

## Schedule

- **2026-05-05 (Sprint 0 milestone):** 200-event labeled set + first precision number ≥85%. Today's run is on **50** events — grow toward 200 by adding entries to `tests/eval/dataset.py`.