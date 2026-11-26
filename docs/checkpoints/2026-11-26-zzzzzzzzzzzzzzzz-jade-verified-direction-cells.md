# Beast Arena Actions — verified Jade source orientations and direction-safe animation (2026-11-26)

## User request, verified visual evidence, exact code scope
Owner supplied original atlas screenshot showing a ROW with RIGHT, LEFT, RIGHT, BACK characters and demanded immediate correction. Previous assistant described one row as "four frames walking left" — false. Directly inspected PRIVATE `experiments/physics_v2/assets/jade_approved_80f.png` (4 columns x 20 rows x 80px): source row0 0/1/2 FRONT, 3 BACK; rows1..4 0 RIGHT, 1 LEFT, 2 RIGHT, 3 BACK. Thus a single source row cannot be assumed to represent the same direction across columns.

## PRIVATE game source already fixed
- `scripts/jade_approved_motion.gd`: an explicit per-direction original-cell resolver (`movement_frame`) maps A/left to source col1, D/right to col2. Source walk rows are ONLY 1/2; source run rows are ONLY 3/4. ALL original moving cells rows1..4 are pixel-exact and no patchwork legs/arms alter them at runtime. W/S face player using complete original frontal row0 col0 still picture, NOT fake side-bodied front "walking". FRONT jump/J/K image selection also uses a complete original front placeholder until authored front action art exists.
- `scripts/character.gd`: physical -Z/+Z remains opposite and 60Hz collider/hit data unmodified; presentation chooses 2 full-body source side walk phases and 2 separate source side run phases; W/S physically move, visually show same genuine front static fallback. Source audit PENDING_ART and user aesthetic FAIL remain valid; this fixes direction mapping, not original 10 animations.
- `tests/visual_smoke.gd`: ART-30 verifies 320x1600 layout, all original side moving cells untouched, direction-specific col1/col2, side walk and run rows disjoint, W/S no sideways cell, baseline foot pivots intact. Replaces false ART-27/28/29 tests that previously rewarded distinct pixels caused by artificial compositing.
- PUBLIC `ci/playwright_physics_v2.py`: verifies real W world travel / floor clearance while rendered FRONT frame is source row0/col0, no longer requires FAKE 4 authored front foot phases; preserves real native J/K state, 2D/3D, P1.5 maps and ramps.
- Existing opt-in Arcade V2, F/G/F+G, run A+A/D+D, and named SpriteFrames importer are NOT changed. `autocheck:false` means owner judges aesthetics, technical CI checks engine only.

## Exact verified CI and pending real Web
- PRIVATE **actually checked out/compiled** `d6ae5c26aa67fdcc751a79edfcc4d30e68bac346` (code/tests; newer PRIVATE docs-only commits do not affect the shipped game). PUBLIC pipeline `1142c019be2e918e4050468f5b4584ea3a0cd081`.
- [Godot/Windows/Web/Pages #45785263338](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45785263338) **SUCCESS** on ALL real jobs; build logs printed `APPROVED JADE DIRECTION-SAFE PASS: W/S genuine front placeholder, left/right whole-body walk rows1-2 and run rows3-4, no runtime limb patch; PENDING_ART` plus `All export checks passed.` New source audit says `PENDING_ART`.
- [Chromium Playwright #45785507440](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45785507440) was **IN PROGRESS** at checkpoint creation: check exact result and log separately before claiming Web E2E PASS.
- Owner preview once final Web test done: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?controls=v2&art=approved&pixel=1&v=45785263338 . W/S real movement shows stationary complete FRONT artist original, while A/D whole-body walk and A+A/D+D whole-body run use verified columns. Existing source offers only two whole side poses per gait, NOT a complete designed 6/8-frame authored clip.

## Remaining blocker
`BLOCKED_ART_SOURCE`: no editable .ase/.aseprite full-body animation timeline and no genuine independently illustrated 80px W/S walk, side walk/run extra poses, front kick/jump. Do not use runtime arm/leg fragment shifting as a replacement. Next: owner reviews direction-fix preview; then author proper 10 clips, strict audit, V2 importer and owner art approval. Whole game roadmap is still OPEN.

**Trạng thái: PARTIAL — chưa hoàn tất** (engine+Pages PASS, owner graphic approval and original art pending).
