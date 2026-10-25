[中文](README.zh-CN.md) | English

# X module: account warming, posting, replies

For an international audience: main posts, replies, and self-replies are all in English. Read the risk disclosure at the end first, then decide whether to do this.

## Direction and mix

- Main line: work log — content from real work done each day (building sites, maintaining products, repo upkeep, research, automation, including failures and fixes), with real proof (screenshots, numbers; links only in self-replies).
- Hot topics: the newest releases and hottest discussions in this field (AI agents, tools, indie dev), followed up right away with your own tests, data, or a clear stance — not opinion-free news reposts.
- Side line: 2 long posts a week, explaining one topic properly (for example, the AI ecosystem in a region).
- Reference mix: work log about half, hot topics three to four tenths, side line about two tenths.

## Cold-start rules (followers < 500, highest priority)

- While followers are under 500, main posts don't cover your own projects or work log (except when you specifically ask for one post). Lead with hot topics in this field — newest releases, hot discussions, angles that spark replies — and build followers first.
- Drafts of your own content still go into the content pool as usual, marked "enable after 500 followers", just not posted.
- At 500 followers and up, the mix above comes back. The side line is topic content, not self-promotion, so it stays during cold start.

## Five-stage warming

Days 1–7 / 8–14 / 15–30 / 31–60 / 61–90, quotas and actions rising each stage. One low-activity day per week.

- **Quota rule**: practitioner ranges sit far below the official limits; follows start around 1/8 of the official limit.
- **New action unlock order**: first post → first thread → first video → outside links (self-replies only) → DMs (from stage 3, people you know only, at most 3 a week, no links).
- **Posting windows**: main window set by audience timezone (example: 21:00–23:00 Beijing time, roughly US East morning + Asia evening); second window 08:00–09:30.
- **Stock**: finished drafts under 5 is an alarm; work-log content pool at 14 or more.

## Post length and layout

- **Post length rotation**: short posts are the mainstay (15–45 words); length bands rotate roughly 50/30/20 so not every post is the same length.
- **Reply length**: median about 10 words; about half are 10 words or under; three sentences or more are rare; no closing punctuation is normal — don't end every line with a period.
- **Layout**: hashtags 0–1 (max 2); emoji 0–2, mostly at the end of the sentence; no Unicode bold, no emoji at the start of every line, no hashtag wall at the end, no templated thread symbols.
- **Concreteness**: every main-line post has at least 2 concrete numbers (counts, hours, lines, prices, error text — pick any) + one clear conclusion (shipped, fixed, failed; for tools, say keep / skip / wait). With no real record, write "according to the official post" — never invent.

## Human-like writing rules

It comes down to one line: **human = reacting to one specific point in the parent post + varied length + concrete numbers and a stance**; AI flavor = always a complete structure.

- **Banned words and patterns**: delve, moreover, furthermore, in conclusion, it's worth noting, overused game-changer, not just X, but Y parallels, a CTA at the end of every post, a question at the end of every post, restating the opening as a summary.
- **Reply no-go zones**: restating the parent post, "Great post! Thanks for sharing" customer-service tone, over-complete answers, bare-link resource drops, one-word praise ("This." style).
- **Pick the move by parent post type**: under show-off and media posts, praise a specific point (no empty praise); under ask posts, lead with personal experience; under tutorial and test posts, lead with questions + experience + added facts; under news and opinion posts, disagreement and corrections are fine, with evidence.
- **Self-replies**: mainly to add info, correct, or continue. Give real replies to replies with substance. Short thanks only go so far — don't answer every one, don't use template thanks. If someone under your own post asks a real question, answer it properly — that is the rarest and most follower-winning part.

## Image rule

- Main posts can't be text-only — especially long ones. Every main post needs at least 1 picture that matches the content; nobody reads pure text to the end.
- **Real pictures first**: official release images, product homepages, event screenshots, real interface screenshots from your own work, public news or original-post screenshots — found online, but verified to match the post's topic, no mismatches; credit the source when quoting someone else's picture.
- When no fitting real picture exists, generate one: made from the post's content, as an illustration only, never passed off as a real photo.
- Red lines don't move: AI pictures avoid real faces and faked real events; look at the original before posting and confirm it's not blurry, doesn't crop key info, and lets a reader tell at a glance what the post is about (data, interface, comparison, process) — not decoration.
- Replies don't need pictures; replies are text-led.

## Content red lines

No buying followers, likes, or accounts; no follow-back groups, no follow trains, no giveaway growth hacks; no mass indiscriminate follow/unfollow; no posting the same or near-identical content across accounts; no impersonating people or organizations; no AI-generated real faces as personas; no deceptive synthetic media (real people, real events); no downloading and re-uploading; no price calls, airdrops, or fake giveaways; no posting other people's private info. AI-written drafts are not themselves a violation — what violates is bulk, repetitive, indiscriminate behavior patterns.

## Review

- Daily KPI log: impressions, engagement, profile clicks, follower growth, reply funnel.
- Weekly review of top / bottom 3 posts, and update this module.
- When reach drops sharply, check the platform's account status page first, then work through three checks: content, behavior, account status.

## Membership

Run free for a month to get baseline data before judging paid membership: long posts without splitting and reply ranking help, but they don't fix the root problem of 0 followers. Re-judge when 30 days of data are in, or when a single post's median impressions stay under 100 for a long time — with data, then decide.

## Risk disclosure (must read)

Automated operation (clicking through screens like a person to post, reply, follow) goes against the spirit of the platform's rules on non-human behavior. The platform checks for this kind of operation, and the account and linked accounts can be banned. This module treats quotas, pacing, and human-like writing as risk reduction, not a free pass. Weigh it yourself before running it. On any verification or restriction prompt, stop immediately and report — don't push through.

## Runnable code (`scripts/check_post.py`)

Check a post before sending it. FAIL items must be fixed; WARN items are your judgment call.

```bash
python3 scripts/check_post.py --text "post text"
python3 scripts/check_post.py --file draft.txt
python3 scripts/check_post.py --text "reply text" --kind reply
```

Checks: banned words, Unicode bold, 🧵👇 full template symbols (these three are FAIL); more than 2 hashtags, more than 2 emoji, fewer than 2 concrete numbers in a main-line post, links in the main text, replies over 30 words (WARN). Chinese counts by character, English by word — otherwise a Chinese post split on spaces is always just a few "words" and the length check never fires.

Test record (2026-10-25): good post 0 FAIL 0 WARN; bad post (banned words + 3 hashtags + Unicode bold + 🧵👇 + bare link) 3 FAIL 3 WARN, exit code 1.

Posting itself is deliberately not automated code: the platform checks for non-human operation, and auto posting, replying, or following can get the account banned (see the risk disclosure above). Once it passes the check, post it yourself in the browser.
