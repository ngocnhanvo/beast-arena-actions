# Public Actions checkpoint — fixed Physics0 camera projection

Date: 2026-11-26.
STATUS: SOURCE FIX / PLAYWRIGHT ASSERTIONS COMMITTED; LIVE TEST PENDING.

Problem: map seems to rotate when player walks, especially over
height gradients, despite correct 3D collision geometry.

Observed: old game script called `camera.look_at(focus)` per-frame
immediately after a smoothed camera follow translation. The difference
in update rates changes camera orientation. This is an inadvertent
render/camera bug, not a deliberate terrain feature.

PRIVATE functional game code: `d5bec34b89c406fe019d17fddfa0829fa7b14bd2`.
PUBLIC E2E script: `e18cf4134e35fbba1774de60ba412ef61522485b`.

Fixed: camera orientation set from fixed offset only on reset,
per-frame camera position smoothly translates without any rotation.
E2E telemetry includes pitch_deg/yaw_deg/roll_deg; asserts <=0.10°
drift during walking, uphill/downhill, map change and teleport.

Build run: https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45676396568
Status at checkpoint creation: not verified yet. Check build/Pages
and downstream browser run, actual logs/telemetry and screenshots
before labeling VERIFIED.

Older source verified slope visibility: CI #45673586733 and
Chromium #45673951103 (Moss +2.14m, Docks -2.39m).
Keep old root P1.5 unchanged, test only staging
https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/


## FINAL VERIFIED — Camera no longer tilts the world (2026-11-26)

- PRIVATE game functional source SHA `cf634df49426bdd893bdd674492424b4ef9d1121`.
- PUBLIC Actions run head SHA `5b9fceb5b576b9c2a5910df869214271f62e8916`.
- First public build #45676396568 FAILED on syntax error in new game telemetry dictionary; detected strict Godot import. No Pages deploy. Patched missing comma in `cf634df`, then triggered fresh build.
- Godot import/physics/map/collision/export + Pages run **#45676762869 SUCCESS** on exact game SHA.
- Chromium browser tests **#45677121093 SUCCESS** for legacy P1.5 and new V2. Downloaded `beast-arena-browser-screenshots` and inspected `physics-v2/result.json`:
  - `status=PASS`, `camera_projection_locked=true`.
  - Camera reference pitch `-37.405356819751°`, yaw `0°`, roll `0°`; Playwright assertions guarantee drift <=0.10° at each walk/ramp/teleport/stage switch checkpoint.
  - Moss player climbed `2.137m`, Night Docks descended `2.476m`, flat dx `4.035m`. `page_errors=[]`, `critical_asset_failures=[]`.
- Staging https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ verified. Original P1.5 root remains unchanged.
- **CAMERA TILT REGRESSION CLOSED.** Smoothed camera POSITION is supported, per-frame angle changes are not. Preserve angle telemetry/acceptance tests.
- Evidence: https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45676762869 and https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45677121093
