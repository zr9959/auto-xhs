[中文](README.zh-CN.md) | English

# motion-lib: the motion library for web-page videos

How a video gets made here: one video is one web page. The animation is laid out on the page, then screenshotted frame by frame, then stitched into a video. This library is the motion kit for that page. Styles live in `motion.css`, motion lives in `motion.js`, both on `window.MotionLib`.

## One hard rule: every effect must freeze

When screenshotting, the timeline is stopped — it jumps to a time t, frame by frame, and shoots. So every effect can only be computed from t: jump to the same t as many times as you like, the picture must be identical every time.

- Never let a clock that runs on its own (like a free-running `requestAnimationFrame`, or `Date.now()`) decide the picture.
- Never use `Math.random()` to roll dice. For randomness, use `MotionLib.mulberry32(seed)` — once the seed is set, the result is set.
- Canvas effects like starfields, confetti, and Lottie get registered as frame updaters (`addFrameUpdater`). The screenshot side calls `runFrameUpdaters(t)` on every frame jump, and they redraw that frame from t.

Break this rule and the captured frames won't line up with the time — the finished video will jump and flicker.

## One layout rule: one delayed entrance per area

Two cards landing in the same area, each with its own entrance delay, will overlap halfway through the animation and can cover the text below. Screenshots freeze frame by frame, so the overlapped frame goes straight into the finished video — there is no hiding from it.

- In one area, either place only one element with an entrance, or put the cards into one layout container (a vertical flex column with spacing set) so they never overlap before, during, or after entering.
- If entrances really must be staggered, work out each card's position at every moment first: no overlap at any moment, not just after everything settles.

## Get the third-party libraries first

The GSAP and lottie-web sources are not in the repo. Run once:

```bash
bash scripts/fetch-vendor.sh
```

It downloads GSAP 3.15.0, lottie-web 5.13.0, and canvas-confetti 1.9.4 into `vendor/`. Versions and checksums are pinned in the script. Version details are in `vendor/README.md`.

## How to include it in a page

Include the stylesheet in the page `<head>`, and the scripts in this order right before `</body>` (adjust the paths to where your page sits):

```html
<link rel="stylesheet" href="../../motion-lib/motion.css">
<script src="../../motion-lib/vendor/gsap/gsap.min.js"></script>
<script src="../../motion-lib/vendor/gsap/SplitText.min.js"></script>
<script src="../../motion-lib/vendor/gsap/DrawSVGPlugin.min.js"></script>
<script src="../../motion-lib/vendor/lottie.min.js"></script>
<script src="../../motion-lib/motion.js"></script>
```

Then build a paused timeline, lay the components on it, and leave the three hooks the screenshot side needs:

```js
const ML = window.MotionLib;
ML.usePlugins();                       // register every plugin you included
const tl = gsap.timeline({ paused: true });
// ……lay components on tl……

window.__renderFrame = function (scene, t) {
  tl.seek(t, false);                   // don't change this second argument to true, or number rollups won't refresh
  ML.runFrameUpdaters(t);              // starfield, confetti, and Lottie land on this frame together
};
```

The ready-made example is `pipeline/templates/scene-template.html` — start from it, it's fastest.

## Component list

Signatures are all `(tl, target, {at, dur, ...})`, where `at` is the second on the timeline it starts at.

