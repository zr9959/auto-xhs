# 三家适配：先看这页再选

小红书全自动化运营发布（适配muse、Dots、Grok Bot）

规矩只有一份，在 `core/`。三家适配不改规矩，只解决三件事：这家怎么读到规矩、这家的批准规则怎么配、定时怎么做。

先纠正一个老误会：三家都是云端 agent，各有自己的一台云端电脑和浏览器。差别不在「有没有云端」，在三处：动手前的批准规则松紧、开放给谁用、我们实测没实测。

- **想直接照着跑通，选 Muse。** 子 agent 分工、定时、浏览器发布都有，而且已经有账号在用它日更，实测全通。
- **在用 Dots，就按 Muse 的接法接。** Dots 是 OpenAI 2026 年 9 月发布的单独产品，不是 ChatGPT 聊天本身。每个 Dot 有专属云端电脑和浏览器，能定时、能派子 agent。发布先问还是直接放行，是你在它的自定义规则里定的：设成先问就是半自动，设成放行就是全自动。要 ChatGPT Pro 或 Business Premium 才能用。我们没账号，没实测过。
- **在用 Grok Bot，看它的暂停规则。** Grok Bot 是 xAI 的云端 agent，还在 beta。agent 跑在云端虚拟机上，但发布、发送、购买、删除前默认先暂停等你批准，天然是一道半自动闸口；设置里的 Always Allow 打开才全自动放行。目前只开放给部分 SuperGrok Heavy 用户。同样没实测过。

## 简表

详表在 `docs/capability-matrix.md`。Muse 那一列是实测过的；Dots、Grok Bot 两列按官方口径写，未实测。

| 能力 | Muse | Dots | Grok Bot |
|---|---|---|---|
| 读规矩、选题、写稿 | 能 | 能 | 能 |
| 做片（网页做片流水线） | 能，脚本在本机跑 | 能，在它自己的云端电脑里跑 | 能，在云端虚拟机里跑 |
| 子 agent 编排 | 能，串行派单是原生路子 | 能 | 能 |
| 定时 | 能，五件事都能建 | 能，自带定时跑 | 能，自带定时跑 |
| 浏览器自动发布 | 能 | 能；先问还是放行，看你定的规则 | 能；先问还是放行看你怎么设，发布前默认先暂停等批准，开 Always Allow 就放行 |
| 发后跟进 | 能，自动盯 2 小时 | 能，靠定时 | 能，靠定时 |
| 周复盘 | 能，定时自动 | 能，靠定时 | 能，靠定时 |

## 各家入口

- Muse：`claude/README.md`，再用 `claude/skill/SKILL.md`。
- Dots：`dots/README.md`，总指令在 `dots/dots-instructions.md`。
- Grok Bot：`grok/README.md`，指令文件是 `grok/AGENTS.md`。

## 不管选哪家，这三样都一样

- 规矩：同一份 `core/`。
- 验收：同一个 `core/validate.py`，同一套过闸标准。
- 待发包：同一种格式——`video.mp4`、`cover.jpg`、`post.md`、`publish-checklist.md`。模板在 `orchestration/publish-checklist.template.md`。

差的只是发布那一下先问谁、以及你现在能不能用上。前面备得好不好，三家一个标准。
