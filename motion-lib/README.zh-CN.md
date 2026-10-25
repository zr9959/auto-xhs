中文 | [English](README.md)

# motion-lib：网页做片的动效库

做片的方法是：一条视频就是一个网页，动画在网页里排好，再一帧一帧截图，最后拼成视频。这个库就是给那个网页用的动效组件，样式在 `motion.css`，动作在 `motion.js`，都挂在 `window.MotionLib` 上。

## 一条硬规矩：所有动效都得能定格

截图时时间线是停住的，一帧一帧跳到某个时刻 t 再截。所以每个效果都只能由 t 算出来：同一个 t 跳多少次，画面都得一模一样。

- 不许用自己跑的时钟（比如 `requestAnimationFrame` 自由跑、`Date.now()`）决定画面。
- 不许用 `Math.random()` 掷骰子。要随机就用 `MotionLib.mulberry32(种子)`，种子定了，结果就定了。
- 星尘、彩带、Lottie 这类画布效果，登记成帧更新器（`addFrameUpdater`）。截图那边每跳一帧会喊 `runFrameUpdaters(t)`，它们按 t 把这一帧重画一遍。

不守这条，截出来的帧会跟时间对不上，成片就会跳、会闪。

## 一条排版规矩：同一块区域，只许一个带延迟的入场

两张卡片落在同一块区域、又各自带不同的入场延迟，动画演到一半就会叠在一起，还可能盖住下面的字。截图是逐帧定格的，叠住的那一帧会原样截进成片，躲不掉。

- 同一块区域里，要么只放一个带入场的元素；要么把几张卡片放进一个布局容器（比如纵向 flex 排好、留好间距），让它们入场前、入场中、停稳后都不重叠。
- 实在要错峰入场，先把每张卡片在每个时刻的位置都想清楚：任何一个时刻都不许重叠，不只是停稳之后不重叠。

## 先备齐第三方库

GSAP 和 lottie-web 的本体不在仓库里，先跑一次：

```bash
bash scripts/fetch-vendor.sh
```

它会把 GSAP 3.15.0、lottie-web 5.13.0、canvas-confetti 1.9.4 下载到 `vendor/`，版本和校验都在脚本里写死了。版本明细看 `vendor/README.md`。

## 网页里怎么引

在页面 `<head>` 里引样式，`</body>` 前按这个顺序引脚本（路径按你的页面放在哪一层自己调）：

```html
<link rel="stylesheet" href="../../motion-lib/motion.css">
<script src="../../motion-lib/vendor/gsap/gsap.min.js"></script>
<script src="../../motion-lib/vendor/gsap/SplitText.min.js"></script>
<script src="../../motion-lib/vendor/gsap/DrawSVGPlugin.min.js"></script>
<script src="../../motion-lib/vendor/lottie.min.js"></script>
<script src="../../motion-lib/motion.js"></script>
```

然后建一条停住的时间线，往上面排组件，最后把截图要用的三个口子留出来：

```js
const ML = window.MotionLib;
ML.usePlugins();                       // 把引了的插件都登记上
const tl = gsap.timeline({ paused: true });
// ……往 tl 上排组件……

window.__renderFrame = function (scene, t) {
  tl.seek(t, false);                   // 第二个参数别改 true，不然数字滚动不刷新
  ML.runFrameUpdaters(t);              // 星尘、彩带、Lottie 跟这一帧一起到位
};
```

现成例子看 `pipeline/templates/scene-template.html`，拿它改最快。

## 组件清单

签名都是 `(tl, 目标, {at, dur, ...})`，`at` 是在时间线上第几秒开始。

