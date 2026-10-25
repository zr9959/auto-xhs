[中文](03-video.zh-CN.md) | English

# Stage guide 03 · Video

> When to read: when the manager dispatches the video task. Read the constitution page first, then this guide.
> All numbers come from the constitution page's numbers table. This guide only cites them, never writes its own.
> This stage must end with one run of `../validate.py <day's material folder path>`, with the output pasted into the evidence list.

## Input

- The full `post.md` and `scripts.txt` handed back by the writing stage.
- The material needs list.
- The motion library (the repo's `motion-lib/`) — every component comes from the library.

## Output

- The finished video file (specs per the table) and a separately made cover image, saved to the day's material folder.
- The finished-video acceptance checklist, written into `post.md` or a `验收.md` (acceptance notes) in the same folder.
- One more line in the run log: the "成片验收过" (finished video passed acceptance) stamp.

## Evidence list to hand back to the manager

- Traces of the two pre-start gates: the material readiness list (each item's file and material type) and each segment's single-frame pre-check result (see "Two gates before starting" below).
- The finished-video acceptance checklist's six items (see the "Finished-video acceptance checklist" section below).
- The full `validate.py` output.
- A mapping table for each major piece of software: software name, interface file, segments and time points where it appears.
- Which motion events this video used, at which time points, plus at least 3 pulled frames showing mid-motion states.
- The four elements for problems (write "none" when there are none).

## Two gates before starting (pass them before any frame-by-frame capture)

- **Material readiness gate.** The first job of video work is not layout, and not capture — it's handing in a material readiness list: every product picture and real interface in `post.md`'s material needs, listed item by item — each matching file already saved to the day's material folder, and genuinely official material (official product pictures, official interface screenshots, official release pictures), not homemade diagrams. The manager checks the list before capture is allowed. When the real product clearly has an official picture but a homemade diagram is offered instead, send it back for a picture swap before starting — never discover it at finished-video acceptance. Shooting the whole video with diagrams first and swapping pictures for a full re-render wastes a whole round.
- **Single-frame pre-check.** Before full capture, grab 1 key frame per segment and run it past the defect list before that segment is cleared: subtitles at most 2 lines, no elements overlapping each other, no cut-off text, subtitle bottom edge and layout zones compliant. Only when every segment's pre-check passes is full capture allowed. Never capture the whole video before looking at a single picture — layout defects (3-line subtitles, cards over pictures, pictures over titles, cut-off text) are whole-video rework errors, and the pre-check exists to catch them.

## How videos are made: web-page video

Videos are made from web pages, not dragged together in an editor:

1. Each video gets one web page: HTML/CSS for layout (gradients, glass feel, glow, shadows — all CSS), GSAP for the animation timeline.
2. Motion components always come from the ready-made components in `motion-lib/` — no copying the library, no building a second set yourself.
3. At capture time, pause the timeline and jump frame by frame to each moment at the table's frame rate, screenshotting each.
4. At the end, ffmpeg joins frames and voiceover into the finished piece.

Two hard requirements:

- **Animation must be a function of time.** Capture works by "jump to time t, screenshot" — so every effect must be computable from the time alone. No self-running timers, no current time, no grab-bag random numbers driving animation. Effects that need a random feel use a fixed seed, so jumping to the same moment always gives the same picture.
- **Library files live on this machine, no online URLs.** Download GSAP and friends to this machine first, then reference them (the repo's script notes say how to pull them). Video work must run with the network off.

Motion baseline: titles popping in character by character or line by line, cards flying in at staggered times, key numbers counting up, bar charts growing, the main item breathing with glow, background halos drifting slowly, product pictures with push-pull. These are the floor — never fall back to uniform fades across the whole video to fill time.

## How landscape works

Portrait is the default. Only when config picks landscape does this section apply — four changes total:

1. **Change two settings.** `video.orientation` becomes `landscape`, `video.width` and `video.height` become 1920 and 1080. Change only one, and acceptance will warn you they don't match.
2. **Add the size to the screenshot command.** capture.js takes extra `--width 1920 --height 1080`, matching what the settings say.
3. **Change the picture template with it.** The STAGE at the top of the template becomes 1920×1080 (the template comments say how); that one place decides horizontal vs. vertical for everything in the page.
4. **Subtitle anchor follows percentages.** The subtitle bottom edge stays fixed at 80% of frame height (the table's row) — same ratio for landscape. The motion library's subtitle class pixel numbers are worked out for a 1920 height, so convert them for the new height, then pull frames and measure the bottom edge again.

One landscape layout reminder: the picture got wider, so lay content out sideways and spread it left and right. Don't write one title line too long, and don't carry over portrait's vertical stacking — it looks empty.

## When the source material is itself landscape (widescreen source special case)

When the main material is already landscape (a full event recording, a landscape screen recording, and the like), the finished video keeps the landscape original size — never fit it onto a portrait canvas with black bars:

- Burn subtitles into the lower part of the picture: font size scales with frame height (about 64px for a 1080-high frame), with a semi-transparent backing box, so it stays readable on phones.
- Comment cards must look clearly different from subtitles: comment cards use a sticker style (color gradient base, white outline, slight tilt, a small label like "网友神评", top netizen comment) — never the same black-bar style as subtitles, or viewers can't tell which is which.
- The channel logo sits inside the top-left corner.
- Intro and outro use the landscape set (see the intro/outro section above), normalized to the same size, then joined directly.

## Motion must be visible

The acceptance standard is "motion you can see at a glance, with punch at the key points" — not "technically there is motion".

- Motion event counts per segment and density across the video follow the table. Dynamic title entry, data drawing or number counting, real-picture reveal or card flip, emphasis landing — each segment gets at least one of each.
- Key numbers must count up to their value. Key conclusions (price gaps, conclusion sentences, the main item) must each get an emphasis landing: light sweep, breathing glow, confetti ribbon, checkmark — pick one. After the landing, pause per the table so people can see it clearly — never flash past it.
- Moves must be big. Entry shifts, zooms, and flips must be large enough that pulled frames show clearly different mid-states. Small drifts and low-opacity fades are only helpers — never counted as main effects.
- Segments connect with transitions: wipes, circle spreads, blur crosses all work — no hard cuts.
- The background layer stays on (stardust, halos, grain, picked by topic) but must not fight the main text.

## The opening needs a title card

After the brand intro clip, before the first main segment, there must be a bold title card: big title plus this episode's key visual, so viewers know at once what the video is about. A small corner label alone doesn't pass. The title card's length matches its voiceover (for a channel with a fixed opening line, the opening line ends and the main video starts — no separate silent title page left in).

## Pictures must carry the picture, not just words

Every video needs pictures, people, and objects tied to the content to carry the screen: every object, graphic, and person talked about must really be drawn or acted out, and every segment must have one dominant object or graphic in motion (section diagrams, object illustrations, particles, person silhouettes, and the like all count). Never a whole segment of text only — text only labels and subtitles. Official product pictures and real interfaces count as qualifying elements, but on their own they're not enough — they still need matching graphics. Material can come from free libraries (icon libraries, free animation material, free illustration) — only free or open-licensed, watermark-free material. Acceptance checks pulled frames segment by segment: any segment with text only gets sent back.

## Brand intro and outro (only read this section when used)

When config fills in `brand.intro_file` / `brand.outro_file`, the finished video joins as "intro + main + outro" (`assemble.sh` `--intro` and `--outro` flags):

- Intro and outro get normalized to the main video's specs first (size, frame rate, encoding, AAC 48kHz) before joining — mismatched specs never get force-joined.
- Directions must match: a vertical main video needs vertical intro and outro — never a vertical main video with a horizontal intro. Landscape channels likewise keep a landscape set.
- When the outro already carries a like-and-follow ask, the main video's ending drops its own ask line or card (the table's intro/outro row) — don't repeat it on both sides.

## On-screen text only says the content

Words on screen only say the content itself: product names, features, prices, conclusions. Never write notes explaining where material came from ("official picture", "source: so-and-so" — not one character of that). Beside a product picture, label text only needs the product name itself. Acceptance checks this frame by frame.

## Every video must look different

- Within one video, the opening animation and the ending animation must not match.
- Across videos, change with the topic: opening style, ending shot, layout, transitions, graphic style, background and accent colors. Never run two videos in a row on the same opening, ending, and layout.
- Only the table's fixed items stay the same: specs, speed, fixed closing line, subtitle anchor, and the like.

## Visual style: layered paper-craft (optional style, see the appendix)

- Style appendix: `core/paper-style.md` (layered paper-craft illustration: color board, fixed prompt prefix, at least 4 layers per scene, parallax between layers, elements moving independently, no pure push-pull inside any 5-second window, physics rules, paper-craft landing language). When using this style, read the appendix before video work starts and check against it item by item at acceptance; when not using it, follow the other sections of this guide — never mix the two.
- Real interfaces and official product pictures still use real pictures, set inside paper-craft framing — never let a paper-craft picture pass itself off as a real shot.

## The cover is made separately

- Make one cover image per video, specs per the table. Never crop the video's first frame to fill in.
- Big-text line count per the table, one hook, high contrast. Layout changes with the topic, but one column keeps one consistent template feel.
- The cover carries an issue-number corner label: "第 X 期" (Episode X), X being this video's cumulative publish number in the ledger. The first video is episode 1, counting up one by one — no skips, no repeats. From which date it becomes mandatory follows the table's `publish.issue_required_from`. The acceptance checklist must check the issue number against the ledger number.
- **The cover's main visual is AI-generated (the model must never write the title text directly).** The main visual comes from an AI image model generating on the spot from this episode's settled title + content: the picture must carry a viral cover's hook (strong subject, strong emotion, high contrast, clear at first glance what it's about), with the prompt distilled from this episode's title and core conclusion — never a generic pretty picture unrelated to the content. The big title text and the "第 X 期" (Episode X) corner label still go through deterministic layout compositing (laid out, then overlaid onto the AI main visual) — never let the image model render Chinese title text directly (it garbles characters). Check the generated picture item by item: no wrong or leftover characters, no watermarks, no distorted subjects. When the picture shows this episode's product, it must look like this product, this model — when the AI draws the product crooked or as another model, switch to "AI scene + official product picture composite" instead, never ship it wrong.
- **Cover provenance (machine gate).** The AI-generated raw main visual must stay in the day's material folder (filename carrying an ai or media-generation- prefix), and the acceptance checklist carries its own machine-readable line, "封面主视觉：AI生成" (Cover main visual: AI-generated) — the acceptance script checks against it, and a missing field or a missing AI source picture in the folder both count as provenance in doubt, failing the gate.
- **A failed generation never gets a downgraded cover.** A failed generation may only be retried with a new prompt or a new model — never fill in with a screenshot or video frame as the cover. When it truly can't be generated, stop the post and report with the four elements. Hard gates never get a pre-written way out: acceptance conditions must never pre-write a fallback like "if it fails, use a screenshot".

## Rhythm and information load

- Voiceover word count and finished length follow the table. The first seconds must be a conclusion or conflict opening, no intro clip. Info point rhythm, minimum count across the video, the mid-video turn, and the ending this-or-that question all follow the table.
- Give numbers in full. For prices and fees, show unit price, subscription price, and the year's total cost. For a product, at least one price or feature comparison against a similar one. Never a run of parameters in a row.

## Material must be real

- Prefer real material: official site screenshots, screenshots from actually operating the software, officially released pictures. Empty shots can be generated, motion graphics can be made yourself (list items lighting up one by one, address bar typing, mouse click ripples, highlight boxes circling key points, and the like). Never pass off a static picture zoom as motion material.
- **When a picture can't be had, degrade in this order — never jump around at random:** ① the vendor's official release page, product page, press release, official material pack; ② the official account, developer, or involved person's first-hand original post pictures; ③ screenshots or official demo pictures from actually operating the official site or software yourself; ④ the same official picture carried by a trusted media outlet with the official release; ⑤ a render labeled "illustration / leak render", or a picture of an existing product from the same line with the screen labeled as to which model it is; ⑥ still nothing, and the product's look is core to this video — swap topics or stop the post, never fill in with an unrelated picture. Each level gets at most one per-source time limit. `post.md`'s material list must state each major material's source type, original page, saved file, and segments where it appears. On failure, log the tried pages and results as the four elements.

### Three hard requirements for product pictures

1. It must be this product, this model — never a product-line group shot or a pile of products passed off as one. Group shots mixing other products are the most common failure.
2. Product pictures appear in the main video for the segment count the table sets. Match the picture to the feature being talked about — never flash it only on the cover and at the opening, then run text cards for the rest.
3. At acceptance, check pulled frames picture by picture: is what's in the picture this product, this model? Wrong shape means swap the picture and redo.

### Software and services need real interfaces

For specific software, apps, and online services, "product picture" means its real interface: the official site's product interface pictures, real feature or pricing page screenshots, official release pictures. A logo alone and a homemade info card don't count. Requirement: every major piece of software talked about needs its real interface on screen, for the segment count the table sets in total; match the interface page to the feature or price being talked about. When it can't be had, write the four elements clearly — never fill in with an unrelated picture. Acceptance lists them one by one as "software name → interface file → segments / time points" — one missing major piece of software means the whole item fails, never just counting total segments.

## Subtitles

- **Position per the table, bottom-anchored.** The subtitle bottom edge stays fixed at the table's anchor (Xiaohongshu vertical measured: 80% of frame height, y=1536 at 1080×1920). 1 line or 2 lines, it's the same: when the line count changes, the block only grows upward, the bottom edge never moves. Why here: the lowest band of the screen is the player's system info area (author avatar, nickname, title, declarations all stacked there), and its top edge measured at 84.4% of height. The subtitle bottom edge at 80% keeps a safe gap from it, so nothing gets covered. Below that line, no subtitles and no key text may enter. Acceptance in two steps: ① pull frames and measure the subtitle backing bar's bottom edge — inside the table's pass band it passes; ② drop the finished video into a preview with a bottom info area and eyeball that subtitles don't overlap the author info area. These numbers are measured reference defaults for Xiaohongshu vertical — on another platform, re-measure first by the motion library's method, don't copy them blindly.
- **Layout zones and content-area use.** The whole frame splits into four zones (1080×1920 numbers, all derived from that same measurement round): ① top safe line y=250 (13%): the viewer's top has a navigation row (back, search, share), so main content lays out below this line; small fixed edge elements (badges, date bars, and the like) are exempt. ② main content area y=250 to 1340, height 1090: titles, info cards, and real interface pictures all go here, its lower bound sitting a little above the top of a two-line subtitle block. ③ subtitle zone: block top varies with line count (2 lines 1376 / 1 line 1440), bottom edge fixed at 1536. ④ system info area: below top edge 1621, no entry. **Use-rate hard requirement:** each segment's main body (title + info cards + real interface pictures as a whole) must span at least 55% of the main content area vertically (about 600px), spread centered in the area, filled top to bottom; blank space at the bottom of the content area must not pass 25% (about 270px). Lay out the main body in the content area first, then place subtitles — never squeeze content small to make room for subtitles. Acceptance checks pulled frames one by one; you can open the motion library's `.ml-guide` guide lines overlaid to look (finished videos must not carry the guide lines) — over-limit blank space means rework.
- **Form:** subtitles follow the voiceover sentence by sentence. Each card carries only the current sentence, at most the table's line count. Never stack a whole voiceover segment into a multi-line big text block. Info cards on screen only carry keywords and numbers — never repeat a whole subtitle segment. Two copies of the same passage on screen at once don't pass. Break lines by meaning; punctuation must not land at the start of the next line. Acceptance pulls frames and checks subtitle form one by one — a fail means re-layout.

## Voiceover and audio

- Voiceover service and voice come from config's `tts.provider` and `tts.voice` — never hard-coded in a guide. Speed per the table, done with setpts/atempo. The last voiceover line is the table's fixed closing line, and the same words must appear on screen too — never dropped, never swapped (except when a brand outro carrying the ask is used — see the intro/outro section).
- **Smoke-test voiceover before starting.** Before voiceover work starts, run `pipeline/tts/tts-smoke.sh` and take the `LIVE=` line it prints as this episode's engine decision, writing the raw output into the acceptance checklist: `LIVE=primary` means use the main engine; `LIVE=fallback` means the main engine is unreachable and it already switched to the backup automatically — this episode goes out on the backup, noted in the checklist; `LIVE=NONE` is the only case where voiceover as a whole is unavailable — stop at the gate and report the four elements (attaching the script's printed failure output). **Never conclude "unavailable" from "can't find it, no such service"** — the only proof an engine is down is an actual call's failure output. Tools and voices live in a long-term directory, never a temp directory — temp directories get cleared at any time, and that's what a real "can't find it" looks like.
- **Engine degrade order.** When an engine as a whole is unavailable, degrade in this order: main engine → same engine retried once → backup engine → still failing means stop at the gate and report the four elements. Never quietly swap in an unapproved voice and ship it. When a backup voice is in use, the run log and acceptance checklist must state this episode's actual voice.
- **Self-check every voiceover segment.** After generating each segment, note its actual length and run that segment's silence spread — don't wait until the whole video is joined to find a bad segment. A bad segment shows as: length clearly out of proportion with the rest of the batch, or a silence reaching the table's flag value inside the segment. Shelve a bad segment first. The same text may only be retried verbatim once (the cache may hand back the same bad audio again). Still bad, split the segment in two by meaning and synthesize each half, checking each small segment again. Still bad after splitting, only then lightly reword or re-punctuate and re-record — never change facts or numbers. Log every step's original length, silence intervals, and retry or split results in the run log, and finish with a per-segment audio-video alignment table.
- **Audio acceptance is a hard rule.** Looking at pulled frames alone is not acceptance. Before publishing, run full-video silence detection on the finished video (ffmpeg silencedetect, threshold and length per the table): any silence past the table's cap outside intro/outro sends it straight back. When joining, align segment by segment — each segment's picture length must sit within the table's value of that segment's voiceover length. When a voiceover rework swaps versions, re-align that segment's picture — never leave a gap.

## Joining and encoding

- Specs and encoding per the table. Encoding rule: H.264 High, yuv420p, video_track_timescale 600, AAC 48kHz, use_editlist 0, faststart — that's what plays cleanly on phones.
- After capture, check frame counts match before joining. Mismatched frame counts never move forward. A receipt saying "done" doesn't count — actual frame counts and files do.

## Finished-video acceptance checklist (missing one item means not accepted)

Write the acceptance conclusion into the day's `post.md` or a `验收.md` (acceptance notes) in the same folder, with at least these six items:

1. The final file's identity: path, size, modification time, total length, plus ffprobe's key fields (resolution, video codec and Profile, pixel format, timescale, audio codec and sample rate, faststart and editlist actual results).
2. A full clean decode pass over the whole video, no errors allowed.
3. A per-segment audio-video alignment table, plus the silence detection threshold and longest silence interval, plus its own line stating the "human listening conclusion": the conclusion from actually listening through the whole video once (no problems, or where the problems are). Pasting machine detection results alone doesn't count as listening.
4. A time-stamped pulled-frame list: covering the opening, every main segment, around transitions, and the ending. Each frame notes the product or interface identity, the measured subtitle bottom edge, the subtitle form, and any unexpected blank frames, pure-white frames, or pure-black frames. **Measured numbers must carry the raw value, the frame's time, and the method** (for example, "59-second frame, subtitle bar bottom edge measured y=1536") — never just a conclusion like "position OK". A bare-conclusion number can't be re-checked later.
5. The cover: file, size (per the table), product identity, text checked once through.
6. The sensitive six-face self-check result (the six faces are in the sensitive appendix).

After a change, the old acceptance is void: any rework, frame patch, or re-render invalidates the old checklist. After changing, bump the final file's version or re-mark its identity clearly, and re-run on the new file: full decode, full-video silence, length and encoding checks, pulled frames for affected segments, pulled frames for the video's key time points. Checking only the small changed part never counts as a full pass. Reporting "fixed, passed" must come with old and new frames or files, re-check time points, and results. Without evidence, the only honest line is "changed, not re-checked".
