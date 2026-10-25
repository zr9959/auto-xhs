[中文](README.zh-CN.md) | English

# Scenario list

A "scenario" is one use of this system. Same engine, different scenario, different output.

The engine is general: search for material, write scripts, make web-page videos, publish, follow up — that chain lives in `core/`, `pipeline/`, and `orchestration/`. A scenario only handles one thing: spelling out what is specific to that use — where the data comes from, how the script changes, how the visuals are made, and where it differs from the general rules.

One scenario, one folder, all in the same format. Fill it in from `scenarios/_template/`.

## List

| Scenario | What it is for | Made by | Suggested level | Where the data comes from | Works with |
|---|---|---|---|---|---|
| Tech news | One tech news or tutorial short video a day — the set this repo ships with | Official example | Semi-auto to start | Tech media, official updates, hot community posts | core v0.1 |
| [Weather forecast](weather-forecast/) | One city's weather a day: today's overview, the next seven days, going-out advice | Official example | Semi-auto | Open-Meteo, free, no sign-up | core v0.1 |

The full tech news example is in [examples/example-issue/](../examples/example-issue/) — topic to acceptance checklist, the complete set. Follow it and you'll see what every step produces.

When you add a scenario, add one row to this table when you submit it, or nobody will find yours. How to add one is in [CONTRIBUTING.md](../CONTRIBUTING.md).

## How to pick a scenario

- First check "What it is for" against the direction you want. If it matches, read that whole folder, focusing on its own README and config example.
- Then check "Suggested level". A scenario marked semi-auto means either its data goes wrong easily, or the platform watches that kind of content closely — run it semi-auto until it's steady, don't switch it to full-auto on day one.
- Finally check "Where the data comes from". Scenarios that need paid data or a paid registered account don't get into this library. Everything you can see in the list is free to get.

## How returning users find new scenarios

This library keeps growing: new scenarios, new platforms, all get added. When you come back looking for something new, go in this order:

1. **Read this table.** A new scenario coming in must add a row to the table. If it's not in the table, it doesn't exist yet.
2. **Read the changelog at the repo root (CHANGELOG).** Every release writes what changed and what scenarios were added, in plain words. Get into the habit: when you come back, read the changelog first, then the list.
3. **Watch this repo on GitHub.** After you click Watch, you'll get a notification when a new version ships — no need to check every day yourself.

Usage doesn't change: update the repo to the latest version, pick a scenario, fill in the config item by item from its README, and hand the rest to your AI assistant. The interfaces are all file conventions — nothing new to install.

## Want to add a scenario

First search the repo's issues for anyone already building it, or anyone who already asked for it. If nobody has, follow [CONTRIBUTING.md](../CONTRIBUTING.md): copy the blank template, fill it in, check it yourself, and add one row to the table above when you submit.
