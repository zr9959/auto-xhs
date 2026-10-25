[中文](CONSTITUTION.zh-CN.md) | English

# Constitution page (template)

This file is the whole system's master rules. The manager only needs to read this one at the start of each round. The details for each stage live in the six guides in `stages/` — read the one for the step you're on.

First, three things to get straight:

- Anything in `{{ }}` is a placeholder. Replace it with your own value before using it, or fill in the matching key in `config.yaml`.
- Key numbers live in one place only: the numbers table below. Guides and task briefs only cite the table, never write their own set. If the two disagree, the table wins, and the weekly review fixes them up.
- Appendices are templates. Before using one, copy it under its proper name and then edit it — see the appendix index at the end.
- Language first: before anything else, ask the operator whether they want Chinese or English, and use that language for everything after — setup, daily runs, and reports. The repo docs come in both languages; read the version in the language picked.

## What this system does

Every day it makes one short video post for the Xiaohongshu account {{account_name}} (account ID {{account_id}}, your own account) — from topic, script, and video all the way to publishing and follow-up — and reports the result to wherever you point it.

- Only free tools and free interfaces, no paid services.
- You pick the automation level in `config.yaml` under `automation.mode`: `full` posts automatically, `semi` prepares a ready-to-post pack and you press publish, `manual` only goes as far as the script. Whichever level you pick, the hard gates below still apply in full — gates don't loosen because you're in a hurry.

## Core standards (top priority — check every script against these four first)

1. **Hook.** A flat topic with no hook gets swapped out. Every topic must pass one test first: can you say in one sentence what this has to do with the viewer — with their money, their device, their account, a service they use? If you can't say it, swap the topic. Even big news must be reframed as "what does this mean for you" — if it can't be reframed, don't post it. Write as many title versions as the numbers table says, then pick the one with the strongest hook. The first line of the script must land on "you" first — the reader's connection first, facts second.
2. **Plain words.** Everyday words, short sentences. A term you can't avoid gets explained in plain words in the same sentence.
3. **Details.** The viewer must come away knowing something. Saying "it's good" means saying clearly what's good about it; saying "it's strong" means saying clearly which detail is strong. For software, show the real interface, where to get it, and how to use it step by step. For a new service, say clearly what it does, how to use it, where the entry point is, whether it costs money, and where it beats similar ones. Conclusions with no details get rewritten. For a product, also answer four questions: who it's for, who has this need, what exactly the need is, and at least one use case from real life — plus one line on who it's not for. Parameters and dates with no people and no need don't pass.
4. **No repeats.** Topics, angles, and material must not repeat what already went out. A product or event already covered stays covered, unless there is a genuinely new development with a genuinely new angle.

## Run safety, log stamps, and handling problems

- **Triple duplicate check.** The first line of the run log must read "开工，防重复三查中" (starting, running the triple duplicate check), then check three places: today's run log, the topic ledger (`paths.ledger_file`), today's material folder, and the account's post list. If today already has a post, stop and report the existing link. If another round is running and its stamps haven't gone stale, log one line saying you're yielding — never run a second post in parallel. Only when the no-stamp limit in the numbers table has passed, or when you get a clear takeover order, do you take over as a failed round.
- **Stage stamps.** Write the first stamp within the time limit in the numbers table after starting. Log one line at the start and end of every stage, with the time, the product paths, and the key numbers (topic and sources, script word count, finished video length, publish link, and so on). Long stages get extra stamps at the table's interval, stating the current sub-step and time used. To judge whether a round is alive or dead, look only at stamps and products — not at whatever status label the scheduler shows. Past the table's limit with no new stamp, treat it as failed.
- **Watchdog split.** The early watchdog only checks whether the first stamp exists. If it doesn't, and the ledger has no entry for today, it alarms and sends out exactly one make-up round. The late watchdog only checks whether the ledger has today's entry, or the run log has a publish-finished stamp. If neither exists, it only alarms and states the last stamp — it never sends a make-up, so it can't collide with a round still running and double-post.
- **Problems come in four levels, same across the whole flow:**
  1. Degradable: one source won't open, non-core material missing, one voiceover segment bad. Follow the replacement order in the matching guide, log the four elements, and keep going — one source or one segment must not stall the round.
  2. Quality or compliance gate: a fact won't check out, a sensitive hit, a product picture that doesn't match, subtitles or audio failing acceptance. Stop at the current stage; swap the topic, swap the material, or redo it. Nothing that fails a gate moves to the next stage.
  3. Publish gate: topic tags not all blue, AI declaration not picked, the file to post doesn't match the file that passed acceptance, the main site not confirmed logged in. Don't press publish. Save a ready-to-post pack and report, as the publish guide says.
  4. Run or session: no stamps, browser session dead, blank page. First check the post list, the main site status, and the stamps to get the real outside state clear, then resume from the unfinished stage. Don't rerun finished stages, don't guess the state.
