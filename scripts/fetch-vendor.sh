#!/bin/bash
# 把做片要用的第三方库下载到 motion-lib/vendor/。
# 版本在下面写死了，下载完会核对压缩包的哈希，哈希对不上就停，不会把坏文件留下。
# 库的清单和许可证看 motion-lib/vendor/README.md。
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
    echo "缺 $cmd，先装上它再跑这个脚本。" >&2
    exit 1
  fi
done

sha_of() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | awk '{print $1}';
  else shasum -a 256 "$1" | awk '{print $1}'; fi
}

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# 下一个包，核对哈希，打印卡在哪一步。
get_pkg() {
  local name="$1" ver="$2" want_sha="$3"
  local file="$TMP/$name-$ver.tgz"
  echo "下载 $name $ver …"
  if ! curl -fsSL --retry 2 -o "$file" "https://registry.npmjs.org/$name/-/$name-$ver.tgz"; then
    echo "卡在下载 $name：网不通，或者 npm 那边连不上。检查网络后重新跑这个脚本。" >&2
    exit 1
  fi
  local got_sha
  got_sha="$(sha_of "$file")"
  if [ "$got_sha" != "$want_sha" ]; then
    echo "卡在校验 $name：下载到的文件哈希对不上，可能是下坏了，也可能源被换了。" >&2
    echo "  想要的：$want_sha" >&2
    echo "  实际的：$got_sha" >&2
    echo "这个文件已经扔掉，没有装。先别改脚本里的哈希，确认来源没问题再说。" >&2
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
# 这个包装里的浏览器版没压缩，就用它，文件名按库里一直用的名字放。
cp "$TMP/canvas-confetti/package/dist/confetti.browser.js" "$VENDOR/confetti.browser.min.js"

# 最后再核对两个关键文件的大小，大小不对说明解压或拷贝出了问题。
check_size() {
  local file="$1" want="$2"
  local got
  got="$(wc -c < "$file" | tr -d ' ')"
  if [ "$got" != "$want" ]; then
    echo "卡在检查：$file 大小是 $got，想要 $want，对不上，先别用。" >&2
    exit 1
  fi
}
check_size "$VENDOR/gsap/gsap.min.js" "72927"
check_size "$VENDOR/lottie.min.js" "305704"

echo "装好了："
echo "  GSAP $GSAP_VER：$VENDOR/gsap/ 下 $(ls "$VENDOR/gsap" | wc -l | tr -d ' ') 个文件"
echo "  lottie-web $LOTTIE_VER：$VENDOR/lottie.min.js"
echo "  canvas-confetti $CONFETTI_VER：$VENDOR/confetti.browser.min.js（只作参考，做片不直接用它）"
