# Instructions — Tonight's Setup

Two tasks. Total time: ~25 minutes. Do them in order — Part 2 doesn't fully work without Part 1 if you want the email side of things.

---

## Part 1 — Gmail SMTP for the 7pm email (10 min)

### Why this matters
Right now the 7pm daily report writes a markdown file at `reports/daily/YYYY-MM-DD/OWNER_FINANCE_REPORT.md` and commits to GitHub. To also have it land in your inbox like a normal email, set up Gmail SMTP.

If you never want email and prefer to read the report by refreshing the repo, **skip this part** — everything still works, the wrapper just no-ops the email send.

### Step 1.1 — Confirm 2-Step Verification is ON
Gmail app passwords require 2-Step Verification.

1. Go to https://myaccount.google.com/security
2. Under **How you sign in to Google**, confirm **2-Step Verification** is **On**
3. If it's off, turn it on (you'll need your phone)

### Step 1.2 — Generate a Google App Password
1. Go to https://myaccount.google.com/apppasswords
2. In the **App name** field, type: `OKR Monitor`
3. Click **Create**
4. Google shows you a 16-character password formatted like `xxxx xxxx xxxx xxxx`
5. **Copy it now** — Google won't show it again. You can paste with or without the spaces; both work.

### Step 1.3 — Paste into your local `.env`
1. Open `C:\Users\aloch\okr-monitor\.env` in your editor
2. Find the email block (near the bottom):
   ```
   SMTP_HOST=
   SMTP_PORT=587
   SMTP_USER=
   SMTP_PASS=
   SMTP_FROM=alochemes@gmail.com
   REPORT_TO_EMAIL=alochemes@gmail.com
   ```
