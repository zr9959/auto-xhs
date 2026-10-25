#!/usr/bin/env python3
"""成片机器验收，只看不改。

用法：python3 core/validate.py <当天素材夹路径>

阈值读仓库根目录的 config.yaml（就是 core 的上一级）。
只认简单的「小节名: 键: 值」写法，不用装任何额外的库。
没有 config.yaml 时用脚本里的推荐默认值，输出第一行会写明。

查这些项：口播字数、post.md 结构、成片规格（顺带看一眼方向和宽高对不对得上）、全片静音、封面、期号，
只提醒不判错的画面检查：最低码率、空白帧、画面冻止（码率与空白帧的来历见 issue #1）、成片大小，
只提醒不判错的文字检查：定稿标题加权字数、正文字数、话题个数、字幕单条长度、标题情绪与锚点，
外加一项旁白码率提示（对一下这期的旁白是不是用定的那个引擎合成的）。
元素溢出画面这一项不做机器检查：抽出来的帧只有像素，分不清「满幅背景」（正常）
和「卡片被裁出画面」（毛病），硬做一个只会天天误报。这一项靠模板规矩防：
同一块区域只许一个带延迟的入场，见 motion-lib/README 的排版规矩。
退出码：有 FAIL 是 1，全过（PASS/WARN）是 0。
数字口径以 core/CONSTITUTION.md 的数字总表为准，两边要一致。
"""

import json
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
    "video.min_bitrate_kbps": 2000,
    "video.blank_min_seconds": 2.0,
    "video.freeze_warn_seconds": 1.0,
    "video.subtitle_max_chars": 38,
    "content.title_max_chars": 20,
    "content.body_max_chars": 1000,
    "content.topics_min": 5,
    "content.topics_max": 8,
    "tts.expected_bitrate_kbps": 0,
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



# ---------- 3b. 成片大小（只提醒不判错） ----------
def check_size(video):
    name = "成片大小"
    if video is None:
        return
    # 老 config.yaml 里可能还没有这个键（CRF 改版后才加），缺了就按 100 算
    cap = float(CFG.get("video.max_size_mb") or 100)
    mb = video.stat().st_size / 1e6
    detail = f"{video.name} {mb:.1f}MB（上限 {cap:.0f}MB）"
    if mb > cap:
        report("WARN", name, detail + "；超了拼片脚本本该自动升 CRF 重拼，人工确认这版是不是最终版")
    else:
        report("PASS", name, detail)


# ---------- 4j. 标题情绪与锚点（只提醒不判错） ----------
def _machine_line(post_text, label):
    # 机读行两种写法都认：「标签：「内容」」或「标签：内容」
    if not post_text:
        return None
    m = re.search(label + r"\s*[:：]\s*「([^」]+)」", post_text)
    if m:
        return m.group(1).strip()
    m = re.search(label + r"\s*[:：]\s*(.+)", post_text)
    return m.group(1).strip() if m else None


def check_emotion_anchor(post_text):
    title = extract_final_title(post_text)
    if not title:
        report("WARN", "标题情绪与锚点", "post.md 里找不到定稿标题，人工核对")
        return
    carrier = _machine_line(post_text, "情绪承载字")
    if not carrier:
        report("WARN", "情绪承载字", "post.md 定稿理由里没有「情绪承载字」机读行，补上再发")
    elif carrier not in title:
        report("WARN", "情绪承载字", f"承载字「{carrier}」不在定稿标题原文里，逐字摘错了，重摘")
    else:
        idx = title.index(carrier)
        w_before = title_weight(title[:idx])
        w_total = title_weight(title)
        if w_before > 10 or w_before > w_total / 2:
            report("WARN", "情绪前置",
                   f"承载短语起点在加权第 {w_before:g} 字（标题共 {w_total:g} 字），情绪吊在后半段了，往前挪")
        else:
            report("PASS", "情绪前置", f"承载短语起点在加权第 {w_before:g} 字，前半段，过")
        report("PASS", "情绪承载字", f"承载字「{carrier}」在标题原文里")
    link = _machine_line(post_text, "情绪关联")
    if not link:
        report("WARN", "情绪关联", "post.md 定稿理由里没有「情绪关联」机读行（格式：具体事实 → 夸张短语），补上再发")
    elif "→" not in link:
        report("WARN", "情绪关联", "「情绪关联」行里没有 → ，格式写成「具体事实 → 夸张短语」")
    else:
        phrase = link.split("→", 1)[1].strip()
        if phrase and phrase not in title:
            report("WARN", "情绪关联", f"关联行箭头右侧「{phrase}」不在定稿标题里，对不上")
        else:
            report("PASS", "情绪关联", "关联行齐全，右侧短语在标题里")
    anchor = _machine_line(post_text, "标题锚点")
    if not anchor:
        report("WARN", "标题锚点", "post.md 里没有「标题锚点」机读行，写稿第 0 步先定锚点")
    elif anchor not in title:
        report("WARN", "标题锚点", f"锚点「{anchor}」没有逐字出现在定稿标题里，标题跑偏了")
    else:
        report("PASS", "标题锚点", f"锚点「{anchor}」逐字在标题里")