- One approach gets at most the table's number of retries. Still stuck after that, switch approaches, or stop at the matching gate. No temporary "hurry up" or "post it now, fix it later" gets around a quality, compliance, or publish gate.

## Numbers table (the only authority — change a number here and in config, nowhere else)

The recommended defaults are the current setup. When you change one, change this table and the matching key in `config.yaml` together, and keep the two in sync.

### Time and scheduling

| Parameter | Recommended default | Config key |
|---|---|---|
| Start time | 06:00 | `schedule.open_time` |
| Publish deadline | Before 08:00 | `schedule.publish_deadline` |
| Early watchdog | 06:20, checks the start stamp | `schedule.watchdog_early_time` |
| Late watchdog | 08:12, checks the publish | `schedule.watchdog_late_time` |
| Weekly review | One day each week | `schedule.review_weekday` (fill in "周日", Sunday) |
| Weekly review time | About 20:18 | `schedule.review_time` |
| First stamp limit | Within 5 minutes of starting | `schedule.stamp_first_minutes` |
| Long-stage extra stamp interval | Every 30 minutes | `schedule.stamp_long_stage_minutes` |
| No-stamp means failed | Over 75 minutes | `schedule.stamp_stale_minutes` |
| Retries per approach | 2 | `ops.retry_max` |

### Topics

| Parameter | Recommended default | Config key |
|---|---|---|
| Total sourcing cap | 30 minutes | `sourcing.total_minutes` |
| Per-source cap | 5 minutes | `sourcing.per_source_minutes` |
| Scan window | First 20 minutes scan wide, after that only check the leading candidates | `sourcing.scan_minutes` |
| Shortlist check count | 2 | `sourcing.shortlist_count` |
| Channel probe cap | 1 minute | `sourcing.probe_minutes` |
| Freshness | Last 48 hours only | `sourcing.freshness_hours` |
| Fallback widening | At most 7 days (the sensitive and fact gates never widen) | `sourcing.freshness_fallback_days` |
| Hot window | 12–24 hours after the event | `sourcing.hotspot_window` |
| Sequel check | Before settling, scan the last 30 days of posted topics for follow-ups (announcements, releases, price or policy changes, results landing); a follow-up means a same-day extra post | `sourcing.sequel_check` |
| Queued topics | Before dispatching, check the queued area first — use an unexpired queued topic directly, and delete it from the queue once used, logging the posted entry as usual | `sourcing.queued_topics` |
| Event matching | During daily topic work, check the activity center and keep a list of ongoing events; when a candidate direction matches an event theme, follow the event's requirements and note them | `sourcing.activity_match` |

### Content