| 组件 | 干什么 | 一句用法 |
|---|---|---|
| `splitChars` | 把标题拆成一个字一个元素 | `const chars = ML.splitChars(el)` |
| `titleIn` | 标题逐字进场，flip 翻入 / wave 升起 / blur 变清 | `ML.titleIn(tl, el, {at:.15, mode:"flip"})` |
| `countUp` | 数字从小滚到大，价格、数量都能用 | `ML.countUp(tl, el, {to:899, at:2, prefix:"¥"})` |
| `barGrow` | 横条从左往右长，ratio 是长满的比例 | `ML.barGrow(tl, bar, {at:1, ratio:.65})` |
| `drawPath` | 沿 SVG 路径描线，走势线、对勾都行 | `ML.drawPath(tl, path, {at:1})` |
| `ringSweep` | 圆环扫过百分之几 | `ML.ringSweep(tl, circle, {at:1, pct:.67})` |
| `cardIn` | 卡片从某个方向滑进来，带回弹 | `ML.cardIn(tl, el, {at:0, from:"left"})` |
| `stackConverge` | 几张卡飞过来叠成一摞 | `ML.stackConverge(tl, [a,b,c], finals, {at:1})` |
| `flipCard` | 3D 翻卡，正面翻到背面 | `ML.flipCard(tl, inner, {at:8})` |
| `shine` | 一道光从元素上扫过去 | `ML.shine(tl, el, {at:3})` |
| `underlineDraw` | 下划线描出来，就是 drawPath | `ML.underlineDraw(tl, path, {at:1})` |
| `breathe` | 发光一涨一缩，强调主推项 | `ML.breathe(tl, el, {at:5, repeats:5})` |
| `wipeIn` | 遮罩擦除，画面一点点露出来 | `ML.wipeIn(tl, el, {at:2, dir:"left"})` |
| `circleReveal` | 一个圆涨开，把画面露出来 | `ML.circleReveal(tl, el, {at:2})` |
| `blurCrossfade` | 旧的糊掉淡出，新的同时变清 | `ML.blurCrossfade(tl, oldEl, newEl, {at:4})` |
| `glowDrift` | 光晕在整段里慢慢挪 | `ML.glowDrift(tl, [{el:"#g", dx:120, dy:60}], 总时长)` |
| `starfield` | 满屏小星点，按种子和 t 重画 | `ML.starfield(canvas, {count:110, seed:11})` |
| `confettiBursts` | 到点喷一束彩带，落点只由 t 算 | `ML.confettiBursts(canvas, [{t0:9.5, x:540, y:600, seed:21}])` |
| `mountLottie` | 把 Lottie 动画钉在时间线上 | `ML.mountLottie(el, {path:".../check.json", at:9.5})` |
| `morphTo` | 一条路径变成另一个形状 | `ML.morphTo(tl, path, "M…", {at:0})` |

样式类在 `motion.css` 顶部有一组变量（`--ml-color-a` 主色、`--ml-color-b` 辅色、`--ml-color-c` 点缀色等），换风格先改变量，别到处翻色值。常用的类：`.ml-stage` 舞台、`.ml-glass` 玻璃卡、`.ml-card` 实色卡、`.ml-img-frame` 图片框、`.ml-grad-text` 渐变字、`.ml-topbar` 顶部彩条。字幕走 `.ml-subs` 一套，规矩看下面两节。

Lottie 示例素材在 `vendor/examples/`：`check.json` 是圆环描完打对勾，`sparkles.json` 是几颗四角星轮流闪，都是本项目自己写的，随便用。

## 字幕锚定标准（贴底锚定，CSS 类 `.ml-subs` 一套）

字幕不许浮动，必须**贴底锚定**：行数变化时块只向上生长、底边纹丝不动，文字在块内贴底对齐。

锚点怎么来的（小红书竖版，1080×1920）：在 App 里以观众身份看视频，画面最下面有一块是播放器自己的地盘——作者头像、昵称、标题、声明都叠在那里，这块叫系统信息区。实测它的顶边在画面高度 **84.4%（y=1621）**；字幕底边定在 **80%（y=1536）**，跟它留出 **85px** 的安全间距，这样 1 行、2 行都不会压住头像。位置偏高会跟正文脱节，偏低会撞信息区，只有贴底锚定，每条都一致。

