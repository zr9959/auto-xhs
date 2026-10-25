#!/bin/bash
# Download the third-party libraries video making needs into motion-lib/vendor/.
# Versions are pinned below; after download, each archive's hash is verified — on a mismatch it stops
# and leaves no bad file behind. The library list and licenses are in motion-lib/vendor/README.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/motion-lib/vendor"

GSAP_VER="3.15.0"
GSAP_SHA="d2e33ad202d4811e9084883f7ff9a27967ac4095caef51ca4c9d20697a253b1c"
LOTTIE_VER="5.13.0"
LOTTIE_SHA="00f306a9b5669abf9622c418b549681d1b858e0b7fa7ea6adc0772ca57c3fd4f"
CONFETTI_VER="1.9.4"
CONFETTI_SHA="c7c7d003c8b444d4f8e340e0b2c2a474abf2803ce34d184f783c1107217853e2"

for cmd in curl tar; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing $cmd — install it, then run this script again." >&2
    exit 1
  fi
done

sha_of() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | awk '{print $1}';
  else shasum -a 256 "$1" | awk '{print $1}'; fi
}

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Download one package, verify its hash, and print which step it gets stuck on.
get_pkg() {
  local name="$1" ver="$2" want_sha="$3"
  local file="$TMP/$name-$ver.tgz"
  echo "Downloading $name $ver …"
  if ! curl -fsSL --retry 2 -o "$file" "https://registry.npmjs.org/$name/-/$name-$ver.tgz"; then
    echo "Stuck downloading $name: no network, or npm unreachable. Check the connection, then run this script again." >&2
    exit 1
  fi
  local got_sha
  got_sha="$(sha_of "$file")"
  if [ "$got_sha" != "$want_sha" ]; then
    echo "Stuck verifying $name: the downloaded file's hash doesn't match — possibly a bad download, possibly a swapped source." >&2
    echo "  Wanted: $want_sha" >&2
    echo "  Got: $got_sha" >&2
    echo "That file was discarded, nothing installed. Don't edit the hash in the script — confirm the source is fine first." >&2
    exit 1
  fi
  mkdir -p "$TMP/$name"
  tar -xzf "$file" -C "$TMP/$name"
}

get_pkg "gsap" "$GSAP_VER" "$GSAP_SHA"
get_pkg "lottie-web" "$LOTTIE_VER" "$LOTTIE_SHA"
get_pkg "canvas-confetti" "$CONFETTI_VER" "$CONFETTI_SHA"

mkdir -p "$VENDOR/gsap"
cp "$TMP/gsap/package/dist/"*.min.js "$VENDOR/gsap/"
cp "$TMP/lottie-web/package/build/player/lottie.min.js" "$VENDOR/lottie.min.js"
# This package's browser build is unminified — use it as is, saved under the name this repo has always used.
cp "$TMP/canvas-confetti/package/dist/confetti.browser.js" "$VENDOR/confetti.browser.min.js"

# Finally, re-check two key files' sizes — a mismatch means the extract or copy went wrong.
check_size() {
  local file="$1" want="$2"
  local got
  got="$(wc -c < "$file" | tr -d ' ')"
  if [ "$got" != "$want" ]; then
    echo "Stuck checking: $file is $got bytes, want $want — mismatch, don't use it yet." >&2
    exit 1
  fi
}
check_size "$VENDOR/gsap/gsap.min.js" "72927"
check_size "$VENDOR/lottie.min.js" "305704"

echo "Installed:"
echo "  GSAP $GSAP_VER: $(ls "$VENDOR/gsap" | wc -l | tr -d ' ') files in $VENDOR/gsap/"
echo "  lottie-web $LOTTIE_VER: $VENDOR/lottie.min.js"
echo "  canvas-confetti $CONFETTI_VER: $VENDOR/confetti.browser.min.js (reference only, not used directly in video making)"