# ---------- 5b. 封面 AI 来源（只提醒不判错） ----------
def check_cover_ai(folder, post_text):
    name = "封面 AI 来源"
    if not post_text or "封面主视觉：AI生成" not in post_text:
        report("WARN", name, "验收单或 post.md 里没有「封面主视觉：AI生成」机读行；用 AI 主视觉时补上这一行")
        return
    srcs = [p for p in folder.glob("ai*") if p.suffix.lower() in (".jpg", ".jpeg", ".png")] \
        + [p for p in folder.glob("*media-generation-*") if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
    if not srcs:
        report("WARN", name, "写了 AI 生成，但素材夹里找不到带 ai 或 media-generation- 前缀的源图，留证缺了")
    else:
        report("PASS", name, f"AI 源图在素材夹里：{srcs[0].name}")

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


# ---------- 4b. 最低码率（只提醒不判错） ----------
def check_bitrate(video):
    name = "最低码率"
    if video is None:
        report("WARN", name, "无成片可测，跳过")
        return
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=bit_rate",
             "-show_entries", "format=bit_rate,duration",
             "-of", "json", str(video)])
    kbps = None
    try:
        info = json.loads(r.stdout or "{}")
        streams = info.get("streams") or [{}]
        raw = streams[0].get("bit_rate")
        if raw:
            kbps = int(raw) / 1000.0
        else:
            # 个别编码不写流码率，就拿整个文件的码率近似（会略高一点，只作提醒够用）
            fmt = info.get("format") or {}
            if fmt.get("bit_rate"):
                kbps = int(fmt["bit_rate"]) / 1000.0
    except Exception:
        kbps = None
    if kbps is None:
        report("WARN", name, "ffprobe 读不到码率，跳过（只提醒的检查，读不到不判错）")
        return
    floor = num("video.min_bitrate_kbps")
    detail = f"视频流约 {kbps:.0f} kb/s（下限 {floor:.0f} kb/s）"
    if kbps < floor:
        report("WARN", name, detail + "；码率偏低，字边容易糊，平台再转码一次会更糊。"
                                   "拼片时把码率地板加上（见 pipeline/assemble.sh）")
    else:
        report("PASS", name, detail)


# ---------- 4c. 空白帧（只提醒不判错） ----------
# 判据（在天气预报好成品和空白样本上实测标定过，2026-10-18）：
# 每 0.5 秒抽一帧，缩到 96x96 灰度图，每 4 个像素取 1 个算直方图。
# 一帧里若有 98% 以上的像素都挤在中位灰度 ±10 以内、且整体方差 <= 100，
# 就算「近乎无内容」：纯色帧方差 0、覆盖 1.0；只有一行标题的帧方差约 25、覆盖约 0.99；
# 正常成片的帧方差 288 起步、覆盖最高约 0.76，两边离得很远，不容易误报。
BLANK_FPS = 2
BLANK_SIZE = 96
BLANK_COVERAGE = 0.98
BLANK_VAR_MAX = 100.0


def _frame_is_blank(fr):
    n = len(fr)
    if n == 0:
        return False
    hist = [0] * 256
    for b in fr:
        hist[b] += 1
    mean = sum(v * hist[v] for v in range(256)) / n
    var = sum(hist[v] * (v - mean) ** 2 for v in range(256)) / n
    if var > BLANK_VAR_MAX:
        return False
    acc = 0
    med = 0
    for v in range(256):
        acc += hist[v]
        if acc >= n // 2:
            med = v
            break
    cov = sum(hist[max(0, med - 10): med + 11]) / n
    return cov >= BLANK_COVERAGE


