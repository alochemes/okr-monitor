# okr-monitor / web

The marketing landing page for OKR Monitor. Next.js 15 (App Router) +
Tailwind CSS, deployable to Vercel.

## Local dev

```bash
cd web
npm install
npm run dev
# http://localhost:3000
```

Requires Node ≥ 18.18 (Next.js 15). Verified on Node 20 + 22.

## What this is

A single-page editorial landing — eight sections — that introduces the
product to a Chief of Staff / Head of Operations buyer. Design intentionally
avoids the generic AI-SaaS aesthetic (no purple gradients, no glow effects,
no "AI-powered" copy). Type system: Fraunces (display) + Inter (body) +
JetBrains Mono (data). Single accent color: persimmon.

## File map

```
web/
├── app/
│   ├── layout.tsx           # html shell, font setup, metadata
│   ├── page.tsx             # composes the 8 sections
│   ├── globals.css          # Tailwind + a few custom utility classes
│   └── api/
│       └── waitlist/
│           └── route.ts     # POST handler for the email-capture form
├── components/
│   ├── Nav.tsx
│   ├── Hero.tsx             # masthead + the printed-memo asset
│   ├── NarrativeMock.tsx    # the "Friday brief" mock (the proof)
│   ├── ProblemSection.tsx   # 02 — the autopsy
│   ├── HowItWorks.tsx       # 03 — Connect / Map / Narrate
│   ├── IntegrationsStrip.tsx # 04 — wordmarks, no logos
│   ├── Pricing.tsx          # 05 — four tiers, "Team" emphasized
│   ├── AudienceSection.tsx  # 06 — for-you-if vs not-yet-if
│   ├── WaitlistFooter.tsx   # 07 — capture + footer
│   ├── WaitlistForm.tsx     # client component (form state)
│   └── SectionHeading.tsx   # shared editorial heading
├── tailwind.config.ts
├── postcss.config.mjs
├── next.config.mjs
├── tsconfig.json
└── package.json
```

## Deploy to Vercel

### One-time setup

1. From the repo root, install the Vercel CLI: `npm i -g vercel` (or use
   the Vercel web UI to import the repo).
2. From the `web/` directory, run `vercel link` — choose the `alochemes`
   scope and create a new project named `okr-monitor`.
3. Set the **Root Directory** to `web/` in the Vercel project settings
   (Settings → General → Root Directory). This tells Vercel to install +
   build inside `web/` rather than the repo root.
4. (Optional) set a custom domain in Vercel's domains settings.

### Deploy

```bash
cd web
vercel deploy --prod
```

Or push to `main` — Vercel auto-deploys preview branches and production.

### Env vars (none required for v0)

The waitlist endpoint writes to `<repo>/data/waitlist.json` locally. On
Vercel the filesystem outside `/tmp` is read-only, so the route falls back
to `console.log("[waitlist:fallback]", { ... })` — entries are recoverable
from the Vercel Function logs.

When you're ready to capture into a real store, replace the `appendToFile`
call in `app/api/waitlist/route.ts` with one of:

- **Resend audiences** (recommended) — `npm i resend`, set `RESEND_API_KEY`,
  call `resend.contacts.create({ email, audienceId })`.
- **Supabase** — insert into a `waitlist` table.
- **Postmark broadcast list** — POST to their list-subscribe API.

## Reading the captured signups

```bash
cat data/waitlist.json | jq '.[].email'
```

If running locally, signups appear immediately. From production, see Vercel
Function logs and grep for `[waitlist:fallback]`.

## Conventions

- Server components by default; `"use client"` only for the form.
- One accent color (persimmon `#C73A14`) — used sparingly. Anything else
  uses ink, paper, or muted tones.
- Tailwind for layout + spacing. Custom utilities live in `globals.css`
  under `@layer components` (`.btn-primary`, `.memo`, `.label`, etc.).
- Editorial conventions: numbered sections (`01`, `02`...), all-caps
  labels with wide tracking, hairline rules between sections, drop caps
  available via `.dropcap`.

## When you change copy

The hero headline and the lede paragraph are in `components/Hero.tsx`. The
"Friday brief" content lives in `components/NarrativeMock.tsx` (the `ROWS`
array). Pricing tiers are in `components/Pricing.tsx` (`TIERS` array). All
section copy lives in its own component file — no copy in `page.tsx`.

## What's next

- Add `/health-check` page — the lead magnet form expanded with a "send us
  your OKR doc" upload. Once the backend exists, this becomes the
  primary conversion path.
- Add `/blog/` route group for the content agent's posts.
- Add `/changelog/` route group for the daily/weekly briefs that get
  committed to `reports/` and `proposals/`.
- Wire the form to Resend (for the email auto-reply with the Health
  Check intake) and Supabase (for the actual waitlist storage).
