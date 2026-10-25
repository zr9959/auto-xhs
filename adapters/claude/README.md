[中文](README.zh-CN.md) | English

# How the Muse path works

This is the most complete of the three paths. An account already posts daily through it, and sub-agent division of labor, scheduling, and browser publishing have all been run through.

## Setup

1. Put the repo where Muse can read it as a working directory.
2. Put `skill/SKILL.md` into your skill directory, or point the project at it. This skill is a thin shell — it holds no rules, only the reading order.
3. Fill in the config by following the setup guide in the repo root: category, sources, publish time, automation level, and the rest.
4. Log in to Xiaohongshu by scanning the QR code yourself. Log in on the main site first, then enter the creator platform from the main site. Details are in the setup guide and the publish guide in `core/stages/`.

## How one daily round runs

The manager reads `core/CONSTITUTION.md` to start, then dispatches by `orchestration/orchestrator.md`: topic picking, script writing, video making, the manager's own acceptance check, publishing, wrap-up. Only one stage runs at a time — the next dispatch goes out only after the previous one passes. Dispatch templates are in `orchestration/dispatch-templates.md`.

## How to build the schedules

Build one scheduled task for each of the five jobs: daily post, early watchdog, late watchdog, post-publish follow-up, weekly review. Templates are in `orchestration/scheduling/cron-claude.example.md` — all five are written out, just fill in the placeholders.

## Automation level

- Full-auto: once acceptance passes, the publish dispatch goes out directly.
- Semi-auto: once acceptance passes, it stops and prepares the ready-to-post pack, waiting for you to approve it. The pack format is below.

New accounts start in semi-auto. Switch to full-auto once it runs steadily. The risk notes are in `docs/compliance.md`.

## Ready-to-post pack (used in semi-auto)

Four fixed files, the same format as the other two assistants:

- `video.mp4`: the finished video that passed acceptance
- `cover.jpg`: the separately made cover
- `post.md`: title, body, topics, AI content declaration, first comment
- `publish-checklist.md`: the tick-through publish checklist, templated in `orchestration/publish-checklist.template.md`

## Where it falls back

If your runtime has no browser ability, it can't publish. It falls back to semi-auto: everything before publishing runs as usual, the ready-to-post pack is prepared, and you publish by hand. The other steps are unaffected.

## Hosted browser input limits (tested — know these before publishing)

Muse's hosted browser has a few known limits on page input. Work around them when publishing (the publish guide 04's click-select topic method was set for exactly this):

- No per-keystroke input and no clipboard channel: it can't send keystroke-by-keystroke typing, and can't use copy-paste shortcuts.
- Right-click doesn't bring up a context menu.
- When filling text into an editor, the drop point stays fixed at the center of the element and doesn't follow the cursor: appending content in the body editor can easily land in the middle of the body text.

What to do instead: publish from a fresh publish page, and add topics by click-select — type `#`, wait for the suggestions to pop up, click the official topic, and check on the spot that it turned blue. The pasting method is the backup. The old continuous-input method is abolished — don't use it. Don't add topics later on a draft edit page. For any job that touches web login state (publishing, adding topics, post-publish follow-up), confirm at dispatch time that the worker has browser ability — a worker without browser tools can only do local jobs (checks, writing, video making). Dispatching wrong means waiting a whole round for nothing.
