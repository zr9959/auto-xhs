[中文](README.zh-CN.md) | English

# More platforms

Xiaohongshu is still this repo's default, complete pipeline (see `core/`). This directory holds modules for other platforms: one guide per platform, enable only the ones you need, they don't interfere with each other.

| Platform | Module | Maturity |
|---|---|---|
| Douyin / TikTok | `douyin/` | Guide + runnable scripts: pick the outlet first (Douyin or TikTok), then pick, download, subtitle, voiceover, cover, title, four sensitivity gates, publish; `scripts/` has subtitle burn-in, outro join, sensitivity scan, download wrapper |
| X | `x/` | Guide + check script: five-stage warming, human-like writing, cold-start rules, image rule; `scripts/check_post.py` checks a post before you send it (posting itself is not automated — see the module's risk disclosure) |
| YouTube | `youtube/` | Playbook + check script: titles, thumbnails, retention, Shorts, SEO, production standards, API-first workflow; `scripts/check_upload.py` checks an upload package (uploading itself goes through the API, no separate script) |
| WeChat Official Accounts | `wechat-mp/` | Draft scripts + manual final publish: `scripts/build_draft.py` builds a draft package, `scripts/mp_api.py` probes and creates drafts; personal uncertified accounts cannot publish via API, content playbook still to come |

## Shared notes

- **Each module stands alone.** Enable one platform, read that module; accounts, topic pools, and data tables are separate per platform, never shared.
- **Risks stated, no guarantees.** Each module opens with that platform's real limits (X checks for non-human operation, WeChat personal accounts cannot publish, Douyin's repost copyright call is the platform's). Read the limits before you decide.
- **Semi-auto first, then full-auto.** New account, new platform: run semi-auto for a week or two first — look at the video, title, and cover yourself — then consider full-auto.
- **Plain words.** Every module's docs, comments, and commit messages use short, plain sentences, no AI-flavored explanations.
- **Contributing.** To add a platform or a use, follow the five-piece format in `scenarios/_template/`, or add a section to the matching module and state what you tested.

Note: the scripts print their messages in English now, and the Xiaohongshu core guides (`core/`, `adapters/`, `docs/`) are in English too — every file has its Chinese version linked at the top.
