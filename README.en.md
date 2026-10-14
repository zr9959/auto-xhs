# 小红书全自动化运营发布（适配muse、Chatgpt dots、Grok bots）

[中文](README.md) | English

## Fully automated Xiaohongshu (RedNote) operation and publishing, run by AI agents — Muse, ChatGPT Dots, and Grok Bots

Auto-xhs is an open-source system that runs a Xiaohongshu (RedNote) account end to end — finding topics, writing scripts, making videos, posting, and replying to comments — through an AI agent's own browser, with no unofficial APIs and no paid tools.

Repository name: Auto-xhs

**Key facts**

- Free. MIT license. Every tool in the chain is free; there are no paid APIs.
- Works with three cloud AI agents: Muse, ChatGPT Dots, and Grok Bots. All three work in their own cloud computer and browser. Muse is the one we run every day and have tested end to end; Dots and Grok Bots are not tested by us yet.
- Recommended start: semi-auto. The agent prepares everything, you look at it, then it posts.
- Videos are portrait 1080×1920 by default; landscape 1920×1080 is an option you can pick in the config.
- Videos are built as web pages and captured frame by frame, not edited in a video editor.
- Nothing goes out until it passes an acceptance script: word count, length, resolution, silence, cover, issue number.

## What this project does

You log your own Xiaohongshu account into the browser your AI agent can use, once. After that, the agent takes over the whole job: every day it searches for fresh material, turns it into a script, builds a video, posts it, and follows up on comments. Everything happens inside the browser, clicked and typed the way a person would. No unofficial APIs. The posting pace is a normal person's pace.

It solves one problem: the slow part of running a Xiaohongshu account is the whole chain — searching, sorting material, making videos, posting, replying to comments. This project automates that whole chain. You only do three things: pick a direction, scan a QR code once, and (in semi-auto mode) take a look before each post goes out.

**Our motto: free, safe, efficient, simple.**

The honest part, up front: "safe" comes from acting like a person in the browser, plus a normal posting pace. It is not a guarantee for any account. Platforms watch fully automated accounts closely, so we recommend new accounts start in semi-auto and check each post before it goes out. The details are in [docs/compliance.md](docs/compliance.md).

## How the videos are made

Every video starts as a web page. That is the part that makes this project different.

First the video is laid out as a page: HTML and CSS for the layout, GSAP for the animation. Good-looking motion — titles coming in, numbers counting up, cards flipping — lives in a ready-made motion library, and the script just calls it. Then a browser holds the animation still and screenshots it frame by frame, 30 frames a second. At the end, ffmpeg stitches the frames into a video, adds the voiceover, and speeds it up to 1.5x.

Why do it this way: web pages are fast and good-looking for cards, charts, and price comparisons, and if a number changes you fix the page instead of re-editing a video. And because every frame is captured one by one, the animation looks exactly the same on every run — nothing drifts between today and tomorrow.

## The three assistants — differences, stated plainly

The rules, the acceptance checks, and the ready-to-post package format are the same for all three. The only difference is who presses the buttons.

One thing to get right first: ChatGPT Dots is not the regular ChatGPT chat. Dots is OpenAI's always-on cloud agent, launched on September 29, 2026. Each Dot has its own cloud computer and its own browser, can run on a schedule, can hand work to sub-agents, and can be told to ask for your approval before it acts. It needs a ChatGPT Pro or Business Premium plan. Grok Bot is xAI's cloud virtual-machine agent; it is still in beta, and by default it pauses before posting and waits for approval. Muse is the setup we run ourselves every day — that one is tested end to end. Dots and Grok Bot follow the same files and rules, but we have not tested them ourselves yet.

| What it can do | Muse | ChatGPT Dots | Grok Bot |
|---|---|---|---|
| Search for material, write scripts | Yes | Yes | Yes |
| Make the video (run the scripts) | Yes | Yes, on its own cloud computer | Yes |
| Split the work step by step | Smoothest — this is how it runs here | Yes — a Dot can hand work to sub-agents | Depends on the version; if not, one job from start to finish |
| Start on its own every day | Yes | Yes — Dots can run on a schedule | Set it up with system scheduling, or start it by hand |
| Publish in the browser by itself | Yes | Yes — and you can set it to ask you first | Pauses before posting and asks, by default |
| Reply to comments after posting | Yes | Yes — on a schedule or when you ask | By hand or semi-auto |
| Weekly review | Yes | On a schedule or when you ask | When you ask |

The full table is in [docs/capability-matrix.md](docs/capability-matrix.md). Read the guide for the assistant you use: [Muse](adapters/claude/README.md), [ChatGPT Dots](adapters/dots/README.md), [Grok Bot](adapters/grok/README.md).

