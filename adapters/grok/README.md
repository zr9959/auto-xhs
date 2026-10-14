# Grok 这条路怎么走

先把丑话说前面：Grok 的多 agent、定时、浏览器这些能力，这份文档写的时候没逐项实测过。下面写的是「按这个思路接」，不是「保证能跑成这样」。接的时候自己先小跑一轮验一下，跑不通的地方按降级路走。

## 装法

1. 把仓库放进 Grok 的工作区或项目里。
2. 把 `AGENTS.md` 放到项目根目录，或者按你用的 Grok 产品的要求放。里面写了读取顺序和干法入口。
3. 按根目录的设置向导填好配置。
4. 小红书登录你本人扫码。先主站，再从主站入口进创作者平台。

## 一轮怎么跑

流程和另外两家一样：读 `core/CONSTITUTION.md`，按阶段读 `core/stages/`，总管协议看 `orchestration/orchestrator.md`。

分两种情况：

- 你的 Grok 能派子 agent：照总管模式来，串行派单，一个验过再派下一个。
- 不能，或者派起来不稳：一个 agent 从头顺着做。选题做完落盘，再写稿，再做片，再自验。每一步的产出和证据清单照样落盘，标准不降。就是慢一点，也没人替总管把关，验收单要自己对着逐项勾。

## 定时怎么做

- 产品自带定时就用自带的，五件事的目的和边界在 `orchestration/scheduling/README.md` 里，照着建。
- 没有自带定时：用系统 cron 到点拉起一次会话，模板在 `orchestration/scheduling/cron-system.example`。
- cron 也用不上：手动喊开工。看门狗省掉，自己多看一眼台账。清单在 `orchestration/scheduling/manual-checklist.md`。

## 发布怎么做

- 有可用的浏览器能力，并且登录态在：可以试全自动。先拿一条不重要的内容试，话题点蓝和 AI 声明这两关亲眼看一遍再放行日常用。
- 没有：半自动。备好待发包，你人工发。

## 待发包（半自动时用）

固定四个文件，和另外两家同一份格式：

- `video.mp4`：验收通过的成片
- `cover.jpg`：单独做的封面
- `post.md`：标题、正文、话题、第一条评论
- `publish-checklist.md`：照着勾的发布清单，模板在 `orchestration/publish-checklist.template.md`
