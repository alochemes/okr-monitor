# content/blog/

Publishable long-form posts. Written in the OKR Monitor voice (see
`notion/01_company/01_mission_and_voice.md`). Each post is ~900–1,100
words, with a single anchor stat, one named anti-pattern, and one
proprietary frame. CTA at the bottom links to `/health-check`.

## Naming convention

`YYYY-MM-DD-slug.md` — date prefix is the **intended publish date**,
not the draft date. Slug matches the post URL.

## Front-matter

Each post has YAML front-matter:

```yaml
---
title: "..."
slug: "..."
date: YYYY-MM-DD
status: draft | scheduled | published
target_word_count: 1000
actual_word_count: 1010
seo_keywords: [...]
anchor_stat: "..."
named_anti_pattern: "..."
proprietary_frame: "..."
social_pull_quote: "..."
---
```

## Where to publish

Three target surfaces, in priority order:

1. **The company blog** — once we have one. For now, post to the founder's
   LinkedIn long-form (max ~3,000 words) with a "originally posted at..."
   pointing back here once the blog exists.
2. **Substack** — `okrmonitor.substack.com` for newsletter delivery and
   discoverability. Free tier is fine until ≥500 subscribers.
3. **LinkedIn long-form / Twitter thread** — re-cut from the post body,
   shorter and punchier per the social setup playbook
   (`notion/04_brand/01_social_media_setup.md`).

## Publication cadence

Per the GTM plan: **3 posts/week** in M3 (July 2026) onwards. Until
then, one polished post per week is enough — quality > volume, and
content debt is a real thing.

## Current drafts (May 2026)

| File | Title | Status |
|---|---|---|
| `2026-05-01-your-okrs-are-lying.md` | "Your OKRs are lying to you, and the standup is the autopsy" | draft (the wedge essay) |
| `2026-05-02-five-in-five.md` | "The 5-in-5: write your real Key Results in five minutes" | draft (markets the playbook) |
| `2026-05-03-two-different-documents.md` | "Your OKR doc and your team's actual work are two different documents" | draft (the alignment-attention frame) |

These three are sequenced as a thematic mini-series — they reinforce
each other if read in order, and they each stand alone if encountered
individually via SEO. Publish on the dates above (M, T, W of the week
the landing page goes live) for maximum compounding.

## Edit before publishing

The drafts above are first-pass. **Read each aloud** before publishing —
voice tone is everything. Things to specifically check:

- Zero exclamation marks. Search and replace.
- No "AI-powered", "leverage", "best-in-class", "revolutionary",
  "game-changer", "disrupt", "delight" (verb).
- The CTA at the bottom matches the current landing page URL.
- The anchor stat is something you would defend if challenged.
