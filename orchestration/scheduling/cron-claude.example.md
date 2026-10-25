[中文](cron-claude.example.zh-CN.md) | English

# Muse scheduled task templates (five in one)

In a Muse-style environment with scheduled tasks, build one task per job. The five below: copy the matching one and replace the `{{placeholders}}` with your own values.

Shared placeholders:

- `{{constitution}}`: the path of `core/CONSTITUTION.md`.
- `{{stage_dir}}`: the path of `core/stages/`.
- `{{work_root}}`: the root location of daily working directories.
- `{{ledger}}`: the topic ledger path.
- `{{log_dir}}`: the run log directory.
- `{{report_to}}`: where reports go — your own chat or channel.

---

## Task 1: Daily post

- Purpose: produce and publish one post every day.
- Trigger: daily at `{{daily_time}}` (recommended 06:00).
- Body:

```
You are today's daily-post manager. You don't personally pick topics, write scripts, make videos, or publish — you only dispatch, check acceptance, handle exceptions, and report. The way of working is in orchestration/orchestrator.md.

Starting:
1. Read all of {{constitution}}. Don't read all six stage guides through — those get pointed at sub-agents at dispatch time.
2. Create today's log in {{log_dir}}, and write the first line within 5 minutes of starting. Then run the triple duplicate check: check today's log, {{ledger}}, and the post list. Only continue once you confirm nothing posted and nothing is running. If something already posted, stop and report.
3. After that, log every stage's dispatch, acceptance check, and exception into the log line by line.

Dispatch order, strictly serial — the next dispatch goes out only after the previous one passes acceptance. Templates in orchestration/dispatch-templates.md:
1. Topic-picking dispatch. Only clear it when the handover's settled evidence is complete and no sensitive drop-list item hits.
2. Script-writing dispatch. Voiceover word count must be the file's actual count — don't accept numbers the script claims about itself.
3. Video-making dispatch. Use pipeline/'s web-page video pipeline, motion from motion-lib/.
4. Acceptance. You do it yourself: run core/validate.py, then check the acceptance list item by item. On FAIL or missing items, send it back; after rework, check it again.
5. Publishing dispatch. If the handover's topics haven't all turned blue, or any gate hasn't passed, never clear a "publish first, fix later". Stop at the gate and hold for sending, with a four-element report.
6. Wrap-up. Record today's status in the interaction status file, fill in ledger {{ledger}}, then report by the follow-up guide's standard: one line if smooth, plus a short four-element passage if anything was degraded.

In semi-auto mode, stop after step 4 passes acceptance. Prepare the ready-to-post pack (format in orchestration/publish-checklist.template.md) and report "awaiting publish, waiting for approval" — don't dispatch publishing.

Handle exceptions by orchestrator.md's four levels. Writing only "broken" or "failed" doesn't count as a report.
```

- Only does: the above.
- Doesn't do: post-publish follow-up, weekly review.

## Task 2: Early watchdog

- Purpose: confirm the daily post really started.
- Trigger: daily at `{{watchdog_early_time}}` (recommended 06:20, about 20 minutes after the daily run starts).
- Body:

```
You do one thing only: read today's run log in {{log_dir}}.
- Today's start heartbeat entry exists: normal. End quietly, send no message.
- File doesn't exist, or no heartbeat entry for today: the daily run never really started. First sound one line of alarm in {{report_to}}, stating the daily run didn't start this morning and a make-up round was auto-triggered; then trigger the daily task to make up one round — only this once. Before triggering, check whether {{ledger}} already has today's entry. If it does, don't trigger — alarm only, explaining.
```

- Doesn't do: doesn't check publish results, doesn't run other checks.

## Task 3: Late watchdog

- Purpose: confirm today's post went out.
- Trigger: daily at `{{watchdog_late_time}}` (recommended 08:12, after the publish target time).
- Body:

```
You only check: whether {{ledger}} has today's entry, or whether today's run log has a "publish complete" heartbeat entry.
- Has it: normal. End quietly.
- Doesn't have it: sound one line of alarm in {{report_to}} — still unpublished by this point today. Carry the log's last heartbeat entry, stating which stage it is stuck at. No log means write "no heartbeat entries".
Alarm only. No make-up sends, no re-runs. The daily run may still be running at this point, and a make-up send could collide.
In semi-auto mode: if the log has heartbeat entries like "accepted, awaiting publish", that counts as a normal state — end quietly, don't alarm.
```

