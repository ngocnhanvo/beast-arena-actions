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
