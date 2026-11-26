# 2026-11-26 — Eight-direction Jade walk, one owner URL

## Request and existing artifact
Owner accepts the short-step Jade guard W/S gait and the 64→70px visible-height correction, and asks to apply the same animation to A, D and diagonals W+A/W+D/S+A/S+D. Do not generate unrelated image assets or separate demo links. One URL only: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ .

## Source and pipeline
- PUBLIC code `dbb3d32b3413ff297d68996f22a8e78ca8f68b66`, PRIVATE compiled source `0d2d2bdfbccd3a331062aaeb7ee402774b3ecba0`.
- PRIVATE reusable movement selector chooses source W/S for full-body 6×80px authored two-clip draft and mirrors complete cell for leftward movement. Actual direction semantic remains `walk_left`/`walk_right` for side and diagonals; underlying physical X/Z movement does not get faked. No new separate 6 art strips drawn. Double-tap run and attack remain independent.
- PRIVATE `pixel_view.gd` restores CanvasItem transform after full-cel mirroring; same facing and alpha-normalized 70px fighter body as Sprite3D; shoe pivot/physics unchanged.
- PUBLIC `ci/playwright_jade_three_quarter.py` now demands EIGHT real physical inputs W, S, A, D, W+A, W+D, S+A, S+D. Each input tests expected actual world velocity in both axes where applicable, correct semantic named tag, correct W/S reused source, complete frame mirror flag, native 80px cel, 70px visible-height parity and advancing animation frame; captures one screenshot per direction on same canonical route.

## Verifiable run state
- [Build, Godot, Web, Windows, Pages #45815352430](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45815352430) **SUCCESS** (actual source 0d2d2b, pipeline dbb3d32, source test printed `JADE THREE-QUARTER PREVIEW PASS: 8 WALK compass inputs from two 6-cel 80px sources`, Pages deployed).
- [Exact Chromium #45815615697](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45815615697) **IN PROGRESS AT CHECKPOINT CREATION**; follow the job result and exact screenshot artifact, fix any failure. Never label browser PASS merely because Pages has deployed.
- Previous browser #45813823212 PASS belongs to earlier W/S-only revision and is not proof of 8-direction gameplay.

## Next / limitations
- Read #45815615697 terminal status and page screenshots, including PixelView floor. If any browser test fails, fix, rebuild and rerun; record actual SHA and job ID.
- Only two 6-frame whole-body W/S editable original candidates exist and are reused/mirrored. Genuine independently authored lateral/diagonal animation sheets, final foot pivots and the complete ten-clip four-fighter Beast Arena remain PENDING_ART. Autocheck:false requires owner visual approval.
- Owner can inspect exclusively at https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ after verifying deployed SHA.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## 2026-11-26 — 8-way Playwright attempt-2 failure diagnostic and isolated retry

- Initial exact Chromium run [#45815615697](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45815615697): attempt 1 FAIL in old Physics V2 test when first J input had no observed attack; attempt 2 PASS for main game, Physics V2, Arcade V2. **New 8-way Jade test still FAILED before S+A**, after successfully capturing W/S/A/D/W+A/W+D screenshots.
- Retrieved real attempt-2 artifact #15116556189 (`jade-34/result.json`): at terminal timeout the player was `x=-40.10, z=28.92, y=-2111.74, grounded=false, human_visual_gait=airborne`. E2E had held the S+A input while waiting 15 seconds for a condition that did not become true, leaving the playable stage; this is NOT evidence that the first 6 directions or 3D native clip rendering failed. Exact cause of missing S+A predicate is not proven. Repeated A/D taps may cause true double-tap sprint (16 physics ticks) and is a *hypothesis*, not a verified root cause.
- Public `ci/playwright_jade_three_quarter.py` committed fix `5d1462b086ee1f8b2867d18cf8c87ffce05fa3c9`: give >16 ticks (340ms) between keys, teleport via existing `R` to actual safe ground before every one of 8 cases, assert player grounded/near stage/velocity stopped/no sprint, lower direction predicate timeout to 5s, print failing label and full read-only Godot telemetry on failure. No game source/physics/visual changes; no test bypass.
- New real pipeline [#45817043378](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45817043378) is pending at checkpoint update, must verify matching PRIVATE `0d2d2bdfbccd3a331062aaeb7ee402774b3ecba0`, new PUBLIC `5d1462b086ee1f8b2867d18cf8c87ffce05fa3c9`, native PASS, Pages PASS, then fresh Chromium run and 8 actual inputs. Owner link stays unchanged.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## Final verified evidence — 2026-11-26

- [Godot/Windows/Web/Pages #45817043378](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45817043378) **SUCCESS**; compiled PRIVATE SHA `d56c61d9539303cf50c81972e5c134883f896140`, pipeline PUBLIC SHA `5d1462b086ee1f8b2867d18cf8c87ffce05fa3c9`. Native 8-compass-direction art test PASS.
- [Real Chromium #45817369199](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45817369199) **SUCCESS**, ALL four tests PASS (P1.5 dx220.5; Physics V2 up2.23m/down2.33m; Arcade V2 combat and run; Jade W/S/A/D/W+A/W+D/S+A/S+D). Exact build run ID and source SHA verified in live PCK.
- [Screenshot artifact #15115119696](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45817369199/artifacts/15115119696) has nine Jade screenshots (idle + eight directions), `jade-34/result.json` with `PASS_TECHNICAL_OWNER_ART_PENDING`, 8 unique physical X/Z velocity directions (cardinals ±4.2m/s, diagonals ±2.97m/s), correct `walk_left_guard`, `walk_right_guard`, `walk_up_guard_front`, `walk_down_guard_front` semantic intents; two W/S original sources selected and full-cel mirror flags correct; all normalized painted fighter heights = 70px.
- Prior browser #45815615697 FAILED (attempt1 old J keyboard flake, attempt2 eight-way test held S+A until Jade wandered off the map). This is documented, not erased. Public test-only fix 5d1462 adds real stage-R reset and >16 tick doubletap separation between each of 8 directional probes, without weakening game/physics assertions. New complete exact build/E2E succeeded.
- ONLY owner game link: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . Eight walking inputs now technically implemented and deployed. Original 8 unique directional art sets and full ten-tag fighter archive remain PENDING_ART, owner visual signoff must be manual under `autocheck:false`.

**Trạng thái: PARTIAL — chưa hoàn tất.**
