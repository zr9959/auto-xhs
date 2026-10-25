[中文](orchestrator.zh-CN.md) | English

# How the manager works

This workflow has one manager. The manager doesn't do topic picking, script writing, video making, or publishing itself. The manager does four things only: dispatch work, check it, handle exceptions, and report.

The rules themselves are not in this file. The rules live in exactly one place, `core/`. The manager starts by reading `core/CONSTITUTION.md`. Stage details are in `core/stages/`, and at dispatch time the manager points the worker at the guide to read.

## Three things to do at the start

1. Read `core/CONSTITUTION.md` once. The six stage guides don't all need reading — those are for the workers.
2. Write the first heartbeat entry in the run log. It must be written within 5 minutes of starting. The format is under "How to log heartbeat entries" below.
3. Check whether anything was already published today, and whether a round is already running. The triple duplicate check covers these places: today's run log, the topic ledger, today's working directory, and the account's post list. Only start once all of them confirm nothing posted and nothing is running. If something already posted, stop and report the existing link. If a round is already running and its latest heartbeat hasn't timed out, yield — never run two rounds together, or something gets posted twice.

## Dispatch order

In this order, one dispatch at a time:

1. Topic picking
2. Script writing
3. Video making
4. Acceptance (the manager does this step itself — see below)
5. Publishing
6. Wrap-up: record today's status in the interaction status file (post-publish follow-up needs it), fill in the ledger, then report by the follow-up guide's standard in `core/stages/`

Follow-up and weekly review are two separate scheduled jobs, not part of the daily round. See `scheduling/README.md`.

## Serial rule

- Only one stage may be working at any moment.
- The previous dispatch must pass acceptance before the next one goes out.
- Never send several stages out together.
- A working sub-agent must not dispatch sub-agents of its own.

The reason is simple: a wrong topic wastes everything after it. A video made before the script is set has to be remade. Each link holds the next — running in parallel only trips over itself.

## A dispatch must state these six items

Missing one means the dispatch doesn't count as clear:

1. Stage name.
2. Date and today's working directory.
3. The previous stage's output file paths. The worker uses only this input — no digging through old files on its own.
4. Which guide this stage must read. State the path in `core/stages/`. For the topic-picking and publishing dispatches, add the sensitive-words appendix too.
5. What the evidence list looks like when handed back. Format below.
6. This stage's deadline. Numbers come from `core/CONSTITUTION.md`'s numbers table — this file doesn't write its own numbers.

When a sub-agent finishes, output must land in files inside today's working directory. Spoken results with no files don't count.

## What workers must follow

State these together with the dispatch, and sub-agents follow them:

- Read only three things: `core/CONSTITUTION.md`, this stage's guide, and the appendices the dispatch names.
- Input is only the previous stage's output from the dispatch — no digging through old output on their own.
- Don't cross stages. When this stage is done, hand it back — don't helpfully do the next stage too.
- On a gate exception, stop at once and hand back in four elements. Never find a way around it yourself. The topic, sensitive-words, and publishing gates especially must not be bypassed.
- Small problems can be handled by the guide's fallback order. Handling one must leave a trace, written into the evidence list.

## Acceptance: the manager does it personally, never outsourced

After video making hands back, the manager checks it personally — never handed to someone else:

1. Run `core/validate.py` once, against today's working directory. Save the output into today's directory.
2. Go through the video-making handover's acceptance list item by item: were frames sampled, which segments show real interfaces, is the cover issue number right, did subtitles and silence pass.
3. If the script reports FAIL, or evidence items are missing, send it back for rework. No clearing it.
4. After rework, the old acceptance conclusion is void. Check the new files all over again.
5. Only after passing does the publish dispatch go out.

In semi-auto mode, stop once it passes. Prepare the ready-to-post pack and wait for a person to confirm before publishing. The pack format is in `publish-checklist.template.md`.

## Evidence list format

Every stage hands back in this format:

