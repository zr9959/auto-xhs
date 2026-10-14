# Auto-xhs — Automated Xiaohongshu (RedNote) Operation and Publishing

Works with AI assistants such as Muse, ChatGPT and Grok.

## What it does

Log your own Xiaohongshu account into the browser your AI assistant can use, once, by scanning a QR code yourself. From then on the assistant runs the whole chain every day: it searches for fresh material, turns it into a script, builds a video, publishes it, and follows up on comments. Everything happens in the browser, clicked and typed the way a person would, at a normal posting pace. No unofficial APIs.

Our principles: **free, ban-resistant, efficient, simple.** Ban-resistant means human-like operation at a normal pace — not a guarantee for any account. New accounts are recommended to start in semi-auto mode and approve each post before it goes out. See [docs/compliance.md](docs/compliance.md).

## How the videos are made

Each video starts as a web page: HTML/CSS for layout, GSAP for animation, with a ready-made motion library for titles, number count-ups, cards and transitions. A browser then steps through the timeline frame by frame (30 fps) and screenshots each frame. ffmpeg stitches the frames, adds the voiceover, and applies 1.5x speed.

## Platform differences, stated plainly

The rules, the acceptance checks and the ready-to-post package format are identical on all three platforms. What differs is who presses the buttons: Muse offers the smoothest full automation (scheduled runs, step-by-step sub-agents, browser publishing). ChatGPT is semi-auto first: the system prepares a ready-to-post package and you publish it yourself. Grok sits in between, depending on the version. Full table: [docs/capability-matrix.md](docs/capability-matrix.md).

## Getting started

Copy the instruction block in the Chinese [README.md](README.md) to your assistant, or run `bash scripts/setup.sh` and follow [SETUP.md](SETUP.md). All tooling is free; the only cost is your own assistant account.

## License

MIT. Third-party libraries keep their own licenses, listed in [motion-lib/vendor/README.md](motion-lib/vendor/README.md).
