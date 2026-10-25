[中文](CONTRIBUTING.zh-CN.md) | English

# How to add things to this repo

This repo welcomes new scenario packs, and new platforms too. Not many rules — read this page first before starting, and you'll avoid a lot of wrong turns.

First, what the interface is: this repo's interface is **file conventions**, not a server, and no plugin to install. AI assistants work by reading files, so scenarios and platforms hand off to each other through fixed-format files. Anything you add, as long as its file format matches, works for existing users as soon as they update the repo to the newest version — nothing new to install.

## Add a scenario pack

1. **Search first.** Search the repo's issues for whether someone is already building this scenario, or has already asked for it. If someone's on it, don't build a duplicate — go help them.
2. **Copy the empty template.** Copy the whole `scenarios/_template/` folder, rename it to your scenario's name (lowercase English plus hyphens), and put it in `scenarios/`.
3. **Fill it in as directed.** Every file in the template states what goes in it. Three things matter most: where the data comes from (full URLs), where it differs from the general rules (only the differences — never copy the parts that are the same), and how the picture gets made.
4. **Self-check.** The checklist below, item by item — all passing before you submit.
5. **Add one line when submitting.** Add one line for your scenario to the scenario list table in `scenarios/README.md`: name, what it's for, who made it, recommended level, where the data comes from, which versions it works with. Without that line, nobody finds yours — work for nothing.

## Pre-submit self-check list

- [ ] Only free data sources. Anything needing money or a paid account is not accepted.
- [ ] No real accounts, keys, or personal information brought in. Names, cities, and products in examples are either made up or public data.
- [ ] Plain words throughout. Docs, comments, and submit notes alike: short sentences, everyday words, no stock phrases.
- [ ] The sample checks itself: run `core/validate.py` once, or state clearly in the scenario notes why this scenario can't run the general acceptance (for example, picture specs differing from the general ones). Stated clearly, it's fine; unstated, it's not.
- [ ] `scenario.yaml` fields unchanged, values all filled in for real. `works_with` lists versions you truly tested — never write versions you didn't test.
- [ ] The general rules were not copied into your scenario. Your pack keeps only what's special to your scenario.

## Asking for a scenario

Want a scenario you can't build yourself? Open an issue and ask. Search first; only open when the search finds nothing. When opening, state two things clearly:

- What the scenario is for, and who it's for.
- Where the data comes from — write down the free sources you know. When you don't know, write that you don't know — never invent.

Someone who picks it up will say so in the issue. Once it's built and merged, the list gains a line, and the asker can use it right away.

## Before changing a general rule, think about one thing first

Before starting, sort out: is the rule you want to change one that affects all scenarios, or only yours?

- **Only yours**: write it in your own `stages-diff.md`, don't touch `core/`. For example, the weather forecast skipping category rotation is that one scenario's business — it belongs in its own pack.
- **Affects all scenarios**: only then change `core/`. When changing, state clearly in the submit: why it changed, which scenarios change with it, and which ones you tested. Numbers change only in the constitution page's numbers table and the matching key in `config.yaml` — both together, never only one side.

When unsure which kind it is, open an issue and ask first — other people's stepped-in pitfalls can save you a lot of trouble.
