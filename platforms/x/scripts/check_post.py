#!/usr/bin/env python3
"""X 发帖前检查：按模块 README 的写法规范逐项过。

用法：
    python3 check_post.py --text "帖子正文"
    python3 check_post.py --file draft.txt
    python3 check_post.py --text "帖子正文" --kind reply   # 回复用更严的口径

检查项（FAIL = 硬规矩，WARN = 提醒）：
  FAIL  禁用词（delve、moreover、furthermore、in conclusion、it's worth noting、
        滥用的 game-changer、not just X, but Y 排比、每帖结尾必 CTA）
  FAIL  Unicode 粗体（数学字母符号区 U+1D400–U+1D7FF）
  FAIL  模板化串帖符号（🧵👇 全套）
  WARN  hashtag 超过 2 个（标准 0–1 个）
  WARN  emoji 超过 2 个（标准 0–2 个，多放句尾）
  WARN  具体数少于 2 个（主线帖标准：≥2 个具体数 + 一个明确结论）
  WARN  正文里带链接（免费号链接只放自回复，正文不放）
  WARN  回复超过 30 词（回复中位约 10 词；只在 --kind reply 时判）

退出码：有 FAIL 为 1，否则 0。
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
    ap = argparse.ArgumentParser(description="X 发帖前检查")
    ap.add_argument("--text")
    ap.add_argument("--file")
    ap.add_argument("--kind", choices=["post", "reply"], default="post")
    args = ap.parse_args()
    if bool(args.text) == bool(args.file):
        print("二选一：--text 传正文，或 --file 传草稿文件", file=sys.stderr)
        return 2
    text = args.text if args.text else open(args.file, encoding="utf-8").read()
    text = text.strip()
    if not text:
        print("正文是空的", file=sys.stderr)
        return 2
    results = []
    low = text.lower()

    found = [w for w in BANNED if w in low]
    if "not just" in low and "but" in low:
        found.append("not just X, but Y 排比")
    if found:
        report(results, "FAIL", "禁用词", "命中：" + "、".join(found))
    else:
        report(results, "PASS", "禁用词", "没命中禁用词")

    bold = [ch for ch in text if 0x1D400 <= ord(ch) <= 0x1D7FF]
    if bold:
        report(results, "FAIL", "Unicode 粗体", "用了数学字母符号区的粗体字，改回普通字")
    else:
        report(results, "PASS", "Unicode 粗体", "没用")

    if "🧵" in text and "👇" in text:
        report(results, "FAIL", "模板化串帖符号", "🧵👇 全套是模板味，去掉")
    else:
        report(results, "PASS", "模板化串帖符号", "没用全套模板符号")

    tags = re.findall(r"#\w+", text)
    if len(tags) > 2:
        report(results, "WARN", "hashtag", f"{len(tags)} 个，超了上限 2 个（标准 0–1 个）")
    else:
        report(results, "PASS", "hashtag", f"{len(tags)} 个")

    emojis = EMOJI_RE.findall(text)
    if len(emojis) > 2:
        report(results, "WARN", "emoji", f"{len(emojis)} 个，超了上限 2 个")
    else:
        report(results, "PASS", "emoji", f"{len(emojis)} 个")

    nums = re.findall(r"\d[\d,.]*", text)
    if args.kind == "post" and len(nums) < 2:
        report(results, "WARN", "具体数", f"只找到 {len(nums)} 个数字，主线帖标准是 ≥2 个具体数")
    else:
        report(results, "PASS", "具体数", f"找到 {len(nums)} 个数字")

    if re.search(r"https?://", text):
        report(results, "WARN", "链接", "正文里带链接；免费号链接只放自回复，正文不放")
    else:
        report(results, "PASS", "链接", "正文没带链接")

    # 中文按字计、英文按词计，不然中文帖子按空格分词永远只有几个“词”，长度检查失效。
    words = (len(re.findall(r"[A-Za-z0-9]+", text))
             + len(re.findall(r"[\u4e00-\u9fff]", text)))
    if args.kind == "reply" and words > 30:
        report(results, "WARN", "回复长度", f"{words} 词/字，回复中位约 10 词，太长了，砍到一个具体点")
    else:
        report(results, "PASS", "长度", f"{words} 词/字")

    fails = results.count("FAIL")
    warns = results.count("WARN")
    print(f"结论：FAIL {fails} 项，WARN {warns} 项")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
