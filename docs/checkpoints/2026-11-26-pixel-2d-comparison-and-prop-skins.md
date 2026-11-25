# Public Actions checkpoint — visual-first dual presentation and authored physics props
Date 2026-11-26. **Overall: PARTIAL — chưa hoàn tất.**

## Canonical source handoff
- PRIVATE `ngocnhanvo/beast-arena/docs/checkpoints/2026-11-26-pixel-2d-comparison-and-prop-skins.md` is the authoritative latest checkpoint. Read AGENTS.md and both START_HERE docs, V3/V4 checkpoint and visual-first roadmap before edits.
- Original Physics0 source has new separately authored skins for all six native 3D physical obstacles; sprites and floor remain from same original pixel assets.
- Private `scripts/pixel_projection.gd` and `scripts/pixel_view.gd` create an OPTIONAL F5 2D visual projection from actual Godot 3D actor/floor Y: fixed horizontal X, 6.5 pixels/m depth for Z, 31 pixels/m physical elevation for Y; original sprite frames and map textures. No second gameplay/physics system, no changes to existing root P1.5 route, no forced F5 default.
- Private `scripts/demo.gd` reports `pixel_projection_mode` + actual draw counts; private new headless `pixel_projection_smoke.gd` validates world-axis/height map switch and 2v2 physical roster connection.
- Public `.github/workflows/build.yml` now runs headless `pixel_projection_smoke.gd`. Public `ci/playwright_physics_v2.py` toggles F5 in Chromium, screenshots `moss-nes-style-2d-preview.png`, asserts tile/character counts, nonflat pixels and restores original 3D preview.
- Pre-existing Public `ci/playwright_physics_v2.py` also requires `pixel_prop_skins=6` on Moss and Night Docks. This verifies native obstacle geometry is visually skinned, not merely created in code.

## Evidence (not a general completion claim)
- Godot build/Pages #45683483080 and Chromium #45683778280 SUCCESS. Real old pixel top-floor image visible but overly steep-looking wide map.
- Compact stage build/Pages #45684576424 and Chromium #45684936382 SUCCESS, private `08d99ab20437346e041c557f4294888c40e21772`; screenshot inspected: original texture detail visible but full-width 3D ramp still occupies too much of the frame, Nekketsu style NOT visually accepted.
- Prop skin build+Pages #45685202832 SUCCESS, checked-out PRIVATE source `549a33eedabb8b327dc511a6af6d887e2b53b137`, public pipeline `c2b6048236bea2770bcc72d8e849cfbb89b5108a`. Follow-up browser #45685557148 in progress at snapshot.
- Source pixel view last code PRIVATE `49ca27ea6e7729c9d35033f4420d2a70bf402cc0`; public CI test code last `ca30f9460e12b92f296cd558e1cb62d81d5e6300`.
- Build #45685585437 / queued #45685624341 will verify optional 2D renderer. **Not yet verified.** Never claim CI successful merely because pushed.

## Required next QA
1. Inspect latest public CI run and exact checkout SHA; repair Godot 4.7 parser/test/runtime failures if any.
2. Confirm Pages deployed and Chrome screenshot `moss-nes-style-2d-preview.png` from the SAME source SHA; compare both 3D and F5 2D mode, verify battle, ground height, silhouette, background and frame size. Check Night Docks through F5 as well before default change.
3. Keep visual acceptance open, no production root migration, no beast transformation until actual user-approved V0–V4 human/gameplay slice.

**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — Verified F5 release, visual feedback, stronger cross-map screenshot QA

- VERIFIED PUBLIC Godot+Pages [#45685585437](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45685585437) SUCCESS, actual PRIVATE source `49ca27ea6e7729c9d35033f4420d2a70bf402cc0`, PUBLIC pipeline `a04fc583d3af6392154f619868451e4fd68d3d60`. Headless physical 3D tests + independent `pixel_projection_smoke.gd` passed.
- VERIFIED browser Chromium [#45685984297](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45685984297) SUCCESS. Artifact screenshot `physics-v2/moss-nes-style-2d-preview.png` downloaded & visually inspected; result has `pixel_2d_overlay_pass=true`, 221 tile draws, four real fighter renderings, 25 3D combat hits, 9 distinct visible color groups, F5 returns to original view.
- Human visual QA: the whole map no longer feels like a single tilted 3D plane, but F5 sky has too much empty space and raised stair tiles lack connected supporting walls. Thus **VISUAL_ACCEPTED=FALSE / USER REVIEW PENDING**; don't conflate this with technical browser PASS.
- PRIVATE new code `40f0cce` adds original sky parallax and pixelated physical retaining walls; unique hair/scarf/armor variants `330f3ce`, `7395afc`, `659e3b4`; source visual test `67c1ac8` checks distinct alpha silhouettes. PUBLIC `ci/playwright_physics_v2.py` commit `79f33d5` captures **both Moss and Docks F5 start** images BEFORE combat in addition to original F5 post-2v2 image.
- **NOT YET VERIFIED** at documentation time: build [#45686677550](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45686677550) and follow-up screenshot runs for new sky/retaining wall/F5 two-map captures. `67c1ac8` alpha test may be newer than that source checkout and must be re-built. Preserve old P1.5 and no V5 deployment.

**Trạng thái: PARTIAL — chưa hoàn tất**
