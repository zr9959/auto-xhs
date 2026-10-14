#!/bin/bash
# 发布前自己先扫一遍：仓库里有没有带进不该带的东西。
# 扫三样：密钥、你填在本地词表里的专属词、写死的本机路径。
# 本地词表叫 privacy-denylist.local.txt，放在仓库根目录，一行一个词。
# 这个文件本身在 .gitignore 里，不会进仓库——词表里写的正是不能公开的词，
# 它要是进了仓库，扫描就白做了。
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FAIL=0

echo "一、扫密钥（gitleaks）"
if command -v gitleaks >/dev/null 2>&1; then
  if gitleaks detect --source . --config .gitleaks.toml --no-banner; then
    echo "gitleaks 扫完，没扫到密钥。"
  else
    echo "gitleaks 报了东西，看上面列的，处理完再扫。"
    FAIL=1
  fi
else
  echo "这台机器上没找到 gitleaks，这一项跳过。发布前务必在有 gitleaks 的机器上补扫一次。"
fi

echo
echo "二、扫专属词（本地词表）"
if [ -f privacy-denylist.local.txt ]; then
  while IFS= read -r word; do
    [ -z "$word" ] && continue
    case "$word" in \#*) continue;; esac
    hits=$(grep -rn --exclude-dir=.git --exclude-dir=data --exclude=privacy-denylist.local.txt -F "$word" . 2>/dev/null | wc -l)
    if [ "$hits" -gt 0 ]; then
      echo "词「$word」在仓库里出现了 $hits 处，处理掉再发。"
      FAIL=1
    fi
  done < privacy-denylist.local.txt
  echo "词表扫完。"
else
  echo "没有 privacy-denylist.local.txt，这一项跳过。"
  echo "发布前把你自己的账号名、账号号、邮箱这类词一行一个写进这个文件，再跑一次。"
fi

echo
echo "三、扫写死的本机路径"
hits=$(grep -rn --exclude-dir=.git --exclude-dir=data -E "/home/[a-z]+/|/Users/[a-z]+/" . 2>/dev/null | grep -v "privacy-scan.sh" | wc -l)
if [ "$hits" -gt 0 ]; then
  grep -rn --exclude-dir=.git --exclude-dir=data -E "/home/[a-z]+/|/Users/[a-z]+/" . 2>/dev/null | grep -v "privacy-scan.sh" | head -10
  echo "上面这些是写死的本机路径，改成相对路径或配置项再发。"
  FAIL=1
else
  echo "没有写死的本机路径。"
fi

echo
if [ "$FAIL" -eq 0 ]; then
  echo "扫完，没发现问题。最后再人工看一遍 README、示例和代码注释，这三处最容易藏真信息。"
else
  echo "有问题，先处理，处理完重新跑这个脚本。"
  exit 1
fi
