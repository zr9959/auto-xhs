# vendor 里放什么

这里放做片要用的第三方库。库的本体不进仓库，运行 `scripts/fetch-vendor.sh` 就会按下面锁定的版本从 npm 官方源下载到这里。

| 库 | 锁定版本 | 从哪下 | 许可证，一句话 |
|---|---|---|---|
| GSAP | 3.15.0 | npm 包 `gsap`，取 `dist/` 里的全部 `.min.js` | 它自己的免费许可证：用不要钱、商用也行，但它不是 MIT，别当开源协议随便转发 |
| lottie-web | 5.13.0 | npm 包 `lottie-web`，取 `build/player/lottie.min.js` | MIT，可以放心用 |
| canvas-confetti | 1.9.4 | npm 包 `canvas-confetti`，取 `dist/confetti.browser.js` | ISC，宽松协议，可以放心用 |

再说一句 canvas-confetti：它在本项目里只作参考，不直接用它放彩带。它靠自己的时钟跑，跟逐帧截图对不上。彩带用 motion.js 里的 `confettiBursts`，算法在库里写死了。

`examples/` 里的 `check.json`（圆环加对勾）和 `sparkles.json`（四角星闪烁）是本项目自己写的 Lottie 小素材，不用下载，随仓库走。
