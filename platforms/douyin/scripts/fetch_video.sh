#!/bin/bash
# 从视频平台下载一条候选片。只是 yt-dlp 的薄包装，不藏任何魔法。
#
# 用法：
#   bash fetch_video.sh <视频地址> [保存目录] [最高高度，默认 1080]
#
# 规矩：
#   - 优先拿最高高度以内的最佳画质 + 最佳音频，合并成 mp4。
#   - 不死卡一条路：这条路拿不到高清，就换客户端、换候选片（见模块 README 下载一节）。
#   - 1080p 阶梯拿不到时，先试给 yt-dlp 加 --remote-components ejs:github 再跑一次。
#   - 没装 yt-dlp 就先装：pip install yt-dlp（或按系统包管理器装）。
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "用法：bash fetch_video.sh <视频地址> [保存目录] [最高高度，默认 1080]" >&2
  exit 2
fi
URL="$1"
OUTDIR="${2:-.}"
MAXH="${3:-1080}"

if ! command -v yt-dlp >/dev/null 2>&1; then
  echo "没找到 yt-dlp，先装：pip install yt-dlp" >&2
  exit 2
fi

mkdir -p "$OUTDIR"
yt-dlp \
  --no-playlist \
  -f "bv*[height<=$MAXH]+ba/b[height<=$MAXH]/bv*+ba/b" \
  --merge-output-format mp4 \
  -o "$OUTDIR/%(title).80s.%(ext)s" \
  "$URL"
echo "下好了，存在：$OUTDIR"