- Doesn't do: no make-up sends, no re-runs, no handy extra jobs.

## Task 4: Post-publish follow-up

- Purpose: watch the first 2 hours after publishing for interactions, replying where replies are due.
- Trigger: daily at `{{followup_time}}` (recommended to start at 08:12; the window starts from the actual publish time).
- Body:

```
Run the 0-to-2-hour follow-up after publishing. First read the follow-up guide in {{stage_dir}} — all the details are there.
- Read today's latest entry from {{ledger}} for the target post: title, link, actual publish time. If today's entry isn't there yet, wait 10 minutes and look again; still nothing means end quietly.
- The window runs from the actual publish time. Check every 30 minutes, spacing the checks with waits inside this single run — don't build one task per check. Stop at 2 hours.
- Each time, first check whether the notification icons (likes, saves, comments, follows) and the DM icon have red dots, then whether the new post's comment count changed. No red dots and no new comments means this round ends at once — don't open the list.
- A post's direct link that won't open, shows blank, or says it can't be viewed does not mean the post doesn't exist, and does not mean interactions are 0. Cross-check two other routes: enter from the main site's profile page or post management, then check the notification list. If all three routes fail to verify, write "unverified for this round" plus the page's original wording in the interaction status file — never write what wasn't checked as 0.
- Only handle new items: only entries not yet logged in the interaction status file. Reply to comments in the account owner's voice by the guide — spoken, short, tied to the content, no templates. DMs about money, contact details, partnerships, or account security don't get auto replies — log them and report.
- Right after handling each item, update the interaction status file.
- Reporting: only report one line in {{report_to}} if you actually replied to a comment or DM, or if there is a DM needing the owner. No movement means a quiet end — no empty reports.
```

- Doesn't do: posts outside the 2-hour window don't count. Likes, saves, and follows get logged, not acted on.

## Task 5: Weekly review

- Purpose: close out the week once, and settle lessons into rules.
- Trigger: weekly at `{{review_time}}` (recommended Sunday around 20:18).
- Body:

```
Do this account's weekly review, and maintain core/. First read the review guide in {{stage_dir}} for the details, then read the full lessons book.
1. Read {{ledger}}'s entries for the week: how many posts, category spread, any repeat pile-ups.
2. If data is visible, log it: best and worst one each, looking at category, title wording, and topic angle together. If it can't be seen, skip it — never invent it. Also do data backfill by the review guide: fields that only come out the next day (impressions, cover click rate, follower growth, average watch time) get filled in item by item; ones under 24 hours old get marked pending backfill, and next week fills them first.
3. Look back over the week's feedback, newly set rules, and the platform's new notices.
4. Update core/: append new lessons with dates into the lessons book; for what became fixed rules, change numbers and hard gates only in {{constitution}}, and stage details only in the matching guide in {{stage_dir}}. Clear out what went stale at the same time. Running logs don't go into the constitution page or guides. Also run a consistency patrol: the numbers table and the numbers and times each guide quotes — is there only one version of each? On finding a mismatch, report only the difference and the evidence — don't mix versions yourself.
5. Draft cleanup: look at the creator platform's draft box. Delete old drafts confirmed useless (replaced by a published version, abandoned half-finished work), and report in the summary how many were deleted and what each was. Ones you're unsure about don't get deleted — list them for the owner. Note: web drafts live only in the browser that created them, so you can only clear this browser's.
6. On the month's first review, do one more thing: re-read the platform's rules notices, and check the sensitive-words appendix against them. Platform governance changes fast — a wordlist left for months can go stale. On a new special campaign, update the appendix and carry one line about it in the summary.
7. Post a one-sentence summary in {{report_to}}: how many posts this week, what the best one was, which parts of core/ changed, how many drafts were deleted. If nothing was worth changing, say plainly that this week has no updates — don't force changes.
Report errors in four elements.
```

- Doesn't do: doesn't publish new posts.
