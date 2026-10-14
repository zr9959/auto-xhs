#!/usr/bin/env python3
"""成片机器验收，只看不改。

用法：python3 core/validate.py <当天素材夹路径>

阈值读仓库根目录的 config.yaml（就是 core 的上一级）。
只认简单的「小节名: 键: 值」写法，不用装任何额外的库。
没有 config.yaml 时用脚本里的推荐默认值，输出第一行会写明。

查六项：口播字数、post.md 结构、成片规格（顺带看一眼方向和宽高对不对得上）、全片静音、封面、期号。
退出码：有 FAIL 是 1，全过（PASS/WARN）是 0。
数字口径以 core/CONSTITUTION.md 的数字总表为准，两边要一致。
"""

import re
import subprocess
import sys
from pathlib import Path

# 推荐默认值，跟宪法页数字总表一致。config 里填了的，以 config 为准。
DEFAULTS = {
    "video.script_chars_min": 480,
    "video.script_chars_max": 650,
    "video.orientation": "portrait",
    "video.width": 1080,
    "video.height": 1920,
    "video.duration_min_seconds": 80,
    "video.duration_max_seconds": 110,
    "video.codec": "h264",
    "video.cover_width": 1080,
    "video.cover_height": 1440,
    "audio.silence_threshold_db": -45,
    "audio.silence_window_seconds": 1.5,
    "audio.silence_max_gap_seconds": 2.0,
    "paths.ledger_file": "data/ledger.md",
    "publish.issue_required_from": "",
}

RESULTS = []


def report(status, name, detail):
    RESULTS.append((status, name, detail))
    print(f"[{status}] {name}: {detail}")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=600)


# ---------- 读 config ----------
def parse_scalar(val):
    # 先把行尾注释去掉：一个字一个字看，引号里面的 # 不算注释。
    # 以前图省事，引号开头的就整行不切，结果「"路径" # 注释」会把注释
    # 一起当成值，路径就成了废的，这里改对。
    out = []
    quote = ""
    for ch in val:
        if quote:
            out.append(ch)
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
            out.append(ch)
        elif ch == "#":
            break
        else:
            out.append(ch)
    val = "".join(out).strip()
    if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
        return val[1:-1]
    low = val.lower()
    if low in ("true", "false"):
        return low == "true"
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        return val


def parse_simple_yaml(text):
    # 只够读这套 config 的小节缩进结构，列表之类的复杂写法不认
    root = {}
    stack = [(-1, root)]
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        key, _, val = stripped.partition(":")
        key = key.strip().strip("\"'")
        val = val.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if val == "":
            node = {}
            parent[key] = node
            stack.append((indent, node))
        else:
            parent[key] = parse_scalar(val)
    return root


def load_settings():
    repo_root = Path(__file__).resolve().parent.parent
    cfg_file = repo_root / "config.yaml"
    settings = dict(DEFAULTS)
    if not cfg_file.exists():
        return settings, repo_root, False
    parsed = parse_simple_yaml(cfg_file.read_text(encoding="utf-8"))

    def walk(node, prefix):
        for k, v in node.items():
            dotted = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                walk(v, dotted)
            elif dotted in settings:
                settings[dotted] = v

    walk(parsed, "")
    # 台账路径有人会写 ledger 也有人会写 ledger_file，两个都认
    ledger_alt = parsed.get("paths", {})
    if isinstance(ledger_alt, dict) and "ledger" in ledger_alt:
        settings["paths.ledger_file"] = ledger_alt["ledger"]
    return settings, repo_root, True


CFG, REPO_ROOT, CFG_FOUND = load_settings()


def num(key):
    return float(CFG[key])


# ---------- 1. 口播字数 ----------
def check_scripts(folder):
    name = "口播字数"
    cand = sorted(folder.glob("scripts*.txt")) or sorted(folder.glob("script*.txt"))
    if not cand:
        report("FAIL", name, "找不到 scripts.txt")
        return
    f = cand[0]
    total = 0
    segs = 0
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        # 一行一段，竖线前是段名，后面才是口播文字
        text = line.split("|", 1)[1] if "|" in line else line
        total += len(re.sub(r"\s", "", text))
        segs += 1
    lo, hi = int(num("video.script_chars_min")), int(num("video.script_chars_max"))
    ok = lo <= total <= hi
    report("PASS" if ok else "FAIL", name,
           f"{f.name} 共 {segs} 段，合计 {total} 字（标准 {lo}–{hi}）")


