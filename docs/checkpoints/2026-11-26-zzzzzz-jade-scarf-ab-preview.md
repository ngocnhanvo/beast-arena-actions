# Beast Arena — Jade Scarf 80-frame pixel art A/B, 2026-11-26

## Scope and provenance
- User priority is a distinctive original expressive chibi human fighter before beast transformation; the earlier generated concept showed teal spiky hair, red scarf and light vest.
- New authored original vector-pixel atlas `experiments/physics_v2/assets/jade_scarf_80f.svg` (256×1280, 4 directional columns ×20 frame rows, each cell 64×64); enhanced hair and trailing scarf, cream vest, dark trousers. No NES game assets or sprites were copied/ripped/traced. Not an exact export of the prior concept mock; still work-in-progress.
- Physics0 `demo.gd` adds **opt-in** `?pixel=1&art=concept` and reversible **F6** comparison. Hero sprite and in-game portrait both switch; original 80-frame atlases for all other combatants remain. Physics/HP/velocity/camera/fixed 60Hz combat, slopes/map and root P1.5 unaffected.
- Private changes include code `9e5eaf9` atlas, `42bbb09` selector, `417ba34` Godot import/art/silhouette and 3D physics-invariance test. Guide: `docs/art/JADE_SCARF_AB_2026-11-26.md`.
- Public `ci/playwright_physics_v2.py` `b4584ef` adds F6 toggling and real Chromium screenshot `moss-jade-scarf-concept.png`, requires actual visible difference from classic and no HP/map changes. The test does not infer art approval from source alone.

## Strict verification
- **Private exact source compiled by new build:** `cd04e33dd9e5820d2e9a24375ae35b463c71b346` (first public runner log, after art direction document).
- Public CI run [#45744769106](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45744769106) Godot strict import and `visual_smoke.gd` art test have completed successfully, along with native 3D slope, original F5 2D, 2v2, fixed-tick combo, Web+Windows export. **Pages and Chromium pending at first checkpoint.**
- Before claiming runtime PASS: check public Pages job and spawned Chromium E2E run, strict exact source SHA/build ID, open actual `moss-jade-scarf-concept.png`, verify read-only report, and assess visual comparison.
- Art acceptance remains **OPEN** until user reviews the actual Web screenshot; vector-pixel style is a provisional alternative, not final NES-level hand-crafted 80-frame set.

## Next steps after QA
- If F6 E2E fails, inspect real job log/artifact and fix only the demonstrated regression.
- Check art at physical 52px scale against existing stage color and enemy silhouettes; next author distinct full motions/frames and export original, editable PNG/LibreSprite sources, not just palette swaps. Then refine foreground/props, grab/throw, AI and eventually beast V5.

**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — build trigger: original world-ground pixel details + 64px fighter art

**TARGET PRIVATE SOURCE HEAD:** `7a661ab099cca2b13753614bb456d8413c9d2ffb`, functional deltas: `pixel_view.gd` adds world-height-linked Moss moss/stone + Night Docks plate rivets; F5 original sprite render rectangle now exact 64×64 pixels with feet anchored; `demo.gd` emits `pixel_floor_details`, `pixel_projection_smoke.gd` PRES-13 (>60 physical floor details both stages) and PRES-14 (64px fighter render).
**PUBLIC E2E SOURCE:** `ci/playwright_physics_v2.py` `795154750a659058852bab259dd996e7911720f5` checks >=15 actually rendered original floor details in **both real Chromium 2D map screenshots**, retains F6 Jade Scarf screenshot comparison/physical state invariance, all 3D slopes/HP/AI/guard/round/camera and P1.5 old smoke.

**History, do not hide the FAILURE:**
- Previous Jade Scarf version: Godot/Pages [#45744769106](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45744769106) PASS; Chromium [#45744980035](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45744980035) PASS, exact source `cd04e33...`, user-facing original-art F6 A/B screenshot changed **8033 visible pixels**, same HP/map, artifact 15082292922. No user aesthetic approval yet.
- First floor-detail/64px run [#45745395296](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45745395296) FAIL `PRES-13` and Pages SKIPPED: Moss 70m width, 3.4m spacing yields 57 markers, under 60-point gate. Verified root cause via real map `dimensions=Vector2(70,26)`. Fixed PRIVATE `84a6bd892156181b40a98c6b026ea0f46d425468`: 3.0m spacing => 66 on Moss, 78 Docks; preserve stricter test threshold instead of removing test.

**Required result of this PUBLIC push-triggered CI:** actual Godot import, PRES-13/PRES-14, original 80f art and physics/2v2 tests PASS; Web+Windows export+Pages; automatic Chromium checking source+build SHA and actual PNGs. Record run IDs/screenshots after completion. If blocked/fail, inspect full job log then fix before claiming PASS.

**Trạng thái: PARTIAL — chưa hoàn tất**
