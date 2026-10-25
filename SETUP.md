[中文](SETUP.zh-CN.md) | English

# First-time setup, one item at a time

No code knowledge needed. Every item states: what it controls, how to fill it in, and what's recommended.
Everything you fill in goes in `config.yaml`. If that file doesn't exist yet, run `bash scripts/setup.sh` first — it copies the sample config for you, and prepares the environment and third-party libraries along the way.

In a hurry? Copy the "easiest way to install" paragraph from the README to your AI assistant (Muse, Dots, or Grok Bot all work) — the repo address is already in that paragraph, and it walks you through the items one by one.

## Before Item 0: which language?

First, ask the operator whether they want Chinese or English, and use that language for everything after — setup, daily runs, and reports. The repo docs come in both languages; read the version in the language picked. (Standing rule: `core/CONSTITUTION.md`.)

## Item 0: pick your automation level first

Set this one first: fill in `automation.mode`. The three levels work like this:

- **Full-auto (`full`)**: sourcing, writing, video, publishing — the whole package, you only look at results. Easiest, but the account is yours, and platforms watch fully automated hosting closely — a new account shouldn't start on this level.
- **Semi-auto (`semi`)**: everything automatic up to publishing, where it stops with a ready-to-post pack ready — you look it over and press publish yourself. **Start on this level**, and talk about moving up after a steady week or two.
- **Manual (`manual`)**: it only helps you source topics and write scripts; video and publishing are yours. Fits trying out script quality first.

You can change levels any time — changing one needs no reinstall.

## Item 1: what direction your account takes

