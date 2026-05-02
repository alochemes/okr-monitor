"""Hand-labeled OKR-Mapper evaluation set v0 — 50 events.

Each example is `{"event": <event_dict>, "labels": <set of KR IDs>, "notes": str}`.

Coverage:
  - 17 KRs from TRACKER.md §2 — at least one example each (skipping qualitative
    KRs that real events rarely tie to)
  - 10 negatives (events that should map to nothing — personal tasks, off-topic
    chatter, infra work in unrelated repos)
  - 4 multi-mapping events (legitimately advance ≥2 KRs at once)

Source distribution (mimics the eventual production mix):
  github        — 16   (PRs, commits, pushes)
  manual / mgmt — 18   (operator-logged events: pilot signups, calls, etc.)
  proposal      — 6    (dogfood — outputs from our own agent system)
  content       — 4    (blog posts, LinkedIn posts)
  slack         — 4    (threads, messages)
  other         — 2    (twitter, calendar)

How to grow this set:
  - Add new examples to `EXAMPLES` (keep `event["id"]` unique)
  - Re-run `python -m tests.eval.run_eval`
  - When this hits 200 entries, migrate to JSONL so external labelers can
    contribute via PRs without merge-conflicting one Python literal

Calibration intent: the labels reflect the *honest* answer — what would a
careful human say this event advances? "Plausible if you squint" is NOT a
correct label; the mapper is supposed to drop those at conf<0.5.
"""

from __future__ import annotations

from typing import Any


# ---------------------------------------------------------------------------
# Helpers — keep examples short by reusing common field shapes.

def _ev(
    eid: str,
    *,
    title: str,
    body: str,
    source: str = "manual",
    kind: str = "note",
    actor: str = "andrew",
    occurred_at: str = "2026-05-01T17:00:00+00:00",
) -> dict[str, Any]:
    return {
        "id": eid, "source": source, "kind": kind, "actor": actor,
        "occurred_at": occurred_at, "title": title, "body": body,
    }


# ---------------------------------------------------------------------------
# The 50 labeled examples. Order is roughly: by KR (1.x, 2.x, 3.x, 4.x),
# then multi-mapping, then negatives.

