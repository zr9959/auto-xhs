[中文](architecture.zh-CN.md) | English

# Architecture: five layers, each minding its own part

Multi-platform automated operation and publishing (for Muse, Dots, Grok Bot)

This thing is not one program — it is five layers stacked up. Each layer minds only its own business. When you switch agent platforms, only the top two layers change. The bottom three stay as they are.

## Layer 1: Rules

Where: `core/`.

What it covers: how topics get picked, how scripts get written, how videos get made, how publishing passes its gates, how follow-up and review work. The constitution page `core/CONSTITUTION.md` sets the overall standards and every number. The six stage guides in `core/stages/` cover each step's details. Sensitive words and lessons are two appendices.

Why only one copy: once rules get copied to a second place, the two copies slowly drift apart. This workflow has been bitten by that before, so the hard rule is: rules live only in `core/`. Other directories may reference them, never copy them.

## Layer 2: Acceptance

Where: `core/validate.py`, plus each episode's acceptance list.

What it covers: turning "is it good" into numbers that can be checked. Word count, length, resolution, silence, cover size, file structure — the script checks each one and outputs PASS and FAIL. The finished video's acceptance list covers what the script can't check: sampled frames showing the right product, real interfaces appearing, issue number correct.

This layer is the gate. Without passing acceptance, the flow is not allowed to move toward publishing. Anything reworked after a check voids the old conclusion — check it again.

## Layer 3: Video making

Where: `pipeline/` and `motion-lib/`.

What it covers: turning a script into a video. The method is web-page video making: each part of the script becomes a web page. HTML and CSS handle layout, GSAP handles animation, and the animation components all live in `motion-lib/`. Then a browser holds the animation timeline still, screenshot by screenshot, and in the end ffmpeg joins the frames and the voiceover into the finished video.

Why not the video-editor route: web layout is easy to change, animation can be reused, and an agent writes HTML more reliably than it operates editing software. The cost is speed: screenshots come one frame at a time, and one video takes a good while to capture. That cost is written in the video-making guide.

This layer has nothing to do with platforms. In any agent's hands, it is the same scripts running on the local machine.

## Layer 4: Orchestration

Where: `orchestration/`.

What it covers: who works first, who works next, who checks the finished work. The manager only dispatches, checks, and reports — it doesn't do stage work itself. Stages run one after another in series. The next one doesn't start until the previous one passes. Every dispatch must hand back an evidence list, and errors are written in four elements.

When switching platforms, this layer's wording changes with it: platforms that can dispatch sub-agents follow the manager model; ones that can't have a single agent work through in order. What changes is the wording. The order and the acceptance checks don't change.

## Layer 5: Scheduling

Where: `orchestration/scheduling/`.

What it covers: when work starts, and who watches whether it went off track. Five jobs in all: daily post, early watchdog, late watchdog, post-publish follow-up, weekly review.

This layer differs most across platforms. Some platforms can build scheduled tasks, some need system cron, some can only start when a person calls out at the set time. When scheduling changes, the first four layers don't move at all — at most, "starts automatically" becomes "starts by hand".

## One line to close

Looked at bottom-up: rules, acceptance, and video making are assets — they move anywhere unchanged. Orchestration and scheduling are interfaces — switching platforms means switching these two layers. Before picking a platform, read `capability-matrix.md`.
