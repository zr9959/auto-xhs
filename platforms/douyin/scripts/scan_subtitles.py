#!/usr/bin/env python3
"""字幕敏感扫描：中英双扫的「扫」这一步。

用法：
    python3 scan_subtitles.py --srt 字幕.srt --wordlist 词库.txt
    python3 scan_subtitles.py --text "要扫的一段话" --wordlist 词库.txt

词库格式：一行一个词或短语，# 开头的是注释行。词库文件自己填——
仓库里只带格式模板（sensitive-words.template.txt），不带任何现成词表。
命中 = 原文里逐字出现该词（英文不区分大小写）；谐音、拆字、拼音首字母、
全角圈字等变体形态要另外写进词库才算命中，脚本不猜变体。

退出码：0 没命中，1 有命中，2 用法或文件不对。
"""

import argparse
import re
import sys
from pathlib import Path


def strip_srt(text):
    lines = []
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln or ln.isdigit():
            continue
        if re.match(r"\d\d:\d\d:\d\d[,.]\d+\s*-->", ln):
            continue
        lines.append(re.sub(r"<[^>]+>", "", ln))
    return "\n".join(lines)


def load_wordlist(path):
    words = []
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            words.append(ln)
    return words


def main():
    ap = argparse.ArgumentParser(description="字幕敏感扫描")
    ap.add_argument("--srt")
    ap.add_argument("--text")
    ap.add_argument("--wordlist", required=True)
    args = ap.parse_args()
    if bool(args.srt) == bool(args.text):
        print("二选一：--srt 传字幕文件，或 --text 传一段话", file=sys.stderr)
        return 2
    wl = Path(args.wordlist)
    if not wl.is_file():
        print(f"找不到词库：{wl}", file=sys.stderr)
        return 2
    words = load_wordlist(wl)
    if not words:
        print("词库是空的（只有注释行），先填词再扫")
        return 0
    if args.srt:
        sp = Path(args.srt)
        if not sp.is_file():
            print(f"找不到字幕：{sp}", file=sys.stderr)
            return 2
        body = strip_srt(sp.read_text(encoding="utf-8-sig"))
    else:
        body = args.text
    hits = []
    lowered = body.lower()
    for w in words:
        if w.lower() in lowered:
            hits.append(w)
    if not hits:
        print(f"扫完：没命中（原文 {len(body)} 字，词库 {len(words)} 条）")
        return 0
    print(f"扫完：命中 {len(hits)} 条：{', '.join(hits)}")
    print("命中即整条弃用，不许删词、打码、剪段挽救（见模块 README 四道闸）")
    return 1


if __name__ == "__main__":
    sys.exit(main())
