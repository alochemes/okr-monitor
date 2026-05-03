"""Manual GitHub ingestion CLI.

Usage:
    # Poll the dogfood repo (alochemes/okr-monitor) for the last 7 days
    python scripts/ingest_github.py

    # Specific repo, custom window
    python scripts/ingest_github.py --repo alochemes/skinmap_agents --since-days 30

    # Multiple repos
    python scripts/ingest_github.py --repo owner/foo --repo owner/bar

    # Backfill a longer window (commits only — PRs always tail-paginate)
    python scripts/ingest_github.py --repo alochemes/okr-monitor --since-days 90 \
        --page-cap 20

Auth: set `GITHUB_TOKEN` in `.env` (PAT with `repo` scope; fine-grained PAT
scoped to target repos preferred). Anonymous works for public repos but is
rate-limited to 60 req/h.

Idempotency: schema-level `UNIQUE(source, source_event_id)` means rerunning
this command never creates duplicate work_events. After ingestion, run
`OKR_MONITOR_DRY_RUN=false python scripts/run_okr_mapper.py` to map the new
events into KRs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass

from core import github_ingest, store  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo", action="append", default=None,
        help="owner/repo (repeatable). Defaults to GITHUB_INGEST_REPOS env "
             "or alochemes/okr-monitor.",
    )
    parser.add_argument("--since-days", type=int, default=7)
    parser.add_argument("--page-cap", type=int, default=5,
                        help="Max pages per endpoint per repo (100/page).")
    parser.add_argument("--no-commits", action="store_true")
    parser.add_argument("--no-prs", action="store_true")
    args = parser.parse_args()

    store.init_db()

    if args.repo:
        repos: list[tuple[str, str]] = []
        for r in args.repo:
            if "/" not in r:
                print(f"[err] --repo expects owner/repo, got: {r}", file=sys.stderr)
                return 2
            owner, name = r.split("/", 1)
            repos.append((owner.strip(), name.strip()))
    else:
        repos = github_ingest.configured_repos()

    summary: list[dict] = []
    total_written = 0
    total_seen = 0
    for owner, repo in repos:
        try:
            res = github_ingest.poll_repo(
                owner, repo,
                since_days=args.since_days,
                include_commits=not args.no_commits,
                include_prs=not args.no_prs,
                page_cap=args.page_cap,
            )
        except Exception as exc:
            summary.append({"owner": owner, "repo": repo, "ok": False,
                            "error": str(exc)})
            continue
        total_written += res["events_written"]
        total_seen += res["events_seen"]
        summary.append({
            "owner": owner, "repo": repo, "ok": True,
            "events_written": res["events_written"],
            "events_seen": res["events_seen"],
            "commits": res["commits"], "prs": res["prs"],
            "errors": res["errors"],
        })

    print(json.dumps({
        "repos": len(repos),
        "events_written": total_written,
        "events_seen": total_seen,
        "per_repo": summary,
    }, indent=2))
    return 0 if all(s.get("ok") for s in summary) else 1


if __name__ == "__main__":
    sys.exit(main())
