#!/bin/bash
# Stitch captured frames and voiceover into one finished video.
#
# Usage:
#   bash assemble.sh --frames frames-dir --scenes open:16.6,step1:35.3 \
#     --audio open=intro.mp3,step1=body.mp3 --out finished.mp4
# Options:
#   --speed 1.5   Speed multiplier, default 1.5. 1 means no speedup.
#   --fps 30      Frames per second the frames were captured at, default 30 — must match what capture.js used.
#   --work DIR    Where intermediate files go; default is an assemble-work folder next to the frames dir.
#   --intro FILE  Brand intro clip (optional). Normalized to the main video's specs first, then joined at the front.
#   --outro FILE  Brand outro clip (optional). Same as above, joined at the end.
#                 Intro/outro orientation must match the main video: a vertical main video takes a vertical intro — never mix.
#   --crf 13      Quality, default 13 (pick 12–14; smaller is clearer and bigger).
#   --max-size-mb 100  Finished-file size cap (MB); over the cap, CRF auto-rises and it re-encodes.
#
# Each segment's frame count is checked first: it should be floor(duration × fps). On mismatch it stops
# and says which segment is short by how many frames.
# Encoding settings are fixed — don't change them casually: H.264 High, yuv420p, timescale 600,
# AAC 48kHz stereo 128k, faststart. If a phone can't play it, one of these was probably changed.
# Quality runs on CRF (fixed quality, not fixed bitrate): default 13, pick 12–14, smaller is clearer.
# No more target bitrate: the old 3M target / 4M cap was a floor for issue #1's low-bitrate problem;
# under CRF the bitrate follows scene complexity on its own, and simple scenes are HD even at low bitrates, so no floor is needed.
# The only hard line is finished size: 100MB by default. Over it, CRF auto-rises by 2 and it re-encodes
# until it fits (the output states the final CRF used).
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
    *) echo "Unknown option: $1" >&2; exit 2;;
  esac
done
case "$CRF" in
  *[!0-9]*|"") echo "Stop: --crf needs an integer (12–14); got $CRF." >&2; exit 2;;
esac
if [ -z "$FRAMES" ] || [ -z "$SCENES" ] || [ -z "$AUDIO" ] || [ -z "$OUT" ]; then
  echo "Usage: bash assemble.sh --frames frames-dir --scenes scene:seconds,... --audio scene=audio-file,... --out finished.mp4 [--speed 1.5] [--fps 30]" >&2
  exit 2
fi
for cmd in ffmpeg; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "Missing $cmd — install ffmpeg first, then run." >&2; exit 1; }
done
[ -n "$WORK" ] || WORK="$(dirname "$FRAMES")/assemble-work"
mkdir -p "$WORK"
# Paths in a concat list are resolved by ffmpeg relative to the list's own folder,
# so convert the work dir to an absolute path first — otherwise it looks in the wrong place.
WORK="$(cd "$WORK" && pwd)"
OUT="$(mkdir -p "$(dirname "$OUT")" && cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"

# Split the open=intro.mp3,step1=body.mp3 form into scene -> file pairs.
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
    echo "Stop: can't find the frames dir for $name: $dir. Run capture.js to capture that segment first." >&2
    exit 1
  fi
  got="$(find "$dir" -maxdepth 1 -name '*.jpg' | wc -l | tr -d ' ')"
  if [ "$got" != "$want" ]; then
    echo "Stop: $name frame count mismatch — got $got frames, want $want ($dur s × $FPS fps). Missing frames usually mean the capture didn't finish; re-run capture.js, then assemble again." >&2
    exit 1
  fi
  audio="${AUDIO_OF[$name]:-}"
  if [ -z "$audio" ] || [ ! -f "$audio" ]; then
    echo "Stop: $name's voiceover file was not given, or not found (given: $audio). --audio must map every scene as scene=file." >&2
    exit 1
  fi
  # Intermediate segments encode near-lossless at CRF 10: final quality lands at 12–14, and if an
  # intermediate segment goes soft first, no later encode can sharpen it back.
  ffmpeg -y -v error -framerate "$FPS" -i "$dir/%04d.jpg" -t "$dur" \
    -c:v libx264 -pix_fmt yuv420p -crf 10 "$WORK/seg-$name.mp4"
  echo "file '$WORK/seg-$name.mp4'" >> "$VIDEO_LIST"
  echo "file '$(cd "$(dirname "$audio")" && pwd)/$(basename "$audio")'" >> "$AUDIO_LIST"
  echo "$name: $got frames match, converted to one segment."
done

ffmpeg -y -v error -f concat -safe 0 -i "$VIDEO_LIST" -c copy "$WORK/video-only.mp4"
ffmpeg -y -v error -f concat -safe 0 -i "$AUDIO_LIST" -c:a pcm_s16le "$WORK/audio-all.wav"

# With intro/outro, the main video first becomes body.mp4, and the three parts join at matching specs at the end;
# without them it goes straight to OUT as before — behavior unchanged.
TARGET="$OUT"
if [ -n "$INTRO" ] || [ -n "$OUTRO" ]; then
  TARGET="$WORK/body.mp4"
fi

encode_final() {
  # $1 = CRF value. Speed or not, only one filter set differs; the rest of the encode settings are shared.
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

# Size gate: over the cap, CRF rises by 2 and it re-encodes until it fits. If CRF reaches 40 and it still doesn't fit,
# stop and say so plainly (usually the video is too long or the cap too small) — never quietly hand over an oversize file.
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
    echo "Stop: CRF already raised to $USE_CRF, but the finished file is still ${SIZE_MB}MB, over the ${MAXMB}MB cap. Raise --max-size-mb, or shorten the video and try again." >&2
    exit 1
  fi
  echo "Finished file ${SIZE_MB}MB is over the ${MAXMB}MB cap — raising CRF from $USE_CRF to $((USE_CRF + 2)) and re-encoding."
  USE_CRF=$((USE_CRF + 2))
done
if [ "$USE_CRF" != "$CRF" ]; then
  echo "Final quality: CRF $USE_CRF (was $CRF — clarity auto-lowered for the size cap)"
else
  echo "Final quality: CRF $USE_CRF"
fi

if [ "$TARGET" != "$OUT" ]; then
  BW="$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$TARGET")"
  BH="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$TARGET")"
  JOIN_LIST="$WORK/join-list.txt"
  : > "$JOIN_LIST"
  norm_part() {
    # $1 = source file, $2 = normalized output name. Scale to the main video's size (pad where short), and match its frame rate, encoding, and audio.
    local src="$1" dst="$WORK/$2"
    [ -f "$src" ] || { echo "Stop: intro/outro file not found: $src" >&2; exit 1; }
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
  echo "Intro/outro joined (main video specs ${BW}x${BH})."
fi

OUT_SIZE="$(stat -c%s "$OUT")"
OUT_MB="$(python3 -c "print(round($OUT_SIZE / 1000000, 1))")"
echo "Done: $OUT (speed $SPEED, size ${OUT_MB}MB, cap ${MAXMB}MB)"
