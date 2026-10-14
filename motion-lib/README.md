# motion-lib：网页做片的动效库

做片的方法是：一条视频就是一个网页，动画在网页里排好，再一帧一帧截图，最后拼成视频。这个库就是给那个网页用的动效组件，样式在 `motion.css`，动作在 `motion.js`，都挂在 `window.MotionLib` 上。

## 一条硬规矩：所有动效都得能定格

截图时时间线是停住的，一帧一帧跳到某个时刻 t 再截。所以每个效果都只能由 t 算出来：同一个 t 跳多少次，画面都得一模一样。

- 不许用自己跑的时钟（比如 `requestAnimationFrame` 自由跑、`Date.now()`）决定画面。
- 不许用 `Math.random()` 掷骰子。要随机就用 `MotionLib.mulberry32(种子)`，种子定了，结果就定了。
- 星尘、彩带、Lottie 这类画布效果，登记成帧更新器（`addFrameUpdater`）。截图那边每跳一帧会喊 `runFrameUpdaters(t)`，它们按 t 把这一帧重画一遍。

不守这条，截出来的帧会跟时间对不上，成片就会跳、会闪。

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

样式类在 `motion.css` 顶部有一组变量（`--ml-color-a` 主色、`--ml-color-b` 辅色、`--ml-color-c` 点缀色、字幕带位置 `--ml-sub-top` 等），换风格先改变量，别到处翻色值。常用的类：`.ml-stage` 舞台、`.ml-glass` 玻璃卡、`.ml-card` 实色卡、`.ml-img-frame` 图片框、`.ml-grad-text` 渐变字、`.ml-topbar` 顶部彩条。

Lottie 示例素材在 `vendor/examples/`：`check.json` 是圆环描完打对勾，`sparkles.json` 是几颗四角星轮流闪，都是本项目自己写的，随便用。
