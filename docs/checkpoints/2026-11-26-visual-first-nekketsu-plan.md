# Beast Arena Actions — visual-first checkpoint
Date 2026-11-26 — **PLANNING / NO NEW WEB BUILD OR CAMERA STYLE PATCH**.

## Trigger and interpretation
- User reports `vẫn nghiêng` and supplies Google Images collage of Nekketsu Kakutō Densetsu references, requesting planning for fix and future features. Images are visual style references, **not browser captures of Beast Arena** and not licensed assets.
- Prior source `cf634df` fixed camera dynamic orientation and parser; public pipeline commit `5b9fceb` updated CI. Direct GitHub job checks this session: #45676762869 preflight/build/Pages **SUCCESS**, #45677121093 browser-smoke **SUCCESS**.
- Prior JSON checkpoint: camera Euler pitch -37.405356819751°, yaw/roll 0°, angle drift <=0.10° during movement/ramp/map switching, physical Y remains correct.
- Yet user has NOT visually approved the camera perspective. Mark visual issue **OPEN**; do not equate `camera_projection_locked` with correct Nekketsu look. Hypotheses: too-steep fixed oblique view, route/cache build mismatch, art/mesh projection. Causes still unverified.

## Planning changes
- PRIVATE plan: `beast-arena/docs/plans/NEKKETSU_VISUAL_FIRST_2026-11-26.md`; private `ROADMAP`, `ART_PIPELINE`, `START_HERE`, `ENGINEERING_LOG` updated.
- PUBLIC `docs/CI_PLAYWRIGHT_RUNBOOK.md` and `docs/START_HERE.md` updated to require visual pixel-art comparison and debug build ID, without weakening existing physical camera/ramps regression tests.
- No runtime code or new original pixel art delivered. No new CI/Pages/Playwright run is claimed for these documentation edits. **Status: PLAN COMMITTED / V0 NOT ACCEPTED.**

## Priority order (must not reorder without user request)
1. V0 diagnose apparent level tilt from correct route/build/screenshots, fix orthographic 2.5D visual framing/projection while preserving real 3D physics.
2. V1 original NES-inspired pixel-art contract and examples, scale + no jitter.
3. V2 one original polished scrolling map with real ramp/obstacle height and editor alignment.
4. V3 one original chibi human fighter with complete base animation, then distinct second stage and more humans.
5. V4 real human 2v2 combat timing, boxes, AI, KO, feedback, tests.
6. V5 original human/beast transformation after visual/combat baseline.

## Future verification gate
Deployed source SHA + route/cache proven; Godot headless tests + Pages + Chromium E2E *and* screenshot comparison against original approved look. Sample flat move/vertical depth move/up/down physical ramps, both maps, far camera, human sprite scale; assert no entire-stage image tilt/shimmer. User visually signs off. Preserve staging vs P1.5 main. Update both checkpoints after every later code change.

Prior verified runs:
https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45676762869
https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45677121093