| Parameter | Recommended default | Config key |
|---|---|---|
| Category list | See `content.categories` — change it in config to your own | `content.categories` |
| Category rotation | As different from yesterday as possible | `content.rotation` |
| Weekly cap for one category (example) | Set a cap for a category that tends to pile up — example 2 posts, change it to your categories | `content.category_weekly_cap` |
| Weekly mix (example) | News 4 : tutorials 3 | `content.weekly_mix` |
| Title versions to write first | 3, then pick | `content.title_versions` |
| Title target length | 10–16 characters | `content.title_target_chars` |
| Title hard cap | 20 characters (weighted: Chinese characters and full-width punctuation count 1, Latin letters, digits, and half-width symbols count 0.5, emoji count 1) | `content.title_max_chars` |
| Title trade-off order | Resonance or conflict hook first, asset signals (numbers, lists, things to take away) second, search term position third; when something must go, cut the asset, never the resonance | — |
| Core search term position | In the first 10 characters | `content.title_keyword_first_chars` |
| Body cap | 1000 characters; everyday slim target about 500 — details go to the video, the body only carries the hook, the conclusion, the takeaway list points, and a this-or-that question, fitting on one screen | `content.body_max_chars` / `content.body_target_chars` |
| Topic tag count | 5–8 (big terms + niche terms + long-tail terms) | `content.topics_min` / `content.topics_max` |
| Title anchor | Step 0 of writing: settle the anchor first (the single most striking concrete point, keyword 4+ characters, appearing word for word in the final title); the 3 versions are three different angles on the same anchor; order rule: anchor → angle → emotional tone | `content.title_anchor` |
| Title emotion | Emotion must be exaggerated (exaggerate feelings only, never facts); the settled-title reasons list two machine-readable lines, "emotion-carrying words" and "emotion link"; the carrying phrase starts no later than weighted character 10 and stays within the first half of the title; neighboring episodes must not share an emotion family | `content.title_emotion` |

### Video and audio

