# Deploy — Vercel

The web app lives in `web/` of the `alochemes/okr-monitor` repo. The Python
brain stays out of the deploy — Vercel only builds and serves Next.js.

## One-time setup

1. **Create the Supabase project** (free tier is fine for Sprint 0).
   - Auth → Providers → Email → enable **Magic Link** (and disable password
     sign-up unless you want both).
   - Auth → URL Configuration → set **Site URL** to your production origin
     (e.g. `https://app.okrmonitor.com`) and add the Vercel preview pattern
     (`https://*.vercel.app`) and `http://localhost:3000` to **Redirect
     URLs**. The magic link callback path is `/app/auth/callback`.
   - Copy the project URL and the `anon` public key from Settings → API.

2. **Create the Vercel project.**
   - "Add New… → Project", import `alochemes/okr-monitor` from GitHub.
   - **Root directory:** `web` (critical — repo root is the Python brain).
   - Framework preset: Next.js (auto-detected).
   - Build command: leave default (`next build`).

3. **Set Vercel environment variables** (Settings → Environment Variables):

   | Name                              | Value                        | Environments     |
   |-----------------------------------|------------------------------|------------------|
   | `NEXT_PUBLIC_SUPABASE_URL`        | `https://<ref>.supabase.co`  | Production, Preview, Development |
   | `NEXT_PUBLIC_SUPABASE_ANON_KEY`   | `<anon public key>`          | Production, Preview, Development |

   The `NEXT_PUBLIC_` prefix is required so the values are inlined into the
   browser bundle. The `anon` key is safe to expose; never paste the
   service-role key here.

4. **Custom domain.**
   - Add `app.okrmonitor.com` (or whatever you registered) under
     Settings → Domains.
   - In your DNS provider, create a `CNAME` from `app` →
     `cname.vercel-dns.com`. Vercel issues TLS automatically.
   - Once DNS resolves, update Supabase's **Site URL** to match.

5. **First deploy.**
   - Push to `main`; Vercel deploys automatically. Or from the CLI:
     ```bash
     cd web
     npx vercel link
     npx vercel --prod
     ```

## What gets deployed

| Route | What it does |
|---|---|
| `/` | Editorial marketing landing |
| `/v2` | Tech "engineering ops console" landing |
| `/health-check` | Inbound OKR Health Check intake form |
| `/api/waitlist` | POST → captures inbound emails |
| `/api/health-check` | POST → captures health-check submissions |
| `/app/login` | Magic-link sign-in (Supabase) |
| `/app/auth/callback` | Magic-link verifier; sets the session cookie |
| `/app/dashboard` | Server-rendered KR scoreboard. Reads `web/public/kr_signals.json`. **Auth-gated** by `middleware.ts`. |

## What is NOT auto-deployed

- The Python brain (`scripts/daily_evening.py`, agents/*, etc.) runs on the
  **GitHub Actions** workflow, not Vercel. See `.github/workflows/`.
- `web/public/kr_signals.json` is committed to git by the daily run; Vercel
  picks it up on the next push. There is no live database connection from
  the Vercel runtime to the Python SQLite file by design — the snapshot is
  the contract.

## Troubleshooting

- **Build fails with "Supabase env not configured"** — env vars not set
  in Vercel for the relevant environment (Production / Preview / Dev).
  Re-deploy after adding them.
- **Magic link redirects to `localhost:3000`** — Supabase Site URL is
  still pointing at dev. Update Auth → URL Configuration.
- **Dashboard shows "No snapshot yet"** — `daily_evening.py` hasn't run
  against this checkout yet. Run it locally with
  `OKR_MONITOR_DRY_RUN=true python scripts/daily_evening.py --no-email`,
  commit `web/public/kr_signals.json`, and redeploy. (Once the GitHub
  Actions cron is wired, this is automatic.)
- **`/app/dashboard` returns a redirect loop** — middleware can't reach
  Supabase to validate the session. Check `NEXT_PUBLIC_SUPABASE_URL` is
  reachable from Vercel's region (`iad1` by default).
