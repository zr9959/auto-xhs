[中文](01-sourcing.zh-CN.md) | English

# Stage guide 01 · Topics

> When to read: when the manager dispatches the topic task. Read the constitution page first, then this guide, plus the sensitive appendix's drop list (the copied `sensitive-words.md`; if there isn't one yet, copy it from the template first) — dropped topics get filtered at this gate.
> All numbers come from the constitution page's numbers table. This guide only cites them, never writes its own.

## Input

- What the manager's dispatch gives you: date, yesterday's category, the past week's category spread.
- The topic ledger (`paths.ledger_file`) — dedup and rotation both read it.
- The source list you filled in config.

## Output

- 1 settled topic (or a fallback topic), written into the day's material folder in the topic section of `post.md`.
- One more line in the run log: the "选题定案" (topic settled) stamp.

## Evidence list to hand back to the manager

- Six items of settled-topic proof: category, relationship to yesterday's category, at least 2 checking sources with dates, one visible heat signal, the sensitive drop-list check result, and the rejected candidates with one line each on why they were rejected.
- How long sourcing took, and each channel's probe result (up or down).
- If you went to fallback, mark it "fallback topic" with its heat rank and signal.
- The four elements for problems (write "none" when there are none).

## Source list (fill it in config — here's how to fill it)

Sources go in `config.yaml` under `sources`. Work out which ones you actually watch using this empty table, then fill it in:

| Source | Type | What to watch | Entry point | Notes |
|---|---|---|---|---|
| (Sample row, delete when filled) Media A | Industry media | Front page, daily charts | Fill in the URL | Replace with your own when filled |
| (Sample row, delete when filled) Official B | Vendor official | Release pages, update notes | Fill in the URL | First-hand source, for fact-checking |
| (Sample row, delete when filled) Community C | Social / forum | Hot posts in the matching board | Fill in the board name | Heat and pain points only |
| | | | | |

When filling it in, note:

- Keep at least one or two official first-hand sources. Key facts get checked against them.
- Social and forum sources need a read-only way of browsing you prepare yourself — look, don't interact, and follow the platform's rules. Never write any account or login info into these files.
- Every source gets its own per-source time limit. When it's up, skip it — see the table.

## How to source

- **Probe liveness first.** Spend the table's probe time at the start trying each channel: does it open, can you search? Write this round's actual up/down state into the run log. Never carry over yesterday's conclusion — a channel's state can change daily.
- **Two stretches.** The first stretch scans wide; the second only checks the leading candidates (count per the table). When the total sourcing cap hits, stop at once — settle only among already-checked candidates. Never stretch the whole round longer just to see one more topic.
- **A source that won't open gets skipped.** Login wall, blocked, blank page — log one line of four elements and skip. One media outlet down means skipping just that one. When all social and forum helper sources are down, degrade to the "media + official" flow and still produce a topic. Two-source checking only happens for the finally settled topic — not a full round for every candidate, that costs too much time.

## How to judge a topic

Three conditions together — missing one pushes it down the list:

1. **New.** Inside the table's freshness window.
2. **Hot.** People are already discussing and sharing it, or it ranks on some chart. Give one visible signal: likes and comments, shares, chart position — pick one and state it clearly.
3. **Connected to the audience.** Say in one sentence what it has to do with the viewer (see constitution core standard 1). A topic only the media covered, with nobody discussing it, goes down the list; a topic people are already talking about goes first. A cold topic nobody discusses only gets picked when its audience connection is extremely strong.

A few more rules:

- **Comments are not fact evidence.** Comments show direction, judge heat, and dig up real pain points. Facts go back to official and media sources to check.
- **A first-hand original post counts as a first-hand source.** Original posts from official accounts, developers, or the people involved (releases, update notes, test posts with original screenshots and data) rank with official updates. Retelling posts are only leads.
- **An original post's pictures can be used as material.** Re-lay the picture into your own layout with your own labels, and tell it in your own words. Never translate a whole piece and repost it as-is — that's reposting, and it risks penalties.
- **More reference material can come after settling.** Once the topic is settled, you can look at sources in other languages and regions for reference, to help understanding and rephrasing. But the topic itself only comes from the sources on your list — reference material doesn't count as a topic source.
- **Many sources get merged into your own script.** Sweep every channel first, cross-check each side's claims and material: use what matches, mark disagreements clearly or drop them. Finally merge it into your own structure, your own wording, plus your own judgment. Even the best single source is only one ingredient.
- **No source labels outside.** Once merged and adapted, it's your own script — body, pictures, and cover carry no source labels. The ledger still records sources as usual; that's for your own checking, not for the public.

