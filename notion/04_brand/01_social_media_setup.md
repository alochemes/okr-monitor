# Social media setup — Twitter, LinkedIn, Facebook

> Step-by-step setup for the three primary social channels. I cannot create accounts on your behalf (browser actions on each platform require you), but everything you need to copy-paste is below — bios, launch posts, asset specs.

---

## Decision: which channels matter for this ICP

Our buyer is a Chief of Staff or Head of Operations at a Series A–C SaaS. Where they actually are:

| Channel | Priority | Why |
|---|---|---|
| **LinkedIn** | 🔴 Highest | Where ops/CoS conversations live. Founder posts + company page both matter. |
| **Twitter / X** | 🟡 Medium | Where founders, VCs, and ops thought-leaders cross-pollinate. Lower volume, higher quality. |
| **Facebook** | 🟢 Low | Buyer is not active here professionally. Set up a basic page for SEO + brand consistency, don't invest. |
| Threads / Bluesky | ⚪ Skip for now | Audience not concentrated yet. Revisit Q4. |

**Recommended order:** LinkedIn (founder + company) → Twitter → Facebook stub.

---

## 1. LinkedIn — Founder profile

Optimize the **founder's personal page** before anything else. Pre-launch, your personal brand is the company brand.

### Headline (220 char max)

```
Building OKR Monitor — connecting OKRs to the work that actually happens. Previously: Skinmap (skin-cancer detection). Open about the build at /in/<your-handle>.
```

### About section (2,600 char max)

```
I'm building OKR Monitor — a B2B tool that connects company OKRs to the actual work happening in code, tickets, and conversations, and surfaces drift in real time.

Why it exists: most companies set OKRs in January and find out at quarter-end that nothing got done on KR-3. The post-mortem is the most honest writing the company does all year. We close that gap by reading the work directly — every Friday at 9 AM, a one-page exec brief lands in your inbox naming which KRs are on track, which are drifting, and exactly which commits, tickets, and conversations moved them.

I'm building this in public. The full repo, the OKRs, the daily reports, and the weekly briefs are all open on GitHub at github.com/alochemes/okr-monitor. We dogfood the product on the company building it — every agent run is itself a "work event" in our database, and we generate our own Friday brief from our own work.

If you're a Chief of Staff or Head of Operations at a Series A–C SaaS company and you've ever spent a Monday morning DM'ing five people to ask "are we on track?", I'd love a 30-minute conversation. We have 5 design partner slots open.

alochemes@gmail.com · skinmap.com (previous company, currently building OKR Monitor full-time)
```

### Profile photo + cover

- **Profile photo:** professional headshot, neutral background. If you don't have one, a phone selfie against a plain wall is fine.
- **Cover image:** 1584 × 396 px. Use this exact spec — the wedge sentence in Fraunces serif on warm paper background. I can generate the design file separately if you want; for v0 use the Canva template "Editorial Personal Brand" and substitute:
  - Top line: `OKR MONITOR · ISSUE 001`
  - Middle (large): `Connecting OKRs to the work that actually happens.`
  - Bottom right: `okrmonitor.com`

### Featured section (3 items)

1. **The wedge essay** — your first long-form post (see launch posts below).
2. **The GitHub repo** — `github.com/alochemes/okr-monitor`.
3. **Apply for design partner** — link to the landing page waitlist.

---

## 2. LinkedIn — Company page setup

### Tagline (120 char max)

```
The Friday brief that connects your OKRs to the work that actually happens.
```

### About / Description (2,000 char max)

```
OKR Monitor reads the work happening in your tools — code commits, tickets, customer conversations — and tells you, every Friday, which OKRs are on track, which are drifting, and exactly which work moved them.

Built for Chiefs of Staff and Heads of Operations at Series A–C SaaS who are tired of finding out at quarter-end that nothing got done on KR-3.

→ One-page Friday exec brief
→ Daily 7 PM cost / roadmap / metrics digest
→ Per-KR drift detection (active / stale / off / drifting / on-track)
→ Connects to GitHub, Linear, Jira, Slack, Notion
→ 30 background agents handling everything from outreach to architecture review

Currently in design-partner phase — apply at okrmonitor.com.
```

### Industry / size

- Industry: **Software Development** (or **Computer Software** if not available)
- Specialties (10 max): `OKR management`, `Engineering metrics`, `Operations tools`, `B2B SaaS`, `AI agents`, `Chief of Staff tools`, `Goal tracking`, `Product analytics`
- Company size: **2–10 employees**
- Founded: **2026**
- Headquarters: your city
- Website: **okrmonitor.com** (point this at the Vercel deployment)

### Logo + cover

- **Logo:** 300 × 300 px. The lock-up — words "OKR Monitor" in Fraunces 600 + a 16×16px persimmon square dot at the baseline.
- **Cover:** 1128 × 191 px. Same wedge sentence treatment as personal cover but slightly different copy: "What your team did this week — tied to what you said matters."

---

## 3. Twitter / X — handle + profile

### Handle suggestions (in priority order)

1. `@okrmonitor` — primary target, check availability first.
2. `@okr_monitor` — fallback if 1 is taken.
3. `@okrmonitorhq` — fallback if both above are taken.

### Bio (160 char max)

```
The Friday brief that connects your OKRs to the work that actually happens. Building in public. Apply for design partner → okrmonitor.com
```

