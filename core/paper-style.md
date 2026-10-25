[中文](paper-style.zh-CN.md) | English

# Appendix: visual style settled — layered paper-craft

> Optional style. When using this style, read it before video stage (03) starts; check against it item by item at acceptance. When not using it, follow the other sections of guide 03 — never mix the two. The color board and prompts are general defaults — change them for a different category, but never drift inside one episode.

## Settled elements (same every episode, no drifting)

- **Drawing method**: layered paper-cut / paper collage illustration — semi-3D paper layers stacked, soft shadows between layers, edges with a paper-cut feel. No flat vector, no realistic photo style, no 3D render style as the main visual.
- **Color board**: cream paper base (around #f2e9d8) + deep teal + burnt orange + near-black text; warnings and danger accents in dark red. Cover, main video, and title card share it — no drifting episode by episode.
- **Texture: light only**: just a hint of paper fiber grain — invisible from far away, a little paper feel up close. No heavy texture: coarse grain, full-screen noise, exaggerated torn-paper fray, or aged stains are all banned. In practice, one low-opacity paper fiber texture layer sits uniformly over the composited picture (strength judged by "faintly visible" when a pulled frame is zoomed in); the layer materials themselves carry no heavy texture.
- **Generation prompt fixed prefix** (carried word for word when generating backgrounds, people, and prop pictures — only the scene description after it changes):
  `layered paper-cut illustration, cream paper background, deep teal and burnt orange palette, soft drop shadows, torn paper edges, semi-3D papercraft style, clean composition`
  For vertical compositions, note portrait composition in the description. **Generated pictures carry no text** — all text goes on later through deterministic layout compositing.

## Splitting scenes into layers (every scene split, never one flat picture)

Every scene splits into at least 4 layers, listed layer by layer in the material list and the video dispatch:

1. **Background layer**: one complete paper-craft scene base picture — place, map, buildings, sky, ground, distant mountains, indoor furnishings, and other environment details all present. **The background must not be simple**: solid color, single gradient, or a base with only halos = failed; the background itself must hold up to being looked at alone (content, foreground and background depth).
2. **Midground layer**: secondary objects in the scene (furniture, trees, vehicles, shelves, clouds, and the like), pictured and moved separately from the background.
3. **Subject layer**: people and main props, each cut out as its own paper-craft element (transparent-background PNG) — one element per picture, never baking people and props into the background.
4. **Foreground layer**: near ornaments (falling paper pieces, near plants, light-spot paper pieces, and the like) that create depth.

- Layers get their 3D feel from **soft shadows + front-back overlap**; when the camera moves, each layer shifts by **parallax** according to depth (far layers slow, near layers fast).
- Charts, number cards, and conclusion cards are likewise made as paper-craft elements (paper cards, paper labels, paper stamps) — never falling back to flat UI cards.

## Moving (runs on top of the motion density targets)

- **Every element has its own motion on the timeline**: people act or shift (walking, peeking out, waving, nodding — done with jointed limbs or whole-element shifts, rotations, bounces), props move (shaking, page-turning, bouncing, rolling), midground and environment layers carry light ambient motion (clouds drifting, lights flickering, leaves swaying gently). Not all layers sliding together to fake it.
- **No 5-second window may contain only camera push-pull**: Ken Burns-style whole-picture zoom doesn't count as motion. At acceptance, pull frame pairs 2 seconds apart — the change must land on elements. A stretch with only global zoom gets sent back.
- The original hard motion targets still hold (at least 4 motion events per segment, at least 2 per 10 seconds across the video, key numbers counting up, key conclusion emphasis landings of 0.3+ seconds) — landing effects now speak paper-craft language (paper stamp pressed down, checkmark paper piece stuck on, paper card flipped over, torn-paper reveal).

## Nature and physics (however dense the motion, breaking physics looks wrong)

- **Gravity**: falling leaves, dropped objects, and falling elements must accelerate downward (ease-in) — never float down at a steady speed. Landings need a pause or a slide-out — never passing through the ground or a tabletop and vanishing.
- **Joints**: a jointed person's head, arms, and legs turn within real human joint range, pivots sitting on the joints — no folding backward, no overextending. Throughout the motion, jointed overlaps keep spare margin — no gaps showing, no parts coming loose.
- **Contact and weight**: feet stand flat on the ground, hands hold objects, sitting weight presses onto the chair seat — nothing floating, nothing sinking in. Objects on a table need contact shadows.
- **Overlap order stays fixed**: front-back relations between layers hold for the whole video — elements never pass through tables, chairs, walls, or people's bodies. Falling objects' paths avoid faces and key subject parts.

## Variety (after the paper-craft style is settled)

Drawing method and color board are settled by this appendix and no longer rotate. Variety happens only at composition, shot scale, scene, person design, arrangement, and transition level.

## Guardrails

- Real interfaces and official product pictures still use real pictures, set inside paper-craft framing — never let a paper-craft picture pass itself off as a real shot.
- Brand intro and outro clips don't get remade.
- Cover and main video drawing methods must not come apart: the cover's main visual follows the paper-craft style too (see guide 03's cover section), and the big title text and issue-number corner label still go through deterministic layout compositing.
