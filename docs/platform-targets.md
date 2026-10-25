[中文](platform-targets.zh-CN.md) | English

# Which platform to publish to: the content-platform dimension

First, keep two dimensions apart — don't mix them:

- `adapters/` covers **which AI assistant does the work**: Muse, Dots, Grok Bot. The difference is who presses the buttons.
- This file covers **which content platform it publishes to**: right now, only Xiaohongshu. The difference is where it goes and which rules of that platform apply.

The two dimensions combine freely: one assistant can publish to different platforms, and one platform can take different assistants. What connects them is still file conventions, explained below.

## Two packs: material pack and ready-to-post pack

The finished video-making output is first a **material pack**. It carries no platform flavor:

```
Material pack/
├── video.mp4    Master video. Vertical, high-definition — every platform works from it later
├── post.md      Script source: voiceover script, key points, topic candidates, data sources — all here
└── cover.jpg    Master cover
```

To publish to a platform, take the material pack and adapt one **ready-to-post pack** per that platform's rules. One per platform, no interference between them:

- Rewrite the title to that platform's length habits.
- Handle topics that platform's way.
- Redo the cover at that platform's ratio — the master cover may not fit.
- Pick declarations and follow steps by that platform's checklist.

That way, one piece of material publishes to several platforms: topic picking, script writing, and video making happen once, and each platform only adds one step — "adapt a ready-to-post pack by its rules, then publish". No need to redo the whole chain per platform.

## To add a new platform, hand in five things

To have this system publish to one more platform, prepare the five things below and put them in a platform guide, formatted like this file:

1. **Login method**: how to log in to this platform. The rule matches Xiaohongshu's: only the account owner scans the QR code themselves — nobody touches anyone else's password or verification code. Write clearly how to confirm the login worked.
2. **Publish step checklist**: from opening the platform to pressing publish, step by step, in the style of `orchestration/publish-checklist.template.md`, each item tickable. Mark which steps are gates (no pass, no publish).
3. **Platform rules and red lines**: what this platform checks and bans. For example, whether content declarations must be picked, how diversion counts, and any special requirements for this kind of content. Only write what has a source. What you haven't verified, write as "unverified" — no guessing.
4. **Copy differences**: compared with Xiaohongshu, which parts of the copy change. For example, title length, whether topics are added, whether the first comment still goes out, what wording the body must not use. Only write the differences — don't copy what is the same.
5. **One filled-in ready-to-post pack example**: take one piece of material that really ran (made-up content is fine), adapt it into a ready-to-post pack by this platform's rules, all four pieces complete, so later readers can check the format against it.

With all five ready, add one line for the platform in this file's platform list, and the platform counts as connected.

## Platform list

| Platform | Status | Where it is explained |
|---|---|---|
| Xiaohongshu | In use | Publish rules in `core/stages/04-publish.md`, ready-to-post checklist in `orchestration/publish-checklist.template.md` |
| Douyin / TikTok | In use | `platforms/douyin/` (guide + runnable scripts) |

## Douyin / TikTok (in use — see the module)

State this clearly first: **the Douyin / TikTok module is built now — see `platforms/douyin/` (guide + runnable scripts: download, subtitle burn-in, outro join, sensitivity scan).** What follows is how the same material gets reused. The five things above now live in the module itself, kept here so a new port can follow the same shape. For TikTok: same pipeline, pick the outlet first (see the module); the sensitivity gates in the module are written for Douyin.

Roughly how the same material gets reused:

- The master video is vertical high-definition, and Douyin also pushes vertical 1080×1920 first — the same vertical material fits it directly as the source, no need to remake the video. Horizontal 1920×1080 also publishes on Douyin, but in the feed it gets black bars top and bottom and takes up less screen — unless the content is screen recording or tutorials, don't use horizontal.
- Copy must change to Douyin's habits: title, topics, and first-comment practices all differ from Xiaohongshu's — and that is exactly what item 4 of the five things must spell out.
- The five things above now live in the module: Douyin's login method (browser creator center), publish step checklist, platform rules and red lines (four sensitivity gates), copy differences, and runnable scripts. TikTok's own community rules are not a separate gate yet.

One more thing when adding it: this library only takes the route of operating like a person inside a browser, never any unofficial interface. If some Douyin step can only be done through an unofficial interface, write honestly in the platform guide: "this step can't be done — semi-auto only". Don't route around it.

New ports follow the same rule: hand in the five things, then add the platform's line to the list above.
