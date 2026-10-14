/* capture.js — 把网页场景一帧一帧截下来。
 *
 * 页面要先留好三个口子（模板里已经写好，照着用就行）：
 *   window.__setScene(场景名)       切到这个场景
 *   window.__renderFrame(场景名, t) 把画面定格在 t 秒这一帧
 *   window.__ready === true         页面说自己准备好了
 *
 * 用法：
 *   node capture.js --html 页面.html --out 帧目录 --scenes open:16.6,step1:35.3
 * 可选项：
 *   --fps 30        每秒截几帧，默认 30
 *   --width 1080    画面宽，默认 1080
 *   --height 1920   画面高，默认 1920
 * 浏览器用哪个：环境变量 CHROMIUM_PATH 指了就用那个；
 * 没指就用 playwright 自带的。装法：npm install playwright，
 * 再 npx playwright install chromium。
 * 截出的帧放在 <帧目录>/<场景名>/0000.jpg、0001.jpg……顺序往下排。
 */
"use strict";
const fs = require("fs");
const path = require("path");

function arg(name, fallback) {
  const i = process.argv.indexOf("--" + name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

const html = arg("html", "");
const outDir = arg("out", "");
const scenesRaw = arg("scenes", "");
const fps = Number(arg("fps", "30"));
const width = Number(arg("width", "1080"));
const height = Number(arg("height", "1920"));

if (!html || !outDir || !scenesRaw) {
  console.error("用法：node capture.js --html 页面.html --out 帧目录 --scenes 场景名:时长秒,场景名:时长秒");
  process.exit(2);
}
const scenes = scenesRaw.split(",").map((s) => {
  const [name, dur] = s.split(":");
  return { name: name.trim(), dur: Number(dur) };
});
for (const sc of scenes) {
  if (!sc.name || !(sc.dur > 0)) {
    console.error(`场景写法不对：「${sc}」。要写成 场景名:时长秒，比如 open:16.6`);
    process.exit(2);
  }
}

let chromium;
try {
  chromium = require("playwright").chromium;
} catch (e) {
  try {
    chromium = require("playwright-core").chromium;
  } catch (e2) {
    console.error("没找到 playwright。先在装了 node 的前提下跑：npm install playwright，然后 npx playwright install chromium。");
    process.exit(1);
  }
}

(async () => {
  const started = Date.now();
  const launchOpts = {
    args: ["--no-sandbox", "--force-color-profile=srgb", "--hide-scrollbars",
           "--disable-dev-shm-usage", "--allow-file-access-from-files"],
  };
  if (process.env.CHROMIUM_PATH) launchOpts.executablePath = process.env.CHROMIUM_PATH;
  const browser = await chromium.launch(launchOpts);
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.log("[页面报错]", e.message));

  await page.goto("file://" + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  try {
    await page.waitForFunction(() => window.__ready === true, null, { timeout: 20000 });
  } catch (e) {
    console.error("等了 20 秒，页面还没说自己准备好（window.__ready 没变成 true）。先看看页面是不是报错了。");
    await browser.close();
    process.exit(1);
  }
  /* 图片都加载完再截，不然会截到半张图。 */
  await page.waitForFunction(() => {
    return Array.from(document.images).every((im) => im.complete && im.naturalWidth > 0);
  }, null, { timeout: 20000 }).catch(() => {
    console.log("[提醒] 有图片 20 秒还没加载完，照样往下截，截完记得抽查那几帧。");
  });
  /* 页面上有 Lottie 槽位的话，等它们都画出第一帧。 */
  const lottieCount = await page.evaluate(() => document.querySelectorAll(".ml-lottie").length);
  if (lottieCount > 0) {
    await page.waitForFunction(
      (n) => document.querySelectorAll(".ml-lottie svg").length >= n,
      lottieCount, { timeout: 15000 }
    ).catch(() => {
      console.log("[提醒] Lottie 槽位没全画出来，照样往下截，出片前抽查那几段。");
    });
  }

  for (const sc of scenes) {
    const dir = path.join(outDir, sc.name);
    fs.rmSync(dir, { recursive: true, force: true });
    fs.mkdirSync(dir, { recursive: true });
    await page.evaluate((s) => window.__setScene(s), sc.name);
    const total = Math.floor(sc.dur * fps);
    const t0 = Date.now();
    for (let i = 0; i < total; i++) {
      await page.evaluate(([s, t]) => window.__renderFrame(s, t), [sc.name, i / fps]);
      await page.screenshot({
        path: path.join(dir, String(i).padStart(4, "0") + ".jpg"),
        type: "jpeg", quality: 90,
      });
    }
    console.log(`${sc.name}：${total} 帧，花了 ${((Date.now() - t0) / 1000).toFixed(1)} 秒`);
  }
  await browser.close();
  console.log(`全部截完，一共 ${((Date.now() - started) / 1000).toFixed(1)} 秒。帧在 ${outDir} 里，按场景分好了。`);
})().catch((e) => { console.error(e); process.exit(1); });
