#!/usr/bin/env python3
"""Machine acceptance for the finished video — read-only, it never edits.

Usage: python3 core/validate.py <day's material folder path>

Thresholds come from the repo-root config.yaml (one level above core).
Only the simple "section: key: value" form is recognized — no extra libraries needed.
Without a config.yaml, the script's built-in recommended defaults apply, and the first output line says so.

Checks: voiceover character count, post.md structure, finished-video specs (including whether orientation
matches the dimensions), whole-video silence, cover, issue number;
warn-only picture checks: minimum bitrate, blank frames, frozen frames (bitrate and blank frames come from issue #1),
finished-video size;
warn-only text checks: final title weighted length, body length, topic count, single subtitle length, title emotion and anchor;
plus a narration bitrate note (checking whether this episode's narration came from the designated voice engine).
Element overflow is not machine-checked: sampled frames are just pixels — they can't tell a "full-bleed background" (fine)
from a "card cropped out of frame" (a defect), and a hard check would false-alarm daily. That one is prevented
by template rules instead: only one delayed entrance per area — see the layout rules in motion-lib/README.
Exit code: 1 if any FAIL, 0 if everything is PASS/WARN.
All numbers follow the numbers table in core/CONSTITUTION.md — the two must agree.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

# Recommended defaults, matching the numbers table in the constitution page. Values in config win.
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


# ---------- read config ----------
def parse_scalar(val):
    # Strip trailing comments, one character at a time: a # inside quotes is not a comment.
    # An earlier shortcut skipped cutting any line starting with a quote, so `"path" # comment`
    # kept the comment as part of the value and broke the path — fixed here.
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
    # Only enough to read this config's indented section structure; lists and other complex forms are not recognized.
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
    # The ledger path may be written as ledger or ledger_file — accept both.
    ledger_alt = parsed.get("paths", {})
    if isinstance(ledger_alt, dict) and "ledger" in ledger_alt:
        settings["paths.ledger_file"] = ledger_alt["ledger"]
    return settings, repo_root, True


CFG, REPO_ROOT, CFG_FOUND = load_settings()


def num(key):
    return float(CFG[key])


# ---------- 1. voiceover character count ----------
def check_scripts(folder):
    name = "Voiceover chars"
    cand = sorted(folder.glob("scripts*.txt")) or sorted(folder.glob("script*.txt"))
    if not cand:
        report("FAIL", name, "scripts.txt not found")
        return
    f = cand[0]
    total = 0
    segs = 0
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        # One segment per line: the part before | is the segment name, the rest is the voiceover text.
        text = line.split("|", 1)[1] if "|" in line else line
        total += len(re.sub(r"\s", "", text))
        segs += 1
    lo, hi = int(num("video.script_chars_min")), int(num("video.script_chars_max"))
    ok = lo <= total <= hi
    report("PASS" if ok else "FAIL", name,
           f"{f.name}: {segs} segments, {total} chars total (standard {lo}–{hi})")


# ---------- 2. post.md structure ----------
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
    name = "post.md structure"
    f = folder / "post.md"
    if not f.exists():
        report("FAIL", name, "post.md not found")
        return None
    text = f.read_text(encoding="utf-8")
    missing = []
    if not (re.search(r"标题三版|三版标题", text) or ("①" in text and "②" in text and "③" in text)):
        missing.append("3 title versions")
    if section(text, "标题") is None and not re.search(r"^##\s*标题", text, re.M):
        missing.append("final title section")
    if section(text, "正文") is None:
        missing.append("body section")
    if section(text, "话题") is None:
        missing.append("topics section")
    if section(text, "置顶评论", "第一条评论", "首评") is None:
        missing.append("pinned comment section")
    if "素材清单" not in text:
        missing.append("material list")
    if missing:
        report("FAIL", name, "Missing: " + ", ".join(missing))
    else:
        report("PASS", name, "3 title versions / final title / body / topics / pinned comment / material list all present")
    return text


# ---------- pick the finished video ----------
def pick_video(folder, post_text):
    # First honor the finished-video name written in post.md; otherwise pick the largest mp4 (skip samples and previews).
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


# ---------- 3. finished video specs ----------
def check_video(folder, post_text):
    name = "Video specs"
    v = pick_video(folder, post_text)
    if v is None:
        report("FAIL", name, "No finished mp4 in the material folder")
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
        problems.append(f"codec {codec}≠{want_codec}")
    if (w, h) != (str(want_w), str(want_h)):
        problems.append(f"resolution {w}x{h}≠{want_w}x{want_h}")
    if not (d_lo <= dur <= d_hi):
        problems.append(f"duration {dur:.1f}s outside {d_lo:.0f}–{d_hi:.0f}")
    detail = (f"{v.name}: {codec} {w}x{h}, {dur:.1f}s"
              f"(standard {want_w}x{want_h}/{want_codec}/{d_lo:.0f}–{d_hi:.0f}s)")
    report("FAIL" if problems else "PASS", name,
           detail + ("; problems: " + ", ".join(problems) if problems else ""))
    # Orientation must also match the dimensions: landscape means width greater than height;
    # portrait means height greater than or equal to width. A mismatch usually means the
    # dimensions weren't updated when the orientation changed — warn only, since the item
    # above already checks dimensions against config.
    ori = str(CFG["video.orientation"]).lower()
    if ori == "landscape" and not want_w > want_h:
        report("WARN", "Orientation",
               f"Orientation is landscape, but dimensions are {want_w}x{want_h}; "
               "landscape needs width greater than height. Set width to 1920 and height to 1080.")
    elif ori == "portrait" and not want_h >= want_w:
        report("WARN", "Orientation",
               f"Orientation is portrait, but dimensions are {want_w}x{want_h}; "
               "portrait needs height greater than or equal to width. Set width to 1080 and height to 1920.")
    return v



# ---------- 3b. finished video size (warn only) ----------
def check_size(video):
    name = "Video size"
    if video is None:
        return
    # Older config.yaml files may not have this key (added in the CRF change) — default to 100 when missing.
    cap = float(CFG.get("video.max_size_mb") or 100)
    mb = video.stat().st_size / 1e6
    detail = f"{video.name} {mb:.1f}MB (cap {cap:.0f}MB)"
    if mb > cap:
        report("WARN", name, detail + "; over the cap — the assemble script should have auto-raised CRF and re-encoded; confirm by hand whether this is the final cut")
    else:
        report("PASS", name, detail)


# ---------- 4j. title emotion and anchor (warn only) ----------
def _machine_line(post_text, label):
    # Machine lines accept two forms: label: 「content」 or label: content
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
        report("WARN", "Title emotion and anchor", "No final title found in post.md — check by hand")
        return
    carrier = _machine_line(post_text, "情绪承载字")
    if not carrier:
        report("WARN", "情绪承载字", "post.md has no 「情绪承载字」 machine line in the final-title rationale — add it before publishing")
    elif carrier not in title:
        report("WARN", "情绪承载字", f"Carrier 「{carrier}」 is not in the final title text — copied wrong, pick it character by character again")
    else:
        idx = title.index(carrier)
        w_before = title_weight(title[:idx])
        w_total = title_weight(title)
        if w_before > 10 or w_before > w_total / 2:
            report("WARN", "情绪前置",
                   f"Carrier phrase starts at weighted char {w_before:g} (title is {w_total:g} chars) — the emotion sits in the back half, move it forward")
        else:
            report("PASS", "情绪前置", f"Carrier phrase starts at weighted char {w_before:g} — front half, passes")
        report("PASS", "情绪承载字", f"Carrier 「{carrier}」 is in the title text")
    link = _machine_line(post_text, "情绪关联")
    if not link:
        report("WARN", "情绪关联", "post.md has no 「情绪关联」 machine line in the final-title rationale (format: concrete fact → punchy phrase) — add it before publishing")
    elif "→" not in link:
        report("WARN", "情绪关联", "The 「情绪关联」 line has no → — write it as 「concrete fact → punchy phrase」")
    else:
        phrase = link.split("→", 1)[1].strip()
        if phrase and phrase not in title:
            report("WARN", "情绪关联", f"Right side of the link 「{phrase}」 is not in the final title — mismatch")
        else:
            report("PASS", "情绪关联", "Link line complete, right-side phrase is in the title")
    anchor = _machine_line(post_text, "标题锚点")
    if not anchor:
        report("WARN", "标题锚点", "post.md has no 「标题锚点」 machine line — step 0 of script writing is to set the anchor first")
    elif anchor not in title:
        report("WARN", "标题锚点", f"Anchor 「{anchor}」 does not appear character for character in the final title — the title drifted")
    else:
        report("PASS", "标题锚点", f"Anchor 「{anchor}」 is in the title character for character")


# ---------- 5b. cover AI source (warn only) ----------
def check_cover_ai(folder, post_text):
    name = "Cover AI source"
    if not post_text or "封面主视觉：AI生成" not in post_text:
        report("WARN", name, "Neither the acceptance sheet nor post.md has the 「封面主视觉：AI生成」 machine line; add it when the cover main visual is AI-generated")
        return
    srcs = [p for p in folder.glob("ai*") if p.suffix.lower() in (".jpg", ".jpeg", ".png")] \
        + [p for p in folder.glob("*media-generation-*") if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
    if not srcs:
        report("WARN", name, "Marked AI-generated, but no source image with an ai or media-generation- prefix in the material folder — the proof file is missing")
    else:
        report("PASS", name, f"AI source image in the material folder: {srcs[0].name}")

# ---------- 4. silence detection ----------
def check_silence(video):
    name = "Whole-video silence"
    if video is None:
        report("FAIL", name, "No finished video to test")
        return
    db = num("audio.silence_threshold_db")
    db = -abs(db)  # Whether config says 45 or -45, treat it as -45dB.
    win = num("audio.silence_window_seconds")
    max_gap = num("audio.silence_max_gap_seconds")
    r = run(["ffmpeg", "-nostats", "-i", str(video),
             "-af", f"silencedetect=noise={db:.0f}dB:d={win}", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    durs = [e - s for s, e in zip(starts, ends)]
    mx = max(durs) if durs else 0.0
    over = [d for d in durs if d > max_gap]
    detail = (f"threshold {db:.0f}dB/{win}s, {len(durs)} silent segments, longest {mx:.2f}s"
              f"(standard: no segment >{max_gap:.0f}s)")
    if len(starts) > len(ends):
        # A trailing silence segment has no end time, so its length is uncertain — noted, not failed
        detail += "; plus 1 unclosed trailing silence segment, not counted"
    report("FAIL" if over else "PASS", name,
           detail + (f"; {len(over)} segments over the limit" if over else ""))


# ---------- 4b. minimum bitrate (warn only) ----------
def check_bitrate(video):
    name = "Minimum bitrate"
    if video is None:
        report("WARN", name, "No finished video to test, skipped")
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
            # Some encoders don't write a stream bitrate — approximate with the whole file's bitrate (slightly high, good enough for a warning).
            fmt = info.get("format") or {}
            if fmt.get("bit_rate"):
                kbps = int(fmt["bit_rate"]) / 1000.0
    except Exception:
        kbps = None
    if kbps is None:
        report("WARN", name, "ffprobe can't read a bitrate — skipped (warn-only check, unreadable is not a failure)")
        return
    floor = num("video.min_bitrate_kbps")
    detail = f"Video stream about {kbps:.0f} kb/s (floor {floor:.0f} kb/s)"
    if kbps < floor:
        report("WARN", name, detail + "; bitrate is low — text edges will blur, and the platform's re-encode will blur them more. "
                                   "Set the bitrate floor when assembling (see pipeline/assemble.sh)")
    else:
        report("PASS", name, detail)


# ---------- 4c. blank frames (warn only) ----------
# Criteria (calibrated on the weather-forecast good cut and blank samples, 2026-10-18):
# sample one frame every 0.5s, shrink to 96x96 grayscale, histogram over every 4th pixel.
# A frame counts as 'nearly empty' when over 98% of pixels fall within median gray ±10 and
# overall variance <= 100: a solid-color frame has variance 0, coverage 1.0; a frame with only
# one title line has variance ~25, coverage ~0.99; normal finished frames start at variance 288
# with coverage at most ~0.76 — the two sides are far apart, so false alarms are unlikely.
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
    name = "Blank frames"
    if video is None:
        report("WARN", name, "No finished video to test, skipped")
        return
    frame_bytes = BLANK_SIZE * BLANK_SIZE
    # run() uses text=True, which would corrupt binary frames — run this one in binary mode.
    proc = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video),
                           "-vf", f"fps={BLANK_FPS},scale={BLANK_SIZE}:{BLANK_SIZE},format=gray",
                           "-f", "rawvideo", "-"], capture_output=True, timeout=600)
    data = proc.stdout or b""
    if len(data) < frame_bytes:
        report("WARN", name, "No frames sampled — skipped (warn-only check, untestable is not a failure)")
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
    detail = (f"One frame every {step:.1f}s, {len(blanks)} frames total, longest near-blank run "
              f"{longest_seconds:.1f}s (standard: at most {limit:.1f}s, warn only)")
    if longest_seconds >= limit and longest > 0:
        start = longest_start * step
        report("WARN", name, detail +
               f"; over-limit run around {start:.1f}–{start + longest_seconds:.1f}s — "
               "usually a scene timed to the voiceover whose animation finished early, leaving seconds of nothing. "
               "Fill that animation out, or shorten the scene")
    else:
        report("PASS", name, detail)


# ---------- 4d. frozen frames (warn only) ----------
def check_freeze(video):
    name = "Frozen frames"
    if video is None:
        report("WARN", name, "No finished video to test, skipped")
        return
    limit = num("video.freeze_warn_seconds")
    r = run(["ffmpeg", "-nostats", "-i", str(video),
             "-vf", f"freezedetect=n=0.003:d={limit}", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"freeze_end: ([\d.]+)", r.stderr)]
    spans = [(s, e) for s, e in zip(starts, ends) if e - s >= limit]
    if len(starts) > len(ends):
        spans.append((starts[-1], -1))  # A freeze running to the end has no end time.
    # Merge adjacent still segments less than 1s apart: the tiny motion between them is usually
    # a subtitle change or background drift — without merging, the count inflates and looks
    # scarier than the one real still stretch.
    merged = []
    for s, e in spans:
        if merged and merged[-1][1] >= 0 and s - merged[-1][1] < 1.0:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    spans = merged
    if not spans:
        report("PASS", name, f"No still segments ≥{limit:.0f}s")
        return
    desc = ", ".join(f"{s:.1f}–{e:.1f}s" if e >= 0 else f"{s:.1f}s–end"
                     for s, e in spans[:3])
    report("WARN", name,
           f"{len(spans)} still segments ≥{limit:.0f}s: {desc}. "
           "Check against sampled frames first: a legitimate static info card, or animation finished / transition stuck? "
           "The second kind goes back to video making — don't wave it through")


# ---------- 4e. final title weighted length (warn only) ----------
def title_weight(title):
    # Weighting: Chinese and full-width punctuation count 1, ASCII letters, digits, and half-width symbols count 0.5, emoji count 1.
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
    # Find a standalone "## 标题" section and take the first non-empty line under it
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
    name = "Title weighted length"
    title = extract_final_title(post_text)
    if not title:
        report("WARN", name, "No final title found in post.md — check by hand (warn-only check)")
        return
    w = title_weight(title)
    cap = num("content.title_max_chars")
    detail = f'Final title "{title}" weighted {w:g} chars (cap {cap:.0f} chars)'
    if w > cap:
        report("WARN", name, detail + "; over the platform cap — shorten before publishing")
    else:
        report("PASS", name, detail)


# ---------- 4f. body length (warn only) ----------
def check_body(post_text):
    name = "Body length"
    if not post_text:
        report("WARN", name, "No post.md to test, skipped")
        return
    body = section(post_text, "正文")
    if body is None:
        report("WARN", name, "No body section in post.md — check by hand")
        return
    n = len(re.sub(r"\s", "", body))
    cap = int(num("content.body_max_chars"))
    detail = f"Body {n} chars (cap {cap} chars)"
    if n > cap:
        report("WARN", name, detail + "; over the cap — cut it down before publishing")
    else:
        report("PASS", name, detail)


# ---------- 4g. topic count (warn only) ----------
def check_topics(post_text):
    name = "Topic count"
    if not post_text:
        report("WARN", name, "No post.md to test, skipped")
        return
    sec = section(post_text, "话题")
    if sec is None:
        report("WARN", name, "No topics section in post.md — check by hand")
        return
    items = []
    for ln in sec.splitlines():
        ln = ln.strip().lstrip("-*").strip()
        if not ln or ln.startswith("（") or ln.startswith("("):
            continue
        items += [t.strip() for t in re.split(r"[、，,；;\s]+", ln) if t.strip()]
    lo, hi = int(num("content.topics_min")), int(num("content.topics_max"))
    detail = f"Topics section has {len(items)} topics (standard {lo}–{hi})"
    if lo <= len(items) <= hi:
        report("PASS", name, detail)
    else:
        report("WARN", name, detail + "; count outside the standard — check against the plan before publishing")


# ---------- 4h. single subtitle length (warn only) ----------
def check_subtitle_len(folder):
    name = "Single subtitle length"
    cand = sorted(folder.glob("scripts*.txt")) or sorted(folder.glob("script*.txt"))
    if not cand:
        report("WARN", name, "scripts.txt not found, skipped")
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
               f"Longest single subtitle {worst} chars ({worst_seg} segment, cap {cap} chars); "
               "that long, it squeezes into 3 lines on screen. Go back to script writing and split this line in two — "
               "don't leave it for video-making rework")
    else:
        report("PASS", name, f"Longest single subtitle {worst} chars (cap {cap} chars)")


# ---------- 4i. narration bitrate note (warn only, never fails) ----------
def check_narration(folder):
    name = "Narration bitrate"
    cands = sorted(folder.glob("audio/*.mp3")) + sorted(folder.glob("n-*.mp3"))
    if not cands:
        return  # No narration source file kept in the material folder — this check stays silent.
    f = cands[0]
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=bit_rate",
             "-of", "csv=p=0", str(f)])
    try:
        kbps = int(r.stdout.strip().split(",")[0]) / 1000.0
    except (ValueError, IndexError):
        report("WARN", name, f"Can't read {f.name}'s bitrate — confirm by hand")
        return
    expect = num("tts.expected_bitrate_kbps")
    if expect > 0 and abs(kbps - expect) / expect > 0.25:
        report("WARN", name,
               f"{f.name} is about {kbps:.0f} kb/s, but expected about {expect:.0f} kb/s — "
               "this episode probably switched voice engines or settings; confirm the switch was intentional before continuing")
    elif expect > 0:
        report("PASS", name, f"{f.name} is about {kbps:.0f} kb/s, matching the expected {expect:.0f} kb/s")
    else:
        report("PASS", name,
               f"{f.name} is about {kbps:.0f} kb/s (no expected bitrate in config, so this just logs the number; "
               "to make this check warn, fill in tts.expected_bitrate_kbps)")


# ---------- 5. cover ----------
def check_cover(folder):
    name = "Cover"
    cands = sorted(folder.glob("cover*.jpg")) + sorted(folder.glob("cover*.png")) \
        + sorted(folder.glob("封面*.jpg")) + sorted(folder.glob("封面*.png"))
    if not cands:
        report("FAIL", name, "No cover image found")
        return
    f = cands[0]
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0", str(f)])
    wh = r.stdout.strip().split(",")
    w, h = (wh + ["?", "?"])[:2]
    want_w, want_h = int(num("video.cover_width")), int(num("video.cover_height"))
    ok = (w, h) == (str(want_w), str(want_h))
    report("PASS" if ok else "FAIL", name,
           f"{f.name}: {w}x{h} (standard {want_w}x{want_h})")


# ---------- 6. issue number ----------
def check_issue(folder, post_text):
    name = "期号"
    m = re.search(r"(\d{4}-\d{2}-\d{2})", folder.name)
    if not m:
        report("WARN", name, f"Folder name {folder.name} shows no date — skipping the check")
        return
    date = m.group(1)
    epoch = str(CFG["publish.issue_required_from"] or "")
    # Without a forced start date this only warns, never fails; once set, it's enforced from that date.
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
        report("WARN", name, f"No {date} entry in the ledger — can't check the issue number")
        return
    if recorded is None:
        report("FAIL" if strict else "WARN", name,
               f"post.md records no issue number; the ledger sequence is issue {seq}"
               + (" (past the forced start date, missing counts as FAIL)" if strict
                  else " (no forced start date set, warn only)"))
        return
    if recorded != seq:
        report("FAIL" if strict else "WARN", name,
               f"post.md says issue {recorded}, but the ledger sequence is issue {seq} — mismatch")
    else:
        report("PASS", name, f"post.md matches the ledger: issue {seq}")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    folder = Path(sys.argv[1]).expanduser()
    if not folder.is_dir():
        print(f"Material folder not found: {folder}")
        return 2
    if CFG_FOUND:
        print("Config: using the repo-root config.yaml")
    else:
        print("Config: no repo-root config.yaml found, using built-in recommended defaults")
    print(f"Checking: {folder}")
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
    print(f"Summary: {len(fails)} FAIL, {len(warns)} WARN, "
          f"{len(RESULTS) - len(fails) - len(warns)} PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
