#!/usr/bin/env python3
"""把 SRT 字幕烧进视频，字幕底边离底部 24%（抖音底部信息区安全距离）。

用法：
    python3 burn_subtitles.py --video 原片.mp4 --srt 字幕.srt --out 成片.mp4
    python3 burn_subtitles.py --video 原片.mp4 --srt 字幕.srt --out 成片.mp4 \\
        --margin-bottom-pct 24 --font-size 46

只依赖 ffmpeg / ffprobe。字幕样式：底部居中，底边距底 = 画面高度 × margin-bottom-pct。
1080×1920 的画幅，默认 24% 就是距底 460 像素那条线（见模块 README 字幕一节）。
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def run(cmd, cwd=None):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        print(f"命令失败：{' '.join(cmd)}\n{r.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return r.stdout


def probe_size(video):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
               "-show_entries", "stream=width,height", "-of", "csv=p=0", str(video)])
    w, h = out.strip().split(",")
    return int(w), int(h)


def parse_srt(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    blocks = re.split(r"\n\s*\n", text.strip())
    cues = []
    for b in blocks:
        lines = [ln.strip() for ln in b.strip().splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        m = re.match(r"(\d\d:\d\d:\d\d[,.]\d+)\s*-->\s*(\d\d:\d\d:\d\d[,.]\d+)", lines[1])
        if not m:
            continue
        body = " ".join(lines[2:])
        cues.append((m.group(1).replace(",", "."), m.group(2).replace(",", "."), body))
    return cues


def to_ass_time(t):
    h, m, rest = t.split(":")
    s, frac = rest.split(".")
    return f"{int(h)}:{m}:{s}.{frac[:2].ljust(2, '0')}"


def main():
    ap = argparse.ArgumentParser(description="SRT 字幕烧录（底边距底 24%）")
    ap.add_argument("--video", required=True)
    ap.add_argument("--srt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--margin-bottom-pct", type=float, default=24.0)
    ap.add_argument("--font-size", type=int, default=46)
    ap.add_argument("--font", default="sans-serif")
    args = ap.parse_args()

    video, srt, out = Path(args.video), Path(args.srt), Path(args.out)
    for p in (video, srt):
        if not p.is_file():
            print(f"找不到文件：{p}", file=sys.stderr)
            return 2
    w, h = probe_size(video)
    cues = parse_srt(srt)
    if not cues:
        print("SRT 里没读出有效字幕段，检查时间轴格式", file=sys.stderr)
        return 2
    margin_v = int(h * args.margin_bottom_pct / 100)  # 向下取整：1920×24% = 460，跟模块文档一致

    ass_lines = [
        "[Script Info]",
        f"PlayResX: {w}",
        f"PlayResY: {h}",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, BackColour, Bold, "
        "Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Format: Style: Default,{args.font},{args.font_size},&H00FFFFFF,&H80000000,"
        f"0,0,1,2,0,2,20,20,{margin_v},1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Text",
    ]
    for start, end, body in cues:
        safe = body.replace("{", "(").replace("}", ")")
        ass_lines.append(f"Dialogue: 0,{to_ass_time(start)},{to_ass_time(end)},Default,,0,0,0,,{safe}")
    out.parent.mkdir(parents=True, exist_ok=True)
    ass_path = out.parent / "burn_subtitles_tmp.ass"
    ass_path.write_text("\n".join(ass_lines) + "\n", encoding="utf-8")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video),
         "-vf", f"ass={ass_path.name}", "-c:a", "copy", str(out)], cwd=str(out.parent))
    ass_path.unlink(missing_ok=True)
    print(f"烧好了：{out}（{w}x{h}，字幕 {len(cues)} 条，底边距底 {margin_v}px = {args.margin_bottom_pct:g}%）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
