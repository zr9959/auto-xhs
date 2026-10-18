#!/bin/bash
# 把截好的帧和配音拼成一条成片。
#
# 用法：
#   bash assemble.sh --frames 帧目录 --scenes open:16.6,step1:35.3 \
#     --audio open=开场.mp3,step1=正文.mp3 --out 成片.mp4
# 可选项：
#   --speed 1.5   倍速，默认 1.5。填 1 就是不加速。
#   --fps 30      帧是按每秒几帧截的，默认 30，要跟 capture.js 用的一致。
#   --work 目录   中间文件放哪，默认在帧目录旁边建一个 assemble-work。
#
# 每段先核对帧数：应该是 floor(时长 × fps)，对不上就停，话会说清哪段差几帧。
# 编码口径写死了，别乱改：H.264 High、yuv420p、timescale 600、
# AAC 48kHz 双声道 128k、faststart。手机上播不出来，多半是这几项被改过。
# 码率有地板：目标 3M、上限 4M（issue #1 实测：585 kb/s 时字边已经糊）。
# 别把 -crf 加回来跟 -b:v 一起用：实测那样以 crf 为准，码率地板等于没有。
set -euo pipefail

FRAMES="" SCENES="" AUDIO="" OUT="" SPEED="1.5" FPS="30" WORK=""
while [ $# -gt 0 ]; do
  case "$1" in
    --frames) FRAMES="$2"; shift 2;;
    --scenes) SCENES="$2"; shift 2;;
    --audio)  AUDIO="$2";  shift 2;;
    --out)    OUT="$2";    shift 2;;
    --speed)  SPEED="$2";  shift 2;;
    --fps)    FPS="$2";    shift 2;;
    --work)   WORK="$2";   shift 2;;
    *) echo "不认识的参数：$1" >&2; exit 2;;
  esac
done
if [ -z "$FRAMES" ] || [ -z "$SCENES" ] || [ -z "$AUDIO" ] || [ -z "$OUT" ]; then
  echo "用法：bash assemble.sh --frames 帧目录 --scenes 场景名:时长秒,... --audio 场景名=音频文件,... --out 成片.mp4 [--speed 1.5] [--fps 30]" >&2
  exit 2
fi
for cmd in ffmpeg; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "缺 $cmd，先装 ffmpeg 再跑。" >&2; exit 1; }
done
[ -n "$WORK" ] || WORK="$(dirname "$FRAMES")/assemble-work"
mkdir -p "$WORK"
# 拼片清单里的路径，ffmpeg 是按清单自己所在的文件夹去找的，
# 所以这里先把工作目录换成绝对路径，省得它找岔了地方。
WORK="$(cd "$WORK" && pwd)"
OUT="$(mkdir -p "$(dirname "$OUT")" && cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"

# 把 open=开场.mp3,step1=正文.mp3 这种写法拆成「场景名 -> 文件」。
declare -A AUDIO_OF=()
IFS=',' read -ra PAIRS <<< "$AUDIO"
for pair in "${PAIRS[@]}"; do
  AUDIO_OF["${pair%%=*}"]="${pair#*=}"
done

VIDEO_LIST="$WORK/video-list.txt"
AUDIO_LIST="$WORK/audio-list.txt"
: > "$VIDEO_LIST"; : > "$AUDIO_LIST"

IFS=',' read -ra LIST <<< "$SCENES"
for item in "${LIST[@]}"; do
  name="${item%%:*}"
  dur="${item#*:}"
  dir="$FRAMES/$name"
  want="$(python3 -c "import math,sys; print(math.floor(float(sys.argv[1]) * int(sys.argv[2])))" "$dur" "$FPS")"
  if [ ! -d "$dir" ]; then
    echo "停：找不到 $name 的帧目录 $dir。先跑 capture.js 把这段截出来。" >&2
    exit 1
  fi
  got="$(find "$dir" -maxdepth 1 -name '*.jpg' | wc -l | tr -d ' ')"
  if [ "$got" != "$want" ]; then
    echo "停：$name 的帧数对不上，有 $got 帧，应该有 $want 帧（时长 $dur 秒 × $FPS 帧）。差的帧多半是截图没跑完，重新跑 capture.js 再来拼。" >&2
    exit 1
  fi
  audio="${AUDIO_OF[$name]:-}"
  if [ -z "$audio" ] || [ ! -f "$audio" ]; then
    echo "停：$name 的配音文件没给，或者找不到（给了的是「$audio」）。--audio 要按 场景名=文件 一段一段对上。" >&2
    exit 1
  fi
  ffmpeg -y -v error -framerate "$FPS" -i "$dir/%04d.jpg" -t "$dur" \
    -c:v libx264 -pix_fmt yuv420p "$WORK/seg-$name.mp4"
  echo "file '$WORK/seg-$name.mp4'" >> "$VIDEO_LIST"
  echo "file '$(cd "$(dirname "$audio")" && pwd)/$(basename "$audio")'" >> "$AUDIO_LIST"
  echo "$name：帧数 $got 对上了，已转成一段。"
done

ffmpeg -y -v error -f concat -safe 0 -i "$VIDEO_LIST" -c copy "$WORK/video-only.mp4"
ffmpeg -y -v error -f concat -safe 0 -i "$AUDIO_LIST" -c:a pcm_s16le "$WORK/audio-all.wav"

if [ "$SPEED" = "1" ] || [ "$SPEED" = "1.0" ]; then
  ffmpeg -y -v error -i "$WORK/video-only.mp4" -i "$WORK/audio-all.wav" -map 0:v -map 1:a \
    -video_track_timescale 600 -c:v libx264 -profile:v high -pix_fmt yuv420p -b:v 3M -maxrate 4M -bufsize 6M \
    -c:a aac -ar 48000 -ac 2 -b:a 128k -use_editlist 0 -movflags +faststart "$OUT"
else
  ffmpeg -y -v error -i "$WORK/video-only.mp4" -i "$WORK/audio-all.wav" -map 0:v -map 1:a \
    -vf "setpts=PTS/$SPEED" -af "atempo=$SPEED" \
    -video_track_timescale 600 -c:v libx264 -profile:v high -pix_fmt yuv420p -b:v 3M -maxrate 4M -bufsize 6M \
    -c:a aac -ar 48000 -ac 2 -b:a 128k -use_editlist 0 -movflags +faststart "$OUT"
fi

echo "拼好了：$OUT（倍速 $SPEED）"