def check_blank_frames(video):
    name = "空白帧"
    if video is None:
        report("WARN", name, "无成片可测，跳过")
        return
    frame_bytes = BLANK_SIZE * BLANK_SIZE
    # run() 用 text=True 会把二进制帧读坏，这里单独用二进制方式跑
    proc = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video),
                           "-vf", f"fps={BLANK_FPS},scale={BLANK_SIZE}:{BLANK_SIZE},format=gray",
                           "-f", "rawvideo", "-"], capture_output=True, timeout=600)
    data = proc.stdout or b""
    if len(data) < frame_bytes:
        report("WARN", name, "抽不到帧，跳过（只提醒的检查，测不了不判错）")
        return
    step = 1.0 / BLANK_FPS
    blanks = []
    for off in range(0, len(data) - frame_bytes + 1, frame_bytes):
        frame = data[off:off + frame_bytes]
        blanks.append(_frame_is_blank(frame[::4]))
    longest = 0
    longest_start = 0
    cur = 0
    cur_start = 0
    for i, b in enumerate(blanks):
        if b:
            if cur == 0:
                cur_start = i
            cur += 1
            if cur > longest:
                longest, longest_start = cur, cur_start
        else:
            cur = 0
    longest_seconds = longest * step
    limit = num("video.blank_min_seconds")
    detail = (f"每 {step:.1f}s 抽一帧共 {len(blanks)} 帧，最长连续近乎空白 "
              f"{longest_seconds:.1f}s（标准：不超过 {limit:.1f}s，只提醒）")
    if longest_seconds >= limit and longest > 0:
        start = longest_start * step
        report("WARN", name, detail +
               f"；超标段约在 {start:.1f}–{start + longest_seconds:.1f}s，"
               "多半是场景时长按配音定、动画先演完了，剩下几秒画面没东西。"
               "把那段动画补满，或把场景时长改短")
    else:
        report("PASS", name, detail)


# ---------- 4d. 画面冻止（只提醒不判错） ----------
def check_freeze(video):
    name = "画面冻止"
    if video is None:
        report("WARN", name, "无成片可测，跳过")
        return
    limit = num("video.freeze_warn_seconds")
    r = run(["ffmpeg", "-nostats", "-i", str(video),
             "-vf", f"freezedetect=n=0.003:d={limit}", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"freeze_end: ([\d.]+)", r.stderr)]
    spans = [(s, e) for s, e in zip(starts, ends) if e - s >= limit]
    if len(starts) > len(ends):
        spans.append((starts[-1], -1))  # 冻到片尾的那段没有结束时间
    # 间隔不到 1 秒的相邻静止段并成一段：中间那点微动多半是字幕切换或背景漂移，
    # 不并的话段数虚高，看着吓人，实际是同一段静止
    merged = []
    for s, e in spans:
        if merged and merged[-1][1] >= 0 and s - merged[-1][1] < 1.0:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    spans = merged
    if not spans:
        report("PASS", name, f"没有 ≥{limit:.0f}s 的静止段")
        return
    desc = "、".join(f"{s:.1f}–{e:.1f}s" if e >= 0 else f"{s:.1f}s–片尾"
                     for s, e in spans[:3])
    report("WARN", name,
           f"有 {len(spans)} 段画面静止 ≥{limit:.0f}s：{desc}。"
           "先对照抽帧看：是合法的静态信息卡，还是动画演完了、转场卡住了。"
           "后一种要回做片改，别直接放行")


# ---------- 4e. 定稿标题加权字数（只提醒不判错） ----------
def title_weight(title):
    # 加权口径：中文与全角标点 1 字，英文字母、数字、半角符号 0.5 字，emoji 1 字
    w = 0.0
    for ch in title:
        if ch.isspace():
            continue
        w += 0.5 if ord(ch) < 128 else 1.0
    return w


def extract_final_title(post_text):
    if not post_text:
        return None
    m = re.search(r"定稿标题\s*[:：]\s*(.+)", post_text)
    if m:
        return m.group(1).strip().strip("《》\"'` ")
    # 找单独的「## 标题」一节，取它下面第一行非空文字
    lines = post_text.splitlines()
    capture = False
    for ln in lines:
        if ln.startswith("## "):
            capture = re.fullmatch(r"##\s*标题\s*", ln.strip()) is not None
            continue
        if capture and ln.strip():
            return ln.strip().strip("《》\"'` ")
    return None


def check_title(post_text):
    name = "标题加权字数"
    title = extract_final_title(post_text)
    if not title:
        report("WARN", name, "post.md 里找不到定稿标题，人工核对（只提醒的检查）")
        return
    w = title_weight(title)
    cap = num("content.title_max_chars")
    detail = f"定稿标题《{title}》加权 {w:g} 字（上限 {cap:.0f} 字）"
    if w > cap:
        report("WARN", name, detail + "；超了平台上限，先改短再发")
    else:
        report("PASS", name, detail)


