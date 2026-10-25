[中文](README.zh-CN.md) | English

# YouTube module: English channel operation

For a US audience, all in English. Topics are rethought around what US viewers care about — money, subscriptions, accounts, privacy, devices, services — not translated from Chinese scripts.

## Three standards (all three must pass)

1. **Why does this matter to me**: open on the viewer's money, account, device, or a service they use.
2. **Plain words**: short, everyday sentences; explain any term in the same sentence.
3. **Real interfaces and concrete details**: real screenshots, concrete numbers, concrete steps — no empty concept talk.

## Titles and thumbnails

- **Titles**: conflict up front, concrete numbers, suspense without clickbait; title and thumbnail complement each other, never repeat the same sentence.
- **Thumbnails**: few big words, strong contrast, a conflict scene readable at a glance; people, scenes, and objects must be there — a thumbnail can't be just big text.
- Production decisions like titles, thumbnails, and scripts are settled from the knowledge base and executed — not brought back one by one for approval. Only account-verification steps that need the owner go back to a person.

## Retention and pacing

- **First 5 seconds act out the title's conflict**: no self-introduction first, no background first — play the conflict from the title straight away.
- **Main body in plain words + viral pacing**: one turn every 20–30 seconds; every key point gets a strong visual, lit up one by one.
- **The picture must have something in it**: every video needs rich visuals tied to the content (people, scenes, objects) — no big-text screens carrying the whole video. An official picture counts as one qualifying element, but on its own it's not enough.

## Production standards

- **Voice roles for acted parts**: different characters get different voices; the narrator keeps one fixed voice.
- **No repeats, keep it moving**: no single composition runs longer than 15 seconds; picture elements must really move (blinking, lip sync, limbs, movement) — not a whole image sliding around to fake it.
- **People extraction**: a person is one whole source image — never cut the head out separately. Only eyes, mouth, arms, and legs may move, taken as patches from that same source. If the source head-neck is broken, regenerate the person — no cutting the head to patch it.
- **Text style**: on-video text uses a cream-paper background with dark text, no flashy backgrounds.
- **Production log**: every episode logs start, end, and time per stage; a long video must be finished two nights before its publish date, leaving one night of buffer.

## Visual style

One paper-craft illustration style across the channel: color board, prompt prefix, and guardrails are in `core/paper-style.md` (the Xiaohongshu appendix — same source shared by both sides, not written twice). Real interfaces still use real screenshots, recomposed inside the style. When the style rules change, both sides check against each other.

## Shorts playbook

Long-video recaps, standalone mini-topics, and long-video teasers, combined on a schedule. Shorts are not the long video's leftovers: a standalone mini-topic gets its opening and ending rewritten to Shorts pacing.

## Publish schedule (example — change it to your audience's timezone)

- Long videos 2 a week (example: Sunday morning, Tuesday afternoon, US Eastern).
- Shorts 5 a week: Monday long-video recap, Wednesday long-video recap, Thursday standalone mini-topic, Friday standalone mini-topic, Saturday long-video teaser.

## SEO and discovery

Titles, descriptions, tags, playlists, end screens, and cards all get done. Descriptions carry timestamp chapters; playlists split by topic; end screens and cards are things the API doesn't cover, so they go through the browser.

## API first

Upload, scheduling, thumbnails, subtitles, playlists, comments, and data all go through the official API first. The browser only handles what the API doesn't have (end screens, cards, premiere settings, copyright appeals, Shorts related videos).

## Monetization and policy notes

- Originality: reposts, repeated content, and low-quality AI stitching fail monetization review.
- Label AI content as the platform requires; no AI visuals involving real people or real events.
- **Pinned comments need advanced feature verification** (video selfie, ID, or channel history — pick one): without it, leave the comment unpinned and don't force it. Later episodes hit the same gate — wait until the owner decides when to verify.
- Account abilities like phone verification and custom thumbnails should be done early, once and for all.

## Data review

Once a week: impressions, click-through rate, retention curve, completion, subscriber sources. Log top / bottom 3, and write review conclusions back into the module. When no trustworthy free data tool exists, calculate it yourself from the official API.

## Runnable code (`scripts/check_upload.py`)

Check an upload package before uploading. FAIL items must be fixed.

```bash
# The package directory holds: title.txt, description.txt, thumbnail.jpg/png, video.mp4, tags.txt (optional)
python3 scripts/check_upload.py --dir <package directory>
```

Checks: title missing or over 100 characters (FAIL), over 70 characters (WARN, display truncates); thumbnail missing or not 1280×720 (FAIL); video missing or undecodable (FAIL); description missing (WARN); chapters not starting at 0:00 (FAIL); tags over 500 characters total (WARN).

Test record (2026-10-25): good package 0 FAIL 0 WARN; bad package (160-character title + 640×360 thumbnail + chapters starting at 2:00) 3 FAIL, exit code 1.

Uploading itself has no separate script: use the official API route in the "API first" section above (needs your own OAuth credentials — the repo carries no credential examples).
