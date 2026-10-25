[中文](README.zh-CN.md) | English

# Douyin / TikTok module: trending videos + subtitles

Every day, find the hottest videos on video platforms, download them, add subtitles, and post them to Douyin or TikTok. The format is the original plus subtitles: keep the original picture and sound, don't re-cut it into a commentary video.

## Douyin or TikTok — pick one first

Douyin is the Chinese name; TikTok is the international one. Same pipeline, two outlets — pick before you start, because the outlet decides three things:

- **Audience and subtitle language**: Douyin = viewers in China, Chinese subtitles. TikTok = international viewers, subtitles in the audience's language (English by default).
- **Where it gets published**: Douyin goes through the Douyin creator center in the browser; TikTok goes through TikTok's creator center / upload page.
- **Where it gets downloaded from**: the download step just takes a video URL — pass a Douyin URL for Douyin, a TikTok URL for TikTok.

One honest limit: the four sensitivity gates below are written for Douyin. TikTok's own community rules are not a separate gate yet — check those before posting to TikTok. The pipeline steps, the scripts, and the stop line are the same for both.

## Pipeline (7 steps)

1. **Pick**: by heat, fit, and how interesting it is. Direction: positive and genuinely fun (heartwarming, clever, warm, fun twist). Never pick dark, freak-show, gross, depressing, or controversial material.
2. **Download**: several routes as backup, never get stuck on one. Different clients get different quality ladders; if one can't get HD, switch clients or switch clips. Only report back when every route is dead, and write down where each route got stuck.
3. **Transcribe and translate**: when there are no official subtitles, transcribe the speech. Never use the smallest transcription model (small models drop lines). The number of transcribed segments must match the number of subtitle lines — every line the person in the video says needs a matching Chinese subtitle, none skipped; mark the parts you can't hear clearly, don't quietly skip them. Parts of the original wording that are a problem (sensitive words, swearing, engagement bait, platform-specific talk, wording that doesn't fit this platform) get rewritten into clean wording with the same meaning — meaning and rhythm kept, problem removed; log every rewrite (rough original → changed to what → why).
4. **Burn in subtitles**: subtitles must stay clear of the app's bottom info area (avatar, account name, title and description, progress bar — about the bottom 22% of the screen). On a 1080×1920 frame, the subtitle bottom edge sits about 24% up from the bottom; other frame sizes scale by height at 24%. Acceptance must include this: pull frames with subtitles, overlay a mock bottom info area, and eyeball that nothing overlaps.
5. **Voiceover (optional)**: clips with spoken lines get voiceover + subtitles (one voice for the whole account); pure music or mood clips get subtitles only, no voiceover (keeps the original feel). The voiceover text is the subtitle text, line by line; numbers, English, and other easy-to-misread bits get rewritten as Chinese characters first, then generated, then checked by transcribing back. In the mix, the original sound ducks automatically under the voiceover; finished loudness about -15 LUFS; voiceover entry within 0.1 seconds of the subtitle start.
6. **Cover and title**: see the two sections below.
7. **Publish**: see the publish section below.

## Cover

- **A homemade titled cover comes first**: a cover you make yourself must carry title text (a big title + one subtitle line). Never use a bare video frame with no words. It only counts once you have actually uploaded it and confirmed in preview that it took effect — don't skip it just because the platform already auto-picked a smart cover.
- Only fall back to a smart cover if upload fails, and the smart cover still needs title text or a strong match to the content — never a wordless pure frame. If even that fails, use the platform default and note it in the report.
- Pick the brand outro by the original's orientation: vertical clips get the vertical outro, horizontal clips the horizontal one. Never stretch a horizontal clip into vertical or the other way around; keep the original frame all the way through. **Never join the outro with a straight concat**: the outro audio can fail to decode in a straight join and go silent at the end — join video + audio on separate tracks, then check the tail has sound (sound counts as passed).

## Title

- Write and polish from the viral title formula bank: open suspense, numbers + result up front, contrast, direct emotion, immersive process + time promise.
- **Hook rule: never spoil the ending in the title** (any wording that gives the result away first is banned). End suspense with a question ("Guess what happened?"); the payoff stays in the video. The cover subtitle matches the title's tone, also a suspense question, never a spoiler on the cover.
- Red lines don't move: no made-up numbers, no empty emotion, no suspense that never pays off.
- Every post's topics must include the account-name topic (posted together with the content topics).

## Watermark

- The channel's own burned-in logo doesn't need removing. Other platforms' watermarks are still avoided. If the outro has its own promo card (subscribe, past videos), it can be cropped, with the seconds logged.

## Four sensitivity gates (in order; any hit drops the whole clip — no deleting words, no blurring, no cutting around it)

1. **Topic filter**: check the category first. Green-light (pickable) = natural science, everyday animals, food making, handmade repair, pure sports moments, pure instrumental music. Red-light (never pick) = political news, foreign elections and political figures, social protests and mass incidents, political talk shows, military and war, religion and ethnicity issues, historically sensitive topics, street interviews touching China, topics that use a group's traits as the joke. Green-light categories have their own veto points too — gates 2–4 still run in full. **Disgusting material is a straight veto**: excrement, secretions, vomit, and other gross substances are never picked — not even as nature science.
2. **Full-video frame check**: watch the whole clip before deciding. Check for the violations that have no words: flags, slogan banners, maps and border drawing, protest crowds, uniforms and weapons, religious rituals, gore. A frame carrying another platform's watermark, logo, or account exposure counts as a violation under the diversion rules too.
3. **Subtitle scan in both languages**: run both the English original subtitles and the Chinese draft through the wordlist. English political jokes or slang that only turn bad once translated into Chinese still count. Homophones, split characters, pinyin initials, full-width circled characters, and other variant forms count — and don't hide words with variants in your own subtitles either.
4. **Title and cover final review**: title, cover text, and copy get one more full pass.

**Judgment rule (shared by all four gates)**: politics and discrimination are judged by topic, not by stance — if the topic, the person, or the core joke falls inside a red-line topic, the whole clip is dropped, whether the original supports, opposes, or jokes about it neutrally. Discrimination covers 13 protected traits: gender, age, region, ethnicity, race, religious belief, nationality, physical condition, mental disability, victim experience, gender identity, economic status, education level. Promoting a stereotype is itself a violation — no slur required. Sensitive areas (medical, finance, legal, minors) are off-limits entirely.

## Publish

- **AI declaration must be checked**: check the platform's AI content declaration on the publish page. Writing one line in the title is not a substitute for checking it. Never remove or edit the labels the platform adds.
- **Scheduled publish 2-hour rule**: a scheduled publish can only pick a time more than 2 hours after the upload is submitted. Slot more than 2 hours past submission → schedule it. Under 2 hours → wait and post directly at the slot. Never change the time to force a schedule, and never post early. If the platform rejects the scheduled time or the option isn't there, don't switch to posting immediately — save a draft and report back.
- **Stop line**: throttling, takedown, copyright complaint, or penalty points — any one of these means stop immediately and review. No posting through it to test.
- **Zero automated interaction**: no auto likes, comments, DMs, or follows. Only reply to real comments.

## Copyright stance (risks stated, your call)

This module sets no copyright-blocking gate by default — but that is one user's own stance, not a recommendation. Whether an as-is repost + subtitles counts as a derivative work is the platform's call, not ours. To play it safe, only post content you own or have licensed. The filters only handle sensitive content, not copyright — think this through before you use it.

## Cost advice

Free routes first: if any step costs money, stop, look for a free replacement, and if there is none, skip it for now. Never pay first and report later for the sake of one video.

## Runnable code (`scripts/`)

Only needs Python 3 standard library + ffmpeg (the download step also needs yt-dlp). Get these steps working before talking about full-auto.

```bash
# 1. Download a candidate clip — pass a Douyin or TikTok video URL, whichever outlet you picked (if yt-dlp is missing it tells you how to install it, no silent failure); the script prints the outlet it guessed from the URL first — confirm it before continuing
bash scripts/fetch_video.sh <video URL> [save directory] [max height, default 1080]

# 2. Sensitivity scan: copy the wordlist template first, fill in your own words, then scan. Scan before burning: a hit drops the whole clip, don't burn first
cp sensitive-words.template.txt sensitive-words.txt   # fill in words; this file is in .gitignore, committing won't carry it
python3 scripts/scan_subtitles.py --srt subtitles.srt --wordlist sensitive-words.txt
# Exit codes: 0 no hit, 1 hit (a hit drops the whole clip), 2 wrong usage or file problem

# 3. Burn in subtitles: bottom edge 24% up from the bottom (1080×1920 = 460px, see pipeline step 4)
python3 scripts/burn_subtitles.py --video original.mp4 --srt subtitles.srt --out finished.mp4

# 4. Brand outro: join on separate tracks (no straight concat, see the cover section)
python3 scripts/append_outro.py --main main.mp4 --outro outro.mp4 --out finished.mp4
```

Test record (2026-10-25): subtitle burn-in with 2 lines, bottom edge 460px; outro 640×360 normalized to 1080×1920, 3s + 1s = 4.04s; sensitivity scan correct on hit, no-hit, and empty wordlist; the download wrapper on this machine correctly reported that yt-dlp was not installed (no live download tested — install yt-dlp first).

Not yet code, still needs a person or another tool: speech transcription, voiceover synthesis, cover generation, final publish (through the matching outlet's creator center — Douyin or TikTok). The wordlist content is not in the repo — the template only shows the format; the wordlist is yours.
