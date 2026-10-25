[中文](README.zh-CN.md) | English

# Scheduling: five jobs in all

This workflow turns on five scheduled jobs. Each job's division of labor is strict — it does only its own part, never overreaching.

All times are placeholder style: `{{start_time}}` and the like get filled in config. The recommended values after them are the times the current daily run uses — fill them in as-is, or change them if you like. When changing, mind the order: watchdogs come after the daily run starts and after the publish target.

## What each of the five does

### 1. Daily post

- Trigger: once a day. Placeholder `{{daily_time}}`, recommended 06:00 in the morning.
- What it does: today's manager starts. Read the constitution page, run the triple duplicate check, dispatch in order, check acceptance, publish, report. The full flow is in `../orchestrator.md`.
- Target: published before `{{publish_by}}`, recommended before 08:00.
- What it doesn't do: no follow-up, no review. Those are jobs 4 and 5 below.

### 2. Early watchdog

- Trigger: about 20 minutes after the daily run starts. Placeholder `{{watchdog_early_time}}`, recommended 06:20.
- Does one thing only: check whether today's run log has its first heartbeat entry.
- Has it: all normal. End quietly, no message sent.
- Doesn't have it: the daily run never really started. First sound one line of alarm, then re-trigger one daily round to make up for it — only once. Before re-triggering, check whether the ledger already has today's entry. If it does, don't re-trigger — alarm only.
- What it doesn't do: doesn't check whether anything published. That is the late watchdog's job.

### 3. Late watchdog

- Trigger: a little after the publish target time. Placeholder `{{watchdog_late_time}}`, recommended 08:12.
- Does one thing only: check whether the ledger has today's entry, or whether the log has a "publish complete" heartbeat entry.
- Has it: normal, end quietly.
- Doesn't have it: one line of alarm, carrying the log's last heartbeat entry, stating which stage it is stuck at. No log means write "no heartbeat entries".
- What it doesn't do: only alarms — no make-up sends, no re-runs. The daily run may still be running at this point, and a make-up send could collide and double-post.

### 4. Post-publish follow-up

- Trigger: placeholder `{{followup_time}}`, recommended to start together with the late watchdog at 08:12. But the window starts from the post's actual publish time, not from this clock time.
- What it does: for 0 to 2 hours after publishing, check every 30 minutes. First look for red dots on notifications and DMs — no red dots means this round ends. New comments get replied to by the guide; DMs needing the owner get reported. Stop at 2 hours.
- Details are in the follow-up guide in `core/stages/`.
- What it doesn't do: interactions outside the 2 hours don't count. Likes, saves, and new follows get logged, not reported.

### 5. Weekly review

- Trigger: once a week. Placeholder `{{review_time}}`, recommended Sunday evening around 20:18.
- What it does: look at the week's posts and data, write lessons into the lessons book, and promote what became rules into `core/`. Also do data backfill, draft cleanup, and wording patrol. The month's first review also re-reads the sensitive-words appendix and updates it against the platform's latest notices. Details are in the review guide in `core/stages/`.
- What it doesn't do: doesn't publish new posts.

## How each of the three does it

### Muse

All five jobs can be built as scheduled tasks, one task per job. Templates are in `cron-claude.example.md` — all five are inside, just fill in the placeholders to build them. This is the only path of the three that already runs end to end.

### Grok

Stated clearly: whether Grok Bot has built-in scheduling, we have not confirmed (it is still in beta) — don't take it as a promise.

- If your side has a scheduling feature, build one per job by the five jobs' purposes above, copying the limits from this file.
- If not, use system cron to start up: at the set time, start one session and feed it that job's instructions. See `cron-system.example` for an example.
- If system cron is also unavailable, do it by hand: call out the start yourself at the set time. The two watchdog jobs can't be done by hand and can be skipped — but keep an extra eye on it beside the ledger, and at weekly review, log the missed checks.

### Dots

Dots has built-in scheduled runs. Build one per job by the purposes above, copying the limits from this file. This path is untested by us, with two reminders:

- How the publish job sends when its time comes depends on the rule you set for it in Dots: publish set to "ask me first" means it prepares the ready-to-post pack, stops, and waits for your approval; set to auto-approve, it publishes on its own. Use the former first, and change it once steady.
- After building all five, manually trigger one daily round first, and check whether it starts on time and whether its evidence is complete — only then trust it to run on its own. Same for the two watchdog jobs: check one round first, then trust them.

## When there is no scheduling at all

Use `manual-checklist.md`. It is a one-page checklist, ticking from start to finish step by step. Manual runs lose nothing — they just need a person present.
