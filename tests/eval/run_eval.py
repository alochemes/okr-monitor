"""Evaluate OKR-Mapper against the labeled set.

Usage:
  # Dry-run (validates wiring; metrics will be poor — mock maps everything to 4.1)
  python -m tests.eval.run_eval

  # Real numbers (requires ANTHROPIC_API_KEY; ~$0.04–$0.08 for 50 events)
  OKR_MONITOR_DRY_RUN=false python -m tests.eval.run_eval

  # Subset for fast iteration
  OKR_MONITOR_DRY_RUN=false python -m tests.eval.run_eval --limit 10

Outputs:
  tests/eval/REPORT.md             — human-readable summary
  tests/eval/last_run.json         — raw per-example predictions for diffing
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass

from agents._base import build_system_prompt  # noqa: E402
from agents.okr_mapper.pipeline import predict_mappings  # noqa: E402
from tests.eval.dataset import EXAMPLES, stats as dataset_stats  # noqa: E402


# ---------------------------------------------------------------------------
# Metrics

def _score_one(true_krs: set[str], pred_krs: set[str]) -> dict[str, int]:
    tp = len(true_krs & pred_krs)
    fp = len(pred_krs - true_krs)
    fn = len(true_krs - pred_krs)
    return {"tp": tp, "fp": fp, "fn": fn}


def _aggregate(per_example: list[dict[str, Any]]) -> dict[str, Any]:
    total_tp = sum(x["score"]["tp"] for x in per_example)
    total_fp = sum(x["score"]["fp"] for x in per_example)
    total_fn = sum(x["score"]["fn"] for x in per_example)

    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) else 0.0
    recall    = total_tp / (total_tp + total_fn) if (total_tp + total_fn) else 0.0
    f1        = (2 * precision * recall / (precision + recall)
                 if (precision + recall) else 0.0)

    # True-negative behavior on the negative set: of the events we labeled with
    # zero true KRs, how many did the mapper correctly predict zero KRs for?
    negatives = [x for x in per_example if not x["true_krs"]]
    neg_correct = sum(1 for x in negatives if not x["pred_krs"])
    neg_rate = neg_correct / len(negatives) if negatives else 0.0

    # Per-KR breakdown.
    krs = sorted({kr for x in per_example for kr in (x["true_krs"] | x["pred_krs"])})
    per_kr: dict[str, dict[str, Any]] = {}
    for kr in krs:
        kr_tp = sum(1 for x in per_example
                    if kr in x["true_krs"] and kr in x["pred_krs"])
        kr_fp = sum(1 for x in per_example
                    if kr in x["pred_krs"] and kr not in x["true_krs"])
        kr_fn = sum(1 for x in per_example
                    if kr in x["true_krs"] and kr not in x["pred_krs"])
        kr_p = kr_tp / (kr_tp + kr_fp) if (kr_tp + kr_fp) else 0.0
        kr_r = kr_tp / (kr_tp + kr_fn) if (kr_tp + kr_fn) else 0.0
        per_kr[kr] = {"tp": kr_tp, "fp": kr_fp, "fn": kr_fn,
                      "precision": kr_p, "recall": kr_r}

    return {
        "tp": total_tp, "fp": total_fp, "fn": total_fn,
        "precision": precision, "recall": recall, "f1": f1,
        "negative_correct": neg_correct,
        "negative_total": len(negatives),
        "negative_rate": neg_rate,
        "per_kr": per_kr,
    }


# ---------------------------------------------------------------------------
# Report writer

_TARGET_PRECISION = 0.85
_TARGET_RECALL = 0.70


def _verdict_glyph(actual: float, target: float) -> str:
    if actual >= target:
        return "🟢"
    if actual >= target * 0.85:
        return "🟡"
    return "🔴"


def _build_report_md(*, agg: dict[str, Any],
                     per_example: list[dict[str, Any]],
                     ds_stats: dict[str, Any],
                     model: str,
                     total_cost_usd: float,
                     wall_seconds: float,
                     dry_run: bool) -> str:
    when = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    p = agg["precision"]
    r = agg["recall"]

    lines: list[str] = [
        "# OKR-Mapper eval — REPORT",
        "",
        f"_Last run: {when} · model: `{model}` · "
        f"{'**DRY_RUN**' if dry_run else 'live'} · "
        f"${total_cost_usd:.4f} · {wall_seconds:.1f}s_",
        "",
        "## Headline",
        "",
        f"- **Precision: {p:.1%}** {_verdict_glyph(p, _TARGET_PRECISION)} "
        f"(target ≥{_TARGET_PRECISION:.0%})",
        f"- **Recall:    {r:.1%}** {_verdict_glyph(r, _TARGET_RECALL)} "
        f"(target ≥{_TARGET_RECALL:.0%})",
        f"- F1:         {agg['f1']:.3f}",
        f"- Negatives correctly classified: "
        f"{agg['negative_correct']}/{agg['negative_total']} "
        f"({agg['negative_rate']:.0%})",
        "",
        "## Counts",
        "",
        f"- Examples: **{ds_stats['total']}**  "
        f"(negatives: {ds_stats['negatives']} · multi-mapping: {ds_stats['multi_mapping']})",
        f"- KRs covered: {len(ds_stats['krs_covered'])} / 17",
        f"- TP: {agg['tp']} · FP: {agg['fp']} · FN: {agg['fn']}",
        "",
        "## Per-KR breakdown",
        "",
        "| KR | TP | FP | FN | Precision | Recall |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for kr, m in sorted(agg["per_kr"].items(), key=lambda kv: kv[0]):
        lines.append(
            f"| **{kr}** | {m['tp']} | {m['fp']} | {m['fn']} | "
            f"{m['precision']:.1%} | {m['recall']:.1%} |"
        )
    lines += ["", "## Failures", ""]

    misses = [x for x in per_example
              if x["score"]["fp"] > 0 or x["score"]["fn"] > 0]
    if not misses:
        lines.append("_No errors — every example matched its labels exactly._")
    else:
        for x in misses[:30]:
            true_s = ", ".join(sorted(x["true_krs"])) or "∅"
            pred_s = ", ".join(sorted(x["pred_krs"])) or "∅"
            lines.append(
                f"- `{x['event_id']}` — **true: {true_s}** vs **pred: {pred_s}**  \n"
                f"  _{x['title'][:90]}_"
            )
        if len(misses) > 30:
            lines.append(f"\n_…and {len(misses) - 30} more — see "
                         "`tests/eval/last_run.json` for full detail._")

    lines += [
        "",
        "## How to improve precision",
        "",
        "- The largest FP cluster is your tightest leverage point. Read the "
        "miss list, find the common shape (e.g. \"docs PRs are mapping to "
        "KR1.4\"), and add one explicit example to "
        "`agents/okr_mapper/prompts/map_event.md`.",
        "- The confidence floor (0.5) is enforced in code. To tighten "
        "precision at the cost of recall, raise the floor in "
        "`agents/okr_mapper/pipeline.py:_map_one` and `predict_mappings`.",
        "- Re-run after each change: `OKR_MONITOR_DRY_RUN=false python -m tests.eval.run_eval`.",
        "",
        "## Schedule",
        "",
        "- **2026-05-05 (Sprint 0 milestone):** 200-event labeled set + first "
        "precision number ≥85%. Today's run is on **50** events — grow toward "
        "200 by adding entries to `tests/eval/dataset.py`.",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None,
                        help="Only run the first N examples (debug).")
    args = parser.parse_args()

    examples = EXAMPLES if args.limit is None else EXAMPLES[: args.limit]
    dry_run = os.environ.get("OKR_MONITOR_DRY_RUN", "true").lower() == "true"

    # Build the cacheable system once. Production pays for the system tokens
    # on the first call and re-reads from cache on the next ~50, so eval cost
    # is dominated by per-example output tokens.
    print(f"[eval] building system prompt (cached across {len(examples)} calls)...",
          file=sys.stderr)
    system = build_system_prompt(
        agent_prompt_md=(ROOT / "agents" / "okr_mapper" / "prompts"
                         / "map_event.md").read_text(encoding="utf-8")
    )

    per_example: list[dict[str, Any]] = []
    total_cost = 0.0
    started = time.time()
    model_seen = "unknown"

    for i, ex in enumerate(examples, 1):
        event = ex["event"]
        true_krs = set(ex["labels"])

        try:
            res = predict_mappings(event, system=system)
        except Exception as exc:
            print(f"[eval] ev_{event['id']} — error: {exc}", file=sys.stderr)
            res = {"mappings": [], "model": "error",
                   "cost_usd": 0.0, "no_mapping_reason": str(exc)}

        pred_krs = {m["kr_id"] for m in res["mappings"]}
        score = _score_one(true_krs, pred_krs)
        total_cost += res.get("cost_usd") or 0.0
        model_seen = res.get("model") or model_seen

        per_example.append({
            "event_id": event["id"],
            "title": event["title"],
            "true_krs": true_krs,
            "pred_krs": pred_krs,
            "predictions": res["mappings"],
            "no_mapping_reason": res.get("no_mapping_reason"),
            "score": score,
        })

        marker = "✓" if not score["fp"] and not score["fn"] else "✗"
        print(f"[eval] {i:3d}/{len(examples)} {marker} {event['id']} "
              f"true={sorted(true_krs)} pred={sorted(pred_krs)}",
              file=sys.stderr)

    wall = time.time() - started
    agg = _aggregate(per_example)

    # Persist raw per-example predictions for diffing across runs.
    raw_out = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "model": model_seen, "dry_run": dry_run,
        "total_cost_usd": round(total_cost, 6),
        "wall_seconds": round(wall, 2),
        "aggregate": {**agg, "per_kr": {k: dict(v) for k, v in agg["per_kr"].items()}},
        "per_example": [
            {**x,
             "true_krs": sorted(x["true_krs"]),
             "pred_krs": sorted(x["pred_krs"])}
            for x in per_example
        ],
    }
    (ROOT / "tests" / "eval" / "last_run.json").write_text(
        json.dumps(raw_out, indent=2, default=str), encoding="utf-8")

    report = _build_report_md(
        agg=agg, per_example=per_example, ds_stats=dataset_stats(),
        model=model_seen, total_cost_usd=total_cost, wall_seconds=wall,
        dry_run=dry_run,
    )
    (ROOT / "tests" / "eval" / "REPORT.md").write_text(report, encoding="utf-8")

    print("\n" + "=" * 60, file=sys.stderr)
    print(f"precision={agg['precision']:.1%}  recall={agg['recall']:.1%}  "
          f"f1={agg['f1']:.3f}  cost=${total_cost:.4f}  "
          f"({len(examples)} examples, {wall:.1f}s)",
          file=sys.stderr)
    print(f"  → tests/eval/REPORT.md", file=sys.stderr)

    # Exit code: 0 if both targets met, 1 otherwise — useful for CI gating
    # later. In dry-run, always 0 (mock metrics aren't meaningful).
    if dry_run:
        return 0
    if agg["precision"] >= _TARGET_PRECISION and agg["recall"] >= _TARGET_RECALL:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
