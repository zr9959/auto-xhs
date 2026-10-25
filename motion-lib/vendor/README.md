[中文](README.zh-CN.md) | English

# What goes in vendor

This is where the third-party libraries for video making live. The library sources don't go into the repo — run `scripts/fetch-vendor.sh` and it downloads them here from the official npm registry, at the locked versions below.

| Library | Locked version | Where from | License, in one line |
|---|---|---|---|
| GSAP | 3.15.0 | npm package `gsap`, all `.min.js` files from `dist/` | Its own free license: free to use, commercial use allowed — but it is not MIT, so don't pass it on as if it were open source |
| lottie-web | 5.13.0 | npm package `lottie-web`, file `build/player/lottie.min.js` | MIT, safe to use |
| canvas-confetti | 1.9.4 | npm package `canvas-confetti`, file `dist/confetti.browser.js` | ISC, a permissive license, safe to use |

One more word on canvas-confetti: in this project it is only a reference — it never fires confetti directly. It runs on its own clock, which doesn't line up with frame-by-frame screenshots. Confetti here uses `confettiBursts` in motion.js, with the algorithm pinned in the library.

The `examples/` files `check.json` (ring plus check mark) and `sparkles.json` (flashing four-pointed stars) are small Lottie assets written for this project. They need no downloading — they travel with the repo.
