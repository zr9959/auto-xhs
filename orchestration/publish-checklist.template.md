[中文](publish-checklist.template.zh-CN.md) | English

# Ready-to-post pack and publish checklist

When publishing fails a gate, or when the mode is semi-auto, the finished video doesn't go out directly. Instead it gets packed into a "ready-to-post pack" for a person to send.

## What is in the ready-to-post pack

Four fixed files. All three assistants use this same pack — no separate versions:

```
Ready-to-post pack/
├── video.mp4              The accepted final video
├── cover.jpg              The separately made cover image
├── post.md                Title, body, topic list, AI content declaration, first comment — all inside
└── publish-checklist.md   This checklist, copied in
```

video.mp4 must be the accepted file. If the file was swapped or re-rendered, the old acceptance is void — it must pass acceptance again before entering the pack.

post.md always has a "发布设置" (publish settings) section, in which the "AI 内容声明" (AI content declaration) line is always present, filled in at script-writing time in a fixed wording: at publish time, pick the "笔记含 AI 合成内容" (post contains AI-generated content) category. This line must not be missing — publishing requires it, and remembering it on the spot is easy to miss. A miss means rework. The publisher picks by this line, without judging for themselves.

## Publish checklist (tick through item by item when sending)

```
- [ ] Open the Xiaohongshu main site, widen the window, confirm logged-in state
- [ ] Enter the creator platform from the entry inside the main site (don't judge by opening the creator platform's URL directly)
- [ ] Upload video.mp4, confirming the uploaded file is this one from the ready-to-post pack
- [ ] Set the cover by uploading cover.jpg, don't use the video's first frame
- [ ] Copy title and body from post.md, don't type by hand — hand typing makes mistakes
- [ ] Add topics one by one: type # , wait for the candidate list to pop up, tap the official topic, watch it turn blue on the spot, then add the next one
- [ ] Count once: blue topic count = planned topic count in post.md. On a mismatch, stop, don't publish
- [ ] Pick the content declaration by the "AI 内容声明" line in post.md's "发布设置" section (usually the "笔记含 AI 合成内容" category; the page's actual wording at the time wins). No need to tick the originality declaration
- [ ] No location, no promotion tools. For scheduled publishing, first open scheduling in "高级选项" (advanced options), set the time, then press publish; after setting, read the time back once in post management before logging it
- [ ] Press publish
- [ ] Open the just-published post and look it over: topics clickable, video plays, cover is the right one
- [ ] Post the first comment with the text from post.md
- [ ] Fill the post link and actual publish time back into the topic ledger
```

## What to do when a step won't pass

- Topics won't turn blue: stop. Don't delete topics and publish bare, and don't pad with plain-text topics. Keep the pack, and report in four elements (which topic got stuck, what the page looked like, how many tries, how it was handled).
- Main site confirms not logged in: stop. Publishing needs the account owner to scan the QR code personally — nobody can do it for them.
- Page won't open, or errors: go back to the main site and enter through a different on-site entry. At most 2 tries. Still failing means stop, keep the pack, and write down the page's original wording.

Four-element wording: see `orchestrator.md`.
