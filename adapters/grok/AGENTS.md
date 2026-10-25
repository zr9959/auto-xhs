[中文](AGENTS.zh-CN.md) | English

# Project instructions for Grok

You are helping the user run a Xiaohongshu account, using the auto-xhs workflow. The rules are not in this file — the rules live in exactly one place, the repo's `core/`. Read in the order below, and work by it.

One note: this file follows the workflow. Your multi-agent, scheduling, and browser abilities are all there, and what follows is the main path. A few places leave fallback wordings — if you don't need them, ignore them.

## Reading order

1. Read `core/CONSTITUTION.md` first.
2. When you reach a stage, read the matching guide in `core/stages/`. Don't read them all at once.
3. For the topic-picking and publishing stages, also read the sensitive-words appendix as the guide requires.

## Way of working

The manager protocol is in `orchestration/orchestrator.md`. The key points:

- One coordinator: start with the triple duplicate check, and log heartbeat entries in the run log.
- Fixed stage order: topic picking, script writing, video making, acceptance, publishing, wrap-up.
- If you can dispatch sub-agents, dispatch in series: only one stage at a time, and the next stage starts only after the previous stage's evidence list passes. Sub-agents don't dispatch further.
- If you can't dispatch sub-agents, work through the stages yourself in order. After finishing each stage, save the output to files, write it up in the evidence list format from `orchestration/orchestrator.md`, then move to the next. Don't push through everything in one breath.
- Never skip acceptance: run `core/validate.py` and tick through the acceptance list item by item. On FAIL, send it back for rework.
- For dispatch wording, see `orchestration/dispatch-templates.md`.

## Scheduling

Read `orchestration/scheduling/README.md` first, and build the five jobs with your built-in scheduling. System cron startup (template in `orchestration/scheduling/cron-system.example`) and the manual checklist (`orchestration/scheduling/manual-checklist.md`) are fallbacks — if you don't need them, ignore them.

## Publishing

- Auto publishing is only on the table with browser ability, login state confirmed on the main site first, and entry into the creator platform from the main site.
- Topics not all blue, AI declaration not picked, or files not matching the accepted ones — if any one of these fails, don't publish. Save the ready-to-post pack and report in four elements.
- Without browser ability: prepare the ready-to-post pack (`video.mp4`, `cover.jpg`, `post.md`, `publish-checklist.md`, templated in `orchestration/publish-checklist.template.md`), hand it to the user to publish by hand, and after publishing, fill the link and time back into the ledger.

## Errors

Write all four elements: which step and which object got stuck, the page or tool's original wording, what you tried and how many times with what result each time, and how it was handled in the end and what it means for the finished video. Just writing "failed" doesn't count.