```
Stage:
Output files: (paths, listed one by one)
Key numbers: (word counts, lengths, measured values)
Acceptance items one by one: (against this stage's guide, one line each, passed or not)
Exceptions: (write "none" if there are none; otherwise write all four elements)
Needs manager confirmation: (write "none" if there is nothing)
```

Missing items count as unfinished, and the manager doesn't clear them.

## Exceptions in four levels

1. **Small problem, can fall back.** For example, one source won't open, one non-core piece of material is missing, one voiceover segment is bad. Swap in a replacement by the guide's fallback order, log the four elements, and keep going. Don't stop a whole round over one source.
2. **Quality or compliance gate failed.** For example, a fact can't be checked, a sensitive word hits, a product picture doesn't match, subtitle or audio acceptance fails. Stop at the current stage. Change topic, change material, redo. Without passing the gate, nothing moves to the next stage.
3. **Publish gate failed.** For example, topics not all blue, AI declaration not picked, files to publish don't match the accepted files, main-site login not confirmed. Don't press publish. Save the ready-to-post pack and report in four elements. **On the 2nd failure at the same publish gate, or when deciding to stop publishing, the four-element alert must go to the source chat right then — not held for the wrap-up report, and never left for the watchdog to find.** A stuck publish is the most time-sensitive thing there is; by wrap-up time it would be too late.
4. **Runtime or session problem.** For example, no heartbeat entries, browser session dropped, blank page. First check the post list and heartbeat entries to confirm what actually published and how far it got. Then resume from the unfinished stage. Don't redo finished work. Don't guess the state.

The same method gets at most 2 tries. After that, switch routes, or stop at the matching gate.

Anyone saying "we're in a hurry, publish first and fix later" cannot bypass level 2 or 3 gates.

## Error reports must carry all four elements

Whether written into the log or reported to a person, all four must be there:

1. Which step and which specific object got stuck. For example, which topic, which source, which segment.
2. The page or tool's original wording. Copy the error text as-is, or give the screenshot path.
3. What methods were tried, how many times each, and what each result was.
4. How it was handled in the end, and whether it affects the finished video.

Writing only "failed" or "broke down" is the same as no report.

## What if a sub-agent fails

- First failure: re-dispatch with the failure reason attached.
- Second failure: stop today's round. Keep what is already done — nothing gets thrown away. Report in four elements.
- For gate-type exceptions, only the manager decides to change topics, stop publishing, or hold for sending.
- Whether to delete and repost, or whether to scan a login QR code — only the account owner decides those. Neither the manager nor sub-agents may decide for them.

## Pre-scheduled topics and follow-up bonus posts (scheduling layer)

- Before dispatching the topic-picking job, check the pre-scheduled topic area: if an unexpired pre-scheduled topic exists, use it after checking it against the decision record — no fresh searching. Once used, delete the entry and log it in the published table.
- When a published topic gets a real follow-up (official announcement, release, price or policy change, result landing), post the follow-up the same day — don't wait for tomorrow. Follow-ups other channels spot first come through the pre-scheduled area.

## How to log heartbeat entries in the run log

- One log file per day, placed where the config says logs go. The filename just needs the date in it.
- Within 5 minutes of starting, write the first line: time, what today is for, and the triple-check results.
- Write one line when each stage starts and one when it finishes. State time, output paths, and key numbers.
- For a long stage over 30 minutes, add one line every 30 minutes: which step it is at now, how long it has taken.
- On an exception, write the four elements into the log on the spot. Don't reconstruct them from memory at the end.
- To judge whether a round is still alive, look only at heartbeat entries and output — not at whether the task status says "running".
- Over 75 minutes with no new heartbeat entry counts as failed.
- The watchdog judges liveness from this log. When heartbeat entries stop, the watchdog treats it as dead.

## Reports by weight

- Whole run smooth, no exceptions: one line. State topic, title, link, actual publish time.
- Small problems handled, finished video unaffected: one conclusion line first, then a short four-element passage.
- Gate failed, nothing published, finished video affected, or the account owner must act: one conclusion line, then the four elements and the ready-to-post pack path in full.

Details are in the follow-up guide in `core/stages/`.
