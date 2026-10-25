[中文](README.zh-CN.md) | English

# How the Grok Bot path works

First, what Grok Bot is: it is xAI's cloud agent, still in beta since August 2026. The agent runs on a cloud virtual machine, can operate software in multiple steps on its own, and comes with 200+ plugins. One account gets one virtual machine, shared by however many bots you own, and the login state is shared too.

It is not a chat-only bot — it has its own computer. But one rule matters most for this system: **for actions like publish, send, buy, and delete, it pauses by default and waits for your approval before acting.** The Always Allow setting, once opened, stops the asking and lets it act directly.

Availability: right now it is only open to some SuperGrok Heavy users. And one honest statement: we have not tested it running this system. What follows is the connection method from the official statements. When you connect it, run a small round yourself first to check it, and where it doesn't work, follow the fallback path.

## Setup

1. Put the repo into Grok Bot's workspace.
2. Give `AGENTS.md` to it as the project instructions (this very file in this directory) — it states the reading order and the way of working.
3. Fill in the config by following the setup guide in the repo root.
4. Xiaohongshu login: open the Xiaohongshu main site in its cloud virtual machine browser and scan the QR code yourself. Note the login state lives on the virtual machine and is shared across bots — don't fiddle with this account in other bots.

## How one round runs

The flow is the same as the other two: read `core/CONSTITUTION.md`, read `core/stages/` per stage, and the manager protocol is in `orchestration/orchestrator.md`.

It can dispatch sub-agents, so use the manager model: serial dispatch, one stage checked before the next goes out. Each step's output and evidence list still land in files. To keep it simple, one agent can also work straight through from start to finish — the standard doesn't drop, it is just slower, and the acceptance list must be ticked item by item by hand.

## How scheduling works

Grok Bot has built-in scheduling. Build one for each of the five jobs by purpose: daily post, early watchdog, late watchdog, post-publish follow-up, weekly review, with limits as in `orchestration/scheduling/README.md`.

System cron startup and manual start also have templates, if you want to swap the scheduling entry: the cron template is in `orchestration/scheduling/cron-system.example`, the manual checklist in `orchestration/scheduling/manual-checklist.md`.

## How publishing works (this assistant's most different step)

- **The default is already a semi-auto gate**: it finishes the earlier work, prepares the ready-to-post pack, and at the actual publish step it stops and waits for your approval. You look at the pack, then clear it. That is exactly the same as this system's recommendation of "new accounts start semi-auto" — no extra setup needed from you.
- **For full-auto**: open Always Allow for publish-type actions, and it stops asking. Before opening it, think through the risk — see `docs/compliance.md`. Don't open Always Allow for delete-type actions.
- Asked or not, the gate standards don't change: confirm login state on the main site first and enter the creator platform from the main site; if topics aren't all blue or the AI declaration isn't picked, and any one of these fails, don't publish.

## Ready-to-post pack

Four fixed files, the same format as the other two assistants:

- `video.mp4`: the finished video that passed acceptance
- `cover.jpg`: the separately made cover
- `post.md`: title, body, topics, AI content declaration, first comment
- `publish-checklist.md`: the tick-through publish checklist, templated in `orchestration/publish-checklist.template.md`
