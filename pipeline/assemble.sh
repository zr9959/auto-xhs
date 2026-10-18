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
#   --intro 文件  品牌片头短片（可选）。会先归一化到与正片同规格再拼到最前。
#   --outro 文件  品牌片尾短片（可选）。同上，拼到最后。
#                 片头片尾的方向必须跟正片一致：竖正片配竖片头，不许混。
#   --crf 13      画质，默认 13（12–14 之间选，越小越清、文件越大）。
#   --max-size-mb 100  成品大小上限（MB），超了自动升 CRF 重拼。
#
# 每段先核对帧数：应该是 floor(时长 × fps)，对不上就停，话会说清哪段差几帧。
# 编码口径写死了，别乱改：H.264 High、yuv420p、timescale 600、
# AAC 48kHz 双声道 128k、faststart。手机上播不出来，多半是这几项被改过。
# 画质走 CRF（定画质不定码率）：默认 13，可在 12–14 之间选，数越小越清。
# 不再用目标码率：以前的目标 3M/上限 4M 是给 issue #1 的低码率兜底的，
# CRF 模式下码率随画面复杂度自己走，简单画面低码率也是高清，不用卡。
# 唯一的硬线是成品大小：默认不超过 100MB。超了就自动把 CRF 往上加 2
# 重拼，一直到装下为止（会在输出里写明最后用了多少）。
set -euo pipefail

FRAMES="" SCENES="" AUDIO="" OUT="" SPEED="1.5" FPS="30" WORK="" INTRO="" OUTRO="" CRF="13" MAXMB="100"
while [ $# -gt 0 ]; do
  case "$1" in
    --frames) FRAMES="$2"; shift 2;;
    --scenes) SCENES="$2"; shift 2;;
    --audio)  AUDIO="$2";  shift 2;;
    --out)    OUT="$2";    shift 2;;
    --speed)  SPEED="$2";  shift 2;;
    --fps)    FPS="$2";    shift 2;;
    --work)   WORK="$2";   shift 2;;
    --intro)  INTRO="$2";  shift 2;;
    --outro)  OUTRO="$2";  shift 2;;
    --crf)    CRF="$2";    shift 2;;
    --max-size-mb) MAXMB="$2"; shift 2;;
    *) echo "不认识的参数：$1" >&2; exit 2;;
  esac
done
case "$CRF" in
  *[!0-9]*|"") echo "停：--crf 要填整数（12–14 之间），给了的是「$CRF」。" >&2; exit 2;;
esac
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
  # 中间段用 CRF 10 近无损编：最终画质定在 12–14，中间段要是先糊一道，
  # 后面编得再清也补不回来。
  ffmpeg -y -v error -framerate "$FPS" -i "$dir/%04d.jpg" -t "$dur" \
    -c:v libx264 -pix_fmt yuv420p -crf 10 "$WORK/seg-$name.mp4"
  echo "file '$WORK/seg-$name.mp4'" >> "$VIDEO_LIST"
  echo "file '$(cd "$(dirname "$audio")" && pwd)/$(basename "$audio")'" >> "$AUDIO_LIST"
  echo "$name：帧数 $got 对上了，已转成一段。"
done

ffmpeg -y -v error -f concat -safe 0 -i "$VIDEO_LIST" -c copy "$WORK/video-only.mp4"
ffmpeg -y -v error -f concat -safe 0 -i "$AUDIO_LIST" -c:a pcm_s16le "$WORK/audio-all.wav"

# 有片头片尾时，正片先拼成 body.mp4，最后把三段按同规格接起来；
# 没有时跟原来一样，直接拼到 OUT，行为不变。
TARGET="$OUT"
if [ -n "$INTRO" ] || [ -n "$OUTRO" ]; then
  TARGET="$WORK/body.mp4"
fi

encode_final() {
  # $1=CRF 值。倍速与否只差一组滤镜，其余编码参数一份。
  local crf="$1"
  if [ "$SPEED" = "1" ] || [ "$SPEED" = "1.0" ]; then
    ffmpeg -y -v error -i "$WORK/video-only.mp4" -i "$WORK/audio-all.wav" -map 0:v -map 1:a \
      -video_track_timescale 600 -c:v libx264 -profile:v high -pix_fmt yuv420p -crf "$crf" \
      -c:a aac -ar 48000 -ac 2 -b:a 128k -use_editlist 0 -movflags +faststart "$TARGET"
  else
    ffmpeg -y -v error -i "$WORK/video-only.mp4" -i "$WORK/audio-all.wav" -map 0:v -map 1:a \
      -vf "setpts=PTS/$SPEED" -af "atempo=$SPEED" \
      -video_track_timescale 600 -c:v libx264 -profile:v high -pix_fmt yuv420p -crf "$crf" \
      -c:a aac -ar 48000 -ac 2 -b:a 128k -use_editlist 0 -movflags +faststart "$TARGET"
  fi
}

