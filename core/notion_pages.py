"""Push a markdown document into Notion as a sub-page.

The OKR seed (`core/notion_okr.py`) operates on databases. This module
operates on free-form pages — what we want when pushing the intake
questionnaire, the 5-in-5 worksheet, the OKR Health Check, etc.

Limited markdown converter on purpose: headings (1-3), paragraphs,
bulleted/numbered lists, blockquotes, horizontal rules, code fences,
tables (rendered as a Notion code block fallback). Inline supports
**bold**, *italic*, `code`, and [text](url). Anything fancier passes
through as plain text.

Notion caps page-children at 100 blocks per request, so the implementation
chunks long pages.
"""

from __future__ import annotations

import re
from typing import Any

from core import notion_client


# ---------- Inline rich-text -----------------------------------------------

_INLINE_RE = re.compile(
    r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[[^\]]+\]\([^)]+\))"
)


def _rich_text(text: str) -> list[dict[str, Any]]:
    """Convert inline markdown to Notion rich_text segments. Each segment is
    capped at Notion's 2000-char limit per element."""
    if not text:
        return []
    out: list[dict[str, Any]] = []
    pos = 0
    for m in _INLINE_RE.finditer(text):
        if m.start() > pos:
            out.append({"type": "text",
                        "text": {"content": text[pos:m.start()][:2000]}})
        tok = m.group(0)
        if tok.startswith("**") and tok.endswith("**"):
            out.append({"type": "text", "text": {"content": tok[2:-2][:2000]},
                        "annotations": {"bold": True}})
        elif tok.startswith("*") and tok.endswith("*"):
            out.append({"type": "text", "text": {"content": tok[1:-1][:2000]},
                        "annotations": {"italic": True}})
        elif tok.startswith("`") and tok.endswith("`"):
            out.append({"type": "text", "text": {"content": tok[1:-1][:2000]},
                        "annotations": {"code": True}})
        elif (lm := re.match(r"\[([^\]]+)\]\(([^)]+)\)", tok)):
            out.append({"type": "text",
                        "text": {"content": lm.group(1)[:2000],
                                 "link": {"url": lm.group(2)}}})
        pos = m.end()
    if pos < len(text):
        out.append({"type": "text", "text": {"content": text[pos:][:2000]}})
    return out


# ---------- Block builders -------------------------------------------------

def _block(kind: str, text: str | None = None,
           rich: list[dict] | None = None,
           extra: dict | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"rich_text": rich if rich is not None
                               else _rich_text(text or "")}
    if extra:
        payload.update(extra)
    return {"object": "block", "type": kind, kind: payload}


def _divider() -> dict[str, Any]:
    return {"object": "block", "type": "divider", "divider": {}}


def _code(content: str, language: str = "plain text") -> dict[str, Any]:
    return {
        "object": "block", "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": content[:2000]}}],
            "language": (language or "plain text").lower() or "plain text",
        },
    }


# ---------- Markdown → blocks ----------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")
_BULLET_RE = re.compile(r"^[-*]\s+(.*)$")
_NUMBERED_RE = re.compile(r"^\d+\.\s+(.*)$")
_QUOTE_RE = re.compile(r"^>\s?(.*)$")
_HR_RE = re.compile(r"^---+\s*$")
_CODE_FENCE_RE = re.compile(r"^```\s*(\w+)?\s*$")
_TABLE_ROW_RE = re.compile(r"^\|.*\|\s*$")


def md_to_blocks(md: str) -> list[dict[str, Any]]:
    """Convert a markdown string to Notion blocks. Tables are rendered as a
    plain-text code block (Notion's table API takes a separate request that
    isn't worth the complexity for our docs)."""
    blocks: list[dict] = []
    lines = md.splitlines()
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]

        # Code fence
        m = _CODE_FENCE_RE.match(ln)
        if m:
            lang = m.group(1) or "plain text"
            buf: list[str] = []
            i += 1
            while i < n and not _CODE_FENCE_RE.match(lines[i]):
                buf.append(lines[i])
                i += 1
            i += 1    # skip closing fence
            blocks.append(_code("\n".join(buf), lang))
            continue

        # Markdown table — render as a fenced code-block fallback. Notion
        # supports tables natively but the API is verbose and our docs
        # don't critically need it; readability is preserved as code.
        if _TABLE_ROW_RE.match(ln):
            tbl: list[str] = [ln]
            j = i + 1
            while j < n and _TABLE_ROW_RE.match(lines[j]):
                tbl.append(lines[j])
                j += 1
            blocks.append(_code("\n".join(tbl), "plain text"))
            i = j
            continue

        # Heading
        if (m := _HEADING_RE.match(ln)):
            level = len(m.group(1))
            kind = {1: "heading_1", 2: "heading_2", 3: "heading_3"}[min(level, 3)]
            blocks.append(_block(kind, m.group(2)))
            i += 1
            continue

        # Horizontal rule
        if _HR_RE.match(ln):
            blocks.append(_divider())
            i += 1
            continue

        # Bullet
        if (m := _BULLET_RE.match(ln)):
            blocks.append(_block("bulleted_list_item", m.group(1)))
            i += 1
            continue

        # Numbered
        if (m := _NUMBERED_RE.match(ln)):
            blocks.append(_block("numbered_list_item", m.group(1)))
            i += 1
            continue

        # Quote
        if (m := _QUOTE_RE.match(ln)):
            blocks.append(_block("quote", m.group(1)))
            i += 1
            continue

        # Blank — skip
        if not ln.strip():
            i += 1
            continue

        # Paragraph (greedy across continuation lines)
        para = [ln]
        j = i + 1
        while j < n and lines[j].strip() and not (
            _HEADING_RE.match(lines[j])
            or _BULLET_RE.match(lines[j])
            or _NUMBERED_RE.match(lines[j])
            or _QUOTE_RE.match(lines[j])
            or _CODE_FENCE_RE.match(lines[j])
            or _HR_RE.match(lines[j])
            or _TABLE_ROW_RE.match(lines[j])
        ):
            para.append(lines[j])
            j += 1
        blocks.append(_block("paragraph", " ".join(para)))
        i = j
    return blocks


# ---------- Page operations ------------------------------------------------

def create_subpage(*, parent_page_id: str, title: str,
                    blocks: list[dict[str, Any]]) -> dict[str, Any]:
    """Create a Notion sub-page under `parent_page_id`. Page title is set
    via the standard `title` property. Children are chunked at 100 blocks
    (Notion's per-request limit)."""
    body = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "properties": {
            "title": {"title": [{"type": "text",
                                  "text": {"content": title[:2000]}}]},
        },
        "children": blocks[:100],
    }
    page = notion_client.post("/pages", body)
    page_id = page["id"]
    for k in range(100, len(blocks), 100):
        notion_client.patch(
            f"/blocks/{page_id}/children",
            {"children": blocks[k:k + 100]},
        )
    return page


def push_markdown_subpage(*, parent_page_id: str, title: str,
                           markdown: str) -> dict[str, Any]:
    """One-shot: parse `markdown` → Notion blocks → create sub-page.
    Returns the Notion page object (id, url, etc.)."""
    return create_subpage(parent_page_id=parent_page_id, title=title,
                          blocks=md_to_blocks(markdown))
