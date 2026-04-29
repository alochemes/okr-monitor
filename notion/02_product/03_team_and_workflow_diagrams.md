# Team & workflow diagrams

> Visual references for the 30-agent org, the data flow, and the tech stack.
>
> Diagrams are written in **Mermaid** — they render natively in GitHub markdown, Notion code blocks (set language to `mermaid`), Obsidian, and most modern markdown viewers. To edit, open the source `.md` file and modify the Mermaid block.

---

## 1. The 30-agent org chart

The company is structured as 6 pods + the operator. Every agent reports to the operator (Stage 0). Once an agent earns Stage 1 trust, it can act on its own outputs within scoped permissions.

```mermaid
graph TD
    OP["⬢ Operator<br/><i>andrew@skinmap.com</i><br/>reviews every proposal"]

    subgraph Strategy[" Strategy Pod (4) "]
        CEO["ceo<br/><i>weekly_priorities · daily_status</i>"]
        CPO["cpo<br/><i>roadmap_review · product_roadmap_report</i>"]
        CTO["cto<br/><i>architecture_review</i>"]
        CFO["cfo<br/><i>pricing_model · cost_projection</i>"]
    end

    subgraph PD[" Product & Design Pod (5) "]
        PM["pm<br/><i>user_stories</i>"]
        UXR["ux_researcher<br/><i>discovery_synthesis</i>"]
        UXD["ux_designer<br/><i>design_brief</i>"]
        UID["ui_designer<br/><i>component_spec</i>"]
        CW["copywriter<br/><i>copy_draft</i>"]
    end

    subgraph ENG[" Engineering Pod (7) "]
        BA["backend_architect<br/><i>api_design</i>"]
        FL["frontend_lead<br/><i>ui_architecture</i>"]
        IE["integrations_engineer<br/><i>integration_design</i>"]
        DP["data_pipeline<br/><i>pipeline_design</i>"]
        AE["ai_engineer<br/><i>eval_proposal</i>"]
        PL["platform<br/><i>infra_review</i>"]
        SEC["security<br/><i>security_review</i>"]
    end

    subgraph AID[" AI / Data Pod (4 — load-bearing) "]
        OM["⚡ okr_mapper<br/><i>map_event</i>"]
        SA["⚙ signals_analyst<br/><i>kr_signals_snapshot · pure compute</i>"]
        FC["⚙ forecasting<br/><i>kr_forecast · pure compute</i>"]
        NA["⚡ narrative<br/><i>weekly_narrative</i>"]
    end

    subgraph GTM[" GTM Pod (6) "]
        GH["growth_hacker<br/><i>experiment_proposal</i>"]
        CT["content<br/><i>blog_post_draft</i>"]
        DG["demand_gen<br/><i>cold_sequence</i>"]
        SE["sales_engineer<br/><i>demo_script</i>"]
        FS["founder_sales<br/><i>outreach_drafts</i>"]
        CPR["community_pr<br/><i>pr_pitches</i>"]
    end

    subgraph CO[" Customer & Ops Pod (4) "]
        OB["onboarding<br/><i>onboarding_playbook</i>"]
        SUP["support<br/><i>ticket_triage</i>"]
        PP["pilot_pm<br/><i>pilot_milestone_review</i>"]
        AO["analytics_ops<br/><i>growth_metrics</i>"]
    end

    Strategy -.proposals.-> OP
    PD -.proposals.-> OP
    ENG -.proposals.-> OP
    AID -.proposals.-> OP
    GTM -.proposals.-> OP
    CO -.proposals.-> OP

    classDef loadbearing fill:#0F0E0C,color:#FAF7F2,stroke:#C73A14,stroke-width:2px;
    class OM,NA,SA,FC loadbearing;
```

**Legend:**
- ⚡ = LLM-driven agent (Anthropic API call per run)
- ⚙ = Pure-compute agent (no LLM, just reads/writes the database)
- ⬢ = Human operator (reviews every proposal)
- Bold-bordered = load-bearing (the product breaks if these break)

---

## 2. Data flow — how a single commit becomes a Friday narrative