| Parameter | Recommended default | Config key |
|---|---|---|
| Script word count | 480–650 characters | `video.script_chars_min` / `video.script_chars_max` |
| Finished video length | 80–110 seconds (after speed-up) | `video.duration_min_seconds` / `video.duration_max_seconds` |
| Speed | 1.5x | `video.speed` |
| Fixed closing line | "记得点赞、关注哦" (Remember to like and follow) — change it to your own | `video.ending_line` |
| Frame size | Portrait 1080×1920 (9:16) by default, landscape 1920×1080 (16:9) optional | `video.orientation` / `video.width` / `video.height` |
| Cover size | Made separately, 1080×1440 (3:4) | `video.cover_width` / `video.cover_height` |
| Cover headline lines | 3–5 lines | `video.cover_lines` |
| Issue number | The cover carries "第 X 期" (Episode X), X being the cumulative publish number in the ledger; from which date it becomes mandatory goes in `publish.issue_required_from` — leave it blank and it only warns, never fails | `video.issue_on_cover` / `publish.issue_required_from` |
| Intro and outro | Optional: one short brand intro and outro clip each, joined before and after the main video. Normalize them to the main video's specs first; direction must match the main video — never a vertical main video with a horizontal intro. When the outro already carries a like-and-follow ask, the main video's ending drops its own ask line or card — don't repeat it on both sides | `brand.intro_file` / `brand.outro_file` |
| Opening | First 3 seconds give the conclusion or the conflict, no intro clip | `video.opening_seconds` |
| Opening title card | After the intro clip, before the first main segment, there must be a bold title card: big title plus this episode's key visual, so viewers know at once what the video is about; a small corner label alone doesn't count | `video.title_card` |
| Info point rhythm | One every 10–15 seconds, at least 5 in the whole video | `video.info_point_every_seconds` / `video.info_points_min` |
| Turn | One turn in the middle; a this-or-that question in the last 5 seconds | `video.ending_question_seconds` |
| Motion events | At least 4 per segment; at least 2 per 10 seconds on average across the video | `video.motion_events_per_segment` / `video.motion_events_per_10s` |
| Pause at motion landing | At least 0.3 seconds after a key conclusion lands | `video.motion_pause_seconds` |
| Subtitle position | Bottom-anchored: the bottom edge fixed at 80% of frame height (y=1536 at 1080×1920); when the line count changes, the block only grows upward, the bottom edge never moves; acceptance measures the bottom edge, pass band ±10px (1526–1546). These numbers are measured reference values for Xiaohongshu vertical — re-measure per the motion library's method before using them on another platform | `video.subtitle_bottom_pct` / `video.subtitle_tolerance_px` |
| Subtitle exclusion zone | Below the top edge of the system info area (84.4% of height, measured y=1621) — no subtitles or key text there | `video.system_info_top_pct` |
| Subtitle line count | Only the current sentence per card, at most 2 lines | `video.subtitle_max_lines` |
| Subtitle line breaks | Break lines during writing to the subtitle rhythm — no single subtitle over 38 characters, so every card fits in at most 2 lines on screen; never leave it to the video stage to discover a 3-line squeeze | `video.subtitle_max_chars` |
| Layout use | The main content area (from the top safe line y=250 down to y=1340 above the subtitle block) must be filled: each segment's main body spans at least 55% of the content area vertically, blank space at the bottom at most 25%; lay out content first, then place subtitles | `video.content_min_span_pct` / `video.content_max_blank_pct` |
| Silence detection threshold | -45dB, 1.5 seconds counts as one silence | `audio.silence_threshold_db` / `audio.silence_window_seconds` |
| Silence fails | Any silence over 2 seconds outside intro/outro sends it back | `audio.silence_max_gap_seconds` |
| Per-segment audio-video alignment | Each segment's picture and voiceover within 0.5 seconds of each other | `audio.segment_align_max_error_seconds` |
| Single-segment silence flag | A silence of 1+ seconds inside one segment means shelve that segment first | `audio.segment_silence_flag_seconds` |
| Product shot segments | For a specific product, product pictures appear in at least 2 main segments; for software, every major piece of software needs its real interface, at least 2 segments total | `video.product_shots_min_segments` |
| Rendering | Web-page video: HTML/CSS layout + GSAP motion, frame-by-frame screenshots on this machine, then joined; 30fps, about 30 minutes for a full video | `video.render_fps` / `video.render_budget_minutes` |
| Encoding | H.264 High, yuv420p, video_track_timescale 600, AAC 48kHz, use_editlist 0, faststart | `video.codec` and others — details in the video guide |
| Picture quality | CRF sets quality (not bitrate): default 13, pick within 12–14, lower means clearer and bigger. Finished size cap 100MB — over that, the join script raises CRF and re-joins until it fits. `pipeline/assemble.sh` `--crf` and `--max-size-mb` defaults match this | `video.crf` / `video.max_size_mb` |
| Minimum bitrate | Video stream under 2000 kb/s (2 Mb/s) only earns a warning from `validate.py`, never a fail. This is a backstop reminder: in CRF mode bitrate follows picture complexity, so a simple picture at low bitrate is still sharp — judge sharpness from pulled frames in the end | `video.min_bitrate_kbps` |
| Blank frames | Picture nearly empty (near-solid color, at most a line or two of text) for 2 seconds straight — `validate.py` only warns, never fails | `video.blank_min_seconds` |
| Frozen picture | Picture still (content present, just not moving) for 1+ seconds straight — `validate.py` only warns, never fails. Not the same as blank frames: freezing mostly means the animation finished or a transition stuck | `video.freeze_warn_seconds` |
| Cover main visual | AI-generated from the title + content; the big title text and issue-number corner label are composited deterministically — the model must never render the Chinese title directly; the AI source picture stays in the material folder, and the acceptance checklist carries its own machine-readable line; a failed generation may only be retried with a new prompt or a new model — never downgraded to a screenshot or video frame | `video.cover_ai_source` |
| Visual style (optional) | The layered paper-craft style lives in the appendix `core/paper-style.md`; read it before starting when you use it, and check against it item by item at acceptance | — |
| Finished size | The 100MB finished-size cap is enforced by the join script; the acceptance script separately checks size once more, and only warns when over | `video.max_size_mb` |
| Voiceover | Pick the voice in config — the repo never hard-codes any voice name. Before starting, run the voiceover smoke test (`pipeline/tts/tts-smoke.sh`): the main engine test-synthesizes one line, and only if it works do you use it; if it fails, it switches to the backup engine automatically. At acceptance, check the voiceover bitrate against the expected value — a mismatch mostly means the engine got swapped | `tts.provider` / `tts.voice` / `tts.expected_bitrate_kbps` |

Portrait is the default direction, and that's enough. Only pick landscape for content that reads better wide — screen recordings, tutorials, scenery — by changing it once in config; every post after that follows it.

### After publishing, and reviews

