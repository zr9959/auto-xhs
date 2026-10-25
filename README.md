<p align="center">
  <img src="docs/assets/banner.png" alt="Auto-xhs" width="760">
</p>

<h1 align="center">Multi-platform automated operation and publishing (Xiaohongshu / Douyin / X / YouTube / WeChat Official Accounts, for Muse, Dots, and Grok Bot)</h1>

<p align="center"><strong>Cloud AI agents run your accounts end to end: Xiaohongshu by default, plus Douyin, X, YouTube, and WeChat Official Accounts as separate modules</strong></p>

<p align="center">
  <img src="https://img.shields.io/github/license/zr9959/auto-xhs" alt="MIT license">
  <img src="https://img.shields.io/github/stars/zr9959/auto-xhs" alt="GitHub stars">
  <img src="https://img.shields.io/github/forks/zr9959/auto-xhs" alt="GitHub forks">
</p>

<p align="center"><a href="README.zh-CN.md">中文</a> | English · <a href="https://auto-xhs.tiybai.com">Landing page</a></p>

Auto-xhs is an open-source system that runs a Xiaohongshu (RedNote) account end to end — finding topics, writing scripts, making videos, posting, and replying to comments — through an AI agent's own browser, with no unofficial APIs and no paid tools.

Repository name: Auto-xhs

**Key facts**

- Free. MIT license. Every tool in the chain is free; there are no paid APIs.
- Works with three cloud AI agents: Muse, Dots, and Grok Bot. All three work in their own cloud computer and browser. Muse is the one we run every day and have tested end to end; Dots and Grok Bot are not tested by us yet.
- Recommended start: semi-auto. The agent prepares everything, you look at it, then it posts.
- Videos are portrait 1080×1920 by default; landscape 1920×1080 is an option you can pick in the config.
- Videos are built as web pages and captured frame by frame, not edited in a video editor.
- Nothing goes out until it passes an acceptance script: word count, length, resolution, silence, cover, issue number.

## More than Xiaohongshu

Xiaohongshu is still this repo's default, complete pipeline (everything in `core/`, from topics to posting and replies). `platforms/` holds four more platform modules, each independent — enable only the ones you need:

- **Douyin**: trending videos + Chinese subtitles pipeline (pick, download, subtitle, voiceover, cover, title, four sensitivity gates, publish).
- **X**: account warming, posting, replies (five-stage warming, human-like writing rules, cold-start rules, image rule).
- **YouTube**: English-channel playbook (titles, thumbnails, retention, Shorts, SEO, production standards, API-first workflow).
- **WeChat Official Accounts**: drafts + manual final publish (personal uncertified accounts cannot publish via API; the content playbook is still to come).

Each module states its own limits and risks up front — read those before you use it. Each module's README ends with a "Runnable code" section: the scripts that are actually tested, and the parts that are still manual. Index: [platforms/README.md](platforms/README.md).

Note on language: the four platform modules are fully in English. The Xiaohongshu core guides (`core/`, `adapters/`, `docs/`, `SETUP.md`) are still in Chinese for now — the Chinese version of this README is [README.zh-CN.md](README.zh-CN.md).

## What this project does

You log your own Xiaohongshu account into the browser your AI agent can use, once. After that, the agent takes over the whole job: every day it searches for fresh material, turns it into a script, builds a video, posts it, and follows up on comments. Everything happens inside the browser, clicked and typed the way a person would. No unofficial APIs. The posting pace is a normal person's pace.

It solves one problem: the slow part of running a Xiaohongshu account is the whole chain — searching, sorting material, making videos, posting, replying to comments. This project automates that whole chain. You only do three things: pick a direction, scan a QR code once, and (in semi-auto mode) take a look before each post goes out.

**Our motto: free, safe, efficient, simple.**

The honest part, up front: "safe" comes from acting like a person in the browser, plus a normal posting pace. It is not a guarantee for any account. Platforms watch fully automated accounts closely, so we recommend new accounts start in semi-auto and check each post before it goes out. The details are in [docs/compliance.md](docs/compliance.md).

## See it first

This is a weather forecast the system made by itself — the official example scenario pack in this repository. The data came live from the free Open-Meteo service; the script, the voice and the visuals were all generated automatically, and all six validation checks passed. As required, it stopped at a ready-to-post pack and was never posted.