| Component | What it does | One-line usage |
|---|---|---|
| `splitChars` | Splits a title into one element per character | `const chars = ML.splitChars(el)` |
| `titleIn` | Title enters character by character: flip in / wave up / blur to sharp | `ML.titleIn(tl, el, {at:.15, mode:"flip"})` |
| `countUp` | Number rolls up from small to big — prices, counts, anything | `ML.countUp(tl, el, {to:899, at:2, prefix:"¥"})` |
| `barGrow` | A horizontal bar grows left to right; ratio is how full it gets | `ML.barGrow(tl, bar, {at:1, ratio:.65})` |
| `drawPath` | Draws along an SVG path — trend lines, check marks, anything | `ML.drawPath(tl, path, {at:1})` |
| `ringSweep` | A ring sweeps across a percentage | `ML.ringSweep(tl, circle, {at:1, pct:.67})` |
| `cardIn` | A card slides in from a direction, with a bounce | `ML.cardIn(tl, el, {at:0, from:"left"})` |
| `stackConverge` | Several cards fly in and stack into one pile | `ML.stackConverge(tl, [a,b,c], finals, {at:1})` |
| `flipCard` | 3D card flip, front to back | `ML.flipCard(tl, inner, {at:8})` |
| `shine` | A beam of light sweeps across an element | `ML.shine(tl, el, {at:3})` |
| `underlineDraw` | An underline draws itself — it's just drawPath | `ML.underlineDraw(tl, path, {at:1})` |
| `breathe` | A glow swells and shrinks, to highlight the main item | `ML.breathe(tl, el, {at:5, repeats:5})` |
| `wipeIn` | A mask wipe, the picture shows bit by bit | `ML.wipeIn(tl, el, {at:2, dir:"left"})` |
| `circleReveal` | A circle grows open and reveals the picture | `ML.circleReveal(tl, el, {at:2})` |
| `blurCrossfade` | The old one blurs out, the new one sharpens at the same time | `ML.blurCrossfade(tl, oldEl, newEl, {at:4})` |
| `glowDrift` | A glow drifts slowly across the whole segment | `ML.glowDrift(tl, [{el:"#g", dx:120, dy:60}], total duration)` |
| `starfield` | A screen full of small stars, redrawn from seed and t | `ML.starfield(canvas, {count:110, seed:11})` |
| `confettiBursts` | A burst of confetti at a set time, landing spots computed from t only | `ML.confettiBursts(canvas, [{t0:9.5, x:540, y:600, seed:21}])` |
| `mountLottie` | Pins a Lottie animation to the timeline | `ML.mountLottie(el, {path:".../check.json", at:9.5})` |
| `morphTo` | One path turns into another shape | `ML.morphTo(tl, path, "M…", {at:0})` |

The style classes have a set of variables at the top of `motion.css` (`--ml-color-a` main color, `--ml-color-b` secondary color, `--ml-color-c` accent color, and so on). To restyle, change the variables first — don't go hunting for color values everywhere. Common classes: `.ml-stage` stage, `.ml-glass` glass card, `.ml-card` solid card, `.ml-img-frame` image frame, `.ml-grad-text` gradient text, `.ml-topbar` top color bar. Subtitles use the `.ml-subs` set — the rules are in the two sections below.

Lottie example assets live in `vendor/examples/`: `check.json` is a ring drawing itself then a check mark, `sparkles.json` is a few four-pointed stars flashing in turn. Both were written for this project — use them freely.

## Subtitle anchor standard (bottom-anchored, the `.ml-subs` class set)

Subtitles must not float. They must be **bottom-anchored**: when the line count changes, the block only grows upward — the bottom edge never moves, and text sits at the bottom inside the block.

Where the anchor comes from (Xiaohongshu portrait, 1080×1920): watch a video in the app as a viewer, and the bottom of the picture belongs to the player itself — author avatar, nickname, title, and declarations all sit on top of it. That area is called the system info area. Measured, its top edge sits at **84.4% of the picture height (y=1621)**. The subtitle bottom edge is set at **80% (y=1536)**, leaving **85px** of safety gap to it, so 1-line and 2-line subtitles never press on the avatar. Higher and the subtitles disconnect from the body; lower and they hit the info area. Only bottom anchoring keeps every line consistent.