# ---------- 2. post.md 结构 ----------
def section(text, *titles):
    lines = text.splitlines()
    out, capture = [], False
    for ln in lines:
        if ln.startswith("## "):
            capture = any(t in ln for t in titles)
            continue
        if capture:
            out.append(ln)
    body = "\n".join(out).strip()
    return body if body else None


def check_postmd(folder):
    name = "post.md 结构"
    f = folder / "post.md"
    if not f.exists():
        report("FAIL", name, "post.md 不存在")
        return None
    text = f.read_text(encoding="utf-8")
    missing = []
    if not (re.search(r"标题三版|三版标题", text) or ("①" in text and "②" in text and "③" in text)):
        missing.append("3 版标题")
    if section(text, "标题") is None and not re.search(r"^##\s*标题", text, re.M):
        missing.append("定稿标题段")
    if section(text, "正文") is None:
        missing.append("正文段")
    if section(text, "话题") is None:
        missing.append("话题段")
    if section(text, "置顶评论", "第一条评论", "首评") is None:
        missing.append("置顶评论段")
    if "素材清单" not in text:
        missing.append("素材清单")
    if missing:
        report("FAIL", name, "缺：" + "、".join(missing))
    else:
        report("PASS", name, "3 版标题/定稿标题/正文/话题段/置顶评论段/素材清单齐全")
    return text


# ---------- 挑成片 ----------
def pick_video(folder, post_text):
    # 先认 post.md 里写明的成片名，找不到再挑最大的 mp4（跳过样片和预览）
    if post_text:
        for m in re.finditer(r"([\w.\-]+\.mp4)", post_text):
            p = folder / m.group(1)
            if p.exists():
                return p
    mp4s = [p for p in folder.glob("*.mp4")
            if "sample" not in p.name.lower() and "preview" not in p.name.lower()]
    if not mp4s:
        return None
    return max(mp4s, key=lambda p: p.stat().st_size)


# ---------- 3. 成片规格 ----------
def check_video(folder, post_text):
    name = "成片规格"
    v = pick_video(folder, post_text)
    if v is None:
        report("FAIL", name, "素材夹里找不到成片 mp4")
        return None
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=codec_name,width,height",
             "-show_entries", "format=duration", "-of", "csv=p=0", str(v)])
    parts = [x.strip() for x in r.stdout.replace("\n", ",").split(",") if x.strip()]
    codec = parts[0] if len(parts) > 0 else "?"
    w = parts[1] if len(parts) > 1 else "?"
    h = parts[2] if len(parts) > 2 else "?"
    try:
        dur = float(parts[3]) if len(parts) > 3 else -1
    except ValueError:
        dur = -1
    want_codec = str(CFG["video.codec"]).lower()
    want_w, want_h = int(num("video.width")), int(num("video.height"))
    d_lo, d_hi = num("video.duration_min_seconds"), num("video.duration_max_seconds")
    problems = []
    if codec.lower() != want_codec:
        problems.append(f"编码 {codec}≠{want_codec}")
    if (w, h) != (str(want_w), str(want_h)):
        problems.append(f"分辨率 {w}x{h}≠{want_w}x{want_h}")
    if not (d_lo <= dur <= d_hi):
        problems.append(f"时长 {dur:.1f}s 不在 {d_lo:.0f}–{d_hi:.0f}")
    detail = (f"{v.name}：{codec} {w}x{h}，时长 {dur:.1f}s"
              f"（标准 {want_w}x{want_h}/{want_codec}/{d_lo:.0f}–{d_hi:.0f}s）")
    report("FAIL" if problems else "PASS", name,
           detail + ("；问题：" + "、".join(problems) if problems else ""))
    # 方向也要跟宽高对得上：选了横版，宽就该大于高；选了竖版，高就该大于等于宽。
    # 对不上多半是改方向时漏改了宽高，只提醒不判错——宽高对不对，
    # 上面那项已经按 config 验过了。
    ori = str(CFG["video.orientation"]).lower()
    if ori == "landscape" and not want_w > want_h:
        report("WARN", "画面方向",
               f"方向选的是横版（landscape），可宽高填的是 {want_w}x{want_h}，"
               "横版应该宽大于高。把 width 改成 1920、height 改成 1080 就对了。")
    elif ori == "portrait" and not want_h >= want_w:
        report("WARN", "画面方向",
               f"方向选的是竖版（portrait），可宽高填的是 {want_w}x{want_h}，"
               "竖版应该高大于等于宽。把 width 改成 1080、height 改成 1920 就对了。")
    return v


