---
name: auto-xhs
description: "Run a Xiaohongshu account with this workflow: topic picking, script writing, web-page video making, publishing, post-publish follow-up, weekly review. Use when the user talks about Xiaohongshu daily posts, posting to Xiaohongshu, automated operation, or reviews."
---

[中文](SKILL.zh-CN.md) | English

# auto-xhs entry point

This file is only an entry point. It holds no rules. The rules live in exactly one place, the repo's `core/` — don't write a second copy here.

## Reading order

1. Read `core/CONSTITUTION.md` first. The manager reads only this one to start each round.
2. When you reach a stage, read the matching guide in `core/stages/`. Don't read them all at once.
3. For the topic-picking and publishing stages, also read the sensitive-words appendix as the guide requires.

## How to work

- Orchestration: see `orchestration/orchestrator.md`. The manager only dispatches, checks, and reports. Stage work goes to sub-agents, one at a time, and the next dispatch goes out only after the previous one passes.
- Write dispatches by `orchestration/dispatch-templates.md`.
- Build schedules from the Muse template in `orchestration/scheduling/`.
- Video making goes through `pipeline/`, motion through `motion-lib/`.
- Config comes from the repo's config file. Category, sources, times, and paths all follow the config — don't hardcode numbers into this file.