3. Fill in like this:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=alochemes@gmail.com
   SMTP_PASS=xxxxxxxxxxxxxxxx
   SMTP_FROM=alochemes@gmail.com
   REPORT_TO_EMAIL=alochemes@gmail.com
   ```
   Replace `xxxxxxxxxxxxxxxx` with your app password (no spaces, no quotes).
4. Save. **Do not commit `.env`** — it's already in `.gitignore`.

### Step 1.4 — Test
From the repo root:
```bash
cd C:/Users/aloch/okr-monitor
OKR_MONITOR_DRY_RUN=true python scripts/daily_evening.py
```
(Dry-run is fine for the email test — the email body will say `DRY_RUN` but the SMTP send is real.)

In the script output you should see:
```json
"email": {
  "sent": true,
  "to": "alochemes@gmail.com",
  "host": "smtp.gmail.com",
  "port": 587,
  "from": "alochemes@gmail.com",
  "subject": "OKR Monitor — Daily OWNER/FINANCE — 2026-04-29 · ..."
}
```
And an email should land in your inbox within a few seconds.

### What can go wrong
| Symptom | Most likely cause | Fix |
|---|---|---|
| `"sent": false`, reason `535 Username and Password not accepted` | Wrong app password | Regenerate at the App passwords URL above |
| `"sent": false`, reason `[Errno 11001] getaddrinfo failed` | Wrong `SMTP_HOST` | Should be exactly `smtp.gmail.com` |
| `"sent": false`, reason `Connection refused` | Wrong `SMTP_PORT` | Should be `587` |
| Email arrives in **Spam** | First-time sender from Gmail SMTP | Mark as "Not spam"; future ones go to inbox |
| Email never arrives, no error | `REPORT_TO_EMAIL` is wrong or unset | Set it to your actual email |

---

## Part 2 — GitHub Actions secret injection (15 min)

### Why this matters
The two remote routines I scheduled (`trig_01Q99GjcE5D58K5WzLt4cJsC` Sunday + `trig_01BMMoRNTGDwuVshakfmapS6` Daily) clone the repo and try to run their wrapper scripts. They don't have access to your local `.env`, so the wrappers fall back to **dry-run mode** and the reports/proposals you get are stub content with a `DRY_RUN` banner.

To get **real LLM output**, the `ANTHROPIC_API_KEY` (and `  ` if you want email) needs to be in the runtime environment when the script runs.

GitHub Actions has first-class secret management. The cleanest path: replace the claude.ai daily routine with a GitHub Actions cron workflow.

I've already added the workflow file: [`.github/workflows/daily.yml`](.github/workflows/daily.yml). All you need to do is add the secrets and enable the workflow.

### Step 2.1 — Add secrets to the GitHub repo
1. Go to https://github.com/alochemes/okr-monitor/settings/secrets/actions
2. Click **New repository secret**
3. Add these one at a time:

   | Name | Value | Required? |
   |---|---|---|
   | `ANTHROPIC_API_KEY` | The same value as in your local `.env` (the funded one with the `sk-ant-api03-L-r...` prefix) | **Yes** — required for real LLM |
   | `SMTP_PASS` | The Gmail app password from Part 1 | Optional — only if you want email; skip if you didn't do Part 1 |

4. After saving, the secrets list should show both names with `Updated <date>` (the values are never displayed back).

### Step 2.2 — Enable Actions on the repo (one-time)
1. Go to https://github.com/alochemes/okr-monitor/actions
2. If you see **"Workflows aren't being run on
 this repository"**, click the green **I understand my workflows, go ahead and enable them** button.
3. You should now see **Daily 7pm OWNER/FINANCE report** in the left sidebar.

### Step 2.3 — Test it manually first
Don't wait until tonight to find out it doesn't work.

1. On the Actions page, click **Daily 7pm OWNER/FINANCE report** in the left sidebar.
2. Top-right of that page, click the **Run workflow** dropdown → **Run workflow** (green button).
3. The page refreshes. Wait ~2 minutes. A new run appears at the top, first yellow (running), then green (success) or red (failure).
4. Click the run to see the logs. The "Run daily report" step should print real (non-`DRY_RUN`) JSON.

If the run is **green**:
- Refresh https://github.com/alochemes/okr-monitor — a new commit should be there: `Daily OWNER/FINANCE report — 2026-04-29` (committed by `github-actions[bot]`).
- Open `reports/daily/2026-04-29/OWNER_FINANCE_REPORT.md` in the repo to read what landed.
- If you set up Part 1, an email should also arrive in your inbox.

If the run is **red**:
- Click the failed step. The most common errors:

  | Error in logs | Fix |
  |---|---|
  | `Your credit balance is too low` | The `ANTHROPIC_API_KEY` secret is the wrong key (Max-account, not funded workspace). Regenerate from the funded workspace at console.anthropic.com → Settings → API Keys, then update the secret. |
  | `403 Forbidden` on push | Repo permissions — go to Settings → Actions → General → "Workflow permissions" → select **Read and write permissions**, save. |
  | SMTP send failed | The `SMTP_PASS` secret is wrong. The script still succeeds (report still commits) but no email — fix the secret if you want email. |

### Step 2.4 — Disable the redundant claude.ai daily routine
GitHub Actions and the claude.ai routine would now both run at 7pm. Pick one:

**Recommended:** Disable the claude.ai daily routine.
1. Go to https://claude.ai/code/routines/trig_01BMMoRNTGDwuVshakfmapS6
2. Toggle **Enabled** off

The Sunday routine (`trig_01Q99GjcE5D58K5WzLt4cJsC`) keeps running for now and produces a dry-run weekly proposal each Sunday. **Keep it for now** as evidence the routine fires; we'll migrate it to Actions in a follow-up session once we know the daily one works.

---

## Verification checklist (do these tonight)

- [ ] `myaccount.google.com/apppasswords` shows an entry named `OKR Monitor`
- [ ] Local `.env` has `SMTP_HOST=smtp.gmail.com` and `SMTP_PASS=<16-char>`
- [ ] `OKR_MONITOR_DRY_RUN=true python scripts/daily_evening.py` → `"sent": true` in output
- [ ] Email arrived in inbox (or spam, marked Not spam)
- [ ] GitHub repo `Settings → Secrets and variables → Actions` shows `ANTHROPIC_API_KEY` (and `SMTP_PASS` if doing email)
- [ ] GitHub repo `Settings → Actions → General → Workflow permissions` is **Read and write**
- [ ] Manual workflow run from Actions tab → green
- [ ] New commit on `main` from `github-actions[bot]` with `reports/daily/2026-04-29/OWNER_FINANCE_REPORT.md`
- [ ] Email arrived (if Part 1 done)
- [ ] claude.ai daily routine toggled off

When all checked, the system runs unattended at 7pm Pacific every day.

---

## What's next (after tonight)

Once the daily flow is proven, the natural follow-ups are:
1. **Migrate the Sunday routine** to GitHub Actions the same way (5-minute copy of the workflow with `0 1 * * 1` cron + Sunday wrapper).
2. **Decide on the API budgeting cap inside the workflow.** Right now `daily_evening.py` respects the daily LLM circuit breaker ($50/day Sprint 0–1 → $100/day Sprint 2+). If the workflow fails because the cap was hit, the report still writes to disk; only the LLM calls were refused.
3. **Add a workflow status badge to README.md** so you can see at a glance whether yesterday's run was green.

---

If something breaks and the symptoms aren't in this file or in `RUNBOOK.md → When something breaks`, paste the failing logs into your next message and I'll diagnose.

---

# Part 3 — Notion OKR setup (eat our own cooking)

**Goal:** OKRs live in Notion (just like they will for every customer). The
agent system reads them via the same code path it'll use for pilots —
`scripts/notion_okr_pull.py` → JSON cache → `TRACKER.md §2`. You edit OKRs
in Notion; the daily run picks up the changes.

This is the production-grade dogfood: customers' OKRs land via the same
ingest, just from their Notion. We are workspace #1.

## 3.1 Create the Notion integration (one-time, ~2 min)

1. Open https://www.notion.so/profile/integrations
2. Click **+ New integration**
3. Settings:
   - **Name:** `OKR Monitor`
   - **Associated workspace:** the workspace where you want to host the OKR database
   - **Type:** Internal
4. Capabilities:
   - ☑️ Read content
   - ☑️ Update content
   - ☑️ Insert content
   - User Information: **No user information** (we don't need it)
5. **Submit** → on the resulting page, copy the **Internal Integration Secret**
   (starts with `ntn_…` or `secret_…`)
6. Open `C:\Users\aloch\okr-monitor\.env` and paste:
   ```
   NOTION_API_KEY=ntn_…
   ```

## 3.2 Pick (or create) the parent page (~1 min)

The OKR database needs a parent page. It can be any page in your workspace.

1. In Notion, create a new page (or pick existing). Name it
   `OKR Monitor — internal` so it's obvious this is OUR workspace, not a
   customer's. (See §4 below for why this distinction matters.)
2. **Connect the integration to that page.** On the page, click the `⋯`
   (top right) → **Connections** → search **OKR Monitor** → select.
   Without this step, every API call returns 404 — the integration only
   sees pages you explicitly grant.
3. **Get the page id.** Open the page in Notion. The URL looks like
   `https://www.notion.so/<workspace>/OKR-Monitor-internal-abc123def456…`.
   The 32-char hex string at the end is the page id. Copy it.