# ---------- 4f. 正文字数（只提醒不判错） ----------
def check_body(post_text):
    name = "正文字数"
    if not post_text:
        report("WARN", name, "没有 post.md 可测，跳过")
        return
    body = section(post_text, "正文")
    if body is None:
        report("WARN", name, "post.md 里找不到正文段，人工核对")
        return
    n = len(re.sub(r"\s", "", body))
    cap = int(num("content.body_max_chars"))
    detail = f"正文 {n} 字（上限 {cap} 字）"
    if n > cap:
        report("WARN", name, detail + "；超上限了，删到限内再发")
    else:
        report("PASS", name, detail)


# ---------- 4g. 话题个数（只提醒不判错） ----------
def check_topics(post_text):
    name = "话题个数"
    if not post_text:
        report("WARN", name, "没有 post.md 可测，跳过")
        return
    sec = section(post_text, "话题")
    if sec is None:
        report("WARN", name, "post.md 里找不到话题段，人工核对")
        return
    items = []
    for ln in sec.splitlines():
        ln = ln.strip().lstrip("-*").strip()
        if not ln or ln.startswith("（") or ln.startswith("("):
            continue
        items += [t.strip() for t in re.split(r"[、，,；;\s]+", ln) if t.strip()]
    lo, hi = int(num("content.topics_min")), int(num("content.topics_max"))
    detail = f"话题段数到 {len(items)} 个（标准 {lo}–{hi} 个）"
    if lo <= len(items) <= hi:
        report("PASS", name, detail)
    else:
        report("WARN", name, detail + "；个数不在标准内，发之前对一下计划")


# ---------- 4h. 字幕单条长度（只提醒不判错） ----------
def check_subtitle_len(folder):
    name = "字幕单条长度"
    cand = sorted(folder.glob("scripts*.txt")) or sorted(folder.glob("script*.txt"))
    if not cand:
        report("WARN", name, "找不到 scripts.txt，跳过")
        return
    cap = int(num("video.subtitle_max_chars"))
    worst, worst_seg = 0, ""
    for line in cand[0].read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        text = line.split("|", 1)[1] if "|" in line else line
        seg_name = line.split("|", 1)[0] if "|" in line else "?"
        for piece in re.split(r"[。！？!?；;，、：…]+", text):
            piece = re.sub(r"\s", "", piece)
            if len(piece) > worst:
                worst, worst_seg = len(piece), seg_name
    if worst > cap:
        report("WARN", name,
               f"最长一条字幕 {worst} 字（{worst_seg} 段，上限 {cap} 字）；"
               "这么长排进画面要挤成 3 行。回写稿阶段把这句断成两条，别留给做片返工")
    else:
        report("PASS", name, f"最长一条字幕 {worst} 字（上限 {cap} 字）")


# ---------- 4i. 旁白码率提示（只提醒，永不判错） ----------
def check_narration(folder):
    name = "旁白码率"
    cands = sorted(folder.glob("audio/*.mp3")) + sorted(folder.glob("n-*.mp3"))
    if not cands:
        return  # 素材夹里没留旁白源文件，这项就不出声
    f = cands[0]
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=bit_rate",
             "-of", "csv=p=0", str(f)])
    try:
        kbps = int(r.stdout.strip().split(",")[0]) / 1000.0
    except (ValueError, IndexError):
        report("WARN", name, f"{f.name} 的码率读不出来，人工确认")
        return
    expect = num("tts.expected_bitrate_kbps")
    if expect > 0 and abs(kbps - expect) / expect > 0.25:
        report("WARN", name,
               f"{f.name} 约 {kbps:.0f} kb/s，跟预期的约 {expect:.0f} kb/s 对不上；"
               "多半是这期换了配音引擎或参数，确认是有意换的再往下走")
    elif expect > 0:
        report("PASS", name, f"{f.name} 约 {kbps:.0f} kb/s，与预期 {expect:.0f} kb/s 对得上")
    else:
        report("PASS", name,
               f"{f.name} 约 {kbps:.0f} kb/s（config 里没填预期码率，只记录数值；"
               "想让这项能报警，把 tts.expected_bitrate_kbps 填上）")


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
    check_title(post_text)
    check_body(post_text)
    check_topics(post_text)
    check_subtitle_len(folder)
    video = check_video(folder, post_text)
    check_size(video)
    check_silence(video)
    check_bitrate(video)
    check_blank_frames(video)
    check_freeze(video)
    check_narration(folder)
    check_emotion_anchor(post_text)
    check_cover(folder)
    check_cover_ai(folder, post_text)
    check_issue(folder, post_text)
    fails = [r for r in RESULTS if r[0] == "FAIL"]
    warns = [r for r in RESULTS if r[0] == "WARN"]
    print(f"结论：FAIL {len(fails)} 项，WARN {len(warns)} 项，"
          f"PASS {len(RESULTS) - len(fails) - len(warns)} 项")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