| 项 | 数值 |
|---|---|
| 画布 | 1080×1920 |
| 背景条底边 | **y = 1536**（高度 80%），容器 `bottom: calc(100% - 1536px)` |
| 系统信息区顶边（实测） | y = 1621（84.4%），字幕底边与它留 85px 间距 |
| 字号 / 行高 | 46px / 64px |
| 背景条内边距 | 上下各 16px（左右 28px），圆角 26px |
| 最多行数 | 2 行（长句先在断句处拆成两条字幕，不许出第 3 行、不许缩字号） |
| 1 行块 | 高 96px，块顶 y = 1440（75.0%） |
| 2 行块 | 高 160px，块顶 y = 1376（71.7%） |

用法（字幕层独立于场景，逐句换 `.ml-subs-line` 的内容就行，位置不用再算）：

```html
<div class="ml-subs"><div class="ml-subs-bar">
  <span class="ml-subs-line">这一句先说完，</span>
  <span class="ml-subs-line">下一句再接上。</span>
</div></div>
```

**验收量法**：成片任意抽两帧（1 行、2 行各一帧），量字幕背景条**底边**的 y，落在 **1526–1546** 才算过。量法：取画面中部横带逐行扫深色像素，最下面一行深色就是底边；背景条的投影是半透明的虚边，颜色明显浅，别算进去。

### 换平台、换设备，先自己重测一遍

上面这套数字只对小红书竖版负责。换个平台（比如抖音）、换个播放器，系统信息区的位置就不一样了，照这个方法重测：

1. 在目标 App 里以观众身份打开任意一条视频，截一张完整的播放画面。截图时视频要是高度填充的状态，别带上下黑边。
2. 在截图上量系统信息区顶边：头像、昵称那一行的最上沿，换算成占视频高度的百分比。
3. 字幕底边定在它上方一点，留安全间距（按 1920 高留 85px 上下，画布矮就按比例少留一点），换算成百分比，这就是你的锚点。
4. 顶部安全线同理：量顶部导航行（返回、搜索那些图标）的下沿，主体内容从它下面开始排。
5. 新数字写进你的 `config.yaml`（`video.subtitle_bottom_pct`、`video.system_info_top_pct`），动效库 `.ml-subs` 里的像素按画布高度换算。

## 版面分区（排版前先看这张表）

字幕锚点落定后，主内容区其实很大，排版必须把内容排满，不许内容挤在上半截、下半截空着。四区数字（1080×1920）都由上面那套实测推导：

| 区 | 范围 | 说明 |
|---|---|---|
| 顶部安全线 | y = 250（13%），这条线以上不排主体 | 观众视角顶部导航行约在高度 11%–14.5%；贴边的固定小元素（徽章、日期条这类）不在此限 |
| 主内容区 | y 250 → 1340，高 1090px | 标题、信息卡、真实界面图全排在这里；下界 1340 = 两行字幕块顶 1376 再留 36px 间隔 |
| 字幕区 | 块顶 1376（2 行）/ 1440（1 行），底边固定 y = 1536（80%） | 见上面「字幕锚定标准」 |
| 系统信息区 | 顶边 1621（84.4%）以下 | 禁入：主体内容和字幕都不许伸进去 |

利用率硬要求：每段主体内容（标题 + 信息卡 + 真实界面图的整体）纵向跨度至少占主内容区的 **55%**（约 600px），在区内居中分布、上下排满；内容区下部空置不许超过 **25%**（约 270px）。排版先排主体、再放字幕，不许反过来迁就字幕把内容挤小。

验收核对分区，用 `motion.css` 里的 `.ml-guide` 导线类（仅验收用，默认不启用）：在页面里加上 `<div class="ml-guide on">`，里面放五个 `<i class="g250" data-label="顶部安全线 250"></i>` 这样带编号的子元素，截图时五条线就会叠在画面上，照着量就行。核对完去掉 `.on`。**正式出片严禁带着 `.on` 渲染**，导线进了成片就是不合格。