# 大小闸：成品超过上限就把 CRF 加 2 重拼，直到装下。CRF 加到 40 还装不下，
# 就停下来把话说清（多半是片子太长或上限填得太小），不许悄悄交个超标的。
LIMIT_BYTES="$(python3 -c "print(int(float('$MAXMB') * 1000000))")"
USE_CRF="$CRF"
while true; do
  encode_final "$USE_CRF"
  SIZE="$(stat -c%s "$TARGET")"
  if [ "$SIZE" -le "$LIMIT_BYTES" ]; then
    break
  fi
  SIZE_MB="$(python3 -c "print(round($SIZE / 1000000, 1))")"
  if [ "$USE_CRF" -ge 40 ]; then
    echo "停：CRF 已经加到 $USE_CRF，成品还是 ${SIZE_MB}MB，超过上限 ${MAXMB}MB。把 --max-size-mb 放大，或者把片子改短再来。" >&2
    exit 1
  fi
  echo "成品 ${SIZE_MB}MB 超过上限 ${MAXMB}MB，CRF 从 $USE_CRF 升到 $((USE_CRF + 2)) 重拼。"
  USE_CRF=$((USE_CRF + 2))
done
if [ "$USE_CRF" != "$CRF" ]; then
  echo "最终画质：CRF $USE_CRF（原定 $CRF，因大小上限自动降了清晰度）"
else
  echo "最终画质：CRF $USE_CRF"
fi

if [ "$TARGET" != "$OUT" ]; then
  BW="$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$TARGET")"
  BH="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$TARGET")"
  JOIN_LIST="$WORK/join-list.txt"
  : > "$JOIN_LIST"
  norm_part() {
    # $1=源文件 $2=归一化后的文件名。缩放到正片尺寸（不够的补边），帧率、编码、音频都对齐正片。
    local src="$1" dst="$WORK/$2"
    [ -f "$src" ] || { echo "停：片头/片尾文件找不到：$src" >&2; exit 1; }
    local has_audio
    has_audio="$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$src" | head -n 1)"
    if [ -n "$has_audio" ]; then
      ffmpeg -y -v error -i "$src" -map 0:v -map 0:a \
        -vf "scale=${BW}:${BH}:force_original_aspect_ratio=decrease,pad=${BW}:${BH}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=${FPS},format=yuv420p" \
        -video_track_timescale 600 -c:v libx264 -profile:v high -crf "$CRF" \
        -c:a aac -ar 48000 -ac 2 -b:a 128k -use_editlist 0 "$dst"
    else
      ffmpeg -y -v error -i "$src" -f lavfi -i anullsrc=r=48000:cl=stereo -map 0:v -map 1:a -shortest \
        -vf "scale=${BW}:${BH}:force_original_aspect_ratio=decrease,pad=${BW}:${BH}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=${FPS},format=yuv420p" \
        -video_track_timescale 600 -c:v libx264 -profile:v high -crf "$CRF" \
        -c:a aac -ar 48000 -ac 2 -b:a 128k -use_editlist 0 "$dst"
    fi
    echo "file '$dst'" >> "$JOIN_LIST"
  }
  [ -n "$INTRO" ] && norm_part "$INTRO" norm-intro.mp4
  echo "file '$TARGET'" >> "$JOIN_LIST"
  [ -n "$OUTRO" ] && norm_part "$OUTRO" norm-outro.mp4
  ffmpeg -y -v error -f concat -safe 0 -i "$JOIN_LIST" -c copy -movflags +faststart "$OUT"
  echo "片头片尾已拼上（正片规格 ${BW}x${BH}）。"
fi

OUT_SIZE="$(stat -c%s "$OUT")"
OUT_MB="$(python3 -c "print(round($OUT_SIZE / 1000000, 1))")"
echo "拼好了：$OUT（倍速 $SPEED，大小 ${OUT_MB}MB，上限 ${MAXMB}MB）"
