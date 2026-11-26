# 2026-11-26 — Jade eight-pose 4+4 run integrated as owner review pilot

## User goal
Replace visually broken six-pose last-to-first leg reversal with eight full-body run poses organized as two four-phase leg cycles. Preserve existing walking, 3D motor and camera. Only one owner URL: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . autocheck=false: owner—not CI—judges art.

## PRIVATE implementation
- New 640×160 RGBA eight RIGHT cells and eight mirrored whole-body LEFT cells. Paths: experiments/physics_v2/art/drafts/jade_run_eight_16.png, jade_run_eight_right.png/.aseprite/.foot.json, jade_run_eight_left.png/.aseprite/.foot.json, jade_run_eight_16.json. All cells native 80×80. Old six art retained (not removed).
- Per-fighter run_review profile now 8+8 indices, stride 0.50m, 85ms source hold, foot reference y74. Generic CharacterBody3D visual renderer accepts even frame counts and authored foot baselines; runtime never splices limbs.
- Native three_quarter_preview_smoke.gd now asserts eight distinct full-body cells per direction, 7→0 wrap and 3→4 half-cycle seam, RGB/alpha mirror, 70px silhouette parity; 8 walking directions unchanged.
- Registered editable eight-frame candidates in candidates.json; removed duplicate historical SIX tags from active registry, preserving their original files.
- Game HUD shows RUN: 8 PHASES (4+4) / OWNER REVIEW.

## PUBLIC tests
- ci/playwright_jade_three_quarter.py requires exact pipeline+build SHA and real A+A/D+D, eight visible rAF phases each direction, Sprite3D selected-phase bitmask 0xFF, atlas 8×2, source index 0..7 / 8..15, screenshots and full walking/physics/Arcade gates.
- Public build initial runs #45856559025 and #45856647084 started after test changes. Check latest run; do not reuse old six-frame PASS.
- Actual pinned LibreSprite roundtrip is required for both new eight-frame Aseprite sources. Read art-toolchain run results.

## Still pending
- Source original sprites designed/generated for review, NOT owner-art-approved. Distinct eight hashes do not prove anatomically correct opposite-leg pairs; frames0/4 may appear too similar. Owner assesses real 4+4 foot inversion, torso/arm exchange, 7→0 seam. Native pivot sidecars y74 still labeled review_required.
- Full original ten-clip art source (punch/kick/idle) not completed.
- If art feels wrong, redraw full-body contact/passing poses in editable .aseprite; never do runtime cropped-limb patch. Re-test.

## Handoff
1. Verify native build/Pages #45856559025/#45856647084 SHA and results.
2. Inspect exact Chromium browser run with screenshots and all eight phases.
3. Verify LibreSprite batch export and PNG pixel parity for source right/left.
4. Owner reviews one canonical /physics-v2/ game link; update two repo checkpoint + engineering log.

Trạng thái: PARTIAL — chưa hoàn tất.

## 2026-11-26 — Actual WebGL failure and post-draw renderer correction
- Prior newest build/Pages #45856928823 succeeded on PRIVATE d486f06e and PUBLIC 4cd8373. Pinned REAL LibreSprite #45856928793 SUCCESS for both 8-cel left/right ASE sources and all existing walk candidates.
- Chromium E2E #45857553417 FAILED the actual run gate (not a compile issue): D+D rAF captured only [2,4,6] while _process selection mask=127 (0..6), real 8x2 atlas, ~6.48m/s physical sprint, 70px body, eight walks/P1.5/Physics/Arcade PASS. This proves the old internal selected mask is not enough to establish drawn WebGL frames.
- Runtime fix PRIVATE b074b377 / 37766233: track actual RenderingServer.frame_post_draw callbacks for each Sprite3D full-body pose; require >=2 genuine drawn frames before advancing source-timed 85ms running phase; record drawn mask and chronological 64-entry history. Reset on action changes. No movement/collider/pivot/map/attack changes.
- PUBLIC test 6b43d5d: must see actual GPU post-draw mask=0xFF and complete ordered [0,1,2,3,4,5,6,7] + wrap [7,0] both A+A/D+D; rAF sampled frames are diagnostic (may under-sample engine draws), not sole proof. Exact source/build SHA retained, strict P1.5/Physics/Arcade/walking gates unchanged.
- New full build #45858816783 queued at checkpoint; require terminal Godot/Web/Pages and exact Chromium before technical PASS. Owner autocheck:false must still assess anatomical 4+4 leg symmetry and overall look; source 8+8 uniquely drawn pilot is not yet art accepted.
**Trạng thái: PARTIAL — chưa hoàn tất.**
