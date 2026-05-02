"""OKR-Mapper evaluation harness.

The mapper is the load-bearing IP for the company (KR1.3, target ≥85%
precision @ ≥70% recall on a 200-event labeled set). This package houses
the labeled examples, the runner that scores the mapper against them, and
the report writer.

Layout:
  dataset.py    — labeled examples (id, event, true_krs)
  run_eval.py   — runs predict_mappings against each example, computes metrics
  REPORT.md     — most recent run's metrics + per-KR breakdown + misses
"""
