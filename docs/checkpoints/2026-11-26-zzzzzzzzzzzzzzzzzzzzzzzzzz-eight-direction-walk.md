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
