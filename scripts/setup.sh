#!/bin/bash
# 一键把环境备齐：先查缺什么，再下第三方库，再备好你的配置文件。
# 已经备好的不会动你的：config.yaml 只要存在，就不覆盖。
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "第一步：查环境缺什么"
if ! bash scripts/check-env.sh; then
  echo "先把上面标「缺」的东西装好，再重新跑这个脚本。后面的步先不做了。"
  exit 1
fi

echo
echo "第二步：下第三方库"
if ! bash scripts/fetch-vendor.sh; then
  echo "库没下成，卡在哪上面已经写了。处理完重新跑这个脚本就行，前面的步不会白跑。"
  exit 1
fi

echo
echo "第三步：备配置文件"
if [ -f config.yaml ]; then
  echo "config.yaml 已经有了，没动它。"
elif [ -f config.example.yaml ]; then
  cp config.example.yaml config.yaml
  echo "已经把 config.example.yaml 抄了一份，叫 config.yaml，你改这一份就行。"
else
  echo "没找到 config.example.yaml，这一步跳过。等仓库里有了示例配置，再自己抄一份改名叫 config.yaml。"
fi

echo
echo "都齐了。接下来按这个顺序走："
echo "  1. 打开 SETUP.md，一项一项对着填 config.yaml。每一项填什么、推荐填什么，那里都写了。"
echo "  2. 自动化程度那一项，先选一个再往下走：全自动、发布前人工看一眼、还是只备稿。可以改，不用一次定死。"
echo "  3. 小红书登录只能你本人扫码，步骤在 SETUP.md 里。配好之前，先拿 examples/ 里的虚构示例把流程跑一遍。"