| Parameter | Recommended default | Config key |
|---|---|---|
| Follow-up window | 2 hours from the actual publish time | `followup.window_hours` |
| Follow-up interval | Check every 30 minutes, stop when the window ends | `followup.interval_minutes` |
| Sensitive library re-check | At the first weekly review of each month, re-read the platform rules and update | `compliance.sensitive_review` |
| Ledger file | Topic and publish records go here | `paths.ledger_file` |
| Interaction state file | Handled comments and DMs go here, for dedup | `paths.interaction_file` |
| Data directory | Each day's material folder goes under here | `paths.data_dir` |

## Hard gate list (no temporary excuse gets around these)

1. **Sensitive content is a straight veto.** Check the topic against the sensitive appendix's drop list first — one hit drops it, no discussion about whether a different angle could work. Before publishing, sweep six faces one by one: title, body, voiceover script, subtitles, cover text and picture, topic tags and first comment. On a hit, rewrite the whole sentence's meaning — no homophones or split characters to dodge it. Details in guides 01 and 04 and the sensitive appendix.
2. **Fact-checking.** A settled key fact needs an official first-hand source, plus at least 1 independent source confirming it. With no official source, at least 2 mutually independent sources must agree. A fact that won't check out gets dropped, or honestly labeled as a leak. Never count several articles on one retelling chain as several sources.
3. **All topic tags blue before posting.** Check one by one before publishing: every tag blue, count matching. Anything less, and publishing is off. A tag that won't turn blue means stop and save a ready-to-post pack — no deleting tags, no posting with a gap. Details in guide 04.
4. **Entry rule.** To do anything on the creator platform, open the Xiaohongshu main site first, widen the window, confirm logged-in status on the main site, then enter through the site's own entry point. Never type the creator platform's domain straight into the address bar, and never take its login popup as a conclusion. Only when the main site, in a wide window, also confirms you're logged out may you say the owner needs to scan a code in person. Details in guide 04.
5. **Pre-publish compliance self-check.** Eight items, one by one: AI declaration, absolute-word sweep across six faces, zero diversion, no source labels, no wholesale copying, no flame wars and no cracking content, no financial advice, sensitive six-face self-check. Write each result into the acceptance checklist — never a single line saying "self-checked". Details in guide 04.
6. **Acceptance needs evidence.** Saying "fixed" or "passed" must come with evidence: old and new frames or files, the re-check time, the measured numbers. A measured number must carry the raw value, the moment it was measured, and the method — a bare conclusion can't be re-checked later, right or wrong. A finished-video acceptance checklist with any of its six items missing doesn't count as passed. After any rework or re-render, the old acceptance is void — re-run the key checks on the new file. Run `validate.py` once at the end of video work as the machine acceptance. Details in guide 03.
7. **Problems get the four elements.** When something goes wrong, reports and logs must carry all four: which step and which exact object; the page's or tool's own words, or the screenshot path; what you tried, how many times each, and what each attempt gave; how it was handled in the end and what it means for the finished piece. Never close with just "broken" or "failed". Report levels are in guide 05.

## How the manager and sub-agents split the work

