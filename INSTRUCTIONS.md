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
