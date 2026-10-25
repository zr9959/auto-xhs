#!/usr/bin/env python3
"""Pre-upload check for YouTube: title, thumbnail, description, tags, and video, item by item.

Usage:
    python3 check_upload.py --dir <package directory>

The package directory holds:
    title.txt        title (one line)
    description.txt  description (optional, but chapter lines must be valid when present)
    thumbnail.jpg    thumbnail (jpg or png)
    video.mp4        finished video
    tags.txt         tags (optional, one per line)

Checks (FAIL = hard rule, WARN = heads-up):
  FAIL  title missing or over 100 chars (platform cap)
  WARN  title over 70 chars (display truncates)
  FAIL  thumbnail missing or not 1280×720
  FAIL  video missing or undecodable
  WARN  description missing
  FAIL  first chapter line not starting at 0:00 (when chapters exist)
  WARN  tags over 500 chars total (platform cap)
  WARN  no chapters in the description (recommended for long videos)

Only needs ffprobe. Exit code: 1 if any FAIL, else 0.
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
    ap = argparse.ArgumentParser(description="Pre-upload check for YouTube")
    ap.add_argument("--dir", required=True)
    args = ap.parse_args()
    d = Path(args.dir)
    if not d.is_dir():
        print(f"Package directory not found: {d}", file=sys.stderr)
        return 2
    results = []

    title_p = d / "title.txt"
    if not title_p.is_file():
        report(results, "FAIL", "Title", "No title.txt")
    else:
        title = title_p.read_text(encoding="utf-8").strip()
        if not title:
            report(results, "FAIL", "Title", "title.txt is empty")
        elif len(title) > 100:
            report(results, "FAIL", "Title", f"{len(title)} chars — over the platform cap of 100 chars")
        elif len(title) > 70:
            report(results, "WARN", "Title", f"{len(title)} chars — display truncates; under 70 chars is better")
        else:
            report(results, "PASS", "Title", f"{len(title)} chars")

    thumbs = sorted(d.glob("thumbnail.*"))
    if not thumbs:
        report(results, "FAIL", "Thumbnail", "No thumbnail.jpg/png")
    else:
        size = thumb_size(thumbs[0])
        if size == (1280, 720):
            report(results, "PASS", "Thumbnail", f"{thumbs[0].name} 1280×720")
        elif size is None:
            report(results, "FAIL", "Thumbnail", f"{thumbs[0].name} size unreadable")
        else:
            report(results, "FAIL", "Thumbnail", f"{thumbs[0].name} is {size[0]}×{size[1]} — standard is 1280×720")

    videos = sorted(d.glob("video.*"))
    if not videos:
        report(results, "FAIL", "Video", "No video.mp4")
    else:
        ok, out = ffprobe_ok(videos[0])
        if ok:
            dur = ""
            for ln in out.splitlines():
                if ln.startswith("duration="):
                    dur = f", duration {float(ln.split('=')[1]):.1f}s"
            report(results, "PASS", "Video", f"{videos[0].name} decodes{dur}")
        else:
            report(results, "FAIL", "Video", f"{videos[0].name} failed to decode")

    desc_p = d / "description.txt"
    if not desc_p.is_file():
        report(results, "WARN", "Description", "No description.txt")
    else:
        desc = desc_p.read_text(encoding="utf-8")
        chapters = re.findall(r"^(\d+:\d\d(?::\d\d)?)\s+.+", desc, re.M)
        if chapters:
            if chapters[0] in ("0:00", "00:00", "0:00:00"):
                report(results, "PASS", "Chapters", f"{len(chapters)} chapter{'s' if len(chapters) != 1 else ''}, first line starts at 0:00")
            else:
                report(results, "FAIL", "Chapters", f"First line is {chapters[0]} — chapters must start at 0:00")
        else:
            report(results, "WARN", "Chapters", "No chapters in the description — long videos should carry timestamp chapters")

    tags_p = d / "tags.txt"
    if tags_p.is_file():
        tags = [ln.strip() for ln in tags_p.read_text(encoding="utf-8").splitlines()
                if ln.strip()]
        total = sum(len(t) for t in tags)
        if total > 500:
            report(results, "WARN", "Tags", f"{len(tags)} tag{'s' if len(tags) != 1 else ''}, {total} chars total — over the platform cap of 500 chars")
        else:
            report(results, "PASS", "Tags", f"{len(tags)} tag{'s' if len(tags) != 1 else ''}, {total} chars total")
    else:
        report(results, "PASS", "Tags", "No tags file — not checked")

    fails = results.count("FAIL")
    warns = results.count("WARN")
    print(f"Summary: {fails} FAIL, {warns} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