Fill in `account.name` (nickname, written as the account shows it) and `account.channel_name` (what you call yourself at the start of videos — leave it blank if you don't have one).
Direction doesn't go in config, but settle one sentence first: who it's for, what it covers, what it never covers. Without that sentence settled, the topic step can't judge "what does this topic have to do with the viewer", and scripts come out flat.

## Item 2: who it's for

Settle this one too: how old the viewers are, in what situation they'd need what you cover, what hurts most. The more concrete, the better. For example, "office workers, scrolling on the commute, hurting over all kinds of membership fees" works far better than "young people". Once it's settled, tell the AI assistant once, so it keeps it in the topic requirements.

## Item 3: categories and rotation

Fill in `content.categories` — swap the sample categories for your own — then settle three things:

- Rotation: as different from yesterday as possible, not the same category several days running.
- The category that tends to pile up: its weekly max, in `content.category_weekly_cap`.
- The week's rough news-to-tutorial ratio, in `content.weekly_mix`. Tutorials get searched for, and old viewers come back to them — don't let the ratio run too low.

## Item 4: source list

Fill in `sources` in config — four things per source: name, URL, what to watch (a chart, a board, an official account — any of them), and max minutes to spend.
Four to six sources is enough to start — don't be greedy. Two reminders:

- Comment sections only show heat and what people are annoyed about — never use them as facts.
- Before covering something, first have the official word, then find an unrelated source that matches it — only then does it count as checked. When they don't match, either don't cover it, or say clearly it's still unannounced news.

## Item 5: Xiaohongshu login (only you can scan the code)

Nobody can do this step for you, and passwords and verification codes go to no one and into no file. Steps:

1. In the browser your AI assistant can use, open the Xiaohongshu main site `www.xiaohongshu.com`.
2. Scan the code with the Xiaohongshu app to log in — logging into your own account.
3. Widen the browser window and confirm the main site's top-right shows your own avatar — only then does it count as logged in.
4. From then on, every creator platform job enters through the main site's own entry point — never type the creator platform's URL straight into the address bar. Typing it directly pops a standalone login page that looks like an expired login, but it isn't. Judging logged-in or not only looks at the main site.
5. Whenever the main site itself shows logged out, scan once more and you're back. Finished videos and scripts stay saved waiting for you — nothing gets lost.

## Item 6: when to post, and how often

Fill in the `schedule` group. Recommended values are already filled in: start work at 6 in the morning, post before 8. The two hours in between exist because rendering one video alone takes about half an hour.
Don't turn off either watchdog: the early one checks real work actually started, the late one checks the post actually went out. A real case of "the task looked like it was running but did nothing" got caught by them.
Keep one weekly review: fill in `schedule.review_weekday` and `review_time`.

## Item 7: voiceover

Fill in `tts.provider` (the two routes below take `edge` and `sherpa` respectively) and `tts.voice`. Both routes are free:

- **edge-tts**: needs internet, many voices, fastest to start. Use this one first.
- **sherpa-onnx plus MeloTTS**: runs on your own machine, no internet needed, but downloads a model file once first. Use it when the network is awkward, or when you want everything on your own machine.

Listen to a few voices yourself and pick one that sounds good, then put its name in `tts.voice`. Once picked, don't keep switching — viewers recognize the voice.
Speed goes in `video.speed` — 1.5 is recommended. The fixed closing line goes in `video.ending_line` — you can swap in your own words.

## Item 8: what videos look like

Fill in the `video` group — the recommended values work as-is. Set the frame direction first, then the three easiest to trip over:

- Frame direction goes in `video.orientation` — and match `video.width` and `video.height` to it. Portrait 1080×1920 is the default (fill in portrait); Xiaohongshu and Douyin both push portrait, full screen on phones. Screen recordings and tutorials read better wide — pick landscape 1920×1080 (fill in landscape, width and height to 1920 and 1080). Pick once in config, and every post after follows it — no per-post changes.
- Don't move the subtitle position. It's bottom-anchored: the bottom edge fixed on the line at 80% of frame height, measured from real viewer screens on the Xiaohongshu app — on phones during playback, avatars, nicknames, and titles all stack on the lowest band, and the subtitle bottom edge sits above that band with a gap, so nothing gets covered. To use it on another platform, re-measure first by the motion library's method, then change `subtitle_bottom_pct` and `system_info_top_pct` in config.
- Voiceover scripts run 480 to 650 words; finished videos run 80 to 110 seconds. Too short says too little; too long and people swipe away.
- Make the cover as its own 3:4 big-text picture — never the video's first frame as a fill-in. With issue numbers on, the issue count becomes a hard rule from the date filled in `publish.issue_required_from`.

## Item 9: sensitivity and compliance

Fill in `compliance.sensitive_review` — once a month re-read is recommended.
Three rules to memorize first: pick the AI content declaration at publish time; the script must carry no diversion wording (contact info, outside links, QR codes, and the like); the sensitive word list lives in `core/sensitive-words.template.md` — run the drop list before picking topics, and drop any topic it touches outright. Finer details live in `docs/compliance.md`, all in plain words.

## Item 10: where your data goes

Fill in the `paths` group — the default sits in the repo's `data/` folder. Three things: each day's material folder, topic and publish records, and handled comment and DM records.
This is your own data — never send it to a public repo. The repo's `.gitignore` already blocks it — don't hand-edit that file.

## Item 11: what it costs, so you know

The tools are all free: the video libraries, ffmpeg for joining, voiceover — none of it costs money.
The only thing that costs is the AI assistant itself. Muse, Dots, or Grok Bot — whichever you use, you need your own account, and subscription or usage fees are yours. This project connects to no paid interface.
Three assistants' bars, stated first: Dots needs ChatGPT Pro or Business Premium to use, and we haven't tested it running this system yet. Grok Bot is still in beta, open only to some SuperGrok Heavy users, also untested. Muse is the one currently running and verified.
One more thing costs no money but costs time: rendering one video takes about half an hour, with the machine on.

## Finally: self-check once

Both must pass before setup counts as done:

1. Run `bash scripts/check-env.sh` — nothing marked "missing" means pass.
2. Check with the sample: `python3 core/validate.py examples/example-issue`. Voiceover word count and post.md structure both PASS is the expected result. The video and cover items reporting FAIL is normal — the sample ships with no real video.

Then the first real post can run. Use semi-auto for the first one: a ready-to-post pack prepared, you look it over yourself, then post.