<p align="center">
  <img src="docs/assets/demo.gif" alt="Animated frames from the weather example" width="300">
  <img src="docs/assets/weather-cover.jpg" alt="Cover of the weather example" width="300">
</p>

Left: animated frames from the finished video. Right: its cover.

## How the videos are made

Every video starts as a web page. That is the part that makes this project different.

First the video is laid out as a page: HTML and CSS for the layout, GSAP for the animation. Good-looking motion — titles coming in, numbers counting up, cards flipping — lives in a ready-made motion library, and the script just calls it. Then a browser holds the animation still and screenshots it frame by frame, 30 frames a second. At the end, ffmpeg stitches the frames into a video, adds the voiceover, and speeds it up to 1.5x.

Why do it this way: web pages are fast and good-looking for cards, charts, and price comparisons, and if a number changes you fix the page instead of re-editing a video. And because every frame is captured one by one, the animation looks exactly the same on every run — nothing drifts between today and tomorrow.

## The three assistants — differences, stated plainly

The rules, the acceptance checks, and the ready-to-post package format are the same for all three. The only difference is who presses the buttons.

One thing to get right first: Dots is not the regular ChatGPT chat. Dots is OpenAI's always-on cloud agent, launched on September 29, 2026. Each Dot has its own cloud computer and its own browser, can run on a schedule, can hand work to sub-agents, and can be told to ask for your approval before it acts. It needs a ChatGPT Pro or Business Premium plan. Grok Bot is xAI's cloud virtual-machine agent; it is still in beta, and by default it pauses before posting and waits for approval. Muse is the setup we run ourselves every day — that one is tested end to end. Dots and Grok Bot follow the same files and rules, but we have not tested them ourselves yet.

| What it can do | Muse | Dots | Grok Bot |
|---|---|---|---|
| Search for material, write scripts | Yes | Yes | Yes |
| Make the video (run the scripts) | Yes | Yes, on its own cloud computer | Yes |
| Split the work step by step | Smoothest — this is how it runs here | Yes — a Dot can hand work to sub-agents | Yes — a Bot can hand work to sub-agents |
| Start on its own every day | Yes | Yes — Dots can run on a schedule | Yes — Bots can run on a schedule |
| Publish in the browser by itself | Yes | Yes — and you can set it to ask you first | Yes — asking first or going ahead is your setting; by default it asks |
| Reply to comments after posting | Yes | Yes — on a schedule or when you ask | Yes — on a schedule |
| Weekly review | Yes | On a schedule or when you ask | Yes — on a schedule |

The full table is in [docs/capability-matrix.md](docs/capability-matrix.md). Read the guide for the assistant you use: [Muse](adapters/claude/README.md), [Dots](adapters/dots/README.md), [Grok Bot](adapters/grok/README.md).

## Three automation levels — you pick

- **Full-auto**: the agent does everything, including pressing publish.
- **Semi-auto** (recommended): the agent prepares a ready-to-post package — video, cover, text — and you look at it before it goes out.
- **Manual**: the agent only picks topics and writes scripts. You make and post the videos yourself.

During setup you choose the level yourself. The setup explains the three, recommends semi-auto to start, and does not decide for you.

## The easiest way to install it

Just copy the text below and paste it to your AI assistant — the repository address is already in it. It will download the repository, set up the environment on its own, and then walk you through the settings one by one:

```
Set up auto-xhs for me. The repository is https://github.com/zr9959/auto-xhs — follow the instructions in it:
1. Download the repository to my machine first (git clone if git is available, otherwise download the archive and unzip it), and go into the repository root. Run all the commands below from there.
2. Run bash scripts/setup.sh. It checks my environment, downloads the third-party libraries, and prepares the config file. If anything is missing, tell me and I will install it.
3. Then open SETUP.md and walk me through config.yaml one item at a time. First, let me choose one of the three automation levels — full-auto, semi-auto, or manual — and explain the difference clearly. Recommend semi-auto to start, but do not decide for me.
4. Stop at the Xiaohongshu login step. Tell me how to scan the QR code; I will scan it myself. Do not touch my password or verification codes.
5. When everything is filled in, run the acceptance checks on the example in examples/ and show me the result, then make the first post. Stop right before publishing it and let me look at it first.
```

## Installing by hand, step by step

Prefer to do it yourself? Six steps. Run every command from the repository root.

