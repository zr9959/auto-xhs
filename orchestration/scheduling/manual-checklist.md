[中文](manual-checklist.zh-CN.md) | English

# Running one round by hand: a one-page checklist

With no scheduling and no sub-agents, tick through this page from top to bottom for a complete daily round. Slower, and it needs a person present, but no step is missing.

## Start

- [ ] Open `core/CONSTITUTION.md` and read it once
- [ ] Create today's working directory and run log, and write the first heartbeat entry (what time it is now, what today is for)
- [ ] Check four places: today's log, the topic ledger, today's working directory, the post list. Confirm nothing posted today and no round is running

## Topic picking

- [ ] Read the topic-picking guide in `core/stages/`, and the sensitive-words appendix's drop list
- [ ] Scan sources, probing liveness first — skip ones that won't open
- [ ] Settle on 1 topic: passed the sensitive list, facts checked against two sources, related to the audience
- [ ] Write the six settled items into today's post.md: category, relation to yesterday's category, 2 sources with dates, one heat signal, drop-list check result, rejected candidates with reasons
- [ ] Log heartbeat entry: topic settled

## Script writing

- [ ] Read the script-writing guide in `core/stages/`
- [ ] Write 3 title versions first, pick one, write the reason into post.md
- [ ] Write body, topic list, and first comment into post.md
- [ ] Write the voiceover script into scripts.txt by segment, format `segment-name|text`, one segment per line
- [ ] Count voiceover words and body words once, against the numbers table
- [ ] Log heartbeat entry: script settled, with word counts

## Video making

- [ ] Read the video-making guide in `core/stages/`
- [ ] Prepare materials: every major piece of software has a real interface, written into post.md's material list
- [ ] Make the video by pipeline/: web-page layout, GSAP motion (using motion-lib/), frame-by-frame capture, voiceover, ffmpeg joining
- [ ] Make the cover as a separate image, issue number matching the ledger sequence number
- [ ] Run `core/validate.py`, no FAIL
- [ ] View sampled frames one by one: products match, subtitles inside the safe band, no blank frames, silence checked
- [ ] Write the six-item acceptance list into post.md. For long stages, add one log line every 30 minutes

## Publishing (full-auto and semi-auto split here)

Semi-auto:

- [ ] Pack video.mp4, cover.jpg, post.md, and publish-checklist.md into a ready-to-post pack (template in `orchestration/publish-checklist.template.md`)
- [ ] Stop here. Once a person is present, publish by ticking through the publish checklist item by item
- [ ] After publishing, fill the link and actual publish time back into the ledger

Full-auto:

- [ ] Read the publishing guide in `core/stages/`
- [ ] Pre-publish compliance self-check, eight items, each with its result
- [ ] Enter the creator platform from the main site; uploaded files match the accepted ones
- [ ] Tap topics blue one by one, blue count = planned count; if not all blue, stop and save the ready-to-post pack
- [ ] Pick the AI declaration, press publish
- [ ] Open the public page to re-check: topics clickable, video plays
- [ ] Post the first comment
- [ ] Ledger entry: date, category, title, link, actual publish time
- [ ] Log heartbeat entry: publish complete

## 2 hours after publishing

- [ ] From the actual publish time, check notifications and DMs for red dots every 30 minutes
- [ ] On new comments, reply, and log each reply into the interaction status file. DMs about money, contact details, partnerships, or account security don't get replies — report them to the account owner
- [ ] When a direct link won't open, re-enter from the profile page or post management, then cross-check with notifications. If nothing verifies, log it as "unverified" — never as 0
- [ ] Stop at 2 hours. No movement means no report needed

## Wrap-up report

- [ ] Smooth run: one line — topic, title, link, publish time
- [ ] With exceptions: one conclusion line first, then the four elements (where it stuck, the page's original wording, what was tried and how many times each, how it was handled)

## Once a week (can be made up manually on a weekend)

- [ ] Read the review guide in `core/stages/` and the lessons book
- [ ] Look at the week's ledger: how many posts, category spread, best and worst one each
- [ ] Data backfill: fill in fields that only come out the next day; mark not-yet-out ones as pending backfill
- [ ] Write new lessons into the lessons book; whatever became a rule, change the matching `core/` file
- [ ] Look at the draft box: delete useless old drafts, keep ones you're unsure about
- [ ] On the month's first time doing this section, re-read the sensitive-words appendix and update it against the platform's latest notices
