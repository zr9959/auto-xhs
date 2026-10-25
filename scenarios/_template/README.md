[中文](README.zh-CN.md) | English

# Scenario name (replace this line with your scenario's name)

This is the scenario's main description. People picking a scenario read this one first — fill in the sections below as written, and don't delete sections.

## What this scenario does

Fill in: one sentence saying what goes out every day. For example, "a daily local vegetable price report" or "a daily one-minute English listening clip".

## Who it is for

Fill in: who watches it, in what situation, and what they get from it. The more specific, the better — the script angle later depends on this paragraph.

## What time it goes out

Fill in: what time work starts, by what time it must go out, and why that time. For example, weather has to beat people's morning commute, vegetable prices have to beat the grocery run.

## Where the data comes from

Fill in: exactly which site, which API each source comes from — one source per line. Write the full URLs.
Hard rule: only data that is free to get. Anything needing sign-up, payment, or someone else's account must not go in.

## What can go wrong

Fill in: what this scenario tends to get wrong, and what happens when it does. For example, data may run late, one claim may touch a sensitive line, or the platform may watch this kind of content closely. Write down everything you can think of, plus one line on how you plan to guard against each.

## Which level to suggest

Fill in: full-auto, semi-auto, or manual — which one you recommend, and why. New scenarios usually start semi-auto, with a person looking before publishing.

## Where the files are

- `scenario.yaml`: the scenario's ID card — its fields are fixed, fill them in as written.
- `config.example.yaml`: the extra config this scenario needs. General config lives in the repo root's `config.yaml` — this file only holds what this scenario adds.
- `stages-diff.md`: where it differs from the general rules. If nothing differs, write "none".
- `scene-notes.md`: how the visuals are made — how many segments, what goes in each, where the template file sits.
- `sources.md` (add it if you need it): how the data is fetched, written out step by step.
