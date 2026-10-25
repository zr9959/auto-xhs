#!/usr/bin/env python3
"""Turn a Markdown draft into the JSON package the official-account draft-box API wants (offline, no API calls).

Usage:
    python3 build_draft.py --md draft.md --title "Title" --out draft.json
    python3 build_draft.py --md draft.md --title "Title" --author "Author" \\
        --digest "Summary" --cover-media-id MEDIA_ID --out draft.json

Markdown to HTML covers only the common cases: # → h2, ## → h3, ### → h4,
- lists → ul/li, **bold** → strong, paragraphs → p. Adjust complex layouts in the web backend.
The output JSON is the articles array level the draft-box API takes (see the module README).
Real API calls use mp_api.py in the same directory; this script touches no network and no credentials.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path


def md_to_html(md):
    out = []
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def inline(s):
        s = html.escape(s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
        return s

    for ln in md.splitlines():
        s = ln.strip()
        if not s:
            close_list()
            continue
        m = re.match(r"^(#{1,3})\s+(.+)", s)
        if m:
            close_list()
            level = {"#": 2, "##": 3, "###": 4}[m.group(1)]
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue
        if s.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(s[2:])}</li>")
            continue
        close_list()
        out.append(f"<p>{inline(s)}</p>")
    close_list()
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Markdown to official-account draft JSON package")
    ap.add_argument("--md", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--author", default="")
    ap.add_argument("--digest", default="")
    ap.add_argument("--cover-media-id", default="")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    md_path = Path(args.md)
    if not md_path.is_file():
        print(f"Draft not found: {md_path}", file=sys.stderr)
        return 2
    md = md_path.read_text(encoding="utf-8")
    article = {
        "title": args.title,
        "author": args.author,
        "digest": args.digest,
        "content": md_to_html(md),
        "thumb_media_id": args.cover_media_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    }
    payload = {"articles": [article]}
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Draft package written: {out_path} (title: {args.title}, body {len(article['content'])} chars)")
    print("Next: mp_api.py --action draft-add --draft-json draft.json (dry-run first to look it over)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
