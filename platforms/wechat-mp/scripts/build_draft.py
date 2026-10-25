#!/usr/bin/env python3
"""把 Markdown 稿子转成公众号草稿箱接口要的 JSON 包（离线，不调接口）。

用法：
    python3 build_draft.py --md 稿子.md --title "标题" --out draft.json
    python3 build_draft.py --md 稿子.md --title "标题" --author "作者" \\
        --digest "摘要" --cover-media-id MEDIA_ID --out draft.json

Markdown 转 HTML 只做最常用的几种：# → h2、## → h3、### → h4、
- 列表 → ul/li、**粗体** → strong、段落 → p。复杂排版请在网页后台再调。
输出的 JSON 就是草稿箱接口 articles 数组那一层（见模块 README）。
真正调接口用同目录的 mp_api.py；本脚本不碰网络、不碰凭据。
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
    ap = argparse.ArgumentParser(description="Markdown 转公众号草稿 JSON 包")
    ap.add_argument("--md", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--author", default="")
    ap.add_argument("--digest", default="")
    ap.add_argument("--cover-media-id", default="")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    md_path = Path(args.md)
    if not md_path.is_file():
        print(f"找不到稿子：{md_path}", file=sys.stderr)
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
    print(f"草稿包已生成：{out_path}（标题：{args.title}，正文 {len(article['content'])} 字符）")
    print("下一步：mp_api.py --action draft-add --draft-json draft.json（先 --dry-run 看一遍）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
