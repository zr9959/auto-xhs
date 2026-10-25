[中文](README.zh-CN.md) | English

# How to read this example

This is one complete daily example, from topic picking to the acceptance checklist, the full set.

First, the honest part: it's all made up. The product "禾苗笔记" (Hemao Notes) doesn't exist, and the prices, sources, and heat signals are all invented — the numbers only need to line up with each other. Learn the format from it; don't take the content as real.

## Files

- `post.md`: the episode's full copy set. Topic evidence, 3 title versions, the final title, the body text, topics, the first comment, the material list, publish settings, and the acceptance checklist are all in there.
- `scripts.txt`: the voiceover script, split by segment. The format is `name|text`, one segment per line. This one runs 570 words in total, inside the recommended 480–650 range.

## Which guide each step maps to

| Part in the example | Matching rule |
|---|---|
| Topic evidence | The topic-picking guide in `core/stages/`: a settled topic needs six items on record — one missing and it doesn't count as settled |
| Three title versions, body text, topics, first comment | The script-writing guide in `core/stages/` |
| Material list | The video-making guide in `core/stages/`: any product mentioned needs its real interface on screen |
| Acceptance checklist | The video-making guide's checklist in `core/stages/`, plus the orchestrator running `core/validate.py` |
| Publish settings, topic taps turning blue | The publishing guide in `core/stages/` |

## How to make your own first episode

1. Copy this directory, rename it, and use it as a template.
2. Replace `post.md` section by section with your own content — don't delete the section headings. The acceptance script reads the structure from those headings.
3. Replace `scripts.txt` with your own voiceover script. Segment names can change, but the `name|text` format must not.
4. When it's done, run `core/validate.py` once and fix things against its output until no FAIL is left.
