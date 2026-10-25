#!/bin/bash
# Check whether the video-making tools are all present. Anything missing gets explained in plain words: which one, and what it's for.
# Exit code: 1 if any hard requirement (ffmpeg, node, python3, curl, tar) is missing, else 0.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fail=0

have() { command -v "$1" >/dev/null 2>&1; }

if have ffmpeg; then
  echo "ffmpeg found: $(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f1-3)"
else
  echo "Missing ffmpeg: the final stitching of frames and sound into a video depends on it — without it, no video. Install ffmpeg, then come back."
  fail=1
fi

if have ffprobe; then
  echo "ffprobe found: reading video and audio durations and dimensions depends on it."
else
  echo "Missing ffprobe: it usually installs with ffmpeg — install ffmpeg, then check again."
  fail=1
fi

if have node; then
  echo "node found: $(node --version), the frame-by-frame capture scripts run on it."
else
  echo "Missing node: frame-by-frame capture depends on it. Get a long-term support version from nodejs.org, then come back."
  fail=1
fi

if have python3; then
  echo "python3 found: $(python3 --version 2>&1), the acceptance script and voiceover examples run on it."
else
  echo "Missing python3: the acceptance script can't run. Install python3 first, then come back."
  fail=1
fi

for cmd in curl tar; do
  if have "$cmd"; then
    echo "$cmd found: downloading third-party libraries depends on it."
  else
    echo "Missing $cmd: downloading third-party libraries depends on it — install it, then run scripts/fetch-vendor.sh."
    fail=1
  fi
done

# Browser for capture: check the environment variable first, then whether node can find playwright.
if [ -n "${CHROMIUM_PATH:-}" ] && [ -x "${CHROMIUM_PATH:-}" ]; then
  echo "Browser found: using the one CHROMIUM_PATH points to."
elif [ -n "${CHROMIUM_PATH:-}" ]; then
  echo "Note: CHROMIUM_PATH is set, but that path isn't executable. Capture will fall back to playwright's own browser."
elif have node && node -e "try{require.resolve('playwright');process.exit(0)}catch(e){try{require.resolve('playwright-core');process.exit(0)}catch(e2){process.exit(1)}}" 2>/dev/null; then
  echo "Note: the playwright package is there, but its bundled browser download isn't confirmed. Before the first capture, run npx playwright install chromium to download the browser."
else
  echo "Note: playwright not found yet. Capture needs it: in the directory holding capture.js, run npm install playwright, then npx playwright install chromium."
fi

# Also glance at whether the third-party libraries are downloaded, so it doesn't surface mid-production.
if [ -f "$ROOT/motion-lib/vendor/gsap/gsap.min.js" ] && [ -f "$ROOT/motion-lib/vendor/lottie.min.js" ]; then
  echo "Third-party libraries found: GSAP and lottie-web are both in motion-lib/vendor/."
else
  echo "Note: third-party libraries not downloaded yet. One run of bash scripts/fetch-vendor.sh downloads them."
fi

if [ "$fail" -ne 0 ]; then
  echo "Summary: install everything marked 'missing' above first, then continue."
  exit 1
fi
echo "Summary: everything hard-required is present. Items marked 'note' don't block you — fill them in as described."
