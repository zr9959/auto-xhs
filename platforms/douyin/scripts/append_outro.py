#!/usr/bin/env python3
"""Join the brand outro after the main video. Join on separate tracks — never a straight concat.

Lesson: joining outro audio with a straight concat demuxer can fail decoding and go silent at the end.
This script first normalizes the outro to the main video's specs (size, frame rate, sample rate), then joins
video + audio on separate tracks with the concat filter, and prints both segment durations and the finished duration.

Usage:
    python3 append_outro.py --main main.mp4 --outro outro.mp4 --out finished.mp4

Only needs ffmpeg / ffprobe.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}\n{r.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return r.stdout


def probe(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
               "-show_entries", "stream=width,height,r_frame_rate",
               "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1", str(path)])
    d = {}
    for ln in out.strip().splitlines():
        if "=" in ln:
            k, v = ln.split("=", 1)
            d[k.strip()] = v.strip()
    num, den = d["r_frame_rate"].split("/")
    return int(d["width"]), int(d["height"]), round(int(num) / int(den)), float(d["duration"])


def main():
    ap = argparse.ArgumentParser(description="Main video + brand outro, joined on separate tracks")
    ap.add_argument("--main", required=True)
    ap.add_argument("--outro", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    main_p, outro_p, out_p = Path(args.main), Path(args.outro), Path(args.out)
    for p in (main_p, outro_p):
        if not p.is_file():
            print(f"File not found: {p}", file=sys.stderr)
            return 2
    w, h, fps, dur_main = probe(main_p)
    _, _, _, dur_outro = probe(outro_p)
    # Both video streams get the same SAR first (the concat filter requires matching parameters, or it errors
    # with parameters do not match — in testing, the test source's SAR differed from the finished video's).
    fc = (
        f"[0:v]setsar=1,format=yuv420p[v0];"
        f"[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];"
        f"[1:v]scale={w}:{h}:force_original_aspect_ratio=disable,"
        f"fps={fps},setsar=1,format=yuv420p[v1];"
        f"[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];"
        f"[v0][a0][v1][a1]concat=n=2:v=1:a=1[outv][outa]"
    )
    run(["ffmpeg", "-y", "-v", "error", "-i", str(main_p), "-i", str(outro_p),
         "-filter_complex", fc, "-map", "[outv]", "-map", "[outa]",
         "-c:v", "libx264", "-c:a", "aac", str(out_p)])
    _, _, _, dur_out = probe(out_p)
    print(f"Done: {out_p} (main {dur_main:.2f}s + outro {dur_outro:.2f}s = finished {dur_out:.2f}s)")
    if abs(dur_out - (dur_main + dur_outro)) > 0.5:
        print("Warning: finished duration differs from the two segments\' sum by over 0.5s — check whether the outro got cut", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
