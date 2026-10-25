#!/usr/bin/env python3
"""把品牌片尾拼到正片后面。必须用分轨拼接，不许用 concat 直拼。

教训：片尾音频用 concat demuxer 直拼时可能解码报错、尾段静音。
本脚本先把片尾归一化到正片规格（尺寸、帧率、采样率），再用 concat 滤镜
分轨拼视频 + 音频，拼完打印两段时长和成品时长。

用法：
    python3 append_outro.py --main 正片.mp4 --outro 片尾.mp4 --out 成片.mp4

只依赖 ffmpeg / ffprobe。
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"命令失败：{' '.join(cmd)}\n{r.stderr.strip()}", file=sys.stderr)
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
    ap = argparse.ArgumentParser(description="正片 + 品牌片尾，分轨拼接")
    ap.add_argument("--main", required=True)
    ap.add_argument("--outro", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    main_p, outro_p, out_p = Path(args.main), Path(args.outro), Path(args.out)
    for p in (main_p, outro_p):
        if not p.is_file():
            print(f"找不到文件：{p}", file=sys.stderr)
            return 2
    w, h, fps, dur_main = probe(main_p)
    _, _, _, dur_outro = probe(outro_p)
    # 两路视频都要先统一 SAR（concat 滤镜要求两路参数一致，否则报
    # parameters do not match；实测里测试源的 SAR 就跟成品不一样）。
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
    print(f"拼好了：{out_p}（正片 {dur_main:.2f}s + 片尾 {dur_outro:.2f}s = 成片 {dur_out:.2f}s）")
    if abs(dur_out - (dur_main + dur_outro)) > 0.5:
        print("提醒：成片时长跟两段之和差 0.5 秒以上，检查片尾有没有被截断", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
