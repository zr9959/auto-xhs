[中文](05-followup.zh-CN.md) | English

# Stage guide 05 · Reporting and follow-up

> When to read: when the manager dispatches a report or follow-up task. Read the constitution page first, then this guide.
> All numbers come from the constitution page's numbers table. This guide only cites them, never writes its own.

## Input

- The publish link and actual publish time handed back by the publish stage, with the ledger's (`paths.ledger_file`) day entry as the authority.
- The interaction state file (`paths.interaction_file`) — dedup reads it.

## Output

- The day's ledger line (saved by the publish stage, checked by the follow-up stage).
- Follow-up results: comments and DMs replied to, interaction state file updated.
- Reports by the level rules below. No new activity means silence — no empty reports.

## Evidence list to hand back to the manager

- The time window this round actually covered (start and end times) and the check route (red dots looked at or not, comment counts changed or not, direct-link state).
- Every handled interaction: post link, commenter, time, original summary, reply text.
- Items that couldn't be verified, with the page's own words; DM categories needing the owner.
- The four elements for problems (write "none" when there are none).

## Three report levels

First get clear on when to write one line and when to write all four elements:

1. **All smooth, no problems: one line.** Only topic plus category plus source, title, link, and actual publish time. No running commentary.
2. **A degradable problem, handled by the rules, finished piece unaffected: one conclusion line first, then a short paragraph completing the four elements.** Never a single line saying only "degraded".
3. **A gate failed, nothing posted, finished piece affected, owner action needed, or records disagreeing with what exists: one conclusion line first, then all four elements plus the ready-to-post file paths.**

The run log ignores these levels — the log always keeps full stages and four elements.

## Problems get four elements (same for every step)

Whenever any step breaks, reports and logs must carry all four:

1. Which step and which exact object (which step, which topic tag, which source — name the exact thing).
2. The page's or tool's own words (copy error text verbatim), or the screenshot path.
3. What you tried yourself, how many times each, and what each attempt gave.
4. How it was handled in the end (stopped for a pack, skipped, degraded), and what it means for the finished piece.

Never close with vague words like "broken", "failed", or "doesn't work". Vague equals unreported — no reviewing it later. Log stamps work the same: when a problem happens, log all four on the spot — never patch them in later from memory.

## How to write the ledger

After publishing, add one line to the ledger (`paths.ledger_file`) carrying at least: date, category, title, link, actual publish time, notes. Notes must state: source summary, topic tags blue count / planned count, AI declaration picked or not, first comment posted or not, and problems still unsolved. The actual publish time must be exact — follow-up window math depends on it.

When the ledger, run log, and post list disagree, check the post list first as the outside fact, then fix the records. Never use an old record to cover over the real publish state.

## Follow-up after posting

The stretch right after posting matters most — follow-up only watches the post that just went out today. Window length and check interval follow the table, both counted from the ledger's actual publish time; when the window ends, stop — no follow-up after that.

For a make-up or delayed post, don't pretend a fixed clock time already covered the whole window. Write clearly in the interaction state which stretch this round actually covered, and let a make-up run or the main session cover the missing stretch separately.

### Save effort: red dots first

- First look at the page's notification icons (likes, saves, comments, follows) and the DM icon — any red dots? No red dots means this round ends right there, without opening any list.
- Whether the target post has new comments: only compare its comment count on the home page or post list against the last round. Unchanged means don't open the comments. Changed, or a comment red dot, means open and handle.
- Only handle the newest unhandled items, by time. Never re-read, never re-reply to anything already seen. Right after handling each item, update the interaction state file at once: post link, commenter, time, original summary, reply text. When no stable item ID is available, use those four as the dedup key.

### When a direct link won't open

A public link showing 404, blank, or "this post is temporarily unavailable" doesn't mean the post doesn't exist, and doesn't mean interactions are 0. Do this: enter from the main site's personal home page or post management first, then cross-check with the notification list. When all three routes fail to confirm, write "unverified this round" in the interaction state, plus the page's own words. Never write no-evidence as 0.

### Rules for replying to comments

- Reply in the owner's own voice: spoken, warm, a sentence or two. Every reply must respond concretely to that comment's content and this post's content — no template sentences, no repeated sentence shapes. A natural follow-up works, or one question to keep it going.
- **Scope: a sincere comment with substance (a concrete opinion, a real question, or a genuine feeling) may be answered directly as soon as it's found — no need to ask the owner item by item.** This isn't limited to today's new post and the follow-up window — the same kind of new comment on an old post gets auto-answered too. Old-post new comments get found and handled in passing, when daily tasks (follow-up, morning patrol, weekly review) sweep notification red dots — no separate standing patrol task just for old posts.
- **Three kinds never answered:** ad sellers, diversion posts, pure emotional name-calling. A negative comment carrying a concrete complaint (factual or experience level) gets one sentence that catches it without arguing (sentence range: "你说的这个情况确实有，我把口径补在这里" — "What you describe is real, let me add the wording here"; "这点是我没讲清，补一句：……" — "I didn't explain this point clearly, one more line: …" — catch the fact, not the emotion). Pure emotion, name-calling, and flame-bait don't get answered — only logged in the interaction state and listed by kind in the report.
- A professional question you're unsure about must not be answered by guessing — reply "这个我确认下再回你" (Let me confirm this and get back to you), and report it to the owner.
- No diversion words, links, or sensitive words, and no promises of any kind.

### Rules for DMs

- Normal DMs about the content get a short reply.
- Anything touching money, contact info, partnership quotes, or account safety doesn't get auto-answered — log it and report it for the owner to handle.

### Look only, don't touch

Likes, saves, and new follows are look-only, never auto-followed-back. These changes only go into the interaction state file — they never trigger a report on their own.

### When to report at all

Only when comments or DMs were actually answered, or when DMs needing the owner exist, does one line go out: how many answered and roughly what, or the categories of DMs waiting. No new activity, or only likes, saves, and follows changing, means ending in silence — no empty reports.
