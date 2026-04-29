"""Push the Notion KB markdown directory to a real Notion workspace.

This is the bridge between this repo (source of truth, version-controlled)
and Notion (the team's reading surface). It walks `notion/` recursively,
creates child pages under a configured parent, and converts each markdown
file into Notion blocks.

v0 scope (intentional):
  - Creates pages and writes content. Does NOT yet maintain a sync map
    (re-running creates duplicate pages). Run once for the initial import,
    then either edit in Notion directly OR delete the imported pages and
    re-import after meaningful repo changes.
  - Supports headings, paragraphs, lists, code blocks, blockquotes,
    horizontal rules, and links. Tables are converted to a code-block
    fallback (Notion's table API is verbose; we'll add a real converter
    when a doc actually needs it).
  - Mermaid blocks become a Notion `code` block with language=mermaid —
    Notion renders them inline.

Required env (in .env or shell):
  NOTION_API_KEY        — internal integration token (starts with `secret_` or `ntn_`)
  NOTION_PARENT_PAGE_ID — id of the parent page to create children under
                          (32-char hex; from the page URL after the title)

Usage:
  python scripts/notion_import.py             # dry-run: prints what it would create
  python scripts/notion_import.py --apply     # actually creates pages
  python scripts/notion_import.py --apply --root notion/02_product   # subset

If env is missing, the script falls back to dry-run mode and prints setup
instructions. No crash, no silent no-op.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass


NOTION_VERSION = "2022-06-28"
NOTION_API = "https://api.notion.com/v1"


# ---------- Notion API helpers ------------------------------------------------


def _request(
    *, method: str, path: str, token: str, body: dict | None = None
) -> dict:
    url = f"{NOTION_API}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Notion-Version", NOTION_VERSION)
    req.add_header("Content-Type", "application/json")
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _create_page(*, token: str, parent_id: str, title: str, blocks: list[dict]) -> dict:
    body = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title[:200]}}]}
        },
        # Notion caps children at 100 per request; chunk if needed.
        "children": blocks[:100],
    }
    page = _request(method="POST", path="/pages", token=token, body=body)
    page_id = page["id"]
    # Append the rest in chunks of 100.
    for i in range(100, len(blocks), 100):
        _request(
            method="PATCH",
            path=f"/blocks/{page_id}/children",
            token=token,
            body={"children": blocks[i : i + 100]},
        )
    return page


# ---------- Markdown -> Notion blocks (small, focused converter) -----------


_HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")
_LIST_RE = re.compile(r"^[-*]\s+(.*)$")
_NUMBERED_RE = re.compile(r"^\d+\.\s+(.*)$")
_QUOTE_RE = re.compile(r"^>\s?(.*)$")
_HR_RE = re.compile(r"^---+\s*$")
_CODE_FENCE_RE = re.compile(r"^```\s*(\w+)?\s*$")


def _rich_text(text: str) -> list[dict]:
    """Convert markdown inline syntax to Notion rich_text. Handles **bold**,
    `code`, and [text](url). Keeps it simple — anything we don't parse
    becomes plain text."""
    if not text:
        return []
    # Notion rich_text caps each segment at 2000 chars. Truncate defensively.
    text = text[:2000]
    out: list[dict] = []
    # Tokenize: split keeping delimiters.
    tokens = re.split(r"(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))", text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            out.append({
                "type": "text",
                "text": {"content": tok[2:-2]},
                "annotations": {"bold": True},
            })
        elif tok.startswith("`") and tok.endswith("`"):
            out.append({
                "type": "text",
                "text": {"content": tok[1:-1]},
                "annotations": {"code": True},
            })
        elif (m := re.match(r"\[([^\]]+)\]\(([^)]+)\)", tok)):
            out.append({
                "type": "text",
                "text": {"content": m.group(1), "link": {"url": m.group(2)}},
            })
        else:
            out.append({"type": "text", "text": {"content": tok}})
    return out


def _block_paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": _rich_text(text)},
    }


def _block_heading(text: str, level: int) -> dict:
    key = {1: "heading_1", 2: "heading_2", 3: "heading_3"}[min(level, 3)]
    return {
        "object": "block",
        "type": key,
        key: {"rich_text": _rich_text(text)},
    }


def _block_list(text: str, *, numbered: bool = False) -> dict:
    key = "numbered_list_item" if numbered else "bulleted_list_item"
    return {
        "object": "block",
        "type": key,
        key: {"rich_text": _rich_text(text)},
    }


def _block_quote(text: str) -> dict:
    return {
        "object": "block",
        "type": "quote",
        "quote": {"rich_text": _rich_text(text)},
    }


def _block_divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def _block_code(content: str, language: str = "plain text") -> dict:
    # Notion has a fixed enum of supported languages; fall back to plain text
    # for unknown values (mermaid IS in the enum).
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": content[:2000]}}],
            "language": language or "plain text",
        },
    }


def md_to_blocks(md: str) -> list[dict]:
    """Convert a markdown string to Notion blocks. Limited but covers our
    actual usage in `notion/`."""
    blocks: list[dict] = []
    lines = md.splitlines()
    i = 0
    in_code = False
    code_lang = "plain text"
    code_buf: list[str] = []

    def flush_code():
        nonlocal in_code, code_buf, code_lang
        if in_code and code_buf:
            blocks.append(_block_code("\n".join(code_buf), code_lang))
        in_code = False
        code_buf = []
        code_lang = "plain text"

    while i < len(lines):
        ln = lines[i]

        # Code fences
        m = _CODE_FENCE_RE.match(ln)
        if m:
            if in_code:
                flush_code()
            else:
                in_code = True
                code_lang = (m.group(1) or "plain text").lower()
                # Notion supports "mermaid" as of 2024.
            i += 1
            continue
        if in_code:
            code_buf.append(ln)
            i += 1
            continue

        # Heading
        if (m := _HEADING_RE.match(ln)):
            blocks.append(_block_heading(m.group(2), len(m.group(1))))
            i += 1
            continue

        # Horizontal rule
        if _HR_RE.match(ln):
            blocks.append(_block_divider())
            i += 1
            continue

        # Bulleted list
        if (m := _LIST_RE.match(ln)):
            blocks.append(_block_list(m.group(1)))
            i += 1
            continue

        # Numbered list
        if (m := _NUMBERED_RE.match(ln)):
            blocks.append(_block_list(m.group(1), numbered=True))
            i += 1
            continue

        # Quote
        if (m := _QUOTE_RE.match(ln)):
            blocks.append(_block_quote(m.group(1)))
            i += 1
            continue

        # Blank line — skip
        if not ln.strip():
            i += 1
            continue

        # Plain paragraph (consume continuation lines)
        para = [ln]
        j = i + 1
        while j < len(lines) and lines[j].strip() and not (
            _HEADING_RE.match(lines[j])
            or _LIST_RE.match(lines[j])
            or _NUMBERED_RE.match(lines[j])
            or _QUOTE_RE.match(lines[j])
            or _CODE_FENCE_RE.match(lines[j])
            or _HR_RE.match(lines[j])
        ):
            para.append(lines[j])
            j += 1
        blocks.append(_block_paragraph(" ".join(para)))
        i = j

    if in_code:
        flush_code()

    return blocks


# ---------- File walker ----------------------------------------------------


def _title_from_md(path: Path) -> str:
    """First H1 in the file, or filename without extension."""
    try:
        for ln in path.read_text(encoding="utf-8").splitlines()[:30]:
            if (m := _HEADING_RE.match(ln)) and len(m.group(1)) == 1:
                return m.group(2).strip()
    except OSError:
        pass
    name = path.stem
    # Strip leading numeric prefix like "01_"
    return re.sub(r"^\d+_", "", name).replace("_", " ").title()


def _gather(root: Path) -> list[Path]:
    out = sorted(p for p in root.rglob("*.md") if p.is_file())
    return out


# ---------- Main ------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="notion", help="Directory to import from.")
    parser.add_argument("--apply", action="store_true", help="Actually call the Notion API. Without this, dry-run.")
    args = parser.parse_args()

    root = (ROOT / args.root).resolve()
    if not root.exists():
        print(f"Error: {root} does not exist.", file=sys.stderr)
        return 1

    files = _gather(root)
    print(f"Found {len(files)} markdown files under {root.relative_to(ROOT)}/")

    token = os.environ.get("NOTION_API_KEY", "").strip()
    parent_id = os.environ.get("NOTION_PARENT_PAGE_ID", "").strip()

    if not token or not parent_id:
        print("\nNotion credentials not set in env.")
        print("To enable real import, do this:")
        print("  1. https://www.notion.so/my-integrations -> New integration -> 'OKR Monitor KB'.")
        print("     Capabilities: Read content, Insert content, Update content.")
        print("     Copy the secret token (starts with `secret_` or `ntn_`).")
        print("  2. Create a Notion page that will hold the KB (e.g. 'OKR Monitor / Operations').")
        print("  3. On that page, click ... -> Connections -> Add -> 'OKR Monitor KB'.")
        print("  4. Copy the page id from the URL — the 32-char hex after the title.")
        print("  5. Add to .env:")
        print("       NOTION_API_KEY=secret_...")
        print("       NOTION_PARENT_PAGE_ID=abc123def456...")
        print("  6. Re-run: python scripts/notion_import.py --apply")
        print("\nDry-run preview:")
        for f in files:
            rel = f.relative_to(ROOT).as_posix()
            title = _title_from_md(f)
            blocks = md_to_blocks(f.read_text(encoding="utf-8"))
            print(f"  - {rel} -> '{title}' ({len(blocks)} blocks)")
        return 0

    if not args.apply:
        print("\nDry-run (use --apply to actually create pages):")
        for f in files:
            rel = f.relative_to(ROOT).as_posix()
            title = _title_from_md(f)
            blocks = md_to_blocks(f.read_text(encoding="utf-8"))
            print(f"  - {rel} -> '{title}' ({len(blocks)} blocks)")
        return 0

    # Apply.
    created = 0
    failed = 0
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        title = _title_from_md(f)
        blocks = md_to_blocks(f.read_text(encoding="utf-8"))
        try:
            page = _create_page(
                token=token, parent_id=parent_id, title=title, blocks=blocks,
            )
            print(f"  [ok]{rel} -> {page.get('url', page['id'])}")
            created += 1
        except (HTTPError, URLError) as exc:
            print(f"  [fail]{rel} — {exc}", file=sys.stderr)
            failed += 1

    print(f"\nDone. Created: {created}, Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
