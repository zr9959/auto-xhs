中文 | [English](AGENTS.md)

# 给 Grok 的项目说明

你在帮用户运营一个小红书号，用的是 auto-xhs 这套流程。规矩不在这份文件里，规矩只在仓库的 `core/` 里存一份。你照着下面的顺序读，照着干。

说明一句：这份文件按流程写的。你的多 agent、定时、浏览器能力都有，下面写的就是正路；个别地方留了备选写法，用不上就不用管。

## 读取顺序

1. 先读 `core/CONSTITUTION.md`。
2. 干到哪个阶段，读 `core/stages/` 里对应的那一份。不要一次全读完。
3. 选题和发布两个阶段，按手册要求另读敏感词附册。

## 干法

总管协议看 `orchestration/orchestrator.zh-CN.md`，要点是：

- 一个人统筹：开工先做防重复三查，在运行日志里打点。
- 阶段顺序固定：选题、写稿、做片、验收、发布、收尾。
- 能派子 agent 就串行派：同一时刻只干一个阶段，上一阶段的证据清单验过，才开始下一阶段。子 agent 不再往下派。
- 不能派子 agent，就自己按顺序做。每做完一个阶段，把产出落盘，按 `orchestration/orchestrator.zh-CN.md` 里的证据清单格式写好，再做下一个。不要一口气闷头干到底。
- 验收不许跳：跑 `core/validate.py`，逐项对验收单。有 FAIL 就打回重做。
- 派单怎么写，看 `orchestration/dispatch-templates.zh-CN.md`。

## 定时

先看 `orchestration/scheduling/README.zh-CN.md`，用你自带的定时照五件事建。系统 cron 拉起（模板在 `orchestration/scheduling/cron-system.example.zh-CN`）和手动清单（`orchestration/scheduling/manual-checklist.zh-CN.md`）是备选，用不上就不用管。

## 发布

- 有浏览器能力、先在主站确认登录态、能从主站入口进创作者平台，才谈自动发布。
- 话题没全点蓝、AI 声明没选、文件和验收的对不上，任何一条不过，不许发。存待发包，按四要素汇报。
- 没有浏览器能力：备待发包（`video.mp4`、`cover.jpg`、`post.md`、`publish-checklist.md`，模板在 `orchestration/publish-checklist.template.zh-CN.md`），交给用户人工发，发完把链接和时间回填台账。

## 出错

按四要素写：卡在哪个环节哪个对象、页面或工具的原话、试了什么各几次什么结果、最后怎么处置对成品有什么影响。只写「失败」不算数。
