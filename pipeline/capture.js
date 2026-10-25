/* capture.js — capture web scenes frame by frame.
 *
 * The page must first expose three hooks (already written in the template — use them as is):
 *   window.__setScene(sceneName)       switch to this scene
 *   window.__renderFrame(sceneName, t) freeze the picture on the frame at second t
 *   window.__ready === true            the page says it is ready
 *
 * Usage:
 *   node capture.js --html page.html --out frames-dir --scenes open:16.6,step1:35.3
 * Options:
 *   --fps 30        frames per second, default 30
 *   --width 1080    frame width, default 1080
 *   --height 1920   frame height, default 1920
 * Which browser: the one CHROMIUM_PATH points to, if set;
 * otherwise playwright's own. Install with: npm install playwright,
 * then npx playwright install chromium.
 * Captured frames go to <frames-dir>/<scene>/0000.jpg, 0001.jpg, … in order.
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
  console.error("Usage: node capture.js --html page.html --out frames-dir --scenes scene:seconds,scene:seconds");
  process.exit(2);
}
const scenes = scenesRaw.split(",").map((s) => {
  const [name, dur] = s.split(":");
  return { name: name.trim(), dur: Number(dur) };
});
for (const sc of scenes) {
  if (!sc.name || !(sc.dur > 0)) {
    console.error(`Bad scene spec: ${sc}. Write it as scene:seconds, e.g. open:16.6`);
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
    console.error("playwright not found. With node installed, run: npm install playwright, then npx playwright install chromium.");
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
  page.on("pageerror", (e) => console.log("[page error]", e.message));

  await page.goto("file://" + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  try {
    await page.waitForFunction(() => window.__ready === true, null, { timeout: 20000 });
  } catch (e) {
    console.error("Waited 20 seconds and the page still hasn't said it's ready (window.__ready never became true). Check whether the page errored.");
    await browser.close();
    process.exit(1);
  }
  /* Wait for all images to load before capturing, or you'll catch half-loaded pictures. */
  await page.waitForFunction(() => {
    return Array.from(document.images).every((im) => im.complete && im.naturalWidth > 0);
  }, null, { timeout: 20000 }).catch(() => {
    console.log("[note] Some images still hadn't loaded after 20 seconds — capturing anyway; spot-check those frames when done.");
  });
  /* If the page has Lottie slots, wait until they've all drawn their first frame. */
  const lottieCount = await page.evaluate(() => document.querySelectorAll(".ml-lottie").length);
  if (lottieCount > 0) {
    await page.waitForFunction(
      (n) => document.querySelectorAll(".ml-lottie svg").length >= n,
      lottieCount, { timeout: 15000 }
    ).catch(() => {
      console.log("[note] Not all Lottie slots rendered — capturing anyway; check those segments before finishing.");
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
    console.log(`${sc.name}: ${total} frames in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
  }
  await browser.close();
  console.log(`All captured in ${((Date.now() - started) / 1000).toFixed(1)}s total. Frames are in ${outDir}, sorted by scene.`);
})().catch((e) => { console.error(e); process.exit(1); });
