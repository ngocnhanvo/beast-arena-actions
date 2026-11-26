# 2026-11-26 — Jade A/D/diagonal step pacing vs W/S

## Request and verified cause
Owner accepts 8-way guard and says A/D + diagonals visibly step a bit fast compared with W/S. W/S accepted pace must remain the anchor. Code inspection: ALL inputs use 4.2 m/s physical world speed, diagonals normalized, while ALL 8 previously had 0.30m/pose cadence (14 poses/s). 2D projection anisotropy X32px/m vs Z6.5px/m contributes to apparent horizontal speed. Do not confuse visible sprite rate, physical speed, and projected screen speed.

## Changes and actual source
PRIVATE game compiled SHA 5c229eae1f526834d8e38a6cc9565e835b66e60b; PUBLIC CI test SHA 7b6e31a94ed75d9ffcbdc7a8fb03688167e1c6c9.
- New common `BeastAnimationIntent.review_walk_distance_per_frame(axis)` returns 0.30m W/S, 0.38m A/D, 0.35m all diagonals. At baseline 4.2 m/s: 14 / 11.05 / 12 poses/s respectively. Only visual six-cel sprite pace changed; motor, slopes, running, combat, original whole-body PNG/ASE, foot anchor, 70px painted height remain unchanged.
- PRIVATE character.gd selects review pose using per-direction stride and exposes `review_walk_distance_per_frame_m` via demo debug state; native Godot W/S/A/D/four diagonals check EXACT rates.
- PUBLIC `ci/playwright_jade_three_quarter.py` asserts physical world velocities, exact eight-way per-pose distance, figure scale, sprite source/mirror, and live screenshots at SINGLE canonical `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/`.

## Build evidence
- [Godot/Windows/Web/Pages #45819228268](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45819228268) **SUCCESS**, source 5c229eae1f526834d8e38a6cc9565e835b66e60b, pipeline 7b6e31a94ed75d9ffcbdc7a8fb03688167e1c6c9; real Godot logs `JADE-WALK-PACE W/S=0.3m/pose, 14.0fps; A/D=0.38m/pose, 11.05fps; 4 diagonals=0.35m/pose, 12.0fps`, followed by successful native smoke, export and Pages deployment.
- [Live Chromium #45819571675](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45819571675) **PENDING at initial checkpoint** — inspect exact terminal job, eight-key gate and screenshot artifact; do not claim browser pass prematurely.

## Lessons and remaining
- Same world movement velocity can look very different in a 2D perspective projection; do not silently rewrite player speed just to adjust leg pose tempo. If owner later reports SCREEN TRANSLATION is too fast, that is a separate design review of physics/camera, not a clip timing patch.
- `autocheck:false` owner visually reviews the change; independent sideways/diagonal source art and full ten-tag fighter animation remain PENDING_ART. One owner-facing URL only.
- Next: verify live Chromium, append artifact and exact source SHA, preserve documented technical vs artistic status.

**Trạng thái: PARTIAL — chưa hoàn tất.**
