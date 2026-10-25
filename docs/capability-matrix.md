[中文](capability-matrix.zh-CN.md) | English

# Three-assistant capability comparison (full table)

Multi-platform automated operation and publishing (for Muse, Dots, Grok Bot)

First, a statement: the Muse column comes from an account already posting daily with it — tested. The Dots and Grok Bot columns follow the two vendors' official release statements. We have no accounts and have not tested them. Before using either, run a small round yourself to check it. Don't treat this table as a promise.

One more thing all three share: they are cloud agents, each with its own cloud computer and browser. What follows compares not "has a cloud or not", but approval-rule strictness and openness.

| Capability | Muse | Dots | Grok Bot |
|---|---|---|---|
| Read rules, pick topics, write scripts | Yes. Skill entry point reads `core/`, guides read per stage | Yes. All of `core/` goes to it as knowledge, master instructions in `adapters/dots/dots-instructions.md` | Yes. AGENTS.md states the reading order |
| Make videos (web-page video pipeline) | Yes. Scripts run on this machine, capture plus joining in one chain | Yes. Scripts run on its own cloud computer, and it checks its own output | Yes. Scripts run on a cloud virtual machine; if they don't run, run the scripts by hand and fill the results back in |
| Sub-agent orchestration | Yes. Manager dispatch, serial order, check per dispatch — the native path | Yes. It can split work across sub-agents, manager model follows `orchestration/` | Yes. It can split work across sub-agents, manager model follows `orchestration/` |
| Scheduling | Yes. Daily post, two watchdogs, follow-up, review — all five can be built | Yes. Built-in scheduling, one per job for all five | Yes. Built-in scheduling, one per job for all five |
| Auto publish in browser | Yes. Confirm login on the main site first, then use the on-site entry | Yes. In its own browser; ask-first or auto-approve is set in its custom rules by you | Yes. In its own browser; before publish, send, buy, or delete it pauses by default and waits for approval — opening Always Allow makes it fully automatic |
| Post-publish follow-up | Yes. Timed checks within 2 hours of publishing, auto replies | Yes. Checks on schedule; replies and other outward actions follow the rules you set, same as publishing | Yes. Checks on schedule; replies and other outward actions follow your approval settings, same as publishing |
| Weekly review | Yes. Runs weekly on schedule, and can also update `core/` directly | Yes. Runs on schedule; suggested `core/` changes go to you first — they land only after you nod | Yes. Runs on schedule; suggested `core/` changes go to you first — they land only after you nod |

## Beyond the table

The three differ in just two things: **at the publish step, does it ask you first or send directly**, and **can you use it right now**.

- Muse: already running. Install it and it posts daily by the book.
- Dots: needs ChatGPT Pro or Business Premium. Set the publish rule to "ask me first" and you have semi-auto; once it runs steadily, change it to auto-approve for full-auto.
- Grok Bot: still in beta, only open to some SuperGrok Heavy users. By default it stops before publishing and waits for approval — that gate needs no extra setup from you. For full-auto, go open Always Allow.

Everything else is the same: the same `core/` rules, the same `core/validate.py` acceptance check, the same ready-to-post pack format (`video.mp4`, `cover.jpg`, `post.md`, `publish-checklist.md`).

So picking one is not about comparing who is smarter. First check whether you can use it at all (subscription, availability), then check whether the publish step's approval rule suits you: for a fully hands-off run, Muse works out of the box, Dots needs one rule changed, Grok Bot needs one switch opened — but new accounts should all start semi-auto and only open up once steady.