```mermaid
graph LR
    subgraph Sources[" Where work happens "]
        GH["GitHub<br/>commit, PR"]
        LIN["Linear / Jira<br/>issue, comment"]
        SLK["Slack<br/>thread, message"]
        NOT["Notion<br/>doc update"]
    end

    Sources ==> WE["work_events<br/><i>UNIQUE on (source, source_event_id)<br/>idempotent ingest</i>"]

    WE ==> OM["⚡ okr_mapper<br/><i>per event:<br/>which KR(s)?<br/>confidence ≥ 0.5?</i>"]

    OM ==> EKM["event_kr_mappings<br/><i>(event, kr, confidence, reasoning)</i>"]

    EKM ==> SA["⚙ signals_analyst<br/><i>per KR:<br/>events_7d, events_30d,<br/>distinct_actors</i>"]

    SA ==> KRS["kr_signals<br/><i>rolling counts<br/>per KR per run</i>"]

    KRS ==> FC["⚙ forecasting<br/><i>per KR:<br/>required vs observed pace<br/>verdict: on_track / drifting / off</i>"]

    FC ==> KRS2["kr_signals<br/><i>verdict columns filled</i>"]

    KRS2 ==> NA["⚡ narrative<br/><i>weekly:<br/>verdict per KR + cited<br/>events + 'do this Monday'</i>"]

    NA ==> NAR["narratives<br/><i>markdown brief</i>"]

    NAR ==> EM["📧 Friday 9 AM email<br/>+<br/>📄 reports/proposals/...md<br/>committed to git"]

    classDef src fill:#FAF7F2,color:#0F0E0C,stroke:#1F1D1A;
    classDef store fill:#F2EDE4,color:#0F0E0C,stroke:#6B6862;
    classDef agent fill:#0F0E0C,color:#FAF7F2,stroke:#C73A14,stroke-width:2px;
    classDef out fill:#C73A14,color:#FAF7F2,stroke:#0F0E0C;
    class GH,LIN,SLK,NOT src;
    class WE,EKM,KRS,KRS2,NAR store;
    class OM,SA,FC,NA agent;
    class EM out;
```

---

## 3. Reporting flow — the daily 7 PM OWNER/FINANCE brief

```mermaid
graph TD
    CRON["GitHub Actions cron<br/>0 23 * * * UTC<br/>= 7 PM Pacific"]

    CRON ==> ORC["scripts/daily_evening.py"]

    ORC ==> SA["⚙ signals_analyst refresh"]
    ORC ==> FC["⚙ forecasting refresh"]

    SA ==> DASH["📊 KPI Dashboard<br/><i>core/dashboard.py<br/>renders kr_signals as<br/>markdown table</i>"]
    FC ==> DASH

    ORC ==> CEO["⚡ ceo.run_daily_status<br/><i>today vs expected</i>"]
    ORC ==> CPO["⚡ cpo.run_product_roadmap_report<br/><i>shipped/in-progress/blocked</i>"]
    ORC ==> CFO["⚡ cfo.run_cost_projection<br/><i>14-day forecast</i>"]
    ORC ==> AO["⚡ analytics_ops.run<br/><i>pilots / CAC / channels</i>"]

    DASH ==> ASM["Assemble report body"]
    CEO ==> ASM
    CPO ==> ASM
    CFO ==> ASM
    AO ==> ASM

    ASM ==> FILE["📄 reports/daily/YYYY-MM-DD/<br/>OWNER_FINANCE_REPORT.md<br/><i>committed to git</i>"]
    ASM ==> EMAIL["📧 SMTP send via core/mailer.py<br/>(if SMTP_HOST set)"]

    classDef cron fill:#FAF7F2,color:#0F0E0C,stroke:#1F1D1A;
    classDef agent fill:#0F0E0C,color:#FAF7F2,stroke:#C73A14,stroke-width:2px;
    classDef pure fill:#1F1D1A,color:#FAF7F2,stroke:#6B6862;
    classDef out fill:#C73A14,color:#FAF7F2,stroke:#0F0E0C;
    class CRON cron;
    class CEO,CPO,CFO,AO agent;
    class SA,FC pure;
    class FILE,EMAIL out;
```

---

## 4. Tech stack — what we run where

