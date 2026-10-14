/* motion.js — 网页做片用的动效组件，都挂在 window.MotionLib 上。
 *
 * 先说最重要的一条：这里的动效都得能「定格」。
 * 做片的方法是把时间线停住，一帧一帧跳到某个时刻截图。
 * 所以任何效果都只能由时刻 t 算出来：同一个 t，画面必须一模一样。
 * 不能用自己跑的时钟，也不能随手掷骰子决定位置。
 * 要随机数就用下面带种子的 mulberry32，种子定了，结果就定了。
 * 画布类的效果（星尘、彩带、Lottie）先登记成帧更新器，
 * 截图那边每跳一帧会喊一声 runFrameUpdaters(t)，大家按 t 重画。
 *
 * 用之前先引 vendor/gsap/gsap.min.js，插件按需再引。
 * Lottie 槽位要先引 vendor/lottie.min.js，没有就不装。
 */
(function () {
  "use strict";
  if (!window.gsap) {
    console.error("[motion-lib] 先引 gsap.min.js，再引这个文件。");
    return;
  }

  /* 带种子的随机数。种子一样，出来的一串数就一样。 */
  function mulberry32(seed) {
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /* 帧更新器名单。跳帧截图时逐个喊，参数只有一个 t。 */
  const updaters = [];
  function addFrameUpdater(fn) { updaters.push(fn); return fn; }
  function runFrameUpdaters(t) { for (const fn of updaters) fn(t); }

  /* 页面上引了哪些 GSAP 插件，就把哪些登记上，没引的跳过。 */
  function usePlugins() {
    const names = [
      "SplitText", "DrawSVGPlugin", "Flip", "MorphSVGPlugin", "CustomEase",
      "CustomBounce", "CustomWiggle", "EasePack", "MotionPathPlugin",
      "TextPlugin", "ScrambleTextPlugin", "CSSRulePlugin",
    ];
    const done = [];
    for (const n of names) {
      if (window[n]) { gsap.registerPlugin(window[n]); done.push(n); }
    }
    return done;
  }

  /* ---- 标题 ---- */

  /* 把一句话拆成一个字一个 span，方便逐字动。
   * 有 SplitText 就用它，没有就自己按字切（中文一个字算一个）。 */
  function splitChars(el, text) {
    if (text != null) el.textContent = text;
    if (window.SplitText) {
      return new SplitText(el, { type: "chars", charsClass: "ml-char" }).chars;
    }
    const out = [];
    const src = el.textContent;
    el.textContent = "";
    for (const ch of src) {
      const sp = document.createElement("span");
      sp.className = "ml-char";
      sp.textContent = ch;
      el.appendChild(sp);
      out.push(sp);
    }
    return out;
  }

  /* 标题进场。mode 三选一：
   * flip 一个个翻进来，wave 一波一波升起来，blur 从模糊变清楚。 */
  function titleIn(tl, target, opts) {
    const o = Object.assign({ at: 0, mode: "flip", stagger: 0.055, dur: 0.6 }, opts || {});
    const chars = target instanceof Element ? splitChars(target) : target;
    if (o.mode === "wave") {
      tl.from(chars, {
        y: 70, opacity: 0, duration: o.dur, ease: "power3.out",
        stagger: { each: o.stagger, ease: "sine.inOut" },
      }, o.at);
    } else if (o.mode === "blur") {
      tl.from(chars, {
        opacity: 0, filter: "blur(16px)", scale: 1.15,
        duration: o.dur, stagger: o.stagger, ease: "power2.out",
      }, o.at);
    } else {
      tl.from(chars, {
        rotationX: -95, y: 44, opacity: 0, transformOrigin: "50% 100% -30px",
        duration: o.dur, stagger: o.stagger, ease: "back.out(2.1)",
      }, o.at);
    }
    return chars;
  }

  /* ---- 数字 ---- */

  function fmtNum(v, o) {
    let s = o.decimals ? v.toFixed(o.decimals) : String(Math.round(v));
    if (o.separator) {
      const parts = s.split(".");
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      s = parts.join(".");
    }
    return (o.prefix || "") + s + (o.suffix || "");
  }

  /* 数字从 from 滚到 to。中间值由时间线位置算，跳到哪帧就是哪个数。 */
  function countUp(tl, el, opts) {
    const o = Object.assign({
      at: 0, dur: 1, from: 0, ease: "power3.out",
      decimals: 0, separator: false, prefix: "", suffix: "",
    }, opts || {});
    const box = { v: o.from };
    el.textContent = fmtNum(o.from, o);
    tl.to(box, {
      v: o.to, duration: o.dur, ease: o.ease,
      onUpdate: () => { el.textContent = fmtNum(box.v, o); },
    }, o.at);
    return box;
  }

  /* ---- 图表 ---- */

  /* 横条从左往右长，ratio 是最后长到多满（0 到 1）。 */
  function barGrow(tl, el, opts) {
    const o = Object.assign({ at: 0, dur: 1.1, ratio: 1, ease: "power3.inOut" }, opts || {});
    tl.fromTo(el, { scaleX: 0 }, { scaleX: o.ratio, duration: o.dur, ease: o.ease }, o.at);
  }

  /* 沿着 SVG 路径描一遍，画线条、对勾都能用。
   * 有 DrawSVG 插件就用插件，没有就自己算长度用虚线偏移顶上。 */
  function drawPath(tl, el, opts) {
    const o = Object.assign({ at: 0, dur: 1, ease: "power2.inOut" }, opts || {});
    if (window.DrawSVGPlugin) {
      tl.fromTo(el, { drawSVG: "0%" }, { drawSVG: "100%", duration: o.dur, ease: o.ease }, o.at);
    } else {
      const len = el.getTotalLength();
      gsap.set(el, { strokeDasharray: len, strokeDashoffset: len });
      tl.to(el, { strokeDashoffset: 0, duration: o.dur, ease: o.ease }, o.at);
    }
  }

  /* 圆环扫过百分之几，pct 是 0 到 1。圆上要先写好 r 属性。 */
  function ringSweep(tl, circleEl, opts) {
    const o = Object.assign({ at: 0, dur: 1.2, pct: 0.75, ease: "power3.inOut" }, opts || {});
    const c = 2 * Math.PI * parseFloat(circleEl.getAttribute("r"));
    gsap.set(circleEl, { strokeDasharray: c, strokeDashoffset: c });
    tl.to(circleEl, {
      strokeDashoffset: c * (1 - o.pct), duration: o.dur, ease: o.ease,
    }, o.at);
  }

  /* ---- 卡片 ---- */

  /* 卡片从某个方向滑进来，带一点回弹。from 是 left/right/top/bottom/none。 */
  function cardIn(tl, el, opts) {
    const o = Object.assign({
      at: 0, dur: 0.8, from: "bottom", dist: 64,
      ease: "back.out(1.55)", scaleFrom: 0.94,
    }, opts || {});
    const off = {
      left: [-o.dist, 0], right: [o.dist, 0],
      top: [0, -o.dist], bottom: [0, o.dist], none: [0, 0],
    }[o.from];
    tl.fromTo(el,
      { x: off[0], y: off[1], opacity: 0, scale: o.scaleFrom },
      { x: 0, y: 0, opacity: 1, scale: 1, duration: o.dur, ease: o.ease }, o.at);
  }

  /* 几张卡从两边飞过来，叠成一摞。
   * finals 跟 els 一一对应，写每张卡最后停的位置和角度。 */
  function stackConverge(tl, els, finals, opts) {
    const o = Object.assign({ at: 0, dur: 1.15, stagger: 0.16, ease: "back.out(1.35)" }, opts || {});
    els.forEach((el, i) => {
      const f = finals[i] || { x: 0, y: 0, rotation: 0 };
      const spread = i - (els.length - 1) / 2;
      tl.fromTo(el,
        {
          x: f.x + spread * 460, y: f.y - 120 - Math.abs(spread) * 30,
          rotation: f.rotation + spread * 15, opacity: 0,
        },
        {
          x: f.x, y: f.y, rotation: f.rotation, opacity: 1,
          duration: o.dur, ease: o.ease,
        }, o.at + i * o.stagger);
    });
  }

  /* 3D 翻卡，从正面翻到背面。结构用 .ml-flip-wrap / .ml-flip-inner / .ml-flip-face。 */
  function flipCard(tl, innerEl, opts) {
    const o = Object.assign({ at: 0, dur: 0.9, ease: "power3.inOut" }, opts || {});
    tl.fromTo(innerEl, { rotationY: 0 },
      { rotationY: 180, duration: o.dur, ease: o.ease }, o.at);
  }

  /* ---- 强调 ---- */

  /* 一道光从卡片上扫过去。光条不用自己写，这个函数会补上。 */
  function shine(tl, hostEl, opts) {
    const o = Object.assign({ at: 0, dur: 0.9, ease: "power2.inOut" }, opts || {});
    let bar = hostEl.querySelector(".ml-shine-el");
    if (!bar) {
      bar = document.createElement("div");
      bar.className = "ml-shine-el";
      hostEl.appendChild(bar);
    }
    hostEl.classList.add("ml-shine");
    tl.fromTo(bar, { x: "-160%" }, { x: "560%", duration: o.dur, ease: o.ease }, o.at);
  }

  /* 下划线描绘，就是 drawPath 换了个顺口的名字。 */
  function underlineDraw(tl, pathEl, opts) { return drawPath(tl, pathEl, opts); }

  /* 发光一涨一缩，像在呼吸。color 是 "r,g,b" 这种写法。 */
  function breathe(tl, el, opts) {
    const o = Object.assign({
      at: 0, half: 1.6, repeats: 5, blurFrom: 18, blurTo: 52,
      color: "56,189,248", alphaFrom: 0.14, alphaTo: 0.5,
      base: "0 18px 44px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.14)",
    }, opts || {});
    const from = `${o.base}, 0 0 ${o.blurFrom}px rgba(${o.color},${o.alphaFrom})`;
    const to = `${o.base}, 0 0 ${o.blurTo}px rgba(${o.color},${o.alphaTo})`;
    tl.fromTo(el, { boxShadow: from }, {
      boxShadow: to, duration: o.half, ease: "sine.inOut",
      yoyo: true, repeat: o.repeats * 2 - 1,
    }, o.at);
  }

  /* ---- 转场 ---- */

  /* 用遮罩把画面擦出来，dir 是擦的方向。 */
  function wipeIn(tl, el, opts) {
    const o = Object.assign({ at: 0, dur: 0.8, dir: "left", ease: "power3.inOut" }, opts || {});
    const from = {
      left: "inset(0 100% 0 0)", right: "inset(0 0 0 100%)",
      top: "inset(0 0 100% 0)", bottom: "inset(100% 0 0 0)",
    }[o.dir];
    tl.fromTo(el, { clipPath: from, opacity: 1 },
      { clipPath: "inset(0 0% 0 0)", duration: o.dur, ease: o.ease }, o.at);
  }

  /* 一个圆从 cx、cy 处涨开，把画面露出来，cx、cy 是百分数。 */
  function circleReveal(tl, el, opts) {
    const o = Object.assign({ at: 0, dur: 0.9, cx: 50, cy: 50, ease: "power3.inOut" }, opts || {});
    tl.fromTo(el,
      { clipPath: `circle(0% at ${o.cx}% ${o.cy}%)` },
      { clipPath: `circle(120% at ${o.cx}% ${o.cy}%)`, duration: o.dur, ease: o.ease }, o.at);
  }

  /* 旧画面糊掉淡出，新画面同时清楚起来。 */
  function blurCrossfade(tl, outEl, inEl, opts) {
    const o = Object.assign({ at: 0, dur: 0.7, ease: "power2.inOut" }, opts || {});
    tl.to(outEl, {
      opacity: 0, filter: "blur(14px)", scale: 0.965, duration: o.dur, ease: o.ease,
    }, o.at);
    tl.fromTo(inEl,
      { opacity: 0, filter: "blur(14px)", scale: 1.03 },
      { opacity: 1, filter: "blur(0px)", scale: 1, duration: o.dur, ease: o.ease }, o.at);
  }

  /* ---- 背景 ---- */

  /* 光晕在整段里慢慢挪，specs 每项是 {el, dx, dy}。 */
  function glowDrift(tl, specs, dur) {
    for (const s of specs) {
      tl.fromTo(s.el, { x: 0, y: 0 },
        { x: s.dx, y: s.dy, duration: dur, ease: "sine.inOut" }, 0);
    }
  }

  /* 星尘：满屏小点，位置只跟种子和 t 有关，每帧按 t 重画一遍。 */
  function starfield(canvas, opts) {
    const o = Object.assign({
      count: 90, seed: 7, maxR: 2.6, drift: 26, twinkle: 0.55,
      colors: ["#9fd8f5", "#ffffff", "#8fe3bb", "#ffc38f"],
    }, opts || {});
    const ctx = canvas.getContext("2d");
    const W = canvas.width, H = canvas.height;
    const rnd = mulberry32(o.seed);
    const stars = [];
    for (let i = 0; i < o.count; i++) {
      stars.push({
        x: rnd() * W, y: rnd() * H,
        r: 0.7 + rnd() * (o.maxR - 0.7),
        c: o.colors[(rnd() * o.colors.length) | 0],
        ph: rnd() * Math.PI * 2, sp: 0.25 + rnd() * 0.7,
        dx: rnd() - 0.5, dy: rnd() - 0.5,
      });
    }
    addFrameUpdater((t) => {
      ctx.clearRect(0, 0, W, H);
      for (const s of stars) {
        const x = s.x + Math.sin(t * s.sp + s.ph) * o.drift * s.dx * 2;
        const y = s.y + Math.cos(t * s.sp * 0.8 + s.ph) * o.drift * s.dy * 2;
        const a = 0.35 + o.twinkle * (0.5 + 0.5 * Math.sin(t * (0.6 + s.sp) + s.ph * 2));
        ctx.globalAlpha = Math.max(0.06, Math.min(1, a));
        ctx.fillStyle = s.c;
        ctx.beginPath();
        ctx.arc(x, y, s.r, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.globalAlpha = 1;
    });
    return stars;
  }

  /* 彩带：到点从一个位置喷一束。
   * 不用现成的彩带库，那个靠自己的时钟跑，定格对不上。
   * 这里每颗纸片飞到哪，只由喷出时刻和 t 算，跳到哪帧都一样。
   * bursts 每项：{t0 喷出时刻, x, y, n 颗数, seed, life 存活秒数}，其余可不填。 */
  function confettiBursts(canvas, bursts) {
    const ctx = canvas.getContext("2d");
    const W = canvas.width, H = canvas.height;
    const ready = bursts.map((raw) => {
      const b = Object.assign({
        n: 90, spread: Math.PI * 0.9, power: 1150, gravity: 1500,
        drag: 0.86, life: 1.7, size: 13, seed: 3,
        colors: ["#38bdf8", "#34c77b", "#f5823c", "#ffffff", "#ffd166"],
      }, raw);
      const rnd = mulberry32(b.seed);
      const bits = [];
      for (let i = 0; i < b.n; i++) {
        const ang = -Math.PI / 2 + (rnd() - 0.5) * b.spread;
        const vel = b.power * (0.45 + rnd() * 0.75);
        bits.push({
          vx: Math.cos(ang) * vel, vy: Math.sin(ang) * vel,
          w: b.size * (0.6 + rnd() * 0.8), h: b.size * (0.35 + rnd() * 0.5),
          rot: rnd() * Math.PI, vr: (rnd() - 0.5) * 14,
          c: b.colors[(rnd() * b.colors.length) | 0], ph: rnd() * Math.PI,
        });
      }
      return { b, bits };
    });
    addFrameUpdater((t) => {
      ctx.clearRect(0, 0, W, H);
      for (const { b, bits } of ready) {
        const dt = t - b.t0;
        if (dt < 0 || dt > b.life) continue;
        const fade = dt > b.life - 0.45 ? (b.life - dt) / 0.45 : 1;
        const dragK = Math.pow(b.drag, dt * 3.2);
        const run = (1 - dragK) / (3.2 * -Math.log(b.drag));
        for (const p of bits) {
          const xx = b.x + p.vx * run;
          const yy = b.y + p.vy * run + 0.5 * b.gravity * dt * dt;
          ctx.save();
          ctx.globalAlpha = Math.max(0, Math.min(1, fade));
          ctx.translate(xx, yy);
          ctx.rotate(p.rot + p.vr * dt);
          ctx.scale(1, 0.55 + 0.45 * Math.sin(p.ph + dt * 9));
          ctx.fillStyle = p.c;
          ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
          ctx.restore();
        }
      }
      ctx.globalAlpha = 1;
    });
  }

  /* Lottie 槽位：把一段 Lottie 动画钉在时间线上。
   * 它自己不播，全靠帧更新器按 t 把它拨到对应帧。at 是它在时间线上的起点。
   * loopAfter 不填就不循环；填了秒数，过了那个点就循环放后半段。 */
  function mountLottie(el, opts) {
    if (!window.lottie) {
      console.error("[motion-lib] 没引 lottie.min.js，这个槽位装不上。");
      return null;
    }
    const o = Object.assign({ at: 0 }, opts || {});
    const params = { container: el, renderer: "svg", loop: false, autoplay: false };
    if (o.animationData) params.animationData = o.animationData;
    else params.path = o.path;
    const anim = window.lottie.loadAnimation(params);
    let loaded = false;
    anim.addEventListener("DOMLoaded", () => {
      loaded = true;
      anim.goToAndStop(0, true);
    });
    addFrameUpdater((t) => {
      if (!loaded) return;
      const fr = anim.frameRate || 30;
      const total = anim.totalFrames || 1;
      let f = (t - o.at) * fr;
      if (o.loopAfter) {
        const lf = o.loopAfter * fr;
        if (f >= lf) f = lf + ((f - lf) % (total - lf));
      }
      anim.goToAndStop(Math.max(0, Math.min(total - 1, f)), true);
    });
    return anim;
  }

  /* 形状变形：把一条路径变成另一个形状。要 MorphSVG 插件，没装就直接改 d 属性顶上。 */
  function morphTo(tl, el, targetD, opts) {
    const o = Object.assign({ at: 0, dur: 0.8, ease: "power2.inOut" }, opts || {});
    if (window.MorphSVGPlugin) {
      tl.to(el, { morphSVG: targetD, duration: o.dur, ease: o.ease }, o.at);
    } else {
      tl.to(el, { attr: { d: targetD }, duration: o.dur, ease: o.ease }, o.at);
    }
  }

  window.MotionLib = {
    mulberry32, addFrameUpdater, runFrameUpdaters, usePlugins,
    splitChars, titleIn, countUp, barGrow, drawPath, ringSweep,
    cardIn, stackConverge, flipCard, shine, underlineDraw, breathe,
    wipeIn, circleReveal, blurCrossfade, glowDrift, starfield,
    confettiBursts, mountLottie, morphTo,
  };
})();