## Category rotation

- The category list lives in `content.categories`. Below are examples — change them to your own: Sample category A, Sample category B, Sample category C, Sample category D, Sample category E. Set the count to your direction; five to seven works well.
- Stay as different from yesterday's category as possible. One category must not pass the table's weekly cap. The week's news-to-tutorial ratio follows the table.
- Tutorial topics should preferably carry a clear search term. Topics people search for keep their traffic longer.
- Order audience preferences by your own positioning. One general order: first things that save people money or help them avoid traps, then things that raise efficiency, and only last pure parameter talk.

## Two gates first

- **Sensitive content is a straight veto.** Run the sensitive appendix's drop list first — one hit drops the topic, no discussion about a different angle. Topics touching sensitive content get filtered at this gate, not left for pre-publish.
- **Fact-checking.** A settled topic's key facts need an official first-hand source plus at least 1 independent source confirming the key numbers and claims; with no official source, at least 2 mutually independent sources must agree. An official original post can prove facts about its own release (price, specs, and the like), but third-party judgments like performance, reviews, and market impact still need an independent source to confirm. Single-source rumors don't get used. A fact that won't check out gets dropped, or labeled as a leak. Never treat one retelling chain as several sources.

## Settled-topic proof

The settled stamp and the day's `post.md` must both state eight items — missing one means the topic isn't settled: category, relationship to yesterday's category, at least 2 checking sources with dates, one visible heat signal, the sensitive drop-list check result, rejected candidates with one rejection reason each, the sequel check result (follow-ups on the last 30 days of posted topics — yes or no, plus how handled), and the event matching result (yes or no, plus the event name and requirement points joined).

## Sequel check (sweep once before settling)

Before settling, sweep the last 30 days of posted topics for real follow-ups: announcements, releases, price or policy changes, results landing. When there is one, handle it as a "same-day sequel extra post": publish the extra post the day you find it, don't wait for the next day's post; the settled proof states what the follow-up is and how it was handled. When there is none, write "none". Follow-ups other channels found first come through the queued-topic area and get picked up the same day.

## Queued topics (check the queue before searching yourself)

Before dispatching, check the queued-topic area: an unexpired queued topic gets used directly for a check-and-settle, with no self-search. Once used, the manager deletes that queued entry and logs the posted entry as usual. Only with no queued topic do you run normal sourcing.

## Event matching (check while picking topics)

Each day while picking topics, check the platform creator center's activity center, record ongoing events (name, dates, theme) in the day's topic brief, and keep a list of ongoing events. When a candidate direction found in the next 2–3 days matches any listed event theme, follow that event: first read the event requirements in full (how to join, required topics or tags, format, deadline), then create per the requirements (carry the required topics, submit to the event page), and note the event name and the requirement points met in post.md and the topic record; the settled proof adds one item, "event matching result" (yes or no, plus the event name and requirement points joined). Three guardrails: the direction must pass on its own first (freshness, heat, audience connection, fact-checking, sensitive list all still apply) — never force an unrelated topic for an event, never bend a topic's facts; when event requirements clash with existing hard gates (compliance list, mandatory AI declaration, topic-tag rules, no originality declaration), the hard gates win — skip the event or join only the non-clashing part, leaving a trace; only official events inside the activity center count — never invent one.

## When there's no topic: fallback

When the total cap is reached and still no candidate passes the fact, sensitive, and audience-connection gates together, don't stop posting, and don't force an unqualified one. Fall back to the round's heat ranking: rank the swept topics by heat, highest first, and take the top one that passes the sensitive list and fact-checking. Freshness may widen per the table for fallback, but the sensitive and fact gates never widen. The settled proof must mark it "fallback topic" and state its heat rank and signal.
