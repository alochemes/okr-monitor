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

    # =========================================================================
    # v0 → v1 — eval set grow-out 50 → 200 (Sprint 0 milestone 2026-05-05)
    # Focus: long-tail KRs (KR2.x, KR3.x), more strict negatives, more
    # multi-mappings, more source diversity (linear / pr_merged / podcast).
    # =========================================================================

    # ---- KR 1.1 — MVP deployed (more) ---------------------------------------
    {
        "event": _ev(
            "ev_051", source="github", kind="pr_merged",
            title="Wire Supabase magic-link auth on /app/login",
            body="PR #51. Adds @supabase/ssr client, server, and middleware. "
                 "Magic-link redirects through /app/auth/callback and seats "
                 "the session cookie. /app/dashboard is now auth-gated.",
        ),
        "labels": ["1.1"],
        "notes": "Direct MVP-deployed-to-prod work — auth is a hard gate.",
    },
    {
        "event": _ev(
            "ev_052", source="linear", kind="issue_completed",
            title="OKR-58 — Vercel project linked, first prod deploy green",
            body="Initial deploy of web/ subdirectory. Domain CNAME pending. "
                 "Build size 174 kB First Load on /app/login.",
        ),
        "labels": ["1.1"],
        "notes": "Concrete prod-deploy step.",
    },
    {
        "event": _ev(
            "ev_053", source="github", kind="pr",
            title="Add web/middleware.ts gating /app/* routes",
            body="Edge middleware revalidates Supabase session on every "
                 "/app/* request and redirects unauthenticated users to "
                 "/app/login with a `next` param.",
        ),
        "labels": ["1.1"],
        "notes": "MVP auth gate — directly the KR1.1 deliverable.",
    },
    {
        "event": _ev(
            "ev_054", source="slack", kind="message",
            title="Vercel staging up at staging.okrmonitor.com",
            body="Posted in #release: 'staging green at "
                 "staging.okrmonitor.com — please poke around.'",
        ),
        "labels": ["1.1"],
        "notes": "Live MVP environment progress.",
    },
    {
        "event": _ev(
            "ev_055", source="github", kind="commit",
            title="Pin Next.js to 15.0.4 to match Vercel build cache",
            body="Avoid build-cache invalidation between local and Vercel.",
        ),
        "labels": ["1.1"],
        "notes": "Build/deploy hygiene that keeps the MVP shippable.",
    },
    {
        "event": _ev(
            "ev_056", source="proposal", kind="ticket_triage",
            title="Cut /app/dashboard First Load JS from 142 kB → 109 kB",
            body="Removed unused @react-three import path from the dashboard "
                 "bundle. Within K10 budget with margin.",
        ),
        "labels": ["1.1"],
        "notes": "Performance work specifically on the MVP product app.",
    },

    # ---- KR 1.2 — Design partners (more) ------------------------------------
    {
        "event": _ev(
            "ev_057",
            title="Delta Software — kickoff scheduled 2026-05-19",
            body="Series B SaaS. CoS Maya Patel agreed to a 60-day pilot. "
                 "Will share read-only GitHub org access on Monday.",
        ),
        "labels": ["1.2"],
        "notes": "Design partner #4 progressing toward kickoff.",
    },
    {
        "event": _ev(
            "ev_058", source="slack", kind="message",
            title="Echo CoS confirmed pilot agreement signed",
            body="Greg from Echo: 'docusign in. we're in.'",
        ),
        "labels": ["1.2"],
        "notes": "Pilot agreement = direct design-partner count.",
    },
    {
        "event": _ev(
            "ev_059",
            title="Foxtrot CTO declined pilot — too early-stage",
            body="Polite no — they're pre-OKR. Closed the loop.",
        ),
        "labels": [],
        "notes": "Decline doesn't move KR1.2 (count of *active* DPs).",
    },
    {
        "event": _ev(
            "ev_060",
            title="Acme onboarded; first GitHub OAuth grant succeeded",
            body="Acme's sandbox repo connected. Mapper produced 12 events "
                 "in the first sweep. Acme is officially DP #1.",
        ),
        "labels": ["1.2"],
        "notes": "Active design partner — onboarded and producing data.",
    },
    {
        "event": _ev(
            "ev_061",
            title="Beta Co weekly check-in — they read 3 narratives this week",
            body="Marcus said the Friday brief saved him a 30-min status call.",
        ),
        "labels": ["1.2"],
        "notes": "Active partner usage (3+/week activation threshold).",
    },
    {
        "event": _ev(
            "ev_062", source="slack", kind="message",
            title="Charlie's COO joined the shared Slack — third user from Charlie",
            body="Onboarded their COO. Charlie now has 3 active users — "
                 "they're firmly DP #3.",
        ),
        "labels": ["1.2"],
        "notes": "Internal user expansion at an active design partner.",
    },
    {
        "event": _ev(
            "ev_063",
            title="DP intake form fielded by Mira at Hotel Inc",
            body="Hotel Inc filled the OKR Health Check intake form. "
                 "Strong-fit reply — booking kickoff for next week.",
        ),
        "labels": ["1.2"],
        "notes": "Pre-onboarding step toward DP #5.",
    },

    # ---- KR 1.3 — Mapper precision (more) ----------------------------------
    {
        "event": _ev(
            "ev_064", source="github", kind="pr_merged",
            title="Add 'no_mapping_reason' to mapper output schema",
            body="Mapper now returns a structured reason when zero KRs are "
                 "predicted. Helps debug FP/FN clusters in the eval REPORT.",
        ),
        "labels": ["1.3"],
        "notes": "Mapper API change → KR1.3 evaluability.",
    },
    {
        "event": _ev(
            "ev_065", source="github", kind="pr",
            title="Bump confidence floor 0.5 → 0.6 for Slack-source events",
            body="Per the eval REPORT, Slack threads are the dominant FP "
                 "cluster. Source-conditioned floor reduces FP rate from "
                 "12% to 4% on Slack at a 2pp recall hit.",
        ),
        "labels": ["1.3"],
        "notes": "Direct mapper precision improvement.",
    },
    {
        "event": _ev(
            "ev_066",
            title="Hand-labeled 50 more events spanning all 17 KRs",
            body="Eval set now at 200 examples (50 negatives, 20 multi-"
                 "mapping). Coverage hits every numeric KR.",
        ),
        "labels": ["1.3"],
        "notes": "Building the ruler for KR1.3 — direct credit.",
    },
    {
        "event": _ev(
            "ev_067", source="github", kind="pr",
            title="Mapper: prompt-cache the KR catalog separately",
            body="Split the system block into two cache_control: ephemeral "
                 "blocks (role+identity, then KR catalog). Only the KR block "
                 "invalidates when TRACKER.md changes.",
        ),
        "labels": ["1.3"],
        "notes": "Mapper-cost work, but it's still mapper IP.",
    },
    {
        "event": _ev(
            "ev_068",
            title="Eval precision 87.4% on 200-event set (live LLM)",
            body="First post-funded run. Precision 87.4%, recall 73.1%, "
                 "F1 0.797. Above 85% gate.",
        ),
        "labels": ["1.3"],
        "notes": "Direct numerical reading on KR1.3.",
    },
    {
        "event": _ev(
            "ev_069", source="github", kind="commit",
            title="Add few-shot example for 'docs PR' anti-mapping",
            body="Three examples showing a typical docs PR with explicit "
                 "'this should map to NOTHING'. Cuts the docs-PR FP cluster.",
        ),
        "labels": ["1.3"],
        "notes": "Mapper prompt improvement.",
    },
    {
        "event": _ev(
            "ev_070",
            title="Mapper sweep produced 47 mappings on 53 new events",
            body="Today's daily run: 53 ingested events, 47 ≥1-KR mappings, "
                 "6 events flagged as no_mapping_reason. Healthy ratio.",
        ),
        "labels": ["1.3"],
        "notes": "Operational signal — mapper is producing for KR1.3.",
    },

    # ---- KR 1.4 — Time-to-first-narrative (more) ---------------------------
    {
        "event": _ev(
            "ev_071", source="github", kind="pr_merged",
            title="Parallelize narrative per-KR section generation",
            body="asyncio.gather across 17 KR sections. Wall time on a fresh "
                 "200-event window: 4m12s → 1m08s.",
        ),
        "labels": ["1.4"],
        "notes": "Direct narrative-latency improvement.",
    },
    {
        "event": _ev(
            "ev_072",
            title="Fresh-account onboarding measured: 19 minutes to first narrative",
            body="DP Hotel Inc: oauth grant 14:01 → narrative 14:20.",
        ),
        "labels": ["1.4"],
        "notes": "Direct measurement of KR1.4.",
    },
    {
        "event": _ev(
            "ev_073", source="github", kind="commit",
            title="Cache TRACKER.md text per narrative run",
            body="Was loading the file 17 times per narrative; now 1.",
        ),
        "labels": ["1.4"],
        "notes": "Latency win on the narrative path.",
    },
    {
        "event": _ev(
            "ev_074", source="linear", kind="issue_completed",
            title="OKR-72 — narrative streaming for SSE",
            body="First sentence appears in <8s now. UX win on perceived "
                 "latency for KR1.4.",
        ),
        "labels": ["1.4"],
        "notes": "Perceived TTFM improvement.",
    },
    {
        "event": _ev(
            "ev_075",
            title="Onboarding measurement: Echo at 28 minutes (within p90)",
            body="Echo's first narrative landed at minute 28 from oauth.",
        ),
        "labels": ["1.4"],
        "notes": "Direct KR1.4 reading.",
    },
    {
        "event": _ev(
            "ev_076", source="github", kind="pr",
            title="Mapper backoff: skip retries on 5xx and surface to narrative",
            body="Was waiting 30s on transient 503s, blowing the TTFM budget. "
                 "Now retries are bounded with cumulative timeout.",
        ),
        "labels": ["1.4"],
        "notes": "TTFM tail-latency fix.",
    },

    # ---- KR 1.5 — Design-partner NPS (more) --------------------------------
    {
        "event": _ev(
            "ev_077",
            title="Beta NPS pulse: 8/10 — 'reliable, no surprises'",
            body="Marcus: solid 8. Constructive: 'wish narratives didn't "
                 "use the word leverage so much.'",
        ),
        "labels": ["1.5"],
        "notes": "Direct NPS data point.",
    },
    {
        "event": _ev(
            "ev_078",
            title="Charlie NPS: 9/10 — confident promoter",
            body="'I told my CFO this is the only tool I'd save in a "
                 "consolidation' (verbatim).",
        ),
        "labels": ["1.5"],
        "notes": "NPS reading toward KR1.5.",
    },
    {
        "event": _ev(
            "ev_079",
            title="Echo NPS: 6/10 — passive, asked for Notion ingestion",
            body="Echo is a passive (6) — they want OKR-doc parsing as table "
                 "stakes. Logged as OKR-104 in backlog.",
        ),
        "labels": ["1.5"],
        "notes": "NPS data point.",
    },
    {
        "event": _ev(
            "ev_080",
            title="Delta NPS: 10/10 — 'transformational'",
            body="Maya: 10. 'I get back the Sunday I used to spend "
                 "preparing the Monday update.'",
        ),
        "labels": ["1.5"],
        "notes": "NPS data point.",
    },
    {
        "event": _ev(
            "ev_081",
            title="NPS rollup week 4: average 8.4 across 5 design partners",
            body="Hotel pending. 4-of-5 promoters. Average 8.4, NPS "
                 "implied ~60. Above target.",
        ),
        "labels": ["1.5"],
        "notes": "Aggregated NPS — direct KR1.5 evidence.",
    },
    {
        "event": _ev(
            "ev_082",
            title="Sent NPS pulse #2 to all 5 design partners",
            body="Cadence: every 30 days during the pilot. Same one-question "
                 "Typeform.",
        ),
        "labels": ["1.5"],
        "notes": "Operational step toward KR1.5 measurement.",
    },

    # ---- KR 2.1 — Cumulative pilots (more) ---------------------------------
    {
        "event": _ev(
            "ev_083",
            title="Pilot signup: November Labs (Series A, 70 ppl)",
            body="Inbound from /health-check. Notion OKRs, GitHub-heavy.",
        ),
        "labels": ["2.1"],
        "notes": "+1 pilot.",
    },
    {
        "event": _ev(
            "ev_084",
            title="Pilot signup: Oscar Inc (Series C fintech, 410 ppl)",
            body="Inbound from a podcast appearance. Big-end-of-ICP.",
        ),
        "labels": ["2.1"],
        "notes": "+1 pilot.",
    },
    {
        "event": _ev(
            "ev_085",
            title="Pilot signup: Papa Tech (Series B, 220 ppl)",
            body="Outbound founder-sales reply. CoS Eve Wright accepting "
                 "intake form on Monday.",
        ),
        "labels": ["2.1"],
        "notes": "+1 pilot from outbound channel.",
    },
    {
        "event": _ev(
            "ev_086",
            title="Pilot count crossed 50 (M2 ahead of schedule)",
            body="50 cumulative pilots reached on 2026-06-22. M2 target was "
                 "75 by 2026-07-09; on pace for ~80.",
        ),
        "labels": ["2.1"],
        "notes": "Direct KR2.1 milestone.",
    },
    {
        "event": _ev(
            "ev_087",
            title="Pilot signup batch: 7 inbound from PH launch day",
            body="7 named SaaS companies signed up between launch hour 0–24.",
        ),
        "labels": ["2.1"],
        "notes": "Pilot-count event.",
    },
    {
        "event": _ev(
            "ev_088",
            title="Pilot signup: Quebec Apps (Series B, 150 ppl)",
            body="From the State of OKR Drift post. Engaged contact.",
        ),
        "labels": ["2.1"],
        "notes": "+1 pilot.",
    },
    {
        "event": _ev(
            "ev_089",
            title="Cumulative pilot count = 100 (M3 milestone hit early)",
            body="100 cumulative pilots on 2026-07-29. M3 target was 175 by "
                 "2026-08-09. Currently tracking ~140 by then.",
        ),
        "labels": ["2.1"],
        "notes": "Direct KR2.1 milestone reading.",
    },
    {
        "event": _ev(
            "ev_090",
            title="Pilot signup: Romeo OS (Series C, 530 ppl) — over the ICP cap",
            body="Slightly over our 500-person cap. Ran the qualification "
                 "rubric: greenlit anyway because Eng VP brought it.",
        ),
        "labels": ["2.1"],
        "notes": "+1 pilot — count goes up.",
    },
    {
        "event": _ev(
            "ev_091",
            title="Pilot signup: Sierra Inc",
            body="Inbound via LinkedIn. CoS Tom Park.",
        ),
        "labels": ["2.1"],
        "notes": "+1 pilot.",
    },
    {
        "event": _ev(
            "ev_092",
            title="Pilot signup: Tango Networks (175 ppl)",
            body="Inbound. Strong fit.",
        ),
        "labels": ["2.1"],
        "notes": "+1 pilot.",
    },

    # ---- KR 2.2 — Pilot activation (more) ----------------------------------
    {
        "event": _ev(
            "ev_093",
            title="Activation snapshot: 28 of 47 pilots read this week's narrative",
            body="Activation rate 59.6% — just under the 60% target.",
        ),
        "labels": ["2.2"],
        "notes": "Direct KR2.2 reading.",
    },
    {
        "event": _ev(
            "ev_094",
            title="November Labs read first narrative on day 4",
            body="Activated within the 7-day window. Counts.",
        ),
        "labels": ["2.2"],
        "notes": "Pilot moves signed → activated.",
    },
    {
        "event": _ev(
            "ev_095",
            title="Charlie active 5/5 weeks in a row",
            body="Charlie has read every weekly narrative. Power user.",
        ),
        "labels": ["2.2"],
        "notes": "Sustained activation — KR2.2 data.",
    },
    {
        "event": _ev(
            "ev_096",
            title="Reactivation experiment: 3 of 8 dormant pilots opened narrative",
            body="Sent a pointed reactivation email to 8 pilots dormant ≥21 "
                 "days. 3 opened, 1 read end-to-end.",
        ),
        "labels": ["2.2"],
        "notes": "Activation-rate intervention.",
    },
    {
        "event": _ev(
            "ev_097",
            title="Activation rollup: 42 of 65 pilots activated (64.6%)",
            body="Above the 60% gate at scale.",
        ),
        "labels": ["2.2"],
        "notes": "Direct KR2.2 measurement.",
    },
    {
        "event": _ev(
            "ev_098",
            title="Echo activated — read first narrative within 6 days",
            body="Echo onboard pace was slow (Notion ingestion still manual) "
                 "but they activated within window.",
        ),
        "labels": ["2.2"],
        "notes": "Activation event.",
    },
    {
        "event": _ev(
            "ev_099",
            title="Quebec Apps still dormant after 14 days",
            body="No narrative reads. Triggered the breakup-email cadence.",
        ),
        "labels": ["2.2"],
        "notes": "Anti-activation signal — still relevant to KR2.2.",
    },

    # ---- KR 2.3 — Pilot → paid intent (more) -------------------------------
    {
        "event": _ev(
            "ev_100",
            title="Beta committed to convert at $899/mo Team tier",
            body="Beta said yes to converting. First paying customer.",
        ),
        "labels": ["2.3"],
        "notes": "Direct paid-intent → conversion event.",
    },
    {
        "event": _ev(
            "ev_101",
            title="Charlie negotiating annual commit at $9k",
            body="Charlie's CFO offered $9k annual prepay. We countered at "
                 "$10.8k (12 × $899 + small commit kicker).",
        ),
        "labels": ["2.3"],
        "notes": "Conversion negotiation — paid intent.",
    },
    {
        "event": _ev(
            "ev_102",
            title="Acme: paid kickoff signed at $899/mo",
            body="Acme converted. Second paying customer.",
        ),
        "labels": ["2.3"],
        "notes": "Direct conversion.",
    },
    {
        "event": _ev(
            "ev_103",
            title="Conversion rollup: 6 of 23 expired pilots converted (26%)",
            body="At pilot end, 6 of 23 say-yes-to-paid. Just over 25% gate.",
        ),
        "labels": ["2.3"],
        "notes": "Direct KR2.3 reading.",
    },
    {
        "event": _ev(
            "ev_104",
            title="Delta requested an enterprise quote",
            body="Maya (Delta) asked for security review materials and "
                 "enterprise pricing. Strong upmarket signal.",
        ),
        "labels": ["2.3"],
        "notes": "Paid-intent event, larger contract size.",
    },
    {
        "event": _ev(
            "ev_105",
            title="Mid-pilot pricing chat with Hotel Inc",
            body="Hotel hinted they're aligned on pricing — wants to see the "
                 "Q3 narrative before committing.",
        ),
        "labels": ["2.3"],
        "notes": "Paid-intent qualitative signal.",
    },
    {
        "event": _ev(
            "ev_106",
            title="Sierra Inc — declined to convert post-pilot",
            body="Sierra said the value is real but their priorities shifted. "
                 "Will revisit Q4.",
        ),
        "labels": [],
        "notes": "A decline doesn't move KR2.3 forward — strict negative for "
                 "this KR even though it's a pilot event.",
    },

    # ---- KR 2.4 — 3 acquisition channels (more) ----------------------------
    {
        "event": _ev(
            "ev_107", source="content", kind="blog_post_published",
            title="Content channel hit 32 pilots/mo for the first time",
            body="July: 32 inbound pilots from content. Channel #2 confirmed.",
        ),
        "labels": ["2.4"],
        "notes": "Channel hits the ≥30/mo threshold.",
    },
    {
        "event": _ev(
            "ev_108",
            title="Outbound founder-sales sustained at 45 pilots/mo",
            body="July: outbound 45/mo. Channel #1, well above threshold.",
        ),
        "labels": ["2.4"],
        "notes": "Channel #1 sustained — direct KR2.4 evidence.",
    },
    {
        "event": _ev(
            "ev_109",
            title="Reddit r/SaaS experiment: 14 pilots in 30 days at $62 CAC",
            body="Below threshold but trending. Continuing experiment.",
        ),
        "labels": ["2.4"],
        "notes": "Channel-experiment progress toward KR2.4.",
    },
    {
        "event": _ev(
            "ev_110",
            title="Podcast inbound channel: 31 pilots last 30 days",
            body="Crossed the 30/mo threshold. Channel #3 confirmed.",
        ),
        "labels": ["2.4"],
        "notes": "Direct KR2.4 — third channel hits gate.",
    },
    {
        "event": _ev(
            "ev_111",
            title="LinkedIn organic posts driving 22 pilots/mo",
            body="Below the 30/mo threshold but trending up.",
        ),
        "labels": ["2.4"],
        "notes": "Channel-progress signal.",
    },
    {
        "event": _ev(
            "ev_112",
            title="Newsletter sponsorship test (Lenny's Newsletter): 9 pilots from one drop",
            body="Spend $5k for 9 pilots = $556 CAC. Below median LTV; "
                 "monitor before scaling.",
        ),
        "labels": ["2.4"],
        "notes": "Channel-validation event.",
    },
    {
        "event": _ev(
            "ev_113",
            title="Affiliate program seeded with 3 ops-community newsletters",
            body="Affiliate kickoff. 12% rev-share; tracker via UTM.",
        ),
        "labels": ["2.4"],
        "notes": "Channel-buildout work.",
    },
    {
        "event": _ev(
            "ev_114",
            title="3-channels-each-≥30/mo officially achieved (M3 review)",
            body="Outbound 45 / Content 32 / Podcast 31. KR2.4 satisfied.",
        ),
        "labels": ["2.4"],
        "notes": "Direct KR2.4 success event.",
    },
    {
        "event": _ev(
            "ev_115",
            title="Productized free tool 'okr-monitor.com/health-check' driving 18 pilots/mo",
            body="The free OKR Health Check tool became its own channel. "
                 "Below 30/mo but growing.",
        ),
        "labels": ["2.4"],
        "notes": "Channel-buildout progress.",
    },

    # ---- KR 2.5 — CAC payback (more) ---------------------------------------
    {
        "event": _ev(
            "ev_116",
            title="Updated CAC computation with channel-mix factor",
            body="Outbound CAC $720 (founder time + tooling); Content CAC "
                 "$310; Podcast CAC $90 (just hosting time). Blended $410.",
        ),
        "labels": ["2.5"],
        "notes": "CAC measurement work for KR2.5.",
    },
    {
        "event": _ev(
            "ev_117",
            title="Cohort 1 payback measured: 4.7 months (vs ≤6 target)",
            body="22 paying pilots. ARPU $899. Gross margin 78%. Payback "
                 "4.7mo. Inside the gate.",
        ),
        "labels": ["2.5"],
        "notes": "Direct KR2.5 reading.",
    },
    {
        "event": _ev(
            "ev_118",
            title="Pricing v2 introduces $1,499 Team-Plus tier",
            body="Mid-tier ARPU bump pulls payback expectation under "
                 "4 months for the next cohort.",
        ),
        "labels": ["2.5"],
        "notes": "Pricing change driving CAC payback.",
    },
    {
        "event": _ev(
            "ev_119",
            title="Discounted Annual prepay reducing CAC payback by ~1mo",
            body="20% off annual prepay lifts cash up-front — payback for "
                 "annual cohort 3.6mo.",
        ),
        "labels": ["2.5"],
        "notes": "CAC payback intervention.",
    },
    {
        "event": _ev(
            "ev_120",
            title="Q3 cohort blended CAC payback: 5.1 months",
            body="Modestly worse than Q2 because LTV is still cohort-light.",
        ),
        "labels": ["2.5"],
        "notes": "Direct KR2.5 reading.",
    },

    # ---- KR 3.1 — Benchmark posts (more) -----------------------------------
    {
        "event": _ev(
            "ev_121", source="content", kind="blog_post_published",
            title="Published 'Why Monthly Reviews Are Too Late' benchmark",
            body="3,800-word post. Anchor stat: 67% of drift is invisible "
                 "until next OKR cycle.",
        ),
        "labels": ["3.1"],
        "notes": "Benchmark post #1 published.",
    },
    {
        "event": _ev(
            "ev_122", source="content", kind="blog_post_published",
            title="Published 'The CoS Stack 2026' benchmark",
            body="6,100-word post on the tooling Chief of Staff buyers use. "
                 "Anchor stat: 71% manual updates.",
        ),
        "labels": ["3.1"],
        "notes": "Benchmark post.",
    },
    {
        "event": _ev(
            "ev_123", source="content", kind="blog_post_published",
            title="Published 'OKR Drift Patterns Across 80 SaaS Companies'",
            body="Cross-pilot benchmark. Top finding: 4 distinct drift "
                 "archetypes.",
        ),
        "labels": ["3.1"],
        "notes": "Benchmark post.",
    },
    {
        "event": _ev(
            "ev_124", source="content", kind="blog_post_draft",
            title="Drafted 'Anti-OKRs: KRs Companies Should Stop Setting'",
            body="Provocative angle. Drafted; in review with copywriter.",
        ),
        "labels": ["3.1"],
        "notes": "In-flight benchmark post.",
    },
    {
        "event": _ev(
            "ev_125", source="content", kind="blog_post_published",
            title="Published 'The 90-Minute OKR Health Check Method'",
            body="Walkthrough of the methodology. Drove 87 health-check "
                 "intakes in week 1.",
        ),
        "labels": ["3.1"],
        "notes": "Benchmark post (also a content channel driver, but the KR "
                 "is publish-count, not pilot-count).",
    },
    {
        "event": _ev(
            "ev_126",
            title="Cumulative benchmark posts: 6 of 12 target",
            body="Halfway to the cycle target. 4 more queued for Q3.",
        ),
        "labels": ["3.1"],
        "notes": "KR3.1 milestone reading.",
    },
    {
        "event": _ev(
            "ev_127", source="content", kind="blog_post_published",
            title="Published 'When KPIs Lie' — co-authored with Beta CoS",
            body="Co-author post with Marcus. 2,400 reads in week 1.",
        ),
        "labels": ["3.1"],
        "notes": "Benchmark post.",
    },
    {
        "event": _ev(
            "ev_128", source="content", kind="blog_post_published",
            title="Published 'A Founder's Guide to Reading OKR Drift'",
            body="2,900-word post. Top of org-design hashtag for 2 days.",
        ),
        "labels": ["3.1"],
        "notes": "Benchmark post.",
    },

    # ---- KR 3.2 — LinkedIn followers (more) --------------------------------
    {
        "event": _ev(
            "ev_129", source="linkedin", kind="post",
            title="LinkedIn carousel 'OKR drift archetypes' — 1,820 reactions",
            body="Drove +287 followers in 24h.",
        ),
        "labels": ["3.2"],
        "notes": "Direct LinkedIn growth event.",
    },
    {
        "event": _ev(
            "ev_130", source="linkedin", kind="post",
            title="LinkedIn post 'Why your QBR feels like a fairy tale'",
            body="912 reactions, 78 comments. +148 followers.",
        ),
        "labels": ["3.2"],
        "notes": "LinkedIn growth.",
    },
    {
        "event": _ev(
            "ev_131",
            title="Hit 2,000 LinkedIn followers (40% to target)",
            body="Milestone — 2k. Compounding well.",
        ),
        "labels": ["3.2"],
        "notes": "KR3.2 progress.",
    },
    {
        "event": _ev(
            "ev_132", source="linkedin", kind="post",
            title="LinkedIn carousel on the 5-in-5 exercise — viral",
            body="3,500 reactions, 290 comments, 410 reposts. +540 followers "
                 "in 48h.",
        ),
        "labels": ["3.2"],
        "notes": "LinkedIn growth — direct KR3.2.",
    },
    {
        "event": _ev(
            "ev_133",
            title="Hit 3,500 LinkedIn followers",
            body="70% to KR3.2 target.",
        ),
        "labels": ["3.2"],
        "notes": "Direct KR3.2 progress.",
    },
    {
        "event": _ev(
            "ev_134", source="linkedin", kind="post",
            title="LinkedIn comment-debate post 'Lattice vs Mooncamp vs Notion'",
            body="High-engagement debate post. +112 followers.",
        ),
        "labels": ["3.2"],
        "notes": "LinkedIn growth event.",
    },
    {
        "event": _ev(
            "ev_135",
            title="Brand account hit 1,200 followers (combined: 4,700)",
            body="Brand account growing organically off founder tags. "
                 "Combined metric per KR3.2 definition: 4,700.",
        ),
        "labels": ["3.2"],
        "notes": "Direct KR3.2 reading.",
    },
    {
        "event": _ev(
            "ev_136",
            title="Crossed combined 5,000 LinkedIn followers (KR3.2 met)",
            body="Founder + brand combined: 5,002. KR3.2 satisfied.",
        ),
        "labels": ["3.2"],
        "notes": "KR3.2 hit.",
    },

    # ---- KR 3.3 — Podcast appearances (more) -------------------------------
    {
        "event": _ev(
            "ev_137",
            title="Aired: SaaStr Founder Stories episode",
            body="Aired 2026-05-29. 14k downloads in week 1.",
        ),
        "labels": ["3.3"],
        "notes": "Aired podcast appearance.",
    },
    {
        "event": _ev(
            "ev_138",
            title="Booked: Lenny's Podcast for 2026-06-19",
            body="Big-fish booking. Topic: 'The single best ops metric '"
                 "I've stopped tracking.'",
        ),
        "labels": ["3.3"],
        "notes": "Booked appearance.",
    },
    {
        "event": _ev(
            "ev_139",
            title="Aired: 'B2B Banter' episode",
            body="Aired 2026-06-12. Drove 14 inbound pilots in 48h.",
        ),
        "labels": ["3.3"],
        "notes": "Aired podcast appearance.",
    },
    {
        "event": _ev(
            "ev_140",
            title="Recorded: 'CoS Notes' episode",
            body="Recorded; airs in 3 weeks.",
        ),
        "labels": ["3.3"],
        "notes": "Recorded podcast.",
    },
    {
        "event": _ev(
            "ev_141",
            title="Cumulative podcast appearances: 8 of 12 target",
            body="Tracking on pace for 12 by 2026-08-28.",
        ),
        "labels": ["3.3"],
        "notes": "KR3.3 milestone.",
    },
    {
        "event": _ev(
            "ev_142",
            title="Booked: 'Operators' podcast for 2026-07-22",
            body="Booked. Pre-recorded.",
        ),
        "labels": ["3.3"],
        "notes": "Booked appearance.",
    },

    # ---- KR 3.4 — Product Hunt top 5 (more) --------------------------------
    {
        "event": _ev(
            "ev_143",
            title="PH launch executed — finished #2 of day",
            body="PH launch went live 2026-06-15. Finished #2 of day with "
                 "1,200 upvotes. KR3.4 met (top 5).",
        ),
        "labels": ["3.4"],
        "notes": "Direct KR3.4 satisfaction.",
    },
    {
        "event": _ev(
            "ev_144",
            title="Engaged 12 hunters and product-hunt VIPs ahead of launch",
            body="Pre-launch coordination. 12 commitments to upvote and "
                 "comment in the first 2h.",
        ),
        "labels": ["3.4"],
        "notes": "Pre-launch prep.",
    },
    {
        "event": _ev(
            "ev_145", source="github", kind="pr_merged",
            title="Add PH-specific landing variant at /v2?via=ph",
            body="Variant landing copy for PH traffic.",
        ),
        "labels": ["3.4"],
        "notes": "PH-launch prep.",
    },
    {
        "event": _ev(
            "ev_146",
            title="PH comment-day playbook executed (replied to 88 comments)",
            body="Replied to every comment within first 12h. 88 replies.",
        ),
        "labels": ["3.4"],
        "notes": "PH-launch execution.",
    },
    {
        "event": _ev(
            "ev_147",
            title="Drafted PH demo video (90s)",
            body="90-second demo video locked. 1.4 MB.",
        ),
        "labels": ["3.4"],
        "notes": "PH-launch prep.",
    },

    # ---- KR 4.1 — Agents tracked as work-units (more) ----------------------
    {
        "event": _ev(
            "ev_148", source="proposal", kind="agent_buildout",
            title="Scaffolded final 13 agents — KR4.1 hits 30/30",
            body="Engineering 7, Customer/Ops 1, Product/Design 2, GTM 3 "
                 "added. Full org online in dry-run.",
        ),
        "labels": ["4.1"],
        "notes": "Direct KR4.1 completion event.",
    },
    {
        "event": _ev(
            "ev_149", source="github", kind="pr_merged",
            title="Each agent emits a `work_event` of source='agent_proposal'",
            body="agents/_proposal.py now snapshots its proposal as a "
                 "work_event so the system tracks itself.",
        ),
        "labels": ["4.1"],
        "notes": "Agents-as-work-units wiring.",
    },
    {
        "event": _ev(
            "ev_150", source="proposal", kind="agent_run",
            title="founder_sales agent dry-run produced 5 outreach drafts",
            body="Generic-mock dry-run. Once API budget unblocks, real drafts.",
        ),
        "labels": ["4.1"],
        "notes": "Agent emitting tracked work — KR4.1 ongoing maintenance.",
    },
    {
        "event": _ev(
            "ev_151",
            title="Agent roster review — all 30 agents 🟢 in TRACKER.md §4",
            body="Status check: every agent has prompt + config + pipeline "
                 "+ run_script and produced a parseable response in dry-run.",
        ),
        "labels": ["4.1"],
        "notes": "KR4.1 ongoing health.",
    },
    {
        "event": _ev(
            "ev_152", source="github", kind="commit",
            title="Generic _default_mock fallthrough for new agents",
            body="Lets newly-scaffolded agents pass smoke without a bespoke "
                 "mock entry.",
        ),
        "labels": ["4.1"],
        "notes": "Tooling for the agent roster.",
    },

    # ---- KR 4.2 — Weekly narrative auto-generated (more) -------------------
    {
        "event": _ev(
            "ev_153", source="proposal", kind="weekly_narrative",
            title="Friday narrative auto-shipped — 04-28 → 05-04 window",
            body="Live LLM run, $0.043, narrative read by founder + 3 DPs.",
        ),
        "labels": ["4.2"],
        "notes": "Direct KR4.2 — auto narrative.",
    },
    {
        "event": _ev(
            "ev_154", source="github", kind="pr_merged",
            title="Narrative agent now formats per-KR sections deterministically",
            body="Reduced run-to-run variance for KR section ordering.",
        ),
        "labels": ["4.2"],
        "notes": "Narrative-loop hardening for KR4.2.",
    },
    {
        "event": _ev(
            "ev_155", source="proposal", kind="sunday_run",
            title="Sunday wrapper produced narrative for empty mapping window",
            body="Tested: 0 events → narrative wrote 'no work this week' "
                 "honestly without divide-by-zero.",
        ),
        "labels": ["4.2"],
        "notes": "Reliability — KR4.2 robustness.",
    },
    {
        "event": _ev(
            "ev_156", source="proposal", kind="weekly_narrative",
            title="Weekly narrative for week of 2026-06-15 — 47 events, 38 mappings",
            body="On-track narrative including PH launch impact.",
        ),
        "labels": ["4.2"],
        "notes": "Direct KR4.2.",
    },
    {
        "event": _ev(
            "ev_157",
            title="100% of weeks have an auto-narrative (Sprint 0 → Sprint 4)",
            body="Tracked: 0 missed weeks across 8 cycles. KR4.2 hit.",
        ),
        "labels": ["4.2"],
        "notes": "Direct KR4.2 — quantitative.",
    },
    {
        "event": _ev(
            "ev_158", source="github", kind="pr",
            title="Add narrative human-rating capture form",
            body="Inline 1-5 rating embedded in the narrative email; ratings "
                 "log to kpi_daily.",
        ),
        "labels": ["4.2"],
        "notes": "Narrative loop instrumentation.",
    },

    # ---- KR 4.3 — Dogfood gaps → backlog within 24h (more) -----------------
    {
        "event": _ev(
            "ev_159", source="proposal", kind="dogfood_finding",
            title="Dogfood: missing per-KR drill-down → opened OKR-117 same day",
            body="Operator hit the missing detail page; ticket opened in 2h.",
        ),
        "labels": ["4.3"],
        "notes": "Textbook KR4.3 cycle.",
    },
    {
        "event": _ev(
            "ev_160", source="proposal", kind="dogfood_finding",
            title="Dogfood: kpi_daily timezone bug → fix shipped within 6h",
            body="Operator caught the off-by-one; fix shipped same day.",
        ),
        "labels": ["4.3"],
        "notes": "KR4.3.",
    },
    {
        "event": _ev(
            "ev_161", source="proposal", kind="dogfood_finding",
            title="Dogfood: stale narrative for Acme on a holiday → ticket OKR-119",
            body="Narrative hit empty window because of a holiday; backlog "
                 "ticket within the same day.",
        ),
        "labels": ["4.3"],
        "notes": "KR4.3.",
    },
    {
        "event": _ev(
            "ev_162",
            title="KR4.3 audit: 14 dogfood gaps → 14 tickets, all within 24h",
            body="100% so far. KR satisfied at the cycle midpoint.",
        ),
        "labels": ["4.3"],
        "notes": "Direct KR4.3 reading.",
    },
    {
        "event": _ev(
            "ev_163", source="proposal", kind="dogfood_finding",
            title="Dogfood: GitHub ingest 404 on rate-limit → fixed in 8h",
            body="Operator noticed missing events; rate-limit handler "
                 "shipped same day.",
        ),
        "labels": ["4.3"],
        "notes": "KR4.3.",
    },
    {
        "event": _ev(
            "ev_164", source="slack", kind="message",
            title="Operator flagged missing Slack ingest — backlog'd in 2h",
            body="OKR-128 opened.",
        ),
        "labels": ["4.3"],
        "notes": "KR4.3 cycle.",
    },

    # ---- Multi-mappings (more) ---------------------------------------------
    {
        "event": _ev(
            "ev_165", source="content", kind="blog_post_published",
            title="Benchmark post co-authored with Beta drives 9 new pilots and +180 LinkedIn followers",
            body="The post itself counts as a benchmark; the LinkedIn teaser "
                 "drove growth; pilot signups attributable.",
        ),
        "labels": ["3.1", "3.2", "2.1"],
        "notes": "Triple multi-mapping — content, LinkedIn, pilots.",
    },
    {
        "event": _ev(
            "ev_166",
            title="Aired podcast → 8 inbound pilot signups",
            body="Lenny's podcast aired; 8 signups in 48h.",
        ),
        "labels": ["3.3", "2.1"],
        "notes": "Podcast + pilot count.",
    },
    {
        "event": _ev(
            "ev_167", source="github", kind="pr_merged",
            title="Mapper precision improvement → narrative quality up; DP NPS pulse 9.2",
            body="Mapper precision improvement directly improved narrative "
                 "quality, which Marcus rated 9.2 in the next pulse.",
        ),
        "labels": ["1.3", "1.5"],
        "notes": "Mapper IP + downstream NPS.",
    },
    {
        "event": _ev(
            "ev_168",
            title="Acme pilot conversion + first paying customer + case study published",
            body="Single event: paid conversion + content (case study).",
        ),
        "labels": ["2.3", "3.1"],
        "notes": "Conversion + benchmark/case study.",
    },
    {
        "event": _ev(
            "ev_169", source="proposal", kind="weekly_narrative",
            title="First weekly narrative auto-shipped to live customer (Beta)",
            body="Beta read the auto-narrative — both the auto-narrative "
                 "loop AND a design-partner activation.",
        ),
        "labels": ["4.2", "1.2", "2.2"],
        "notes": "Narrative loop + DP active + activation.",
    },
    {
        "event": _ev(
            "ev_170",
            title="Outbound channel hits 30/mo at the same time pilot count crosses 50",
            body="Two milestones in one event window.",
        ),
        "labels": ["2.4", "2.1"],
        "notes": "Channel-threshold + cumulative-pilot count.",
    },
    {
        "event": _ev(
            "ev_171",
            title="PH launch landed 47 inbound pilots and #2 of day finish",
            body="PH (3.4) and pilot count (2.1) both move.",
        ),
        "labels": ["3.4", "2.1"],
        "notes": "Multi-mapping — already kind of in ev_039 too; this is a "
                 "different worded version for the eval.",
    },
    {
        "event": _ev(
            "ev_172", source="content", kind="blog_post_published",
            title="LinkedIn post and benchmark blog about the 5-in-5 exercise",
            body="Benchmark post (3.1) plus LinkedIn distribution (3.2).",
        ),
        "labels": ["3.1", "3.2"],
        "notes": "Content + LinkedIn growth.",
    },
    {
        "event": _ev(
            "ev_173", source="github", kind="pr_merged",
            title="Auth wiring + dashboard renders → MVP usable for first DP",
            body="Auth + dashboard live = MVP-deployed-to-prod milestone "
                 "and made it possible for first DP to onboard.",
        ),
        "labels": ["1.1", "1.2"],
        "notes": "MVP deploy unlocks DP onboarding.",
    },
    {
        "event": _ev(
            "ev_174",
            title="Case study with Acme published, drove 6 inbound pilots",
            body="Case-study content (3.1) + pilot count (2.1).",
        ),
        "labels": ["3.1", "2.1"],
        "notes": "Multi-mapping.",
    },
    {
        "event": _ev(
            "ev_175",
            title="Mapper hits 88% precision → unblocks productionizing for paying tier",
            body="Mapper precision (1.3) unblocked the paid tier (2.3).",
        ),
        "labels": ["1.3", "2.3"],
        "notes": "IP improvement enables paid intent.",
    },
    {
        "event": _ev(
            "ev_176", source="proposal", kind="dogfood_finding",
            title="Dogfood-driven dashboard improvement also benefits Echo onboarding",
            body="Dogfood gap (4.3) closed → faster TTFM (1.4) for Echo's "
                 "onboarding window.",
        ),
        "labels": ["4.3", "1.4"],
        "notes": "Dogfood + TTFM.",
    },
    {
        "event": _ev(
            "ev_177",
            title="Reactivation campaign brought 4 dormant pilots to active and 1 to paid",
            body="Activation (2.2) + paid intent (2.3).",
        ),
        "labels": ["2.2", "2.3"],
        "notes": "Activation + conversion in same event.",
    },
    {
        "event": _ev(
            "ev_178", source="github", kind="pr_merged",
            title="GitHub integration ingest live — first DP (Acme) sees their own commits in dashboard",
            body="Integration shipped (engineering-pod KR), Acme onboarded "
                 "(1.2), MVP felt magical (1.1).",
        ),
        "labels": ["1.1", "1.2"],
        "notes": "Multi-mapping spanning MVP + DP.",
    },
    {
        "event": _ev(
            "ev_179",
            title="Founder appeared on 'Operators' podcast and crossed 4,500 LinkedIn followers same day",
            body="Podcast appearance + LinkedIn growth.",
        ),
        "labels": ["3.3", "3.2"],
        "notes": "Multi-mapping.",
    },
    {
        "event": _ev(
            "ev_180",
            title="Cumulative pilots crossed 100 the same week 3 channels each ≥30/mo",
            body="Pilot count (2.1) + channels (2.4) both move.",
        ),
        "labels": ["2.1", "2.4"],
        "notes": "Multi-mapping at a milestone moment.",
    },
    {
        "event": _ev(
            "ev_181",
            title="Operator wrote a benchmark post inspired by a dogfood finding",
            body="Dogfood finding (4.3) became a benchmark post (3.1).",
        ),
        "labels": ["4.3", "3.1"],
        "notes": "Multi-mapping.",
    },

    # ---- Strict negatives (more) -------------------------------------------
    {
        "event": _ev(
            "ev_182", source="github", kind="pr",
            title="Bump react-three/drei to 10.1 in unrelated graphics demo",
            body="Personal demo project.",
        ),
        "labels": [],
        "notes": "Not okr-monitor — strict negative.",
    },
    {
        "event": _ev(
            "ev_183", source="slack", kind="message",
            title="Anyone want to grab lunch at Tartine on Thursday?",
            body="Lunch coordination.",
        ),
        "labels": [],
        "notes": "Social — strict negative.",
    },
    {
        "event": _ev(
            "ev_184", source="calendar", kind="event",
            title="Dentist appointment 2026-05-15 09:30",
            body="Personal calendar.",
        ),
        "labels": [],
        "notes": "Personal.",
    },
    {
        "event": _ev(
            "ev_185", source="github", kind="profile_update",
            title="Updated personal pinned repos on GitHub profile",
            body="Cosmetic.",
        ),
        "labels": [],
        "notes": "Personal cosmetic.",
    },
    {
        "event": _ev(
            "ev_186", source="slack", kind="thread",
            title="Long thread debating mechanical keyboard switches",
            body="MX Brown vs MX Red etc. Personal.",
        ),
        "labels": [],
        "notes": "Off-topic hardware discussion.",
    },
    {
        "event": _ev(
            "ev_187", source="twitter", kind="tweet",
            title="Tweet replying to a Lakers game",
            body="Sports content.",
        ),
        "labels": [],
        "notes": "Off-topic + wrong channel even if it were on-topic.",
    },
    {
        "event": _ev(
            "ev_188", source="github", kind="pr",
            title="Contributing fix to a Rust crate (anyhow)",
            body="OSS contribution to an unrelated upstream.",
        ),
        "labels": [],
        "notes": "OSS contribution to unrelated project.",
    },
    {
        "event": _ev(
            "ev_189",
            title="Booked a haircut",
            body="Personal calendar event.",
        ),
        "labels": [],
        "notes": "Personal.",
    },
    {
        "event": _ev(
            "ev_190", source="linear", kind="issue_opened",
            title="OKR-test-issue created during integration test",
            body="A throwaway test issue created during Linear integration "
                 "smoke test. Should NOT map to a KR.",
        ),
        "labels": [],
        "notes": "Test-data noise — strict negative even if the title looks "
                 "OKR-shaped.",
    },
    {
        "event": _ev(
            "ev_191", source="github", kind="pr",
            title="Investigate intermittent CI flake (no fix yet)",
            body="Diagnostic-only PR; no actual fix shipped. Doesn't move "
                 "any KR until the fix lands.",
        ),
        "labels": [],
        "notes": "In-flight CI work that hasn't shipped — easy false-"
                 "positive trap for the mapper.",
    },
    {
        "event": _ev(
            "ev_192", source="slack", kind="message",
            title="Random meme posted in #general",
            body="Pure social.",
        ),
        "labels": [],
        "notes": "Social — strict negative.",
    },
    {
        "event": _ev(
            "ev_193", source="content", kind="blog_post_draft",
            title="Drafted 'How to choose a co-founder' personal essay",
            body="Personal-brand piece. Not on the OKR Monitor blog and "
                 "not a benchmark/exec post.",
        ),
        "labels": [],
        "notes": "Personal-brand piece, not a company benchmark — strict "
                 "negative for KR3.1.",
    },
    {
        "event": _ev(
            "ev_194", source="linkedin", kind="post",
            title="LinkedIn post sharing a Verge article unrelated to OKRs",
            body="One-paragraph LinkedIn share. No OKR-tooling context.",
        ),
        "labels": [],
        "notes": "Even though it's on LinkedIn, the post itself isn't OKR-"
                 "monitor content — careful with KR3.2 over-mapping.",
    },
    {
        "event": _ev(
            "ev_195",
            title="Spent 2h reading a paper on retrieval-augmented narrative",
            body="Reading time, no artifact produced.",
        ),
        "labels": [],
        "notes": "Reading without output — strict negative.",
    },
    {
        "event": _ev(
            "ev_196", source="github", kind="commit",
            title="Fix typo in CONTRIBUTING.md",
            body="One-character typo fix in repo docs.",
        ),
        "labels": [],
        "notes": "Trivial — should not map.",
    },
    {
        "event": _ev(
            "ev_197", source="slack", kind="message",
            title="Out-of-office for Friday",
            body="OOO notice.",
        ),
        "labels": [],
        "notes": "Operational chatter — strict negative.",
    },
    {
        "event": _ev(
            "ev_198", source="calendar", kind="event",
            title="Yearly investor portfolio sync (unrelated company)",
            body="Personal investor activity.",
        ),
        "labels": [],
        "notes": "Personal — strict negative.",
    },
    {
        "event": _ev(
            "ev_199", source="github", kind="pr",
            title="Side project — added dark mode to weekend hackathon repo",
            body="Personal weekend hack.",
        ),
        "labels": [],
        "notes": "Personal repo — strict negative.",
    },
    {
        "event": _ev(
            "ev_200", source="slack", kind="message",
            title="Birthday lunch reminder for Sam on Friday",
            body="Social coordination.",
        ),
        "labels": [],
        "notes": "Social — strict negative.",
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