## Three automation levels — you pick

- **Full-auto**: the agent does everything, including pressing publish.
- **Semi-auto** (recommended): the agent prepares a ready-to-post package — video, cover, text — and you look at it before it goes out.
- **Manual**: the agent only picks topics and writes scripts. You make and post the videos yourself.

During setup you choose the level yourself. The setup explains the three, recommends semi-auto to start, and does not decide for you.

## The easiest way to install it

Copy the text below, together with this repository's address, and paste it to your AI assistant. It will set up the environment on its own and then walk you through the settings one by one:

```
Set up auto-xhs for me, following the instructions in the repository:
1. Run bash scripts/setup.sh first. It checks my environment, downloads the third-party libraries, and prepares the config file. If anything is missing, tell me and I will install it.
2. Then open SETUP.md and walk me through config.yaml one item at a time. First, let me choose one of the three automation levels — full-auto, semi-auto, or manual — and explain the difference clearly. Recommend semi-auto to start, but do not decide for me.
3. Stop at the Xiaohongshu login step. Tell me how to scan the QR code; I will scan it myself. Do not touch my password or verification codes.
4. When everything is filled in, run the acceptance checks on the example in examples/ and show me the result, then make the first post. Stop right before publishing it and let me look at it first.
```

Installing by hand works too: run `bash scripts/setup.sh`, then fill in `config.yaml` by following [SETUP.md](SETUP.md).

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
- [adapters/](adapters/): how each of the three assistants connects to the system.
- [examples/](examples/): one complete made-up example, from topic to checklist, so you can see what every step produces.
- [docs/](docs/): how the system is put together, the full three-assistant comparison, compliance notes, and common questions.
- [scenarios/](scenarios/): add-on uses ("scenario packs") — a daily weather forecast is the worked example — plus the template for making your own.

## Does it cost anything?

No. The video libraries, the stitching tools, and both voiceover routes are free. The only money involved is your own AI assistant account, which is between you and that service — and note that ChatGPT Dots needs a Pro or Business Premium plan. This project connects to no paid API.

## FAQ

**Is it free?**
Yes. The project is MIT-licensed and every tool it uses is free. The only cost is the AI assistant account you already pay for, if you pay for one.

**Is it safe for my account?**
It is built to be careful: it works inside a browser the way a person would, at a normal pace, and uses no unofficial APIs. That lowers the risk, but it is not a guarantee — no honest project can promise that. Platforms are strict with fully automated accounts, so start in semi-auto and look at each post before it goes out.

**Which AI assistant do I need?**
Any one of the three cloud agents: Muse, ChatGPT Dots, or Grok Bot. All three have their own cloud computer and browser; the difference is their approval rules and how open they are. Muse is the one we run and have tested. Dots needs a ChatGPT Pro or Business Premium plan and is not tested by us yet. Grok Bot is still in beta and is not tested by us yet.

**Can it post to Douyin or TikTok?**
The chain itself — research, script, video, checks — is not tied to one platform. A Douyin version is planned out in [docs/platform-targets.md](docs/platform-targets.md), with the file formats ready, but it is not built or tested yet. TikTok is not covered. If you build either, send it back — that is exactly the kind of addition this project wants.

**Do I need to know how to code?**
No. The normal way to install is to paste one paragraph (the one above) to your assistant and answer its questions. Reading the guides helps you understand what it is doing, but you do not have to write code.

## Add your own uses — and ports to other platforms

This system is not only for tech news. The chain — search, sort, make a video, post, follow up — is general. Point it somewhere else and it can post a daily weather forecast, a short calming animation, local reminders, and so on. If you build a new use, add it back and the library grows for everyone.

New uses have a fixed format: one use is one "scenario pack". Fill in the template in [scenarios/_template/](scenarios/_template/) and you are done. The weather forecast in [scenarios/weather-forecast/](scenarios/weather-forecast/) was made exactly that way. All packs are listed in [scenarios/README.md](scenarios/README.md) — if you come back looking for new features, check that list first.

Ports to other platforms are welcome too. Topic picking, script writing, video making, and the checks are all general, so one piece of material can become a ready-to-post package for several platforms — one for Xiaohongshu, another for Douyin. What you need to hand in is listed in [docs/platform-targets.md](docs/platform-targets.md). The Douyin section has the formats ready; it has not been tested yet, and filling it in is welcome.

To add a pack, ask for a new use, or change a shared rule, read [CONTRIBUTING.md](CONTRIBUTING.md) first — it fits on one page.

## License

MIT. Use it freely; just keep the copyright notice. The third-party libraries have their own licenses, listed in [motion-lib/vendor/README.md](motion-lib/vendor/README.md).
