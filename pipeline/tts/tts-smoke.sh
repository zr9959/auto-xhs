#!/bin/bash
# 配音开工冒烟：正式合成之前，先拿一句短话试合成，定这一轮用哪个引擎。
#
# 为什么要这一步：配音引擎会悄悄坏（服务挂了、工具被清了、网络不通），
# 等整片合成完才发现没声音，一整轮就白烧了。开工先试一句，一分钟的事。
#
# 用法：bash pipeline/tts/tts-smoke.sh [仓库根目录]
# 读仓库根 config.yaml 的 tts 段两行：
#   command:          主引擎命令，占位 {text} 和 {out}，例：
#                     edge-tts --voice 你的音色 --text "{text}" --write-media "{out}"
#   fallback_command: 备用引擎命令，同样写法。可以不填（那就没有备用）。
# 输出最后一行是结论，写进验收单：
#   LIVE=primary   主引擎通，用主引擎
#   LIVE=fallback  主引擎不通，已切到备用引擎，这一轮用备用
#   LIVE=NONE      两个都不通（退出码 1），按闸口异常停下，把上面的失败输出附进汇报
set -uo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
CFG="$ROOT/config.yaml"
if [ ! -f "$CFG" ]; then
  echo "找不到 $CFG，先照 config.example.yaml 复制一份填好再跑。" >&2
  echo "LIVE=NONE"
  exit 1
fi

mapfile -t CMDS < <(python3 - "$CFG" <<'PYEOF'
import re, sys
in_tts, vals = False, {}
for raw in open(sys.argv[1], encoding="utf-8"):
    if re.match(r"^[A-Za-z]", raw):
        in_tts = raw.startswith("tts:")
        continue
    if in_tts:
        m = re.match(r"\s+(command|fallback_command)\s*:\s*(.*)$", raw)
        if m:
            v = m.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                q = v[0]
                v = v[1:-1]
                if q == '"':
                    v = v.replace('\\"', '"').replace("\\\\", "\\")
            vals[m.group(1)] = v
print(vals.get("command", ""))
print(vals.get("fallback_command", ""))
PYEOF
)
CMD_PRIMARY="${CMDS[0]:-}"
CMD_FALLBACK="${CMDS[1]:-}"

try_engine() {
  # $1=命令模板。成功返回 0：文件生成了、时长也像句话。
  local tmpl="$1" out="$2"
  local cmd="${tmpl//\{text\}/配音测试，一切正常。}"
  cmd="${cmd//\{out\}/$out}"
  rm -f "$out"
  if ! timeout 120 bash -c "$cmd" >"$out.log" 2>&1; then
    echo "试合成失败，命令输出在 $out.log"
    return 1
  fi
  if [ ! -s "$out" ]; then
    echo "命令跑完了但没生成文件，命令输出在 $out.log"
    return 1
  fi
  local dur
  dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out" 2>/dev/null)"
  if [ -z "$dur" ] || ! python3 -c "exit(0 if float('$dur') > 0.3 else 1)" 2>/dev/null; then
    echo "生成的文件时长不对（${dur:-读不出}），多半是坏的"
    return 1
  fi
  echo "试合成通过：$out（${dur} 秒）"
  return 0
}

TMP="$(mktemp -d)"
if [ -z "$CMD_PRIMARY" ]; then
  echo "config.yaml 的 tts.command 没填，先填主引擎命令。" >&2
  echo "LIVE=NONE"
  exit 1
fi

echo "先试主引擎……"
if try_engine "$CMD_PRIMARY" "$TMP/primary.mp3"; then
  echo "LIVE=primary"
  exit 0
fi

if [ -n "$CMD_FALLBACK" ]; then
  echo "主引擎不通，试备用引擎……"
  if try_engine "$CMD_FALLBACK" "$TMP/fallback.mp3"; then
    echo "LIVE=fallback"
    exit 0
  fi
else
  echo "没有配备用引擎（tts.fallback_command 没填）。"
fi

echo "LIVE=NONE"
exit 1