EXAMPLES: list[dict[str, Any]] = [
    # ---- KR 1.1 — MVP deployed to production ---------------------------------
    {
        "event": _ev(
            "ev_001", source="github", kind="push", actor="andrew",
            title="Set up Vercel project for product app",
            body="Created a new Vercel project named okr-monitor-app. "
                 "Configured environment variables for SUPABASE_URL and "
                 "SUPABASE_ANON_KEY. First deploy succeeds with placeholder "
                 "page. Next: wire the auth wall.",
        ),
        "labels": ["1.1"],
        "notes": "Concrete step toward MVP-in-prod (KR1.1 deliverable).",
    },
    {
        "event": _ev(
            "ev_002", source="github", kind="pr", actor="andrew",
            title="Deploy MVP v0 to staging at app.okrmonitor.com",
            body="PR #12 — staging environment now responding 200 at the "
                 "custom domain. End-to-end auth flow + a stub dashboard. "
                 "Production cutover gated on an integration test pass.",
        ),
        "labels": ["1.1"],
        "notes": "Direct MVP deploy progress.",
    },
    {
        "event": _ev(
            "ev_003", source="linear", kind="issue_closed", actor="andrew",
            title="Configure custom domain DNS for production",
            body="Linear issue OKR-43 closed. CNAME app.okrmonitor.com → "
                 "cname.vercel-dns.com is propagated. SSL active.",
        ),
        "labels": ["1.1"],
        "notes": "Infra step that makes prod accessible at canonical URL.",
    },
    {
        "event": _ev(
            "ev_004", source="slack", kind="message", actor="andrew",
            title="Production deploy went green at 14:32 UTC",
            body="Posted in #release: 'okr-monitor-app prod deploy green. "
                 "Smoke tests pass. MVP is live for invite-only.'",
        ),
        "labels": ["1.1"],
        "notes": "Live signal — MVP literally is in production now.",
    },

    # ---- KR 1.2 — 5 active design partners -----------------------------------
    {
        "event": _ev(
            "ev_005",
            title="Kickoff call with Acme Corp scheduled for 2026-05-14",
            body="Booked 60-min kickoff with Sarah Chen (CoS) at Acme. "
                 "They'll come with their current quarterly OKRs and grant "
                 "OAuth access to a sandbox GitHub org.",
        ),
        "labels": ["1.2"],
        "notes": "Pre-onboarding step for a design partner — counts toward 5.",
    },
    {
        "event": _ev(
            "ev_006",
            title="Beta Co signed pilot agreement",
            body="DocuSign returned. 60-day pilot at $0; auto-converts to "
                 "Team tier ($899/mo) unless either party opts out. Beta is "
                 "design partner #2.",
        ),
        "labels": ["1.2"],
        "notes": "Direct evidence of design-partner count change.",
    },
    {
        "event": _ev(
            "ev_007", source="slack", kind="thread",
            title="Charlie Inc onboarded — read first narrative this morning",
            body="Charlie's Head of Ops (Marcus) just confirmed they read "
                 "the first auto-narrative. They flagged one false positive "
                 "on a docs PR, which we've added to the eval set.",
        ),
        "labels": ["1.2"],
        "notes": "Active partner — onboarded and using product weekly.",
    },

    # ---- KR 1.3 — OKR-Mapper precision ≥85% ---------------------------------
    {
        "event": _ev(
            "ev_008", source="github", kind="pr",
            title="Improve mapper prompt for Slack threads",
            body="PR #34 — adds explicit guidance to the mapper system "
                 "prompt for handling Slack thread events: don't infer KR "
                 "linkage from emoji reactions alone, weight the message "
                 "body 3x over the channel name. Eval precision went from "
                 "76% → 84% on slack-source events specifically.",
        ),
        "labels": ["1.3"],
        "notes": "Pure mapper improvement — direct KR1.3 progress.",
    },
    {
        "event": _ev(
            "ev_009", source="github", kind="pr",
            title="Drop mapper confidence floor of 0.5 across pipeline",
            body="Hardens the existing 0.5 floor by enforcing it in code "
                 "even when the model returns 0.4 with high prose conviction.",
        ),
        "labels": ["1.3"],
        "notes": "Mapper hardening — defense in depth on KR1.3.",
    },
    {
        "event": _ev(
            "ev_010",
            title="Hand-labeled 50 more events for OKR-Mapper eval set",
            body="Eval set is now at 100 examples. Next 100 will come from "
                 "real GitHub events on the okr-monitor repo (dogfood).",
        ),
        "labels": ["1.3"],
        "notes": "Building the ruler that measures KR1.3.",
    },
    {
        "event": _ev(
            "ev_011", source="github", kind="commit",
            title="Add prompt cache key to mapper system block",
            body="Marks the system block as cache_control: ephemeral so "
                 "back-to-back mapper calls share the cache hit. Cuts cost "
                 "of a 100-event sweep from $0.75 to $0.21.",
        ),
        "labels": ["1.3"],
        "notes": "Cost-side improvement to the mapper, but still mapper IP. "
                 "Not 1.4 — that's narrative latency, not mapper latency.",
    },

    # ---- KR 1.4 — Time-to-first-narrative ≤30 min ---------------------------
    {
        "event": _ev(
            "ev_012", source="github", kind="pr",
            title="Reduce narrative tokens from 8K to 4K via per-KR slicing",
            body="Narrative agent now generates per-KR sections in parallel "
                 "and concatenates, instead of one big prompt. Cuts wall "
                 "time on a fresh account from 4 min to 1.2 min.",
        ),
        "labels": ["1.4"],
        "notes": "Latency improvement on the narrative pipeline (KR1.4).",
    },
    {
        "event": _ev(
            "ev_013",
            title="First narrative for new account in 22 minutes",
            body="From OAuth grant on Charlie's GitHub to the first auto-"
                 "narrative landing in their inbox: 22:14. Within the 30-min "
                 "p90 target.",
        ),
        "labels": ["1.4"],
        "notes": "Direct measurement of KR1.4.",
    },

    # ---- KR 1.5 — Design-partner NPS ≥50 ------------------------------------
    {
        "event": _ev(
            "ev_014",
            title="Sent NPS survey to all 5 design partners",
            body="One-question Typeform sent to Sarah (Acme), Marcus (Charlie),"
                 " etc. Replies will come in over the next week.",
        ),
        "labels": ["1.5"],
        "notes": "Operational step toward measuring KR1.5.",
    },
    {
        "event": _ev(
            "ev_015",
            title="Acme rated us 9/10 on first NPS pulse",
            body="Sarah replied with 9 + 'this is what I've been waiting for "
                 "— I no longer dread Mondays.' One data point doesn't make "
                 "the average, but it's a clean promoter.",
        ),
        "labels": ["1.5"],
        "notes": "Single NPS response — direct KR1.5 evidence.",
    },

    # ---- KR 2.1 — 300 cumulative pilots --------------------------------------
    {
        "event": _ev(
            "ev_016",
            title="New pilot signup: Echo Inc.",
            body="Echo (Series B fintech, 180 people, OKRs in Notion) "
                 "signed up via the inbound /health-check form.",
        ),
        "labels": ["2.1"],
        "notes": "+1 pilot to the cumulative count.",
    },
    {
        "event": _ev(
            "ev_017",
            title="Pilot count crossed 25 (M1 milestone hit)",
            body="As of today, 25 cumulative pilots. M1 target was 25 by "
                 "2026-06-09; we hit it on 2026-05-30.",
        ),
        "labels": ["2.1"],
        "notes": "Direct progress on the 300-pilot KR.",
    },

    # ---- KR 2.2 — ≥60% pilot activation --------------------------------------
    {
        "event": _ev(
            "ev_018",
            title="Beta Co read 4th weekly narrative this week",
            body="Beta has now read 4 of 4 weekly narratives. They count as "
                 "an activated pilot per the KR2.2 definition (≥1 narrative "
                 "read).",
        ),
        "labels": ["2.2"],
        "notes": "Pilot moves from signed → activated.",
    },

    # ---- KR 2.3 — ≥25% pilot→paid intent -------------------------------------
    {
        "event": _ev(
            "ev_019",
            title="Acme: pilot-to-paid kickoff call booked for 2026-06-01",
            body="Sarah asked to discuss pricing/terms before the 60-day "
                 "pilot expires. Strong paid-intent signal.",
        ),
        "labels": ["2.3"],
        "notes": "Pre-conversion signal — counts toward KR2.3 qualitative read.",
    },

    # ---- KR 2.4 — 3 acquisition channels each producing ≥30 pilots/mo --------
    {
        "event": _ev(
            "ev_020", source="proposal", kind="experiment_proposal",
            title="Started Reddit r/SaaS growth experiment as 4th channel",
            body="Goal: prove a 4th sustainable channel. Initial bench: 10 "
                 "pilot signups in 30 days at <$80 CAC. If it hits, this is "
                 "channel 4 of the 'each ≥30/mo' KR.",
        ),
        "labels": ["2.4"],
        "notes": "New-channel experiment that, if successful, contributes to "
                 "KR2.4. Honest label even though not yet validated.",
    },
    {
        "event": _ev(
            "ev_021",
            title="Outbound channel hit 32 pilots this month",
            body="Outbound (founder-sales agent + LinkedIn DMs) is now "
                 "producing >30 pilots/mo. That's channel 1 of 3 confirmed.",
        ),
        "labels": ["2.4"],
        "notes": "Direct evidence of one channel hitting threshold.",
    },

    # ---- KR 2.5 — CAC payback ≤6 months --------------------------------------
    {
        "event": _ev(
            "ev_022",
            title="First cohort blended CAC computed: $480, payback 5.3mo",
            body="Across all paid pilots that converted: blended CAC = "
                 "$480, gross margin LTV month 1 = $90. Payback 5.3 months "
                 "— inside the 6-month KR target.",
        ),
        "labels": ["2.5"],
        "notes": "First numerical reading on KR2.5.",
    },

    # ---- KR 3.1 — 12 benchmark posts ----------------------------------------
    {
        "event": _ev(
            "ev_023", source="content", kind="blog_post_published",
            title="Published 'State of OKR Execution Q2 2026' benchmark post",
            body="6,200-word benchmark post drawing on data from our 14 "
                 "active pilots. Pull quote: '74% of OKR drift is invisible "
                 "to leadership for 30+ days.'",
        ),
        "labels": ["3.1"],
        "notes": "Concrete benchmark publication — direct KR3.1 increment.",
    },
    {
        "event": _ev(
            "ev_024", source="content", kind="blog_post_draft",
            title="Drafted benchmark post on KR drift in B2B SaaS",
            body="First draft (3,400 words) ready for editing. Will publish "
                 "next week.",
        ),
        "labels": ["3.1"],
        "notes": "In-flight benchmark post — counts as in-progress for 3.1.",
    },

    # ---- KR 3.2 — 5,000 LinkedIn followers -----------------------------------
    {
        "event": _ev(
            "ev_025", source="linkedin", kind="post",
            title="LinkedIn post 'Why monthly check-ins are too late' — 487 reactions",
            body="487 reactions, 64 comments, 28 reposts. Drove +124 "
                 "follower count.",
        ),
        "labels": ["3.2"],
        "notes": "Direct KR3.2 follower-growth event.",
    },
    {
        "event": _ev(
            "ev_026",
            title="Hit 1,000 LinkedIn followers milestone",
            body="Milestone — 20% of way to KR3.2 target (5,000).",
        ),
        "labels": ["3.2"],
        "notes": "Direct KR3.2 progress.",
    },

    # ---- KR 3.3 — 12 podcast appearances -------------------------------------
    {
        "event": _ev(
            "ev_027",
            title="Booked SaaStr Founder Stories podcast for 2026-05-22",
            body="Booked. Pre-recorded format, 45 min. Topic: 'How agents "
                 "rewrote my Monday morning.'",
        ),
        "labels": ["3.3"],
        "notes": "Booked appearance — counts when recorded/aired per KR.",
    },
    {
        "event": _ev(
            "ev_028",
            title="Recorded 'B2B Banter' episode on operational visibility",
            body="Recorded yesterday. Airs in 3 weeks. That's appearance "
                 "#1 for the cycle.",
        ),
        "labels": ["3.3"],
        "notes": "Recorded podcast episode — direct 3.3 count.",
    },

    # ---- KR 3.4 — Product Hunt top 5 ----------------------------------------
    {
        "event": _ev(
            "ev_029",
            title="Drafted Product Hunt launch hero asset and copy",
            body="Hero image, tagline, demo video script all locked. "
                 "Comments-day playbook ready. Launch scheduled for 2026-06-15.",
        ),
        "labels": ["3.4"],
        "notes": "Pre-launch prep — KR3.4 in-flight.",
    },
    {
        "event": _ev(
            "ev_030",
            title="Submitted Product Hunt scheduled launch for 2026-06-15",
            body="Scheduled. Launch goes live at 12:01 AM PT.",
        ),
        "labels": ["3.4"],
        "notes": "Launch lock-in — KR3.4 specific work.",
    },

    # ---- KR 4.1 — 30 agents tracked as work-units ---------------------------
    {
        "event": _ev(
            "ev_031", source="proposal", kind="org_buildout",
            title="Scaffolded 8 more agents using shared _proposal helper (8/30 → 16/30)",
            body="pm, ux_researcher, copywriter, founder_sales, demand_gen, "
                 "content, pilot_pm, onboarding now scaffolded. KR4.1 at "
                 "16/30.",
        ),
        "labels": ["4.1"],
        "notes": "Direct KR4.1 progress (note: KR4.1 is now at 30/30; this "
                 "is a historical-style event for breadth).",
    },

    # ---- KR 4.2 — Weekly narrative auto-generated ---------------------------
    {
        "event": _ev(
            "ev_032", source="proposal", kind="weekly_narrative",
            title="Friday weekly narrative auto-generated (period 04-21 → 04-27)",
            body="proposals/2026-04-27/weekly_narrative.md committed. "
                 "Narrative agent ran on 4 events, 4 mappings, 1 KR active.",
        ),
        "labels": ["4.2"],
        "notes": "Direct KR4.2 evidence.",
    },
    {
        "event": _ev(
            "ev_033", source="proposal", kind="sunday_run",
            title="Sunday workflow committed proposals/2026-05-04/MONDAY_BRIEF.md",
            body="Strategy pod ran, weekly narrative generated, MONDAY_BRIEF "
                 "committed. The whole loop fired without operator touch.",
        ),
        "labels": ["4.2"],
        "notes": "End-to-end KR4.2 reading — auto loop.",
    },
    {
        "event": _ev(
            "ev_034", source="github", kind="pr",
            title="Fix narrative agent for empty mapping windows",
            body="When the mapping window has 0 mappings, the agent used to "
                 "raise a divide-by-zero in the alignment-score calc. Now "
                 "it returns a 'no work this week' brief honestly.",
        ),
        "labels": ["4.2"],
        "notes": "Reliability improvement on the auto-narrative — keeps "
                 "KR4.2 loop healthy.",
    },

    # ---- KR 4.3 — Dogfood gaps → backlog within 24h -------------------------
    {
        "event": _ev(
            "ev_035", source="proposal", kind="dogfood_finding",
            title="Dogfood: report email format unreadable → opened backlog ticket",
            body="Operator (CEO) flagged that the daily 7pm email is too "
                 "dense to skim. Opened OKR-78 within the same day. Fix "
                 "shipped in 4h.",
        ),
        "labels": ["4.3"],
        "notes": "Textbook KR4.3 cycle — dogfood gap → backlog inside 24h.",
    },
    {
        "event": _ev(
            "ev_036", source="proposal", kind="dogfood_finding",
            title="Dogfood: noticed daily report has DRY_RUN spam — fixed within 24h",
            body="Identified that the 4 agent-section bodies were just "
                 "DRY_RUN stubs polluting the email. Banner-and-collapse "
                 "fix shipped same day.",
        ),
        "labels": ["4.3"],
        "notes": "KR4.3 — gap to backlog inside 24h.",
    },

    # ---- Multi-mapping (legitimately advances ≥2 KRs) -----------------------
    {
        "event": _ev(
            "ev_037", source="content", kind="blog_post_published",
            title="Published State of OKR Drift report and posted teaser to LinkedIn",
            body="Benchmark post lives on the blog. Two-paragraph teaser on "
                 "LinkedIn drove 4,200 impressions and +89 followers.",
        ),
        "labels": ["3.1", "3.2"],
        "notes": "Legit dual-mapping: it's a benchmark post (KR3.1) AND a "
                 "LinkedIn-follower-growth event (KR3.2).",
    },
    {
        "event": _ev(
            "ev_038",
            title="Recorded podcast — drove 14 inbound demo requests",
            body="The B2B Banter recording drove 14 form fills in the 48 "
                 "hours after airing. Channel mix is shifting — podcasts "
                 "are now a meaningful inbound source.",
        ),
        "labels": ["3.3", "2.4"],
        "notes": "Multi-mapping: it's a podcast appearance (3.3) and "
                 "evidence of an acquisition channel (2.4).",
    },
    {
        "event": _ev(
            "ev_039",
            title="Product Hunt launch — 47 new pilot signups",
            body="Launched Tuesday. Top 5 of day. 47 inbound pilot signups "
                 "via the /health-check form within 72h.",
        ),
        "labels": ["3.4", "2.1"],
        "notes": "PH launch (3.4) + new pilots (2.1) in one event.",
    },
    {
        "event": _ev(
            "ev_040", source="github", kind="pr",
            title="MVP /app/dashboard route — wires kr_signals snapshot",
            body="First real customer-facing dashboard view. Reads our own "
                 "kr_signals.json (dogfood snapshot). PR #41.",
        ),
        "labels": ["1.1", "4.3"],
        "notes": "MVP-app progress (1.1) AND a dogfood-driven gap fixed "
                 "fast (4.3).",
    },

    # ---- Negatives (should map to NOTHING) ----------------------------------
    {
        "event": _ev(
            "ev_041", source="github", kind="pr", actor="andrew",
            title="Bump eslint to 9.16 in unrelated personal repo",
            body="Routine dependency bump on `andrew/dotfiles-cli`. "
                 "Has nothing to do with OKR Monitor.",
        ),
        "labels": [],
        "notes": "Personal repo, unrelated to company OKRs.",
    },
    {
        "event": _ev(
            "ev_042", source="slack", kind="message",
            title="Reminder: team lunch Friday at noon",
            body="Lunch reminder in #social. No KR.",
        ),
        "labels": [],
        "notes": "Pure social — should not map.",
    },
    {
        "event": _ev(
            "ev_043", source="github", kind="profile_update",
            title="Update profile picture and bio in GitHub settings",
            body="Cosmetic profile change.",
        ),
        "labels": [],
        "notes": "Personal cosmetic action.",
    },
    {
        "event": _ev(
            "ev_044", source="slack", kind="thread",
            title="Thread on which monitor stand to buy for desk setup",
            body="6-message thread weighing options. Off-topic.",
        ),
        "labels": [],
        "notes": "Personal hardware decision — should not map.",
    },
    {
        "event": _ev(
            "ev_045", source="calendar", kind="event",
            title="Doctor appointment 2026-05-08 14:00",
            body="Annual check-up. Personal.",
        ),
        "labels": [],
        "notes": "Personal calendar event.",
    },
    {
        "event": _ev(
            "ev_046",
            title="Replied to recruiter on LinkedIn (declined)",
            body="Polite decline to inbound recruiter. Nothing to do with "
                 "company OKRs.",
        ),
        "labels": [],
        "notes": "Career chatter — not company progress.",
    },
    {
        "event": _ev(
            "ev_047", source="github", kind="pr", actor="andrew",
            title="Pushed commit to Hacktoberfest fork of someone else's project",
            body="Open-source contribution to `vercel/next.js`. Nice "
                 "citizenship; no relation to OKR Monitor's KRs.",
        ),
        "labels": [],
        "notes": "OSS contribution to an unrelated project.",
    },
    {
        "event": _ev(
            "ev_048", source="twitter", kind="tweet",
            title="Tweet: 'this espresso machine just changed my life'",
            body="A tweet about coffee. Tempting to map to KR3.2 (LinkedIn) "
                 "but Twitter ≠ LinkedIn AND it's off-topic anyway.",
        ),
        "labels": [],
        "notes": "Wrong platform AND off-topic — strict negative.",
    },
    {
        "event": _ev(
            "ev_049", source="slack", kind="message",
            title="Random AI article shared in #general",
            body="Posted a Verge article about an unrelated AI product.",
        ),
        "labels": [],
        "notes": "Reading list / curiosity — not KR work.",
    },
    {
        "event": _ev(
            "ev_050", source="github", kind="pr",
            title="Refactored personal dotfiles repo to use stow",
            body="Reorganized andrew/dotfiles to use GNU stow for symlink "
                 "management.",
        ),
        "labels": [],
        "notes": "Personal repo — strict negative.",
    },
]


def labeled_examples() -> list[dict[str, Any]]:
    """Return a copy of the eval set so callers can mutate freely."""
    return [{"event": dict(ex["event"]), "labels": list(ex["labels"]),
             "notes": ex["notes"]} for ex in EXAMPLES]


def stats() -> dict[str, Any]:
    """Quick summary — useful when wiring tests."""
    n = len(EXAMPLES)
    n_neg = sum(1 for ex in EXAMPLES if not ex["labels"])
    n_multi = sum(1 for ex in EXAMPLES if len(ex["labels"]) > 1)
    kr_coverage: dict[str, int] = {}
    for ex in EXAMPLES:
        for kr in ex["labels"]:
            kr_coverage[kr] = kr_coverage.get(kr, 0) + 1
    return {
        "total": n,
        "negatives": n_neg,
        "multi_mapping": n_multi,
        "krs_covered": sorted(kr_coverage.keys()),
        "kr_counts": dict(sorted(kr_coverage.items())),
    }
