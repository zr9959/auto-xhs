#!/usr/bin/env python3
"""最小配音例子：读 scripts.txt，逐段用 edge-tts 出 mp3，打印每段时长。

用法：
    python3 tts-edge-example.py scripts.txt 音频输出目录

先装 edge-tts：pip install edge-tts
音色用环境变量 TTS_VOICE 改，不改就用默认那个。
一段坏了（时长离谱、中间有大段静音）怎么处理，看同目录 README.md 最后一节。
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

VOICE = os.environ.get("TTS_VOICE", "zh-CN-XiaoxiaoNeural")


def duration_of(path):
    """用 ffprobe 量一个音频有多长，量不到就返回 None。"""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def longest_silence(path):
    """查这段里最长的静音有几秒。没有 ffmpeg 就跳过，返回 None。"""
    if not shutil.which("ffmpeg"):
        return None
    r = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path),
         "-af", "silencedetect=noise=-45dB:d=1.5", "-f", "null", "-"],
        capture_output=True, text=True)
    starts, ends = [], []
    for line in r.stderr.splitlines():
        if "silence_start:" in line:
            starts.append(float(line.split("silence_start:")[1].strip()))
        if "silence_end:" in line:
            ends.append(float(line.split("silence_end:")[1].split("|")[0].strip()))
    spans = [e - s for s, e in zip(starts, ends)]
    return max(spans) if spans else 0.0


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    scripts = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    if not scripts.is_file():
        print(f"找不到稿子文件：{scripts}")
        return 1
    if not shutil.which("edge-tts"):
        print("没找到 edge-tts 命令。先装：pip install edge-tts")
        return 1
    if not shutil.which("ffprobe"):
        print("没找到 ffprobe，时长量不出来。装好 ffmpeg 再跑。")
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)

    total = 0.0
    for line in scripts.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        key, _, text = line.partition("|")
        key, text = key.strip(), text.strip()
        if not text:
            print(f"{key}：这行没有要念的话，跳过了。")
            continue
        target = out_dir / f"{key}.mp3"
        r = subprocess.run(
            ["edge-tts", "--voice", VOICE, "--text", text, "--write-media", str(target)],
            capture_output=True, text=True)
        if r.returncode != 0 or not target.is_file():
            print(f"{key}：生成失败。edge-tts 的原话：{r.stderr.strip()[:300]}")
            print("这段先停下，别硬拼。处理办法看 tts/README.md 最后一节。")
            return 1
        dur = duration_of(target)
        total += dur or 0
        note = ""
        sil = longest_silence(target)
        if sil is not None and sil >= 1.0:
            note = f"（注意：里面有 {sil:.1f} 秒静音，这段先别用，按 README 最后一节处理）"
        print(f"{key}：{target.name}，{dur:.2f} 秒{note}")
    print(f"一共 {total:.2f} 秒。拼片时拿这个数对画面时长。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
