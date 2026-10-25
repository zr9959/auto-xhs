#!/usr/bin/env python3
"""Subtitle sensitivity scan: the "scan" step of the bilingual Chinese-English scan.

Usage:
    python3 scan_subtitles.py --srt subtitles.srt --wordlist wordlist.txt
    python3 scan_subtitles.py --text "a passage to scan" --wordlist wordlist.txt

Wordlist format: one word or phrase per line; lines starting with # are comments. Fill in the wordlist yourself —
the repo only ships the format template (sensitive-words.template.txt), no ready-made wordlist.
A hit means the word appears in the text character for character (English is case-insensitive); homophones, split characters,
pinyin initials, full-width circled characters, and other variant forms only count if written into the wordlist — the script doesn't guess variants.

Exit codes: 0 no hit, 1 hit, 2 wrong usage or file problem.
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
    ap = argparse.ArgumentParser(description="Subtitle sensitivity scan")
    ap.add_argument("--srt")
    ap.add_argument("--text")
    ap.add_argument("--wordlist", required=True)
    args = ap.parse_args()
    if bool(args.srt) == bool(args.text):
        print("Pick one: --srt for a subtitle file, or --text for a passage", file=sys.stderr)
        return 2
    wl = Path(args.wordlist)
    if not wl.is_file():
        print(f"Wordlist not found: {wl}", file=sys.stderr)
        return 2
    words = load_wordlist(wl)
    if not words:
        print("Wordlist is empty (comment lines only) — fill in words first, then scan")
        return 0
    if args.srt:
        sp = Path(args.srt)
        if not sp.is_file():
            print(f"Subtitle file not found: {sp}", file=sys.stderr)
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
        print(f"Scan done: no hits (text {len(body)} chars, wordlist {len(words)} entries)")
        return 0
    print(f"Scan done: {len(hits)} hit{'s' if len(hits) != 1 else ''}: {', '.join(hits)}")
    print("A hit drops the whole clip — no deleting words, blurring, or cutting around it (see the module README's four gates)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