4. Paste it into `.env`:
   ```
   NOTION_PARENT_PAGE_ID=abc123def456…
   ```

## 3.3 Seed the database from TRACKER.md (one-time, ~30 sec)

Push the 17 OKRs currently in `TRACKER.md §2` up to Notion.

```powershell
cd C:\Users\aloch\okr-monitor

# Dry-run first — prints what would be created. No API call yet.
python scripts/notion_okr_seed.py

# When the dry-run output looks right:
python scripts/notion_okr_seed.py --apply
```

What the seed does:
- Creates a Notion **database** named `OKRs` under your parent page.
- Schema: `KR ID` (title), `Objective`, `Statement`, `Target`, `Current`,
  `Owner Pod`, `Due Date`, `Status`.
- Inserts one row per KR (17 total today).
- Prints the database id and writes it to
  `data/workspaces/okrmonitor-internal/notion.json`.

Paste the printed `NOTION_OKR_DATABASE_ID=…` into `.env` so cron finds it
without re-reading the workspace file.

## 3.4 First pull (~10 sec)

```powershell
python scripts/notion_okr_pull.py
```

This fetches the OKR rows from Notion, regenerates `TRACKER.md §2`, and
writes `data/workspaces/okrmonitor-internal/okrs.json`. Output should
report `objectives: 4, krs: 17`. The round-trip works:

> Edit OKRs in Notion → next pull regenerates TRACKER.md → next agent run
> sees the new state.

The daily cron (`scripts/daily_evening.py`) calls this automatically every
evening, so once setup is done you can stop running it manually.

## 3.5 Editing OKRs from now on

- **Edit in Notion**, not in `TRACKER.md`. Anything you change in
  `TRACKER.md §2` will be silently overwritten by the next pull. That's the
  point — a single source of truth for OKRs, with `TRACKER.md` as the
  cached read surface.