| Item | Value |
|---|---|
| Canvas | 1080×1920 |
| Background bar bottom edge | **y = 1536** (80% of height), container `bottom: calc(100% - 1536px)` |
| System info area top edge (measured) | y = 1621 (84.4%), subtitle bottom edge leaves 85px of gap to it |
| Font size / line height | 46px / 64px |
| Background bar padding | 16px top and bottom (28px left and right), 26px corner radius |
| Max lines | 2 lines (split a long sentence into two subtitle lines at a sentence break first — never a 3rd line, never shrink the font) |
| 1-line block | 96px tall, block top y = 1440 (75.0%) |
| 2-line block | 160px tall, block top y = 1376 (71.7%) |

Usage (the subtitle layer stands apart from the scene — just swap the contents of `.ml-subs-line` line by line, no need to recompute positions):

```html
<div class="ml-subs"><div class="ml-subs-bar">
  <span class="ml-subs-line">Finish this line first,</span>
  <span class="ml-subs-line">then pick up the next one.</span>
</div></div>
```

**How to measure for acceptance**: pull any two frames from the finished video (one 1-line frame, one 2-line frame) and measure the y of the subtitle background bar's **bottom edge** — it only passes inside **1526–1546**. How to measure: take a horizontal band across the middle of the picture, scan rows for dark pixels — the lowest dark row is the bottom edge. The bar's shadow is a semi-transparent soft edge, clearly lighter in color — don't count it.

### New platform, new device? Measure it yourself first

The numbers above only cover Xiaohongshu portrait. On another platform (like Douyin) or another player, the system info area sits somewhere else — re-measure with this method:

1. In the target app, open any video as a viewer and screenshot one full playback frame. The video must be filling the height when you shoot — no black bars top and bottom.
2. On the screenshot, measure the system info area's top edge: the top of the avatar-and-nickname row, converted to a percentage of the video height.
3. Set the subtitle bottom edge a little above it, leaving a safety gap (about 85px on a 1920-tall canvas; scale it down proportionally on a shorter canvas). Convert to a percentage — that is your anchor.
4. The top safe line works the same way: measure the bottom edge of the top navigation row (back, search, and those icons), and lay the main content out below it.
5. Write the new numbers into your `config.yaml` (`video.subtitle_bottom_pct`, `video.system_info_top_pct`), and convert the pixel values in the motion library's `.ml-subs` by canvas height.

## Layout zones (read this table before laying anything out)

Once the subtitle anchor is set, the main content area is actually large — the layout must fill it. Never squeeze the content into the top half and leave the bottom half empty. All four zone numbers (1080×1920) come from the same measurements above:

| Zone | Range | Notes |
|---|---|---|
| Top safe line | y = 250 (13%) — no main content above this line | From the viewer side, the top navigation row sits around 11%–14.5% of the height. Small fixed edge elements (badges, date bars, and the like) are exempt |
| Main content area | y 250 → 1340, 1090px tall | Titles, info cards, and real interface pictures all go here. The bottom edge 1340 = the 2-line subtitle block top 1376 minus 36px of gap |
| Subtitle area | Block top 1376 (2 lines) / 1440 (1 line), bottom edge fixed at y = 1536 (80%) | See "Subtitle anchor standard" above |
| System info area | Below top edge 1621 (84.4%) | Off-limits: neither main content nor subtitles may reach into it |

Hard usage rule: each segment's main body (title + info cards + real interface pictures as a whole) must span at least **55%** of the main content area vertically (about 600px), centered in the area, filled top to bottom. Empty space at the bottom of the content area must not pass **25%** (about 270px). Lay out the main body first, then place the subtitles — never shrink the content to fit around the subtitles.

To check zones during acceptance, use the `.ml-guide` guide-line class in `motion.css` (acceptance only, off by default): add `<div class="ml-guide on">` to the page, with five numbered child elements inside like `<i class="g250" data-label="Top safe line 250"></i>`, and the five lines will overlay the picture when you screenshot — measure against them. Remove `.on` when the check is done. **Never render a finished video with `.on` on** — guide lines in the finished video mean it fails.
