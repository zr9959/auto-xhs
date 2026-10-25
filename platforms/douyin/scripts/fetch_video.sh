#!/bin/bash
# Download one candidate clip from a video platform. Just a thin yt-dlp wrapper, no hidden tricks.
#
# Usage:
#   bash fetch_video.sh <video URL> [save directory] [max height, default 1080]
#
# Rules:
#   - Print the outlet first, guessed from the URL: douyin.com -> Douyin,
#     tiktok.com -> TikTok, anything else -> other (check the module README
#     before publishing — the two outlets share one pipeline, but the outlet
#     decides the audience, the subtitle language, and which creator center
#     publishes it).
#   - Prefer the best quality within the max height + best audio, merged to mp4.
#   - Never get stuck on one route: if this route can't get HD, switch clients or switch clips (see the module README download section).
#   - If the 1080p ladder is missing, first retry yt-dlp with --remote-components ejs:github.
#   - If yt-dlp isn't installed, install it first: pip install yt-dlp (or your system package manager).
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: bash fetch_video.sh <video URL> [save directory] [max height, default 1080]" >&2
  exit 2
fi
URL="$1"
OUTDIR="${2:-.}"
MAXH="${3:-1080}"

case "$URL" in
  *douyin.com*) OUTLET="Douyin" ;;
  *tiktok.com*) OUTLET="TikTok" ;;
  *) OUTLET="other (not Douyin or TikTok — check the module README before publishing)" ;;
esac
echo "Outlet: $OUTLET"

if ! command -v yt-dlp >/dev/null 2>&1; then
  echo "yt-dlp not found — install it first: pip install yt-dlp" >&2
  exit 2
fi

mkdir -p "$OUTDIR"
yt-dlp \
  --no-playlist \
  -f "bv*[height<=$MAXH]+ba/b[height<=$MAXH]/bv*+ba/b" \
  --merge-output-format mp4 \
  -o "$OUTDIR/%(title).80s.%(ext)s" \
  "$URL"
echo "Downloaded to: $OUTDIR"
