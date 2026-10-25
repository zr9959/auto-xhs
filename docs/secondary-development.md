[中文](secondary-development.zh-CN.md) | English

# Secondary development: switching uses and platforms, where to start

This system was built for Xiaohongshu, but its skeleton is not Xiaohongshu-specific. Searching for material, consolidating scripts, web-page video making, publishing, operating — that chain runs the same for a different use or a different platform. This file states: when you start, what stays untouched and what gets rewritten.

First, remember how the interface is set: this library runs on **file conventions**. AI assistants read files to work, so anything new you add — a use or a platform — connects as long as its file formats line up with the existing ones. No plugins to write, no servers to start, no runtime for users to install. When existing users update the repo once, the new feature works for them.

## What is general — leave it alone

These five are the engine. They have nothing to do with use or platform, and secondary development uses them as-is:

- **Sourcing method**: how to probe sources for liveness, how to cap time, how to judge heat, how facts get checked. Rules in `core/stages/01-sourcing.md`.
- **Script standards**: plain words, real detail, numbers given in full, titles written in several versions first. Rules in `core/stages/02-script.md` and the constitution page's core standards.
- **Web-page video making**: scripts laid out as web pages, frame-by-frame screenshots, joining. Scripts in `pipeline/`, motion in `motion-lib/`.
- **Acceptance script**: `core/validate.py`. Word count, length, resolution, silence, cover — checked item by item, the same for any video.
- **Manager orchestration**: dispatching, serial order, acceptance clearance, heartbeat entries, four-element errors. In `orchestration/`.

## What gets rewritten

When switching uses or platforms, these five change:

- **Source list**: which sites, sections, and data sources to watch. Written in config and in your own use pack.
- **Category and script voice**: which category to cover, what tone, who it is for. The use decides this, not the engine.
- **Visual templates**: what goes in each segment, what the layout looks like. Data topics are all data cards; product topics need product pictures — completely different templates.
- **The publish step**: every platform's entry, steps, and gates differ. This part must be rewritten per platform, honestly written — what hasn't been tested gets marked untested.
- **Platform rules**: every platform checks different things. Sensitive words, declarations, diversion red lines — all per the new platform.

## Route 1: switch uses, make a scenario pack

What you post is still Xiaohongshu, only the content changes — weather forecasts, vegetable price reports, calming animations, local reminders — all take this route:

1. Copy `scenarios/_template/` and fill it in by `CONTRIBUTING.md`.
2. Only write what is specific to your use: data sources, script voice, visuals, and differences from the general rules. Not one line of the engine changes.
3. When handing it back, add one line in `scenarios/README.md`'s list.

The weather forecast is the first example built this way, in `scenarios/weather-forecast/`. Read it first before starting.

## Route 2: switch platforms, add a content platform

You want the same material on other platforms — say, one copy on Xiaohongshu and another on Douyin — take this route:

1. Read `docs/platform-targets.md` first, and get the material pack and ready-to-post pack concepts clear.
2. Prepare the new platform's five things: login method, publish step checklist, platform rules and red lines, copy differences, and one ready-to-post pack example.
3. Nothing before video making needs redoing: topic picking, script writing, video making, and acceptance are all general. The only extra work is the last stretch: adapt the material pack into that platform's ready-to-post pack by its rules, then publish by its checklist.

The Douyin / TikTok module is built now — see `platforms/douyin/` (guide + runnable scripts). The same rule still applies to new ports: don't write untested steps as if they work.

## Last line

When done, contributions back into this library are welcome: uses go into the use list, platforms into the platform list. Later readers won't have to build it again — they take yours and use it. That is also how this library grows.
