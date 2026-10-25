[中文](faq.zh-CN.md) | English

# Frequently asked questions

## Does it cost money?

The tool chain costs nothing: GSAP, ffmpeg, Playwright, and free voiceover are all free. Whether the agent platform itself costs money depends on which one you use and what plan — that bill is not in this repo. There is one more cost, in time: web-page videos are captured frame by frame, so rendering one video takes quite a few minutes of waiting.

## Can I use it without knowing code?

You don't need to write code, on any path. Setting up the environment and building schedules means typing a few commands by following the guide, and the guide is written so you can copy every command as-is. If a script fails, paste the error's original wording back to the assistant and it will tell you the next step. If that still doesn't work, use `orchestration/scheduling/manual-checklist.md` — fully manual, slower, but it runs.

## Can the account get banned?

Nobody can promise it won't. The platform governs AI hosting explicitly, and fully automated posting and interacting is the highest-risk tier. If you fear a ban, go semi-auto: prepare the ready-to-post pack, look at it yourself, and press publish yourself. Details are in `compliance.md`.

## Which of the three should I pick?

All three are cloud agents. The differences are approval rules and whether you can use them. For full-auto that already works, pick Muse — an account already posts daily with it. With ChatGPT Pro or Business Premium in hand, Dots is worth trying: capability matches Muse, but we haven't tested it, so set publishing to ask-for-approval in its rules first. Grok Bot is still in beta, only open to some SuperGrok Heavy users, and by default it stops before publishing and waits for approval — also untested by us. The full table is in `capability-matrix.md`.

## Why make videos as web pages?

Because agents write HTML most fluently. Layout goes in CSS, animation in GSAP, components pile up in `motion-lib/` for reuse, and changing one line of copy doesn't mean re-cutting the whole video. The cost is rendering by frame-by-frame screenshots, which is slow. To go faster you would need a different tool chain, and this workflow doesn't provide one.

## Can I switch categories and stop doing tech?

Yes. Only three places in the rules tie to a category: the category list in config, the source list, and the examples in the topic-picking guide. Swap those three for your field, and the rest of the flow — writing standards, video making, acceptance, publishing gates — works unchanged. The sensitive-words appendix follows platform rules, so keep it even after switching categories.

## Must I post every day?

No. Frequency lives in config — three posts a week works too. The daily-post times are only recommended values. Posting less often doesn't break the watchdogs or follow-up — just line their trigger times up with your publishing rhythm.

## What if publishing fails, or topics won't turn blue?

Stop first. Don't force it. Topics not turning blue is a publishing gate — deleting topics and publishing bare is not allowed. Save the ready-to-post pack, re-enter the creator platform from the main site by the checklist, and try again, at most twice. If it still fails, publish by hand in the app — nothing in the ready-to-post pack goes missing. For how to write the error into a report, see the four elements in `orchestration/orchestrator.md`.
