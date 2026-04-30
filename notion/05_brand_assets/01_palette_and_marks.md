# Brand assets — palette, type, marks

> The visual system in one place. If you're producing anything new (a one-pager, a deck, a tradeshow banner, a podcast cover), start here.

---

## Color palette

The system has **one accent color**. Anything more = noise.

| Role | Hex | Where it shows up |
|---|---|---|
| **Paper** (background) | `#FAF7F2` | Page background everywhere. Warm, slightly cream. |
| **Paper-deep** | `#F2EDE4` | Secondary background — for muted sections. |
| **Ink** (text) | `#0F0E0C` | Body text, headlines, primary buttons. |
| **Ink-soft** | `#1F1D1A` | Secondary text, borders that should read as "structural." |
| **Muted** | `#6B6862` | Captions, labels, supporting text. |
| **Rule** | `#D9D2C4` | Hairline rules between sections, table borders. |
| **Persimmon** (the only accent) | `#C73A14` | Highlight, CTA hover, links, the brand dot, drop caps. |
| **Persimmon-dark** | `#A52E0F` | Persimmon hover state. |
| Verdict — on track (green) | `#1F6F44` | Product output only — verdict glyphs in the brief. |
| Verdict — drifting (amber) | `#A66A00` | Product output only. |
| Verdict — off (red) | `#9C2A1A` | Product output only. |

**Forbidden colors** (do not introduce, ever):
- Any blue (over-used in B2B SaaS — every competitor is blue).
- Any purple gradient.
- Any neon, any glow effect, any drop shadow that isn't structural.

---

## Type system

Three families. Each with one job.

| Family | Use | License |
|---|---|---|
| **Fraunces** | Display — headlines, masthead, brand wordmark. | Open Font License (Google Fonts). |
| **Inter** | Body — paragraphs, navigation, labels, UI. | Open Font License (Google Fonts). |
| **JetBrains Mono** | Data — code, KR IDs, commit titles, monospaced numbers. | Apache 2.0 (Google Fonts). |

**Web:** loaded via `next/font/google` in `web/app/layout.tsx`. **Print/social:** download from Google Fonts and self-host with the same weights (400/500/600/700).

**Forbidden type choices:** Roboto, Arial, Montserrat, Open Sans, Helvetica Neue. They are technically fine and are the reason most B2B SaaS landing pages look the same.

---

## Logo files (in `web/public/`)

| File | Dimensions | Use |
|---|---|---|
| `logo.svg` | 320 × 64 | Wordmark — the standard logo. Use everywhere there's room. |
| `logo-icon.svg` | 64 × 64 | Square mark — favicon, app icons, social profile photos, anywhere the wordmark won't fit. The "OM" monogram with the persimmon dot. |
| `og.svg` | 1200 × 630 | Open Graph image — shows when the landing URL is shared on LinkedIn / Twitter / Slack. SVG is included; convert to PNG before uploading to those platforms (most don't render SVG previews). |

**Conversion to PNG (when needed):**
```bash
# Using rsvg-convert (sudo apt install librsvg2-bin) or Inkscape
rsvg-convert -w 1200 -h 630 web/public/og.svg > web/public/og.png

# Or in the browser: open the SVG and screenshot it
```

For the favicon, modern browsers accept SVG directly. To support older browsers, also export `favicon.ico` (16 × 16 + 32 × 32 PNG bundled).

---

## Photography & illustration policy

**No photography.** No stock photos. No team-around-a-laptop, no abstract-business-people. They cheapen everything.

**No illustration.** No vector hero scenes, no character mascots, no "isometric office" art. Same reason.

**The visual moment is typography + the product output itself.** The hero asset on the landing page is a styled mock of the actual Friday brief — not a screenshot, not an illustration. The brief IS the illustration.

If you ever need a "visual" for an article cover or social post, the answer is: a piece of typography from the post itself, set in Fraunces, on warm paper, with the persimmon dot as a single accent. Open the OG SVG and modify it.

---

## Logo lockup rules

- Always render the wordmark with the persimmon dot. The dot is the brand. Without it, the wordmark is just a name.
- The dot sits to the **right of the wordmark**, on the **baseline**, sized to roughly the height of the lowercase letters.
- Minimum clear space around the lockup: equal to the height of the dot.
- On dark backgrounds, the wordmark becomes paper-color (`#FAF7F2`) and the dot stays persimmon.
- Never recolor the dot to anything other than persimmon. Not white, not gray, not "for accessibility."

---

## Social profile sizing reference

| Platform | Profile photo | Cover/header |
|---|---|---|
| LinkedIn personal | 400 × 400 (display 200 × 200) | 1584 × 396 |
| LinkedIn company | 300 × 300 (display 268 × 268) | 1128 × 191 |
| Twitter / X | 400 × 400 (display 200 × 200) | 1500 × 500 |
| Facebook | 360 × 360 (display 170 × 170) | 851 × 315 desktop, 640 × 360 mobile |
| Instagram (skip for now) | 320 × 320 | — |

For all profile photos: use `logo-icon.svg`, exported to PNG at the platform's required size.
For cover images: use a 16:5 (or 8:3) variant of the OG image — modify `og.svg` to the right aspect ratio, export PNG.

---

## Don't ship

- Gradient backgrounds of any kind
- Multi-color logos (we have one accent)
- Logo on a colored background that isn't paper or ink
- The wordmark stretched, condensed, italicized, or scaled non-uniformly
- The persimmon dot used as a bullet point in body text (it's a brand element, not a typographic element — use a regular bullet for lists)
- Comic Sans, marketing-cliché serif, or any "AI-generated logo" output
- Any social post lacking the persimmon accent — it's how readers visually identify our content in feeds

---

## Source files

The Fraunces variable font, the Inter font, and JetBrains Mono are all on Google Fonts and load via `next/font/google` for web. For non-web use (Keynote, Figma, print), download from:

- Fraunces: https://fonts.google.com/specimen/Fraunces
- Inter: https://fonts.google.com/specimen/Inter
- JetBrains Mono: https://fonts.google.com/specimen/JetBrains+Mono

For Figma — install all three via the Google Fonts plugin, then your Figma source files render the same as the web.
