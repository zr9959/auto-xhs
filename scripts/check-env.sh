#!/bin/bash
# 看一眼做片要用的东西齐不齐。缺什么会用人话说清缺的是哪个、干什么用的。
# 返回值：硬缺（ffmpeg、node、python3、curl、tar 里少任何一个）为 1，其余情况为 0。
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fail=0

have() { command -v "$1" >/dev/null 2>&1; }

if have ffmpeg; then
  echo "ffmpeg 有：$(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f1-3)"
else
  echo "缺 ffmpeg：最后把帧和声音拼成视频靠它，没有它出不了片。先装 ffmpeg 再回来。"
  fail=1
fi

if have ffprobe; then
  echo "ffprobe 有：查视频和音频的时长、尺寸靠它。"
else
  echo "缺 ffprobe：它一般跟 ffmpeg 一起装，装好 ffmpeg 再看看。"
  fail=1
fi

if have node; then
  echo "node 有：$(node --version)，逐帧截图的脚本靠它跑。"
else
  echo "缺 node：逐帧截图靠它。去 nodejs.org 装一个长期支持版再回来。"
  fail=1
fi

if have python3; then
  echo "python3 有：$(python3 --version 2>&1)，验收脚本和配音示例靠它。"
else
  echo "缺 python3：验收脚本跑不了。先装 python3 再回来。"
  fail=1
fi

for cmd in curl tar; do
  if have "$cmd"; then
    echo "$cmd 有：下载第三方库靠它。"
  else
    echo "缺 $cmd：下载第三方库靠它，装上再跑 scripts/fetch-vendor.sh。"
    fail=1
  fi
done

# 截图用的浏览器：优先看环境变量，再看 node 能不能找到 playwright。
if [ -n "${CHROMIUM_PATH:-}" ] && [ -x "${CHROMIUM_PATH:-}" ]; then
  echo "浏览器有：用的是 CHROMIUM_PATH 指的那个。"
elif [ -n "${CHROMIUM_PATH:-}" ]; then
  echo "提醒：CHROMIUM_PATH 写了，但那个路径打不开。截图时会退回用 playwright 自带的浏览器。"
elif have node && node -e "try{require.resolve('playwright');process.exit(0)}catch(e){try{require.resolve('playwright-core');process.exit(0)}catch(e2){process.exit(1)}}" 2>/dev/null; then
  echo "提醒：找到 playwright 包了，但没确认它自带的浏览器下没下。第一次截图前先跑 npx playwright install chromium，把浏览器下好。"
else
  echo "提醒：还没找到 playwright。截图这一步要它：在放 capture.js 的目录里 npm install playwright，再跑 npx playwright install chromium。"
fi

# 第三方库下没下也顺手看一眼，省得做片时才发现。
if [ -f "$ROOT/motion-lib/vendor/gsap/gsap.min.js" ] && [ -f "$ROOT/motion-lib/vendor/lottie.min.js" ]; then
  echo "第三方库有：GSAP 和 lottie-web 都在 motion-lib/vendor/ 里。"
else
  echo "提醒：第三方库还没下。跑一次 bash scripts/fetch-vendor.sh 就行，它会自动下好。"
fi

if [ "$fail" -ne 0 ]; then
  echo "结论：上面标了「缺」的先补上，再接着往下走。"
  exit 1
fi
echo "结论：硬要用的都齐了。标「提醒」的不挡路，按它说的补就行。"