- **The manager** runs each round. It reads this constitution page first, runs the triple duplicate check, writes the first stamp; then dispatches stages in order, 01 through 05. On receiving each stage's evidence list, it checks it item by item against that stage guide's acceptance items — only then dispatching the next stage, sending back failures for rework, or handling them by problem level. It keeps the run log's stamps throughout, and reports at the end by guide 05's level rules. Weekly reviews run the same way under guide 06: dispatch, accept, report.
- **Serial, never parallel.** Only one stage sub-agent runs at a time. Until the previous stage passes acceptance, the next one doesn't start. Sub-agents never dispatch their own sub-agents. The reason is practical: topic, script, video, and publishing feed on each other — each step eats the previous step's accepted product. Parallel work only steps on products, repeats work, and in the worst case double-posts.
- **Sub-agents**, one per stage. Each reads only the constitution page plus its own stage guide (plus that stage's named appendices). Its input is only the previous stage's product paths from the manager's dispatch — it doesn't go digging through old products on its own. Products must land in the day's material folder or the named record file, and come back in the stage guide's evidence-list format. It doesn't casually do the next stage's work. On a gate problem it stops at once and hands the four elements back to the manager — never finding its own way around, especially on the topic, sensitive, and publish gates.
- **Every dispatch must state:** stage name, date and the day's material folder path, previous stage product file paths, the guide path for this stage, the evidence-list format to return, and this stage's deadline requirements (numbers per the table).
- **Shared evidence-list format:** stage name / product file paths and key numbers / item-by-item results against this stage's acceptance items / the four elements for problems (write "none" when there are none) / items awaiting manager confirmation (write "none" when there are none). An evidence list with missing items counts as unfinished — the manager must not wave it through.
- **Who can decide:** degradable problems, the sub-agent handles itself by the guide's replacement order, leaving a trace. Quality, compliance, and publish gates: only the manager decides to swap topics, hold a post, or save a ready-to-post pack. Things the owner must decide (deleting and reposting, scanning a code to log in), neither manager nor sub-agent may decide for them.

On a platform with no sub-agents, a single agent does the same steps in the same order: after each stretch, self-check the evidence list, pass it, then do the next stretch. The rules don't change — only the headcount becomes one.

## Stage guide index (`stages/` — read the one for the step you're on)

- `01-sourcing.md` Topics: how to fill in sources, probe liveness, judge heat, check facts, what proof a settled topic keeps, and how to fall back when there's no topic. Read when dispatching topics, plus the sensitive appendix's drop list.
- `02-script.md` Writing: script structure, title and body standards, writing acceptance. Products on disk are `post.md` and `scripts.txt`.
- `03-video.md` Video: the web-page video method, material and real-interface requirements, subtitle and audio rules, the finished-video acceptance checklist. Run `validate.py` at the end.
- `04-publish.md` Publishing: the entry rule, the eight-item compliance self-check, the topic-tag gate, the first comment, post-publish re-check, and what to do when publishing breaks. Read when dispatching publishing, plus the sensitive appendix.
- `05-followup.md` Reporting and follow-up: three report levels, how to write the ledger, how to reply to comments and DMs, how dedup works, and what to write when something can't be verified.
- `06-review.md` Weekly review: data backfill, draft cleanup, monthly sensitive library maintenance, consistency patrol, and how rules get updated.

## Appendix index

- `viral-playbook.md`: the viral knowledge base — title formulas, opening hooks, two body structures (save-type / comment-type), cover text rules. Check before writing: pick a formula for the title first, settle the body type before writing. The examples inside are illustrations; the formulas and order are general — swap in your category's content.
- `sensitive-words.template.md`: the sensitive content appendix, with the drop list, sensitive word categories, and the six-face self-check. Before using it, copy it as `sensitive-words.md` and add or remove entries for your own categories. Must read before settling a topic, must read for the pre-publish self-check, and re-read and maintain at the first weekly review of each month.
- `paper-style.md`: the layered paper-craft visual style appendix — color board, fixed prompt prefix, at least 4 layers per scene, parallax between layers, elements moving independently, no pure push-pull inside any 5-second window, physics rules, paper-craft landing language. When making videos in this style, read it before starting and check against it item by item at acceptance. Its color board and prompts are general defaults — change them for a different category.
- `lessons.template.md`: the empty template and writing rules for the lessons log. Before using it, copy it as `lessons.md` and append review conclusions by date. Must read at weekly reviews; when topics or video work hit something that looks like an old problem, flip through it. When an entry becomes a fixed rule, promote it into the constitution page or the matching guide, and mark on the original entry where it went.
- `validate.py`: the finished-video machine acceptance script — reads only, never edits files. Usage: `python3 core/validate.py <day's material folder path>`. Run once at the end of video work and once at manager acceptance, and paste the output into the evidence list. Thresholds come from the repo root's `config.yaml`; without one, the script's recommended defaults apply, and the output says so.

## How to change a rule

- These files are alive. The newest version of this constitution page rules; details follow the matching stage guide. When the two conflict, the constitution page wins, and the weekly review fixes them up.
- Numbers change only in the table and in config — never a second copy inside a guide.
- Every change, and why it changed, gets one line in the lessons log or the review record, so it's findable later.
