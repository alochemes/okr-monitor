# OKR Monitor — Notion Knowledge Base

> The company knowledge base. Every doc here is **drag-importable into Notion** as a page (Notion → Settings → Import → Markdown). Together they form the operating manual we dogfood internally and the playbook our customers receive at pilot kickoff.

---

## How to import this into Notion

1. In Notion, create a top-level page called **OKR Monitor / Operations**.
2. Open it → click `···` (top-right) → **Import** → **Markdown / CSV**.
3. Select the entire `notion/` directory from this repo.
4. Notion preserves the folder structure as nested pages.
5. After import, optionally run `python scripts/notion_import.py --sync` to keep Notion in sync with this repo automatically (requires `NOTION_API_KEY` + parent page id in `.env`). See `scripts/notion_import.py` for setup.

This repo remains the **source of truth**. Notion is a read surface for the team. Edits go through PRs, not Notion.

---

## Structure

### 01 / Company
- [Mission, voice, and brand](01_company/01_mission_and_voice.md)

### 02 / Product
- [How it works — full product runbook](02_product/01_how_it_works.md)
- [Daily / weekly cadence — what fires when](02_product/02_daily_weekly_cadence.md)

### 03 / Playbooks
- [Customer OKR + KPI framework (the big one — what we teach customers)](03_playbooks/01_customer_okr_kpi_framework.md)
- [Knowledge-base mining during onboarding](03_playbooks/02_kb_mining_during_onboarding.md)
- [60-day pilot kickoff](03_playbooks/03_pilot_kickoff_60_days.md)

### 04 / Brand
- [Social media setup — Twitter, LinkedIn, Facebook](04_brand/01_social_media_setup.md)

---

## Why this exists

Two reasons. **One:** we dogfood the product on the company building it, which means OUR knowledge base is the first one OKR Monitor has to make sense of. If our `okr_mapper` agent can read the OKRs in `02_product/...` and tie our work events to them, the product works. **Two:** roughly half of our pilots arrive with OKRs that need cleanup before they can be measured against. The customer-facing playbook in `03_playbooks/01` is the artifact we hand them on day one.

---

## Conventions

- Heading 1 (`#`) → Notion page title.
- Heading 2 (`##`) → Notion section.
- Numbered prefix on filenames (`01_`, `02_`) controls Notion sort order.
- Code blocks render in Notion with syntax highlighting.
- Cross-references use relative markdown links (Notion preserves them).

---

_Source: [github.com/alochemes/okr-monitor/tree/main/notion](https://github.com/alochemes/okr-monitor/tree/main/notion). Last refreshed: see commit log._