- Adding a new Objective: create the new `O5 — …` value in the
  **Objective** select column (Notion will offer to add it). Then add KR
  rows under it.
- Removing a KR: delete the row in Notion. The pull drops it from
  TRACKER.md §2 on the next run.

## 3.6 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `Notion 401: API token is invalid` | `NOTION_API_KEY` wrong / not pasted | Re-copy from notion.so/profile/integrations |
| `Notion 404 …` on seed | Integration not granted access to parent page | Page → ⋯ → Connections → OKR Monitor |
| Pull returns 0 OKRs | `NOTION_OKR_DATABASE_ID` wrong | Open the DB in Notion; the URL fragment after the workspace name is the id |
| TRACKER.md §2 not updating | Pull ran with `--no-tracker`, or check stderr | Run `python scripts/notion_okr_pull.py` without flags |
| `Could not locate §2 / §3 boundary` | Someone hand-edited TRACKER.md and broke the section anchors | Restore the `## 2. Company OKRs (…)` and `## 3. Pod-Level OKRs` headers exactly |

---

# Part 4 — Workspace separation (us vs pilots)

This is the architecture that keeps our dogfood data cleanly separated
from any customer (pilot) data. Worth understanding because it shapes how
every customer-facing artifact will be stored.

## 4.1 What's a "workspace"?

A workspace is one organization's data — their OKRs, their integrations,
their work events, their narratives. Two workspaces never mix in any
table, file, or report.

- **Our workspace:** slug = `okrmonitor-internal`. Committed to git so
  future-us can audit "did we eat our own cooking?".
- **Each pilot:** slug = `<company-slug>` (e.g. `acme-corp`). Lives at
  `data/workspaces/<slug>/`. **Gitignored.**

## 4.2 What lives per workspace

```
data/workspaces/<slug>/
├── workspace.yaml      # name, kind=internal|pilot, contacts, integrations
├── okrs.json           # cached OKRs (canonical source: their Notion DB)
├── notion.json         # Notion DB ids for this workspace
├── intake.md           # pilot intake questionnaire — their answers
├── 5in5.md             # 5-in-5 exercise output
└── health-check.md     # generated OKR Health Check report
```

The **templates** for `intake.md`, `5in5.md`, and `health-check.md` live
in `notion/03_playbooks/`. Those are the master copies (blank). The
**filled-out instances** live per-workspace in their own Notion (and
cached locally).

## 4.3 Code-level guards

- `core/workspace.assert_internal()` — call this at the top of any
  function that writes to repo-tracked files (`TRACKER.md`, etc.). The
  Notion seed and the pull's tracker-rewrite both have this guard, so it
  is impossible to accidentally regenerate `TRACKER.md` from a customer's
  Notion data.
- `OKR_MONITOR_WORKSPACE_ID` env var — set this in any pilot-specific
  invocation (e.g. cron jobs) so the right workspace is active. Default
  is `okrmonitor-internal`.

## 4.4 Multi-tenancy migration debt (Sprint 1)

Today the SQLite tables `work_events`, `event_kr_mappings`, `kr_signals`,
`narratives`, `proposals`, `runs` do **not** carry a `workspace_id`
column. They implicitly belong to `okrmonitor-internal`. **Before pilot #1
onboards, those columns must be added** + the existing rows backfilled to
`okrmonitor-internal`.

Building the columns now would slow Sprint 0 without buying anything;
deferring keeps shipping speed but creates a hard gate before pilot #1.

---

# Part 5 — Eating our own cooking on the customer flow

The whole product premise is that companies install our OKR/KPI framework
and we watch their work against it. Customers run a specific onboarding
flow:

1. **Pilot intake questionnaire** (30 questions, ~15 min) — template at
   `notion/03_playbooks/04_pilot_intake_questionnaire.md`.
2. **5-in-5 exercise** — template at
   `notion/03_playbooks/01_customer_okr_kpi_framework.md` §4.
3. **OKR Health Check** report — generated from #1 + #2.
4. **Install OKRs in Notion.** ✅ Just done in Part 3.
5. **Connect integrations** (GitHub, Linear, Slack). ✅ Already done.
6. **Receive weekly auto-narrative.** ✅ Loop already wired.

We should run **steps 1–3 on ourselves** before showing the flow to a
design partner. Otherwise we're shipping a process we haven't lived
through.

## 5.1 Where to put OUR filled-out artifacts

The principle: **same shape as customers, different workspace.**