**Step 1: Install these first.** The video pipeline needs them; all are free:

- `ffmpeg` (with `ffprobe`, which normally comes with it): ffmpeg stitches frames and sound into the final video; ffprobe reads durations and dimensions.
- Node.js: get the long-term support version from nodejs.org. The frame-by-frame capture scripts run on it.
- `python3`: the acceptance checker and the voiceover examples run on it.
- `curl` and `tar`: the third-party libraries are downloaded with these. Most systems already have them.

You do not have to guess whether they are all there: after downloading the repository in Step 2, run `bash scripts/check-env.sh`. It names each item one by one and says in plain words what a missing one is for. The one-command script in Step 3 runs this same check first.

**Step 2: Download the repository.** With git:

```
git clone https://github.com/zr9959/auto-xhs
```

Without git, use the green Code button on the repository page to download the archive, then unzip it. Then go into the root — every command below runs from there:

```
cd auto-xhs
```

**Step 3: Run the setup script.**

```
bash scripts/setup.sh
```

It does three things, in order:

1. Checks the environment — the same check from Step 1. If a hard requirement is missing, it stops and tells you to install what is marked missing and run it again. Nothing already done is wasted.
2. Downloads the third-party libraries: GSAP 3.15.0, lottie-web 5.13.0, and canvas-confetti 1.9.4, into `motion-lib/vendor/`. Each package's hash is verified before it is installed. If the network is down, it says the download is where it stopped — fix the connection and run it again. If a hash does not match, it discards the file and stops, and it will tell you not to edit the hash written in the script; check the download source first.
3. Prepares your config file: it copies `config.example.yaml` to `config.yaml`, and you edit that copy. It never overwrites an existing `config.yaml`.

When it finishes by printing that everything is ready, plus the three next steps, this step is done.

**Step 4: Fill in config.yaml, following SETUP.md item by item.** Open [SETUP.md](SETUP.md) and go from item 0 to item 11. Each item says what it controls, how to fill it in, and what is recommended. Two things to know up front:

- Item 0 is the automation level, and it comes first: full-auto (`full`), semi-auto (`semi`), or manual (`manual`). SETUP.md explains the difference. Semi-auto is the recommended start, the choice is yours, and you can change it any time.
- Stop at item 5, the Xiaohongshu login. Only you can do this step: open the Xiaohongshu home page, `www.xiaohongshu.com`, in a browser and log in by scanning the QR code with the Xiaohongshu app. Never give your password or verification codes to any assistant, and never write them into any file.

**Step 5: Check the install with two commands.**

```
bash scripts/check-env.sh
python3 core/validate.py examples/example-issue
```

First command: it passes when nothing is marked missing (exit code 0; if something is missing the exit code is 1 — install it and run again). Second command: the voiceover word count and the post.md structure should both say PASS. The video, silence, and cover items reporting FAIL is expected — the example ships without a real video. Ignore those.

**Step 6: Make the first post.** The self-check above already ran the fictional example bundled in `examples/`, so the flow itself is verified. For your first real post, use semi-auto: it does all the work up to the point of publishing and stops with a ready-to-post package. Read it through yourself, and only then publish.

## How a day's work runs

There is one manager that hands out work and checks it. Workers go one at a time, and the next step only starts after the previous one passes its check:

1. **Pick a topic.** Scan the sources and pick something from the last 48 hours, in a different category from yesterday's post. Check the sensitive list first — anything that touches it is dropped on the spot. Key facts need an official source, plus one unrelated source that says the same thing.
2. **Write the script.** Write the title three ways and pick one. The voiceover script is 480 to 650 characters. It opens with why this matters to the viewer. Numbers like prices are worked out in full — unit price, subscription, yearly total — and compared with at least one similar product.
3. **Make the video.** Build the web page from the script, record the voiceover, capture frame by frame, stitch it together. Product images must be pictures of the actual product, and software must show its real interface. A logo image dressed up as a screenshot does not pass.
4. **Check it.** Run `core/validate.py`. It checks word count, length, resolution, silence, cover, and issue number, one by one. The person who made the video fills in a checklist, and the manager checks it again. If anything fails, it goes back to be redone.
5. **Publish.** Enter from the Xiaohongshu home page — do not open the creator platform address directly. Before posting, tap each topic tag until it turns blue; the count has to match before posting is allowed. Select the AI content declaration. Right after posting, post the first comment as the account owner.
6. **Follow up and review.** For two hours after posting, check every half hour for new comments and reply to them. Once a week, review the week and write what was learned back into the rules.