### Header image

1500 × 500 px. Same editorial treatment as LinkedIn covers — the wedge sentence in Fraunces, persimmon accent.

### Pinned tweet (after first launch tweet — see below)

```
We're building OKR Monitor — a Friday brief that tells you which OKRs are on track, which are drifting, and which work actually moved them.

Open repo: github.com/alochemes/okr-monitor
Apply for design partner: okrmonitor.com

5 slots open. Reply if interested.
```

---

## 4. Facebook — page setup (low priority)

Create the page but don't invest beyond setup. It's for brand consistency and SEO (Facebook pages rank well for brand-name searches).

### Page name
```
OKR Monitor
```

### Category
```
Software Company
```

### Short description (155 char max)
```
The Friday brief that connects your OKRs to the work that actually happens. Apply for design partner → okrmonitor.com
```

### Long description (same as LinkedIn About, abbreviated to 500 chars if needed)

### Profile photo + cover
- **Profile:** 170 × 170 px display, upload at 360 × 360 px. The square logo lock-up.
- **Cover:** 851 × 315 px desktop, 640 × 360 px mobile. Same wedge sentence editorial treatment.

### CTA button
"Sign Up" → linked to `okrmonitor.com#waitlist`.

---

## 5. Launch sequence — the first 5 posts

### Post 1 — LinkedIn personal (long-form, ~600 words)

**Title:** "Why I'm building OKR Monitor (and why your OKRs are probably lying to you)"

This is the founder essay. The structure I'd write to:

- **Hook:** "Last quarter, my friend's company missed their headline OKR. The post-mortem was the most honest writing they did all year. The drift was visible in week 3. They didn't see it until week 11."
- **The pattern:** Why this happens — OKR doc and work-in-tools are two different documents.
- **The product:** What we built — the Friday brief.
- **The dogfood:** We're our own first customer; here's the GitHub repo.
- **The ask:** "5 design partner slots open. If you've ever played telephone on a Monday to find out if your OKRs are real, I'd love a 30-min conversation. alochemes@gmail.com or apply at okrmonitor.com."

### Post 2 — Twitter thread (8–10 tweets)

Same essay, broken into a tweet thread. Use Typefully or Hypefury to draft + schedule.

### Post 3 — LinkedIn company page

Repost the essay (with credit to founder) on the company page 24 hrs after Post 1.

### Post 4 — LinkedIn personal (short, with image)

A screenshot of an actual Friday brief from the dogfood (one we generated against our own OKRs). Caption:

```
Here's the Friday brief OKR Monitor wrote about our own company yesterday.

3 KRs on track. 1 drifting. 1 off (we know — we're restating it).

We dogfood the product on the company building it. Every commit I push is mapped against a KR with calibrated confidence. Every Friday at 9 AM, the brief writes itself.

If your team has OKRs but your Monday standup is the autopsy — DM me.

(repo open: github.com/alochemes/okr-monitor)
```

### Post 5 — Twitter (the contrarian one)

```
The OKR doc and the work happening in your team's tools are two different documents.

By Q-end, the gap between them is the size of a quarter.

We close that gap by reading the work directly. Not a new dashboard — a Friday brief.

okrmonitor.com
```

---

## 6. Posting cadence (sustainable)

| Channel | Cadence | Who writes |
|---|---|---|
| LinkedIn personal (founder) | 2–3 posts / week | Founder (drafted by `content` and `founder_sales` agents, edited by founder) |
| LinkedIn company | 1 post / week | Cross-post + 1 original (drafted by `content` agent) |
| Twitter / X | 1 thread / week + 5 short tweets / week | Founder for threads; agent-drafted for short tweets |
| Facebook | Mirror LinkedIn, no original | Cross-post only |

Schedule with Typefully (Twitter + LinkedIn) or Buffer. Our `content` agent drafts the long-form; the operator approves; the post is scheduled.

---

## 7. What NOT to do

- ❌ No automated DM outreach. Period. The buyer can spot it instantly and we lose the conversation forever.
- ❌ No paid ads in the first 60 days. Earn the audience first.
- ❌ No reposting the same post across LinkedIn / Twitter / Facebook unmodified. Each platform has its own register; rewrite for each.
- ❌ No "5 lessons I learned from..." style listicles. Voice rules in `01_company/01_mission_and_voice.md` apply.
- ❌ No engagement-bait questions ("agree?" "thoughts?"). Make a claim; let the comments come.
- ❌ No emojis in posts (we never use them in copy except as data glyphs in product output).

---

## 8. Setup checklist (do these tonight, in order)

- [ ] LinkedIn personal — update headline, About, photo, cover, featured section
- [ ] LinkedIn company page — create, fill in tagline + about + logo + cover, set CTA
- [ ] Twitter — claim handle, set bio + header, pin first tweet
- [ ] Buffer / Typefully account — connect LinkedIn + Twitter for scheduling
- [ ] Facebook — create page (low priority — 10 min, then leave it)
- [ ] Schedule launch sequence (Post 1 → Post 5) over the next 2 weeks
- [ ] Add the social URLs to the landing page footer (`web/components/WaitlistFooter.tsx` — currently has placeholder `#` for LinkedIn)

When the URLs exist, send them and the agents can start linking to them in outbound copy.
