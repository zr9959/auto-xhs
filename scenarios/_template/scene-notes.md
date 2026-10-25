[中文](scene-notes.zh-CN.md) | English

# How the visuals are made

This file spells out this scenario's video visuals. The person (or AI assistant) making the video lays out every episode from it.

## How many segments, what goes in each

Write it segment by segment. Like this:

- **Segment 1 (opening)**: what goes in. One hook sentence to hold the viewer first, carrying the episode's most important piece of information.
- **Segment 2 (body)**: what goes in. The data items one by one, numbers done with the motion library's number rollup — don't stack a whole screen of text.
- **Last segment (close)**: what goes in. One piece of advice or one question, plus the fixed closing line.

For each segment, also write two things: roughly how many words its voiceover runs, and which numbers appear on screen (those numbers must match the script).

## Where the template file sits

Fill in: where this scenario's scene template file lives. For example, right in this folder, called `scene.html`; or adapted from the general template in `pipeline/templates/`.
Say clearly which one. Whoever makes the video needs to find it directly.

## Where it differs from the general video rules

Write it if there is one, otherwise write "none". Common cases: this scenario doesn't use real product pictures, its visuals are all data cards; or its cover is a fixed layout, only the date and numbers change.
Subtitle position, silence acceptance, and the other hard rules must not be changed here — those live in `core/` and apply to every scenario.