- Our Notion workspace hosts the canonical filled-out documents:
  - `OKR Monitor — internal` (parent page, already created in §3.2)
    - `OKRs` (the database from §3.3)
    - `Intake — 2026-05-02` (page; you create + fill out)
    - `5-in-5 — 2026-05-02` (page)
    - `OKR Health Check — 2026-05-02` (page)
- The Python brain caches them locally in
  `data/workspaces/okrmonitor-internal/`. Today only `okrs.json` is
  auto-cached (via the pull). Intake / 5-in-5 / Health Check stay in
  Notion only — Sprint-1 work to wire them through `core/notion_intake.py`.

**Why fill it out in Notion (not by editing the templates in `notion/`):**
the `notion/03_playbooks/*.md` files are the master templates customers
will receive. If you fill them out on yourself, customers will inherit
your answers as starter content. Keep them blank; fill out **your copy**
in your own Notion workspace.

## 5.2 How customer artifacts will land (Sprint 1+)

1. Customer goes through the intake questionnaire **in their Notion** (we
   send them the template).
2. They grant the OKR Monitor integration access to their pages.
3. `core/notion_intake.py` (TBD) fetches their answers + caches under
   `data/workspaces/<their-slug>/intake.md`.
4. A new agent (`okr_health_check`) generates the Health Check report
   from intake + 5-in-5 inputs.
5. `data/workspaces/<their-slug>/` is gitignored, so customer data never
   touches our repo.

Until that wiring lands, customers fill out the template in *their*
Notion and we manually pull the markdown into our system if we need it.

## 5.3 Today's recommendation

If you have ~75 minutes:

1. ✅ Part 3 done — your OKRs are in Notion.
2. **Block 30 minutes.** Sit down with
   `notion/03_playbooks/04_pilot_intake_questionnaire.md` open. Create a
   fresh Notion page `Intake — 2026-05-02` under `OKR Monitor — internal`.
   Answer each section honestly **about OKR Monitor itself**.
3. **Block another 25 minutes.** Do the 5-in-5 exercise from
   `notion/03_playbooks/01_customer_okr_kpi_framework.md` §4. Output goes
   to a Notion page `5-in-5 — 2026-05-02`.
4. **Compare your 5-in-5 outputs to TRACKER.md §2.** The surprises are
   signal — adjust the OKRs in Notion (which the next pull will land in
   TRACKER.md). This is the dogfood loop.

The auto-Health-Check report ships in Sprint 1 — once you've done the
manual version above, we'll have ground-truth to validate the agent
against.

---

# Part 6 — Integration matrix (every tool the customer might use)

Customers don't change their stack for us; we read from whatever they
already run. The full matrix — **33 integrations across 3 categories**
— is designed and stubbed in
[`notion/02_product/04_okr_source_integrations.md`](notion/02_product/04_okr_source_integrations.md).
This section gives you the operator's-eye summary.

## 6.1 The three categories

| Category | What it does | Lives at | Sources |
|---|---|---|---|
| **OKR sources** | Provides the KR catalog | `core/okr_sources/` | Notion ✅, Monday, Asana Goals, Mooncamp, Coda, Lattice, Workboard, Google Docs (LLM), CSV |
| **Work-event sources** | Provides the work to map | `core/work_event_sources/` | code (GitHub ✅, GitLab, Bitbucket), tickets (Linear ✅, Jira, Asana, Shortcut, GH Issues), docs (Notion, Confluence, GDrive, Coda), chat (Slack, Teams, Discord), CRM (HubSpot, Salesforce, Pipedrive, Attio) |
| **KPI sources** | Provides the metrics that should always be green | `core/kpi_sources/` | Datadog, Mixpanel, Amplitude, PostHog, Grafana |

✅ = shipped today. The other 30 are scaffolded: each has a Python
module with a clear docstring documenting auth, API endpoints, customer
setup, and effort estimate. None are yet implemented; they raise
`NotImplementedError` pointing at the design doc.

## 6.2 Where to see status at a glance

Two places — both surface the same data:

- **Web UI:** `/app/integrations` (signed-in). Shows all 33 sources as
  cards grouped by category, with live connection status (🟢 connected
  / 🟠 stale / 🔴 error / ⚪ not configured) sourced from
  `web/public/integration_status.json`.
- **JSON snapshot:** `web/public/integration_status.json` — written by
  `scripts/daily_evening.py` on every daily run. Same shape as
  `kr_signals.json` (versioned `schema: 1`).

