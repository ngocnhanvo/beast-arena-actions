# Public Actions checkpoint — Original pixel-human 2v2 gameplay candidate

**Date 2026-11-26 — Overall status: PARTIAL / source committed, NO NEW CI/Pages/Playwright proof.**

## Current repositories / exact checkpoint
- PRIVATE beast-arena source head after PRIVATE checkpoint commit: `844ec06b2c8c1aac956368f45c141518f5f3a609`. Read `docs/checkpoints/2026-11-26-v3-v4-human-combat-source.md` in PRIVATE first.
- PUBLIC Actions source head before this checkpoint: `d5011d448de6828df3f212402e79a8d89037b12b`; latest functional public test commits `b7c5b792236171202bef481c7256a329ff88075f` browser, `85bf3272db250073c5cc40cf62b5ec04daad1b33` headless 2v2 and `5533be3` syntax preflight. Do not confuse docs HEAD with code tested.
- Previous known PASS was #45676762869 Godot/Pages + #45677121093 Playwright on original steep-view source `cf634df`. It says NOTHING about newer V0-V4 source.

## CI code that actually changed
- `.github/workflows/build.yml` now stamps exact private source SHA, public Actions SHA and numeric run ID into the isolated `scripts/build_version.gd` before strict import; all identifiers safe/public. An earlier printf newline-escape mistake was fixed in `4f2c3a0`; inspect the latest file.
- Build must run `physics_smoke.gd`, `map_editor_smoke.gd`, `obstacle_collision_smoke.gd`, `visual_smoke.gd`, `combat_v2_test.gd` and `combat_scene_smoke.gd` on separate Physics0 project, plus legacy P1.5 tests, before exporting both Web variants and publishing Pages.
- `ci/playwright_physics_v2.py`: verifies exact SHA, shallow camera pitch and world horizon/noYbob, original Moss+Docks pixel textures/meshes/facades, 4-direction × 20 row human atlas, J animation tied to attack request, physically real slopes on both maps, and opt-in C-triggered AI round with actual HP loss and human-only 2v2 screenshot.
- `ci/validate.sh`: preflights Python syntax with `python3 -m py_compile`, not just shell+secret grep.
- Public browser artifact expected: `beast-arena-browser-screenshots` with `playwright-report/physics-v2/result.json`, `moss-start.png`, `moss-light-preview.png`, `moss-human-2v2.png`, `docks-high-platform.png`, slope entry/mid screenshots and other scene frames. These artifacts have **NOT** been observed for latest source.
- Browser must never publish private raw game source or unlicensed Nekketsu assets. All four human atlas colorways are independently authored; same silhouette/palette variants only, not four finished fighters.

## Gate table
| Phase | Status | Outstanding acceptance |
|---|---|---|
| V0 shallow camera | CODE PRESENT | Current deployed source SHA, screenshot/horizon/user visual approval |
| V1 original pixel art | CODE PRESENT | Real Godot Web SVG/nearest rendering, sprite size & frame screenshots |
| V2 two map templates | PARTIAL CODE | Editor usability, polished map art/foreground, collision/UV and camera E2E |
| V3 80-frame human art, 4 palettes | SOURCE PRESENT | Real animation Web E2E, distinct silhouettes, polished animation |
| V4 2v2 human combat code | SOURCE PRESENT | Godot headless, Playwright real HP, more hitboxes/guard/grab/AI and full match |
| V5 beast transformation | NOT STARTED | Do only after V0–V4 acceptance |

## Confirmed blocker / next action
GitHub connector in this chat can fetch workflow jobs only for known run IDs, not list newest runs/dispatch. Web opening GitHub public Actions returned DisabledError and network DNS failed for api.github.com. Therefore **not possible to truthfully assert any new CI/build/Pages/browser PASS here**. Public `build.yml` automatically triggers on public workflow/test pushes and hourly checks; scheduled intent is not actual success.

NEXT: find the next run at https://github.com/ngocnhanvo/beast-arena-actions/actions/workflows/build.yml, inspect exact source SHA and failing steps, fix/build until green; then separate Chrome Web E2E and visual screenshot review, update both repos START_HERE/ENGINEERING_LOG/checkpoints and preserve current P1.5 root. Do not ship unapproved V2 migration. Existing task automation `6b072e50a28c81918b45f9359c805ce7` was checked active with next scheduled 03:00 +07 on 2026-11-26.

**Trạng thái: PARTIAL — chưa hoàn tất**


## Original 2v2 health bars (source update)
- PRIVATE `b8bf2e5` to `da1313e`: four screen-space color-coded original HP bars, width from `BeastCombatState.health` and debug `hud_hp_bar_px` for each human. PRIVATE source before docs update includes `da1313e44ada873febdddcdeda4b59e05f1b3868`.
- PUBLIC `916750336fad01213e9ef43ff72450df3ffc6dfd`: Chromium after C 2v2 AI checks all four visual HP fills against actual state (<=3.5 px difference). Screenshot `moss-human-2v2.png` needed for color/layout quality.
- Still **NO VERIFIED new CI/Web run**, no visual acceptance; prior PASS IDs are old source only. Required next action unchanged: inspect newest build run and actual browser screenshots, fix errors, update checkpoint.


## 2026-11-26 — Actual CI failure recovered, rerun necessary
- **OBSERVED** latest public push workflow run #45681701357 `failure`; preflight PASS, Godot strict import PASS, Physics0 `physics_smoke.gd` PASS, then `map_editor_smoke.gd:84` FAIL `SCALE-01: sprite vs viewport is inconsistent: 1028.57144389834`. Pages job SKIPPED and browser E2E skipped. Exact failing build job #139443703361.
- **Root cause:** old art scale test counts entire 20-row animation atlas texture rather than the 64-pixel-height current frame. PRIVATE source `c7c408873102731bf00514c7d2d076857c167c62` now divides `texture.get_height()` by `Sprite3D.vframes` before projection. Expected ~51.43 pixels at 960×540 orthographic size 16.8. The previous failure is NOT an actual 1028px fighter, and is not to be hidden by weakening the true 50–59px visual contract.
- **NEXT** this new Public docs commit (WITHOUT skip-ci) intentionally triggers normal build workflow to check the corrected PRIVATE head. Inspect run, source SHA, all subsequent tests, Pages and Chromium. Fix following failures in order; no success claim for this checkpoint yet.
