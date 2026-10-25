#!/usr/bin/env python3
"""Pre-post check for X: run through the module README's writing rules item by item.

Usage:
    python3 check_post.py --text "post text"
    python3 check_post.py --file draft.txt
    python3 check_post.py --text "post text" --kind reply   # replies use a stricter rule

Checks (FAIL = hard rule, WARN = heads-up):
  FAIL  banned words (delve, moreover, furthermore, in conclusion, it's worth noting,
        overused game-changer, not just X, but Y parallelism, a CTA at the end of every post)
  FAIL  Unicode bold (Mathematical Alphanumeric Symbols, U+1D400–U+1D7FF)
  FAIL  templated thread symbols (the full 🧵👇 set)
  WARN  more than 2 hashtags (standard 0–1)
  WARN  more than 2 emoji (standard 0–2, mostly at sentence ends)
  WARN  fewer than 2 concrete numbers (main-line standard: ≥2 concrete numbers + one clear conclusion)
  WARN  links in the main text (free accounts put links in self-replies only, not the main text)
  WARN  reply over 30 words (reply median is about 10 words; only checked with --kind reply)

Exit code: 1 if any FAIL, else 0.
"""

import argparse
import re
import sys

BANNED = [
    "delve", "moreover", "furthermore", "in conclusion",
    "it's worth noting", "it is worth noting", "game-changer", "game changer",
]
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]"
    "|[\u2600-\u27BF]"
)


def report(results, status, name, detail):
    results.append(status)
    print(f"[{status}] {name}: {detail}")


def main():
    ap = argparse.ArgumentParser(description="Pre-post check for X")
    ap.add_argument("--text")
    ap.add_argument("--file")
    ap.add_argument("--kind", choices=["post", "reply"], default="post")
    args = ap.parse_args()
    if bool(args.text) == bool(args.file):
        print("Pick one: --text for post text, or --file for a draft file", file=sys.stderr)
        return 2
    text = args.text if args.text else open(args.file, encoding="utf-8").read()
    text = text.strip()
    if not text:
        print("Post text is empty", file=sys.stderr)
        return 2
    results = []
    low = text.lower()

    found = [w for w in BANNED if w in low]
    # "not just X, but Y" must be a parallel in one sentence: X is usually just a few words, so if but sits
    # more than 40 characters after not just, it isn't that construction — otherwise any but in a long post would false-alarm.
    if re.search(r"not just\b.{0,40}?\bbut\b", low):
        found.append("not just X, but Y parallelism")
    if found:
        report(results, "FAIL", "Banned words", "Hit: " + ", ".join(found))
    else:
        report(results, "PASS", "Banned words", "No banned words hit")

    bold = [ch for ch in text if 0x1D400 <= ord(ch) <= 0x1D7FF]
    if bold:
        report(results, "FAIL", "Unicode bold", "Mathematical Alphanumeric Symbols bold used — switch back to plain text")
    else:
        report(results, "PASS", "Unicode bold", "Not used")

    if "🧵" in text and "👇" in text:
        report(results, "FAIL", "Templated thread symbols", "The full 🧵👇 set reads templated — drop it")
    else:
        report(results, "PASS", "Templated thread symbols", "Full template set not used")

    tags = re.findall(r"#\w+", text)
    if len(tags) > 2:
        report(results, "WARN", "hashtag", f"{len(tags)} — over the max of 2 (standard 0–1)")
    else:
        report(results, "PASS", "hashtag", f"{len(tags)}")

    emojis = EMOJI_RE.findall(text)
    if len(emojis) > 2:
        report(results, "WARN", "emoji", f"{len(emojis)} — over the max of 2")
    else:
        report(results, "PASS", "emoji", f"{len(emojis)}")

    nums = re.findall(r"\d[\d,.]*", text)
    if args.kind == "post" and len(nums) < 2:
        report(results, "WARN", "Concrete numbers", f"Only {len(nums)} number{'s' if len(nums) != 1 else ''} found — main-line standard is ≥2 concrete numbers")
    else:
        report(results, "PASS", "Concrete numbers", f"{len(nums)} number{'s' if len(nums) != 1 else ''} found")

    if re.search(r"https?://", text):
        report(results, "WARN", "Links", "Links in the main text; free accounts put links in self-replies only, not the main text")
    else:
        report(results, "PASS", "Links", "No links in the main text")

    # Chinese counts by character, English by word — otherwise a Chinese post split on spaces is always just a few "words" and the length check never fires.
    words = (len(re.findall(r"[A-Za-z0-9]+", text))
             + len(re.findall(r"[\u4e00-\u9fff]", text)))
    if args.kind == "reply" and words > 30:
        report(results, "WARN", "Reply length", f"{words} words/chars — reply median is about 10 words, too long; cut it to one concrete point")
    else:
        report(results, "PASS", "Length", f"{words} words/chars")

    fails = results.count("FAIL")
    warns = results.count("WARN")
    print(f"Summary: {fails} FAIL, {warns} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
