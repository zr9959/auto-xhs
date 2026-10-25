[中文](dispatch-templates.zh-CN.md) | English

# Dispatch templates

One per stage, six in all. When the manager dispatches work, copy the matching template and replace the `{{placeholders}}` with the day's actual values before sending.

Placeholder notes:

- `{{date}}`: today's date, e.g. 2026-01-05.
- `{{work_dir}}`: today's working directory. Topic-picking, script-writing, and video-making output all go here.
- `{{stage_doc}}`: this stage's guide path, inside `core/stages/`.
- `{{prev_output}}`: the previous stage's output file paths.
- `{{deadline}}`: this stage's deadline, copied from `core/CONSTITUTION.md`'s numbers table.
- `{{ledger}}`: the topic ledger file path, set in config.
- `{{log_file}}`: today's run log file.

Every template must end with this line, the same for all six:

> When handing back, write by the evidence list format in `orchestration/orchestrator.md`. On a gate exception, stop and hand back in four elements. Don't find a way around it yourself.

---

## 1. Topic-picking dispatch

```
Stage: topic picking
Date: {{date}}
Working directory: {{work_dir}}
Guides to read: {{stage_doc}} (the topic-picking guide), plus the sensitive-words appendix's drop list
Input: {{ledger}} (for dedup and category rotation)
Deadline: {{deadline}}

What to do: scan sources by the guide, settle on 1 topic, and write it into the topic section of {{work_dir}}/post.md.
Probe liveness first: for each channel, spend under 1 minute checking whether it opens, and write the results into {{log_file}}. Skip channels that won't open — don't get stuck on one channel.

Hand back:
- The settled category, and its relation to yesterday's category
- At least 2 checking sources, each with its date
- One visible heat signal (for example, a post's like count, a ranking position)
- The sensitive drop-list check result
- Rejected candidates, one sentence of rejection reason each
- Each channel's actual live/dead state
- How long sourcing took in total
- If a fallback topic was used, mark it "fallback", with its heat rank
```

## 2. Script-writing dispatch

```
Stage: script writing
Date: {{date}}
Working directory: {{work_dir}}
Guides to read: {{stage_doc}} (the script-writing guide)
Input: {{prev_output}} (the settled topic, in post.md)
Deadline: {{deadline}}

What to do: write the full script, saved to two files — complete {{work_dir}}/post.md, and write the segmented voiceover script to {{work_dir}}/scripts.txt.

Hand back:
- Paths of post.md and scripts.txt
- Voiceover script's actual word count (counted from the file, no estimating)
- Body text's actual word count
- 3 title versions and the reason for the picked one
- Where each of the four product questions is answered, by paragraph (only when covering a product)
- Where the full text's judgment sentences are, where the comparisons or turns are
- Topic list
- First comment text
- Four-element exceptions, or "none"
```

## 3. Video-making dispatch

```
Stage: video making
Date: {{date}}
Working directory: {{work_dir}}
Guides to read: {{stage_doc}} (the video-making guide)
Input: {{prev_output}} (post.md and scripts.txt)
Deadline: {{deadline}}

What to do: produce the video by pipeline/'s web-page video pipeline — HTML layout, GSAP motion, frame-by-frame capture, ffmpeg joining. Use motion-lib/ components, don't write a second set yourself. Make the cover as a separate image. At the end, run core/validate.py once.

Hand back:
- Finished video path, cover path
- validate.py output in full
- Finished video acceptance list, all six items (format in the guide)
- One line per major piece of software: software name → interface file → which segment and time point it appears in
- Motion list: which motions were used, at which time points, with at least 3 sampled mid-motion frames
- Four-element exceptions, or "none"
```

## 4. Acceptance dispatch (the manager does it, never dispatched)

This step has no dispatch template. The manager does it personally, steps in `orchestrator.md`'s "Acceptance" section.

Tick through this list item by item at acceptance:

