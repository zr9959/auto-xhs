#!/usr/bin/env python3
"""YouTube 上传前检查：标题、封面、简介、标签、成片逐项过。

用法：
    python3 check_upload.py --dir <待发包目录>

待发包目录里放：
    title.txt        标题（单行）
    description.txt  简介（可选，但有章节行时要合规）
    thumbnail.jpg    封面（jpg 或 png）
    video.mp4        成片
    tags.txt         标签（可选，一行一个）

检查项（FAIL = 硬规矩，WARN = 提醒）：
  FAIL  标题缺失或超过 100 字（平台上限）
  WARN  标题超过 70 字（展示会被截断）
  FAIL  封面缺失或尺寸不是 1280×720
  FAIL  成片缺失或解码失败
  WARN  简介缺失
  FAIL  章节行第一行不是 0:00 开头（有章节时）
  WARN  标签总字数超过 500 字（平台上限）
  WARN  简介里没放章节（长视频建议放）

只依赖 ffprobe。退出码：有 FAIL 为 1，否则 0。
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def report(results, status, name, detail):
    results.append(status)
    print(f"[{status}] {name}: {detail}")


def ffprobe_ok(video):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "stream=width,height,codec_name",
                        "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1", str(video)],
                       capture_output=True, text=True)
    return r.returncode == 0, r.stdout


def thumb_size(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0",
                        str(path)], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    w, h = r.stdout.strip().split(",")
    return int(w), int(h)


def main():
    ap = argparse.ArgumentParser(description="YouTube 上传前检查")
    ap.add_argument("--dir", required=True)
    args = ap.parse_args()
    d = Path(args.dir)
    if not d.is_dir():
        print(f"待发包目录不存在：{d}", file=sys.stderr)
        return 2
    results = []

    title_p = d / "title.txt"
    if not title_p.is_file():
        report(results, "FAIL", "标题", "没有 title.txt")
    else:
        title = title_p.read_text(encoding="utf-8").strip()
        if not title:
            report(results, "FAIL", "标题", "title.txt 是空的")
        elif len(title) > 100:
            report(results, "FAIL", "标题", f"{len(title)} 字，超了平台上限 100 字")
        elif len(title) > 70:
            report(results, "WARN", "标题", f"{len(title)} 字，展示会被截断，压到 70 字内更好")
        else:
            report(results, "PASS", "标题", f"{len(title)} 字")

    thumbs = sorted(d.glob("thumbnail.*"))
    if not thumbs:
        report(results, "FAIL", "封面", "没有 thumbnail.jpg/png")
    else:
        size = thumb_size(thumbs[0])
        if size == (1280, 720):
            report(results, "PASS", "封面", f"{thumbs[0].name} 1280×720")
        elif size is None:
            report(results, "FAIL", "封面", f"{thumbs[0].name} 读不出尺寸")
        else:
            report(results, "FAIL", "封面", f"{thumbs[0].name} 是 {size[0]}×{size[1]}，标准 1280×720")

    videos = sorted(d.glob("video.*"))
    if not videos:
        report(results, "FAIL", "成片", "没有 video.mp4")
    else:
        ok, out = ffprobe_ok(videos[0])
        if ok:
            dur = ""
            for ln in out.splitlines():
                if ln.startswith("duration="):
                    dur = f"，时长 {float(ln.split('=')[1]):.1f}s"
            report(results, "PASS", "成片", f"{videos[0].name} 能解码{dur}")
        else:
            report(results, "FAIL", "成片", f"{videos[0].name} 解码失败")

    desc_p = d / "description.txt"
    if not desc_p.is_file():
        report(results, "WARN", "简介", "没有 description.txt")
    else:
        desc = desc_p.read_text(encoding="utf-8")
        chapters = re.findall(r"^(\d+:\d\d(?::\d\d)?)\s+.+", desc, re.M)
        if chapters:
            if chapters[0] in ("0:00", "00:00", "0:00:00"):
                report(results, "PASS", "章节", f"{len(chapters)} 个章节，第一行 0:00 开头")
            else:
                report(results, "FAIL", "章节", f"第一行是 {chapters[0]}，章节必须从 0:00 开始")
        else:
            report(results, "WARN", "章节", "简介里没放章节，长视频建议放时间戳章节")

    tags_p = d / "tags.txt"
    if tags_p.is_file():
        tags = [ln.strip() for ln in tags_p.read_text(encoding="utf-8").splitlines()
                if ln.strip()]
        total = sum(len(t) for t in tags)
        if total > 500:
            report(results, "WARN", "标签", f"{len(tags)} 个标签共 {total} 字，超了平台上限 500 字")
        else:
            report(results, "PASS", "标签", f"{len(tags)} 个标签共 {total} 字")
    else:
        report(results, "PASS", "标签", "没放标签文件，不判")

    fails = results.count("FAIL")
    warns = results.count("WARN")
    print(f"结论：FAIL {fails} 项，WARN {warns} 项")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