Every step has to leave evidence: where the file is, what the numbers are, what was checked. A claim of "done" with no source does not count. The details are in [orchestration/orchestrator.md](orchestration/orchestrator.md).

## What is in the repository

- [core/](core/): all the rules, in one place only. A constitution page sets the overall standards, six stage guides explain each step, and there is a sensitive-words template and the acceptance script.
- [motion-lib/](motion-lib/): the web motion library. How titles come in, how numbers count up, how cards flip — it is all here.
- [pipeline/](pipeline/): the video-making scripts. Frame-by-frame capture, stitching, the cover template, and how to plug in a voice.
- [orchestration/](orchestration/): how the manager hands out work, how to write the scheduled tasks, and a checklist for running a round by hand.
- [platforms/](platforms/): four more platform modules — Douyin, X, YouTube, WeChat Official Accounts — each with its own guide and runnable scripts.
- [adapters/](adapters/): how each of the three assistants connects to the system.
- [examples/](examples/): one complete made-up example, from topic to checklist, so you can see what every step produces.
- [docs/](docs/): how the system is put together, the full three-assistant comparison, compliance notes, and common questions.
- [scenarios/](scenarios/): add-on uses ("scenario packs") — a daily weather forecast is the worked example — plus the template for making your own.

## Does it cost anything?

No. The video libraries, the stitching tools, and both voiceover routes are free. The only money involved is your own AI assistant account, which is between you and that service — and note that Dots needs a Pro or Business Premium plan. This project connects to no paid API.

## FAQ

**Is it free?**
Yes. The project is MIT-licensed and every tool it uses is free. The only cost is the AI assistant account you already pay for, if you pay for one.

**Is it safe for my account?**
It is built to be careful: it works inside a browser the way a person would, at a normal pace, and uses no unofficial APIs. That lowers the risk, but it is not a guarantee — no honest project can promise that. Platforms are strict with fully automated accounts, so start in semi-auto and look at each post before it goes out.

**Which AI assistant do I need?**
Any one of the three cloud agents: Muse, Dots, or Grok Bot. All three have their own cloud computer and browser; the difference is their approval rules and how open they are. Muse is the one we run and have tested. Dots needs a ChatGPT Pro or Business Premium plan and is not tested by us yet. Grok Bot is still in beta and is not tested by us yet.

**Can it post to Douyin or TikTok?**
Douyin has its own module now: [platforms/douyin/](platforms/douyin/) — trending videos + Chinese subtitles pipeline, with runnable scripts (download, subtitle burn-in, outro join, sensitivity scan). TikTok is not covered. If you build it, send it back — that is exactly the kind of addition this project wants.

**Do I need to know how to code?**
No. The normal way to install is to paste one paragraph (the one above) to your assistant and answer its questions. Reading the guides helps you understand what it is doing, but you do not have to write code.

## Add your own uses — and ports to other platforms

This system is not only for tech news. The chain — search, sort, make a video, post, follow up — is general. Point it somewhere else and it can post a daily weather forecast, a short calming animation, local reminders, and so on. If you build a new use, add it back and the library grows for everyone.

New uses have a fixed format: one use is one "scenario pack". Fill in the template in [scenarios/_template/](scenarios/_template/) and you are done. The weather forecast in [scenarios/weather-forecast/](scenarios/weather-forecast/) was made exactly that way. All packs are listed in [scenarios/README.md](scenarios/README.md) — if you come back looking for new features, check that list first.

Ports to other platforms are welcome too. Topic picking, script writing, video making, and the checks are all general, so one piece of material can become a ready-to-post package for several platforms — one for Xiaohongshu, another for Douyin. Four platform modules already live in [platforms/](platforms/) (Douyin, X, YouTube, WeChat Official Accounts). What you need to hand in for a new port is listed in [docs/platform-targets.md](docs/platform-targets.md).

To add a pack, ask for a new use, or change a shared rule, read [CONTRIBUTING.md](CONTRIBUTING.md) first — it fits on one page.

## License

MIT. Use it freely; just keep the copyright notice. The third-party libraries have their own licenses, listed in [motion-lib/vendor/README.md](motion-lib/vendor/README.md).
