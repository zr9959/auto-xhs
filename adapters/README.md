[中文](README.zh-CN.md) | English

# The three adapters: read this page first, then pick

Multi-platform automated operation and publishing (for Muse, Dots, Grok Bot)

There is only one set of rules, in `core/`. The three adapters don't change the rules. They solve three things only: how this assistant reads the rules, how its approval rules are set, and how scheduling works.

First, clear up an old misunderstanding: all three are cloud agents, each with its own cloud computer and browser. The difference is not "has a cloud or not". It is three things: how strict the pre-action approval rules are, who can use it, and whether we have tested it.

- **To follow a path that already works, pick Muse.** Sub-agent division of labor, scheduling, and browser publishing all work, and an account already posts daily with it. Tested end to end.
- **If you use Dots, connect it the same way as Muse.** Dots is a separate product OpenAI released in September 2026, not the ChatGPT chat itself. Each Dot has its own cloud computer and browser, can run on a schedule, and can hand work to sub-agents. Whether publishing asks you first or goes straight ahead is set in its custom rules: ask-first is semi-auto, auto-approve is full-auto. It needs ChatGPT Pro or Business Premium. We have no account and have not tested it.
- **If you use Grok Bot, mind its pause rule.** Grok Bot is xAI's cloud agent, still in beta. The agent runs on a cloud virtual machine, but before publish, send, buy, or delete actions it pauses by default and waits for your approval — a built-in semi-auto gate. Only opening Always Allow in settings lets it go ahead without asking. Right now it is only open to some SuperGrok Heavy users. Also not tested by us.

## Short table

The full table is in `docs/capability-matrix.md`. The Muse column is tested. The Dots and Grok Bot columns follow the official statements and are untested.

| Capability | Muse | Dots | Grok Bot |
|---|---|---|---|
| Read rules, pick topics, write scripts | Yes | Yes | Yes |
| Make videos (web-page video pipeline) | Yes, scripts run on this machine | Yes, on its own cloud computer | Yes, on a cloud virtual machine |
| Sub-agent orchestration | Yes, serial dispatch is the native path | Yes | Yes |
| Scheduling | Yes, all five jobs can be built | Yes, built-in scheduling | Yes, built-in scheduling |
| Auto publish in browser | Yes | Yes; ask-first or auto-approve depends on the rules you set | Yes; ask-first or auto-approve depends on your settings — by default it pauses before publishing and waits for approval, opening Always Allow lets it go ahead |
| Post-publish follow-up | Yes, watches automatically for 2 hours | Yes, on a schedule | Yes, on a schedule |
| Weekly review | Yes, automatic on a schedule | Yes, on a schedule | Yes, on a schedule |

## Entry point for each

- Muse: `claude/README.md`, then `claude/skill/SKILL.md`.
- Dots: `dots/README.md`, with the master instructions in `dots/dots-instructions.md`.
- Grok Bot: `grok/README.md`, with the instruction file `grok/AGENTS.md`.

## No matter which one you pick, these three are the same

- Rules: the same `core/`.
- Acceptance: the same `core/validate.py`, the same pass standards.
- Ready-to-post pack: the same format — `video.mp4`, `cover.jpg`, `post.md`, `publish-checklist.md`. The template is in `orchestration/publish-checklist.template.md`.

The only differences are who gets asked before the publish step, and whether you can use it right now. How well the earlier steps were prepared is judged by one standard for all three.
