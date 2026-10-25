[中文](README.zh-CN.md) | English

# How the Dots path works

First, clear up an easy mix-up: Dots is not the ChatGPT chat box. The official name is just Dots (OpenAI's own writing often uses lowercase "dots", and one agent is called a dot). There is no product called "ChatGPT Dots". It is a separate product OpenAI released at DevDay on September 29, 2026 — an always-on cloud agent: each Dot has its own cloud computer and browser, runs on the GPT-6 Astra model. You enter it inside ChatGPT (chatgpt.com/dots), and you can also hand it work from Slack and Teams. It can run on a schedule, split work across sub-agents, and connect to 4000+ apps.

So this path connects basically the same way as the Muse path: it has a cloud computer, a browser, scheduling, and sub-agents. It is not a cut-down semi-auto version.

One honest statement up front: we have no Dots account, so this path is untested. What follows is the connection method written from the official release statements. When you run your first post, watch it yourself.

## Who can use it

- You need ChatGPT Pro or Business Premium.
- For now, one user builds one Dot first. That one Dot runs this whole system.

## Setup

1. Build a Dot at chatgpt.com/dots.
2. Give it the rules: the master instructions are `dots-instructions.md` in this directory, and the whole repo `core/` goes to it as knowledge (the constitution page plus the six stage guides). The complete rules are `core/` — the instructions only state the general way of working.
3. Fill in `config.yaml` by following the setup guide in the repo root, and give the filled-in config to it too.
4. Build the schedules: Dots can run scheduled runs. Build one for each of the five jobs — daily post, early watchdog, late watchdog, post-publish follow-up, weekly review — with purpose and limits written as in `orchestration/scheduling/README.md`.
5. Xiaohongshu login: open the Xiaohongshu main site in its cloud browser and scan the QR code yourself. Passwords and verification codes are typed only by you — never give them to anyone, never write them into any file.

## The most important step: set "publish" to ask for approval first

Dots has a custom rules system: each action can be set to auto-approve, ask you first, or forbidden. This system's semi-auto and full-auto are exactly this one rule's difference in Dots:

- **Set it this way first (recommended)**: for outward actions like publishing and posting the first comment, set "ask me before acting". It does all the earlier work, prepares the ready-to-post pack, stops, and waits for your nod. You look it over, approve, and only then does it publish. That is semi-auto.
- **Change it once it runs steadily**: once you are sure its topics, scripts, and videos are solid, change the publish rule to auto-approve. That is full-auto. Before changing, think it through: the account is yours, and platforms watch fully automated hosting closely. The risk notes are in `docs/compliance.md`.
- **Delete-type actions** should stay forbidden or ask-first. Don't auto-approve them.

One more rule that doesn't conflict with this system: when it has no task, Dots only does read-only "proactive research" — looking at sources and sorting information. It won't publish anything on its own.

## How a day runs

Same manager model as the Muse path. The manager protocol is in `orchestration/orchestrator.md`:

1. At the scheduled time it starts on its own, and first runs the triple duplicate check.
2. It dispatches sub-agents in order: topic picking, script writing, video making. Each stage hands back its output and evidence list, and the manager only clears the next stage after checking them.
3. The video-making scripts run on its own cloud computer. Your computer doesn't need to stay on.
4. Acceptance runs `core/validate.py`, checked item by item against the acceptance list. Any FAIL goes back for rework.
5. At the publish step, it follows the rule you set: ask-first means it stops and waits for you; auto-approve means it publishes on its own.
6. Post-publish follow-up and weekly review keep running on schedule.

## Ready-to-post pack

When publish is set to ask for approval, the pack it stops and waits with is the ready-to-post pack, the same format as the other two assistants:

- `video.mp4`: the finished video that passed acceptance
- `cover.jpg`: the separately made cover
- `post.md`: title, body, topics, AI content declaration, first comment
- `publish-checklist.md`: the tick-through publish checklist, templated in `orchestration/publish-checklist.template.md`

Before approving, look at all four. Two checklist lines not to skip: topics must be tapped one by one until blue — if the blue count doesn't match, stop. And the content declaration must pick the AI-generated item.
