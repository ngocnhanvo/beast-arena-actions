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
