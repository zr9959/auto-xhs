# 三家适配：先看这页再选

小红书全自动化运营发布（适配muse、Chatgpt dots、Grok bots）

规矩只有一份，在 `core/`。三家适配不改规矩，只解决三件事：这家怎么读到规矩、这家缺的能力怎么补、定时怎么做。

先说结论，三家体验不一样，别当成一样：

- **想全自动，选 Muse。** 子 agent 分工、定时、浏览器发布，这条路全有，而且已经有账号在用它日更，跑通了。
- **在用 ChatGPT，就走半自动。** 选题、写稿、做片、验收它都能干，最后发布这一步它备好待发包，你自己点。没有等价的常驻定时，也没有稳定的子 agent 编排。
- **在用 Grok，走 AGENTS.md。** 规矩照读，流程照走。它的多 agent 和定时能力以你用的时候的产品为准，这份文档写的时候没实测过。弱的地方按单 agent 顺序执行降级，不丢规矩，只丢速度。

## 简表

详表在 `docs/capability-matrix.md`，口径一样，这里是简版。

| 能力 | Muse | ChatGPT | Grok |
|---|---|---|---|
| 读规矩、选题、写稿 | 能 | 能 | 能 |
| 做片（网页做片在本机跑） | 能 | 能，多半要你在本机配合跑脚本 | 有本地执行环境就能 |
| 子 agent 编排 | 能，串行派单是原生路子 | 没有稳定的，单 agent 顺着做 | 看产品，未验证；弱了就单 agent 顺着做 |
| 定时 | 能，五件事都能建 | 没有常驻定时，手动喊 | 未验证；没有就用系统 cron 拉起或手动 |
| 浏览器自动发布 | 有浏览器能力时能 | 半自动：备待发包，人工发 | 看浏览器能力，没有就半自动 |
| 发后跟进 | 能自动盯 2 小时 | 手动去看，或把评论贴回来拟回复 | 手动或 cron 拉起 |
| 周复盘 | 能定时自动 | 手动喊一次 | 手动或 cron 拉起 |

## 各家入口

- Muse：`claude/README.md`，再用 `claude/skill/SKILL.md`。
- ChatGPT：`chatgpt/README.md`，项目指令粘贴稿在 `chatgpt/project-instructions.md`。
- Grok：`grok/README.md`，指令文件是 `grok/AGENTS.md`。

## 不管选哪家，这三样都一样

- 规矩：同一份 `core/`。
- 验收：同一个 `core/validate.py`，同一套过闸标准。
- 待发包：同一种格式——`video.mp4`、`cover.jpg`、`post.md`、`publish-checklist.md`。模板在 `orchestration/publish-checklist.template.md`。

差的只是最后谁来按发布按钮。前面备得好不好，三家一个标准。