```
- [ ] core/validate.py run, output saved into {{work_dir}}
- [ ] validate.py reports no FAIL
- [ ] Video-making handover's acceptance list has all six items
- [ ] Sampled frames viewed one by one: products match, subtitles inside the safe band, no blank frames
- [ ] Real interface list complete: every major piece of software appears on screen
- [ ] Cover issue number matches the ledger sequence number
- [ ] Sensitive six-surface self-check has per-item results, not just "checked"

Conclusion: pass / send back (on send-back, state which item and which stage it goes back to)
```

After a send-back, the old conclusion is void. Once redone, verify again from the first item.

## 5. Publishing dispatch

```
Stage: publishing
Date: {{date}}
Working directory: {{work_dir}}
Guides to read: {{stage_doc}} (the publishing guide), plus the sensitive-words appendix
Input: {{prev_output}} (accepted finished video, cover, post.md, as recorded in the acceptance list)
Deadline: {{deadline}}

What to do: publish through the creator platform by the guide's entry route. Uploaded files must match the ones recorded in the acceptance list — if filename, size, or modification time mismatches on any one of them, stop and come back to confirm first.

Hand back:
- Pre-publish compliance self-check, eight items, each with its result
- Topic blue-tap result: how many turned blue, how many were planned, checked one by one
- Publish link and actual publish time
- Proof the AI declaration was picked
- Proof the first comment was posted
- Post-publish public page re-check result: topics clickable, video plays
- If a missing or un-blue topic is found only after publishing: first go to the edit page to add topics (the pencil icon that appears when hovering a card in post management), then check blue again. If the edit page can't add them either, hand back in four elements — don't delete and repost
- If stopped and held for sending: the four ready-to-post pack file paths, plus the platform draft's own wording on whether it saved
- Four-element exceptions, or "none"
```

## 6. Follow-up dispatch / review dispatch

These two are separate scheduled jobs, not part of the daily round. Templates sit together, same format.

Follow-up dispatch:

```
Stage: post-publish follow-up
Date: {{date}}
Guides to read: {{stage_doc}} (the follow-up guide)
Input: {{ledger}}'s latest entry for today (title, link, actual publish time)
Window: from the actual publish time, 0 to 2 hours, checking every 30 minutes, stopping at 2 hours

What to do: first check whether the notification and DM icons have red dots. No red dots and no comment-count change means this round ends right here — don't open the list. Only handle new items, logging each one into the interaction status file as you go.
A direct link that won't open, shows blank, or says it can't be viewed does not mean the post doesn't exist: re-enter from the main site's profile page or post management, then cross-check with the notification list. If all three routes fail to verify, write "unverified" plus the page's original wording — never write it as 0.
Hand back: this round's covered time span, routes checked, each handled interaction (post, who, when, rough original text, reply text), items not verified with page wording, and DM categories needing the account owner.
Reporting rule: report one line only if you actually replied to a comment or DM, or if there is a DM needing the owner. No movement means a quiet end.
```

Review dispatch:

```
Stage: weekly review
Date: {{date}} (Sunday)
Guides to read: {{stage_doc}} (the review guide), plus the full lessons book
Input: this week's {{ledger}} entries, each post's acceptance list, this week's feedback and run logs
Deadline: {{deadline}}

What to do: look at how many posts went out this week, category spread, which did well and which did badly, and write conclusions into the lessons book. Whatever became a rule goes up into the matching core/ file by the review guide's rule-promotion rules. Also do data backfill, draft cleanup, and wording-consistency patrol. On the month's first review, re-read the sensitive-words appendix for timeliness and update it against the platform's latest notices.

Hand back:
- This week's post count, category spread, best and worst one each with evidence (if data hasn't come out, write that it hasn't — never invent it)
- Data backfill results, item by item
- Draft cleanup: how many deleted, what each was; ones not deleted, listed for confirmation
- Consistency patrol: check results item by item, differences found
- Which parts of core/ changed this time, and why
- Four-element exceptions, or "none"
Finally, post a one-sentence summary at the report spot.
```
