# 2026-11-26 — Jade new six-frame running design integrated in original game

## Owner intent
Use the newly designed Jade six-pose running sequence IN GAME, not another drawing. Must preserve user's prior approved 8-way walk/70px body and one public URL https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . Owner `autocheck:false` reviews actual running; do not self-promote visual art to accepted.

## Source proof
- Actual PRIVATE game contains `art/drafts/jade_run_owner_six_12.png` (480×160, 6×2 native 80×80 RGBA, no background), right source indices 0..5 and whole-body mirrored left 6..11, six new distinct poses from the design in current conversation, NOT reused legacy row/column sprites.
- Editable sources `jade_run_owner_six_right.aseprite`, `jade_run_owner_six_left.aseprite` with native 80px, six timeline cels, 85ms source frame cadence, per-frame draft foot sidecars and separate native 480×80 exports; no runtime limb mixing. GENERATION source helper/private provenance JSON retained in Private. Whole-body paint height73px normalized to existing Jade 70px.
- Reusable `run_review.indices` contract in PRIVATE profile/character supports arbitrary per-fighter source atlas indices and legacy row/column fallback. Real doubletap A+A / D+D physical sprint ≈6.51m/s selects correct 6×2 row. W/S/A/D/diagonal walking, idle, hitbox, camera/physics unchanged.
- PUBLIC `ci/playwright_jade_three_quarter.py` now validates actual screen frame and live six-phase cycle during both real sprints, source-row indices, owner-designed status, active Sprite3D frame, images on the SAME canonical link. It also verifies all 8 walked directions, guard and idle.

## Actual Actions
- [Godot/Windows/Web/Pages #45837312371](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45837312371) SUCCESS (PRIVATE 6c89df6e7cec1f6f68a3d9fe0199a22ee525a592, PUBLIC fa5714e4355ed7027328d042fb62bfe9f2659290). Native print `JADE RUN SIX POSE PASS`: 6+6 native frames, distinct mirrored left, visible70px, no walk regressions. Pages publishing successful on only /physics-v2/.
- [Pinned LibreSprite CLI #45837312555](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45837312555), attempt2 SUCCESS, source PRIVATE bee1173e2dd558f67487ee474d7a464e10077329: all four registered ASE candidates round-trip to pixel-exact PNG, tag, duration and original foot sidecar. Initial FAIL was a legacy hardcoded 100ms in generic draft test despite actual W/S115ms and RUN85ms; fixed properly using per-candidate `duration_ms`, not by changing artwork tempo.
- [Old browser #45836835052](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45836835052) FAIL in unrelated historical Physics V2 timeout; later [#45837687033](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45837687033) passed P1.5/Physics V2/Arcade V2 but failed the new six-phase *per-index waiting test* on A+A after holding movement so long that the physical fighter reached a stage obstacle and properly stopped leg animation. E2E screenshot artifact #15125369222 proves real right run pose, correct new HUD, map visible, while final A+A remained unverified. No game physics bug established from that timeout.
- PUBLIC browser test changed in commit `ddcd9d8cf6fb5a22d885e0e9a0b85dd7a6f88d1b`: sample actual frame states with one requestAnimationFrame loop bounded to 850ms, require observed 0..5 for EACH key; no "hold key for 2s per missing phase" stage-wall condition. [Latest full build #45839072298](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45839072298) in progress at checkpoint write. Must check build/Pages and subsequent Chromium E2E before claiming final browser PASS. No test bypasses: full six live phases still mandatory.

## Remaining
1. Inspect build #45839072298, ensuing exact Chrome run and screenshot artifact for six live phases both A+A/D+D and unchanged other scene tests. Fix actual technical failures using evidence.
2. User tests running visually on ONLY https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . Manual owner artistic acceptance not CI.
3. 8+ independent-authored final run clips and original punch/kick/true idle/source foot signoff remain pending. Final game roadmap unfinished.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## 2026-11-26 latest six-pose integration proof and unrelated W/Physics test repair

- Do not regenerate or overwrite PRIVATE owner-designed art: 480×160 PNG 6 native 80px complete-body RIGHT cels [0..5], mirrored LEFT [6..11], separate editable ASE + foot pivot source already committed to PRIVATE 0dd6c491ac2ce17fb6dd568f853fb127544ce05e; pinned LibreSprite [#45837312555](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45837312555) attempt2 SUCCESS on four real W/S/left/right candidates (walk115ms,run85ms).
- Exact latest [Godot/Web/Windows/Pages #45844347100](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45844347100) **SUCCESS** with PUBLIC de0746f49b17497f03bcecccdfa9d01281e41104 and PRIVATE 0dd6c491. Native Godot log printed `JADE RUN SIX POSE PASS`, 6 genuinely distinct frames each direction, 70px normalized body height, original 8-way walk unaffected, Pages deployed.
- Previous [Chromium #45839451719](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45839451719) **FAIL before Jade test**, unrelated existing Physics V2 W/Z predicate: artifact #15127775589 shows grounded player moved beyond safe Moss z=-13 stage edge while test held real W for up to 10s; terminal z=-56.60/y=-1018.12, airborne. Public commit de0746 *only* changes `ci/playwright_physics_v2.py` to stop at z<-3.2 (safe) and always release W immediately, retains grounded >0.9m real travel + foot pivot + J/K checks. No gameplay motor/scene edits and no test gate disabled.
- New exact [Chromium #45844648520](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45844648520) was running at checkpoint write: must check final Physics V2 PASS and actual `ci/playwright_jade_three_quarter.py` A+A/D+D all six live phases, screen captures and exact SHA before E2E PASS.
- Owner checks only https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . `autocheck:false`: technical build/test does not imply aesthetic acceptance; punch/kick/strict full-source 10-tag still PENDING_ART.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## 2026-11-26 15:09 — Slow-WebGL six-run-pose regression and renderer fix
- Previous Chromium #45844648520 on Pages #45844347100: P1.5 PASS, Physics V2 PASS (climb2.21m/down2.54m), Arcade V2 PASS; Jade D+D strict six-phase check FAIL `rAF=[0,2,3,4,5]` (missing pose1). In-game source genuinely 6×2 native80, velocity6.479m/s, body70px, on floor. Physical-distance-to-frame direct `floor(metres/0.50)` can leap painted body poses under low WebGL FPS; rAF-only collection can also miss a transient frame.
- Fixed **game** in PRIVATE `animation_intent.gd`+`character.gd`: maintain a displayed sequence phase separately from 60Hz distance, advance no more than one next full-body pose per render tick, reset on direction/gait switch; no motor, map, collision, walk or source sprite changes. `review_run_presented_phase_mask` records actual Sprite3D frame selections. Native simulated distance steps `0,2,5,7,11,14` require displayed phases `0,1,2,3,4,5`; PUBLIC `ci/playwright_jade_three_quarter.py` now asserts 0x3F actually selected both A+A and D+D and still demands rAF observations of all six. No weakened checks.
- PRIVATE commits 98f495/34a170/56f2d0/092586, PUBLIC test `77c1aa8b1d9c1230e0c14d3986912b17207abf64`; Godot/Web/Windows/Pages #45846134771 triggered. **Check terminal build and subsequent Chromium results** before claiming E2E PASS. Original source PNG and editable Aseprite unchanged; pinned LibreSprite #45837312555 attempt2 PASS. One user URL https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/; autocheck:false owner visuals and full ten-tag art still pending.

**Trạng thái: PARTIAL — chưa hoàn tất.**