Today's run shows **3/33 connected** (Notion OKRs, GitHub commits,
Linear issues). The remaining 30 are scaffolded with full setup notes
in their module docstrings.

## 6.3 How to wire a new source

When you (or a contractor) implement source #N:

1. **Read the module docstring** (`core/<category>_sources/<key>.py`).
   It already has the API URL, auth model, customer-setup steps, and
   gotchas. Replace `NotImplementedError` with the implementation.
2. **Update both registries**:
   - Python: `core/<category>_sources/__init__.py` — flip `status` to
     `shipped`.
   - TypeScript: `web/lib/integrations/registry.ts` — same flip.
3. **Add to `SHIPPED_AGENT`** in `core/integration_status.py` so the
   freshness probe finds the run rows.
4. **Run the daily** — `python scripts/daily_evening.py --no-email` —
   to confirm the new source flips to 🟢 in `/app/integrations`.

## 6.4 Sequencing

See `notion/02_product/04_okr_source_integrations.md` §3. Headline:

- **Sprint 1**: Slack (work-events), Monday.com (OKRs + work-events).
  The orchestrator (`core/okr_pull.py`) gets extracted so source #2
  is a clean drop-in.
- **Sprint 2**: Asana (Goals + tasks), Jira, Coda, Mooncamp, CSV
  fallback.
- **Sprint 3**: Lattice (first OAuth source — also unblocks the
  multi-tenant OAuth platform), Workboard, HubSpot, Datadog, Mixpanel.
- **Sprint 4+**: long-tail, ICP-driven (Salesforce, GitLab, Bitbucket,
  Confluence, Google Drive, Discord, Teams, Pipedrive, Attio, Shortcut,
  Amplitude, PostHog, Grafana, Google Docs LLM extractor).

## 6.5 The auth phase boundary

| Phase | When | Mechanism |
|---|---|---|
| **v0** | Sprint 0–2 | Operator pastes tokens into `.env`. Single workspace. |
| **v1** | Sprint 3+ | OAuth platform (`core/oauth.py`) for the OAuth-required sources. Per-pilot grant flow lands in `/app/integrations/<source>/connect`. |
| **v2** | Sprint 4+ | Self-serve onboarding — pilot signs up, walks through 3 connection flows, sees first narrative within 30 min (KR1.4). |

**Don't build OAuth before Sprint 3** — the first OAuth-required source
that lands is Lattice. Doing it once unlocks every OAuth source at once;
doing it before there's demand is YAGNI.

## 6.6 Front-end contract — how the web stays in sync with the back-end

The web app reads the `integration_status.json` snapshot. The Python
brain writes it. Drift between the TypeScript registry
(`web/lib/integrations/registry.ts`) and the Python registries is
caught by a CI check (Sprint 1 deliverable) that parses both and fails
the build on mismatch. Until that check ships, eyeball the two files
when you add a source.

Every page that renders integrations handles 5 missing-data cases
gracefully (snapshot missing, source stale, source erroring, source
unknown, no integrations configured). See the design doc §11.5.

## 6.7 What the customer sees (the answer to "ANY combination of flows")

When a pilot fills out the intake questionnaire (sections 3–4), each
answer maps to one integration in the matrix:

| Intake Q | Customer answer | Integration to wire |
|---|---|---|
| Q8 | Notion / Asana / Mooncamp / Lattice / Workboard / Coda / Monday / Google Doc / CSV | `okr_sources/<that one>` |
| Q14 | Datadog / Mixpanel / Amplitude / PostHog / Grafana | `kpi_sources/<that one>` |
| Q18 | GitHub / GitLab / Bitbucket | `work_event_sources/<that one>` |
| Q19 | Linear / Jira / Asana / Shortcut / GH Issues | `work_event_sources/<that one>` |
| Q20 | Notion / Confluence / GDrive / Coda | `work_event_sources/<that one>` |
| Q21 | Slack / Teams / Discord | `work_event_sources/<that one>` |
| Q22 | HubSpot / Salesforce / Pipedrive / Attio | `work_event_sources/<that one>` |

7 categories × ~5 options each = 78,000 paper combinations. In practice
**~12 archetype stacks cover ~80% of pilots** (e.g., the modal SaaS
stack: GitHub + Linear + Notion + Slack + Datadog). Build by frequency.
