---
name: auto-xhs
description: "用这套流程运营一个小红书号：选题、写稿、网页做片、发布、发后跟进、周复盘。用户说到小红书日更、发小红书、自动运营、复盘时用。"
---

# auto-xhs 入口

这份文件只是个入口，不存规矩。规矩只在仓库的 `core/` 里存一份，别在这里另写一套。

## 读取顺序

1. 先读 `core/CONSTITUTION.md`。总管每轮只读这一份开工。
2. 干到哪个阶段，读 `core/stages/` 里对应的那一份。不要一次全读。
3. 选题和发布两个阶段，按手册要求另读敏感词附册。

## 怎么干

- 编排看 `orchestration/orchestrator.md`：总管只派单、验收、汇报，阶段活派给子 agent，一个一个来，验过才派下一个。
- 派单照 `orchestration/dispatch-templates.md` 写。
- 定时照 `orchestration/scheduling/` 里 Muse 那份模板建。
- 做片走 `pipeline/`，动效用 `motion-lib/`。
- 配置从仓库的配置文件读。品类、信源、时刻、路径都以配置为准，不要把数字写死在这份文件里。