```mermaid
graph TB
    subgraph LOCAL[" Operator's laptop "]
        PY["Python 3.11+<br/>Click CLI / agents"]
        SQL["SQLite (WAL)<br/>data/okr_monitor.db"]
        ENV["local .env<br/>(funded API key,<br/>SMTP creds)"]
        VS["Cursor / VS Code<br/>+ Claude Code CLI"]
        TR["TRACKER.md<br/><i>source of truth</i>"]
    end

    subgraph GH_REPO[" GitHub: alochemes/okr-monitor (private) "]
        SRC["Source of truth"]
        PROP["proposals/<br/>weekly proposals"]
        REP["reports/daily/<br/>nightly briefs"]
        WF["GitHub Actions<br/>workflows<br/>(daily.yml, sunday.yml)"]
        SECR["GitHub Secrets<br/><i>ANTHROPIC_API_KEY<br/>SMTP_PASS</i>"]
    end

    subgraph CLOUD[" Cloud / SaaS "]
        ANT["Anthropic API<br/><i>Sonnet 4.6 + caching</i>"]
        VC["Vercel<br/><i>web/ landing page</i>"]
        NX["Next.js 15 build"]
        PH["PostHog<br/><i>analytics + A/B flags</i>"]
        SM["Gmail SMTP<br/><i>email delivery</i>"]
    end

    subgraph FUTURE[" Planned / not yet built "]
        SUP["Supabase<br/>production DB"]
        NAN["Nango<br/>integration OAuth"]
        RES["Resend<br/>transactional email"]
        OBS["Sentry / Axiom<br/>observability"]
    end

    PY --> SQL
    PY --> ENV
    PY --> ANT
    PY --> SM
    VS --> PY
    VS --> SRC
    SRC --> PROP
    SRC --> REP
    SRC --> WF
    WF --> SECR
    WF --> ANT
    WF --> SM
    WF --> PROP
    WF --> REP
    SRC --> NX
    NX --> VC
    VC --> PH

    classDef local fill:#FAF7F2,color:#0F0E0C,stroke:#1F1D1A,stroke-width:2px;
    classDef ghub fill:#F2EDE4,color:#0F0E0C,stroke:#6B6862;
    classDef cloud fill:#0F0E0C,color:#FAF7F2,stroke:#C73A14,stroke-width:2px;
    classDef fut fill:#FAF7F2,color:#6B6862,stroke:#D9D2C4,stroke-dasharray: 5 5;
    class PY,SQL,ENV,VS,TR local;
    class SRC,PROP,REP,WF,SECR ghub;
    class ANT,VC,NX,PH,SM cloud;
    class SUP,NAN,RES,OBS fut;
```

**Stack rationale (in 30 words each):**

| Tech | Why this, why not the alternative |
|---|---|
| **Python 3.11+** | Stdlib-rich, great Anthropic SDK, agents stay readable. Not Go: agents are mostly LLM glue, not perf-critical. |
| **SQLite (WAL)** | Zero ops, single file, good enough for ~1k pilots. Move to Supabase Postgres at first multi-tenant customer. |
| **Anthropic Sonnet 4.6 + prompt caching** | The cached system block (TRACKER.md + company.yaml) is ~4500 tokens; cache hit drops cost ~10×. Opus only for edge cases. |
| **GitHub Actions for cron** | First-class secret management, free for our scale, runs are visible in the UI. Better than the claude.ai routine for production cadences. |
| **Next.js 15 on Vercel** | Server components reduce JS shipped; Vercel's preview branches are the right deploy story for a marketing site iterating fast. |
| **PostHog** | A/B flags + analytics + session replay in one tool. Open-source-core, EU + US options for data residency. |
| **Tailwind + Fraunces + Inter + JetBrains Mono** | Editorial typography pairing avoids the generic SaaS look. Single accent color (persimmon) keeps signal high. |

---

## 5. Operator workflow — a typical week

```mermaid
gantt
    title  Operator week — what falls on the calendar
    dateFormat  HH:mm
    axisFormat  %a

    section Mon
    Read Sunday brief                     :08:30, 15m
    cli/review --all (last week's proposals) :09:00, 30m
    Standup grounded in brief             :10:00, 15m
    Daily 7pm brief lands                 :19:00, 5m

    section Tue
    Daily 7pm brief lands                 :19:00, 5m

    section Wed
    Daily 7pm brief lands                 :19:00, 5m
    Mid-week check on at-risk KRs         :15:00, 30m

    section Thu
    pilot_pm review (queue)               :10:00, 20m
    Daily 7pm brief lands                 :19:00, 5m

    section Fri
    Friday auto-narrative arrives         :09:00, 5m
    Forward brief to leaders              :09:30, 10m
    Daily 7pm brief lands                 :19:00, 5m

    section Sat
    Off                                   :00:00, 24h

    section Sun
    Sunday strategy pod fires (auto)      :18:00, 60m
```

**Total operator time per week on OKR Monitor itself: ~2 hours.** The product's job is to give back the hours your CoS used to spend playing telephone — not add ceremony.