# ---------- 4. 静音检测 ----------
def check_silence(video):
    name = "全片静音"
    if video is None:
        report("FAIL", name, "无成片可测")
        return
    db = num("audio.silence_threshold_db")
    db = -abs(db)  # config 里写 45 或 -45 都按 -45dB 算
    win = num("audio.silence_window_seconds")
    max_gap = num("audio.silence_max_gap_seconds")
    r = run(["ffmpeg", "-nostats", "-i", str(video),
             "-af", f"silencedetect=noise={db:.0f}dB:d={win}", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    durs = [e - s for s, e in zip(starts, ends)]
    mx = max(durs) if durs else 0.0
    over = [d for d in durs if d > max_gap]
    detail = (f"阈值 {db:.0f}dB/{win}s，共 {len(durs)} 段静音，最长 {mx:.2f}s"
              f"（标准：无 >{max_gap:.0f}s 静音段）")
    if len(starts) > len(ends):
        # 片尾那段静音没有结束时间，长度算不准，只提示不判错
        detail += "；另有 1 段片尾静音未闭合，未计入"
    report("FAIL" if over else "PASS", name,
           detail + (f"；超标段 {len(over)} 个" if over else ""))


# ---------- 5. 封面 ----------
def check_cover(folder):
    name = "封面"
    cands = sorted(folder.glob("cover*.jpg")) + sorted(folder.glob("cover*.png")) \
        + sorted(folder.glob("封面*.jpg")) + sorted(folder.glob("封面*.png"))
    if not cands:
        report("FAIL", name, "找不到 cover 封面图")
        return
    f = cands[0]
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0", str(f)])
    wh = r.stdout.strip().split(",")
    w, h = (wh + ["?", "?"])[:2]
    want_w, want_h = int(num("video.cover_width")), int(num("video.cover_height"))
    ok = (w, h) == (str(want_w), str(want_h))
    report("PASS" if ok else "FAIL", name,
           f"{f.name}：{w}x{h}（标准 {want_w}x{want_h}）")


# ---------- 6. 期号 ----------
def check_issue(folder, post_text):
    name = "期号"
    m = re.search(r"(\d{4}-\d{2}-\d{2})", folder.name)
    if not m:
        report("WARN", name, f"素材夹名 {folder.name} 里看不出日期，跳过核对")
        return
    date = m.group(1)
    epoch = str(CFG["publish.issue_required_from"] or "")
    # 没填强制起始日就不判错，只提醒；填了就从那天起算强制
    strict = bool(epoch) and date >= epoch
    ledger = Path(str(CFG["paths.ledger_file"])).expanduser()
    if not ledger.is_absolute():
        ledger = REPO_ROOT / ledger
    seq = None
    if ledger.exists():
        rows = [ln for ln in ledger.read_text(encoding="utf-8").splitlines()
                if re.match(r"\|\s*20\d{2}-\d{2}-\d{2}\s*\|", ln)]
        for i, ln in enumerate(rows, 1):
            if ln.split("|")[1].strip() == date:
                seq = i
                break
    recorded = None
    if post_text:
        mm = re.search(r"第\s*(\d+)\s*期", post_text)
        if mm:
            recorded = int(mm.group(1))
    if seq is None:
        report("WARN", name, f"台账里查无 {date} 条目，无法核对期号")
        return
    if recorded is None:
        report("FAIL" if strict else "WARN", name,
               f"post.md 未记录期号；台账序号为第 {seq} 期"
               + ("（已到强制起始日，缺失判 FAIL）" if strict
                  else "（未设强制起始日，只提醒）"))
        return
    if recorded != seq:
        report("FAIL" if strict else "WARN", name,
               f"post.md 记第 {recorded} 期，台账序号为第 {seq} 期，不一致")
    else:
        report("PASS", name, f"post.md 与台账一致：第 {seq} 期")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    folder = Path(sys.argv[1]).expanduser()
    if not folder.is_dir():
        print(f"素材夹不存在：{folder}")
        return 2
    if CFG_FOUND:
        print("配置：用了仓库根的 config.yaml")
    else:
        print("配置：没找到仓库根的 config.yaml，用内置推荐默认值")
    print(f"验收对象：{folder}")
    check_scripts(folder)
    post_text = check_postmd(folder)
    video = check_video(folder, post_text)
    check_silence(video)
    check_cover(folder)
    check_issue(folder, post_text)
    fails = [r for r in RESULTS if r[0] == "FAIL"]
    warns = [r for r in RESULTS if r[0] == "WARN"]
    print(f"结论：FAIL {len(fails)} 项，WARN {len(warns)} 项，"
          f"PASS {len(RESULTS) - len(fails) - len(warns)} 项")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
