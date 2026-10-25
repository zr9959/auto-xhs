中文 | [English](README.md)

# Grok Bot 这条路怎么走

先说清 Grok Bot 是什么：它是 xAI 的云端 agent，2026 年 8 月起还是 beta。agent 跑在一台云端虚拟机上，能自己多步操作软件，带 200 多个插件。一个账号一台虚拟机，你名下几个 bot 共用这一台，登录态也是共用的。

它不是只能聊天的机器人，它有自己的电脑。但有一条对这套系统最要紧：**发布、发送、购买、删除这类动作，它默认先暂停，等你批准了才干。** 设置里有个 Always Allow，打开了才不问、直接干。

开放范围：目前只开放给部分 SuperGrok Heavy 用户。再加一句实话：我们没实测过它跑这套系统，下面是按官方口径写的接法。接的时候自己先小跑一轮验一下，跑不通的地方按降级路走。

## 装法

1. 把仓库放进 Grok Bot 的工作区。
2. 把 `AGENTS.md` 给它当项目说明（就是本目录这份），里面写了读取顺序和干法入口。
3. 按根目录的设置向导填好配置。
4. 小红书登录：在它的云端虚拟机浏览器里打开小红书主站，你本人扫码。注意登录态在虚拟机上、几个 bot 共用，别在别的 bot 里乱动这个号。

## 一轮怎么跑

流程和另外两家一样：读 `core/CONSTITUTION.md`，按阶段读 `core/stages/`，总管协议看 `orchestration/orchestrator.zh-CN.md`。

它能派子 agent，照总管模式来：串行派单，一个验过再派下一个。每一步的产出和证据清单照样落盘。想省事的话，一个 agent 从头顺着做也行，标准不降，就是慢一点，验收单要自己对着逐项勾。

## 定时怎么做

Grok Bot 自带定时。照着五个任务的目的各建一个：日更、早看门狗、晚看门狗、发后跟进、周复盘，边界看 `orchestration/scheduling/README.zh-CN.md`。

系统 cron 拉起和手动喊开工也留了模板，定时入口想换着用的可以看：cron 模板在 `orchestration/scheduling/cron-system.example.zh-CN`，手动清单在 `orchestration/scheduling/manual-checklist.zh-CN.md`。

## 发布怎么做（这家最不一样的一步）

- **默认就是一道半自动闸口**：它把前面的活干完、待发包备好，真到发布那一下会停住等你批准。你看过包再放行。这跟这套系统推荐的「新号先半自动」正好是一回事，不用你另设。
- **想全自动**：把发布这类动作的 Always Allow 打开，它就不再问了。打开之前先想清风险，看 `docs/compliance.zh-CN.md`。删除这类动作别开 Always Allow。
- 不管问不问，闸口标准不变：先在主站确认登录态、从主站入口进创作者平台；话题没全点蓝、AI 声明没选，任何一条不过，不许发。

## 待发包

固定四个文件，和另外两家同一份格式：

- `video.mp4`：验收通过的成片
- `cover.jpg`：单独做的封面
- `post.md`：标题、正文、话题、AI 内容声明、第一条评论
- `publish-checklist.md`：照着勾的发布清单，模板在 `orchestration/publish-checklist.template.zh-CN.md`
