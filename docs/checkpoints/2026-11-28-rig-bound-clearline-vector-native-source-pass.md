# 2026-11-28 — Rig-bound clearline v2 exact private artwork source QA

## Source-pin and terminal outcome
Public isolated workflow `.github/workflows/rig-bound-clearline-native.yml` branch `ci/rig-bound-clearline-v2-native-qa`, tested workflow SHA `f04071ca9b55d1835824c4fcc4392dd46553fa66`. Transient checkout of exact PRIVATE source code/art SHA `f0bbac7c1e707946d115f26b44169570d4f42639` from `ngocnhanvo/beast-arena` Draft branch `feat/rig-bound-clearline-v2-native-qa`. Does NOT publish private source, SVG/PNG, GIF or artifacts.

[GitHub Actions #46046387150](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46046387150) **COMPLETED SUCCESS**, job `140666594810` **COMPLETED SUCCESS**, actual logs inspected.

## Exact checks
1. `BEAST_CLEARLINE_PORTABLE_27_TESTS_PASS`: 27 independent positive/adversarial tests for original FK/IK 6-phase motion and six original smooth-line vector art SVG sources. Source binds per-frame SHA-256 of `pose-contract.json` with permanent RIGHT/LEFT arm/leg identity; F2→F3 and F5→F6 ownership, fixed bone length and world-space stance foot validated.
2. `BEAST_CLEARLINE_NATIVE_4_TESTS_PASS`: four project-specific independent native tests including corrupt SVG fingerprint, faked art owner approval, source overwriting and 15-layer/gear-slot integrity. 31/31 total.
3. `BEAST_CLEARLINE_GIT_SVG_ALL_6_EXACT_RIG_AND_GIF_24_PASS`: actual six SVG in private Git tree byte-identical to rerendered `motion_rig.pose_at` source at exact SHA; all six pose JSON identical and 24-frame GIF reexports.
4. `BEAST_CLEARLINE_NATIVE_15_LAYERS_6_CELS_14_EMPTY_GEAR_PASS`: original smooth 480px vector art rasterized to separate 80px editor compatibility, 14 genuinely empty gear slots, 15 native ASE layers and six ORA.
5. `BEAST_CLEARLINE_OFFICIAL_LIBRESPRITE_PIXEL_EXACT_PASS`: official pinned LibreSprite 1.3 independent native ASE sheet re-export has **bitwise identical RGBA bytes** to exact source 480×80 neutral raster atlas. This is not merely codec read/write self-test.
6. `BEAST_VECTOR_CLEARLINE_GODOT_480PX_IMPORT_PASS_6_CELS`: pinned Godot 4.7.2 isolated source import of high-res 480px RGBA cels with linear filtering. This is **NOT** the actual game gameplay/Web E2E.

## Artistic and release boundaries
Artwork uses clean line vector / cel shading per owner request and is materially more coherent than old mannequin. Still visually under-polished at compressed/rear-leg phases. PRIVATE `pose-binding.json` reports `visual_self_review=FAIL_NOT_PRODUCTION_QUALITY`, `art_release=BLOCKED`, `gameplay_e2e=NOT_RUN`. Owner visual acceptance has not been granted. Do not equate technical CI with art PASS. Both PRIVATE and PUBLIC branches must stay draft/unmerged. No game/Pages deploy, no Jade/physics modifications, no production costume system.

Next: self-review/edit actual rig-driven art, preserve documented contact and source hash; then rerun exact source native and actual game motor/Web E2E; obtain owner art acceptance before merging or releasing. Keep this pinned checkpoint in both repos.

**Trạng thái: PARTIAL — chưa hoàn tất.**


## Latest terminal run — world-space rendered foot-lock QA

Source-only extension, not a game Pages deployment. In-place animation with fixed root can visually resemble foot skating even if world-toe mathematics are fixed; an independent review picture must include character root displacement and a fixed world floor. The PRIVATE exact code now emits 24-frame `vector_world_motion_24.gif` and `world-contact-trace.json`, and its test asserts **actual review pixels** for RIGHT stance at X=510/Y=432 and LEFT stance at X=690/Y=432, constant within each support interval. These coordinates are in the temporary 1200×480 review canvas.

**Final pinned evidence:** PRIVATE exact code SHA `eaa64cfa19201d639f3a631d7a5bea586d89a62a`, PUBLIC workflow SHA `8ae130d00f162e7f3a51544630b4caa2d0b7bac1`. [GitHub Actions #46047066962](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46047066962) **COMPLETED SUCCESS**, job `140668853271` COMPLETED SUCCESS; logs `BEAST_CLEARLINE_PORTABLE_28_TESTS_PASS`, `BEAST_CLEARLINE_NATIVE_4_TESTS_PASS`, `BEAST_WORLD_MOTION_VISIBLE_BOTH_STANCE_FOOT_LOCKS_PASS`, source SVG exact rerender PASS, official LibreSprite native strict RGBA PASS, Godot 4.7.2 isolated 480px source import PASS. Source-code tests total 32/32. Earlier 31/31 successful #46046387150 was before the world-motion test and is superseded.

Nothing from this PRIVATE art is stored in the PUBLIC repo or published to Pages/Artifacts. Actual gameplay/physics/Chromium E2E and owner art review are still blocked; source marks `FAIL_NOT_PRODUCTION_QUALITY`, release `BLOCKED`. No merge/deploy, Jade/physics unmodified.

**Trạng thái: PARTIAL — chưa hoàn tất.**


## Latest terminal v3 — corrected articulated load, flight and rear recovery

PUBLIC tested workflow SHA `976155e03991f05e8da517196b0f005830f52476` pins exact PRIVATE source/art SHA `d07fc8ac6fd13b40f1cb3a3d8f864f6257cbe8a3`. [GitHub Actions #46048568171](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46048568171) **COMPLETED SUCCESS**, job `140673881390` **COMPLETED SUCCESS** (log independently inspected). The actual Private art has revised rig biomechanics: load frames 2/5 hip visually drops; flight frames 3/6 hips rise; the forward knee does not exceed pelvis height and the rear recovery shin folds instead of dragging. All six committed SVG bytes and canonical pose-contract/source binding are exactly reproducible from the same time-continuous FK/IK source.

New external-pose adversarial gates: `LOAD_HIP_FAILED_TO_DESCEND`, `FLIGHT_HIP_FAILED_TO_RISE`, `FRONT_FLIGHT_KNEE_ABOVE_PELVIS`, `FRONT_FLIGHT_TOE_UNNATURALLY_HIGH`, `REAR_RECOVERY_SHIN_NOT_FOLDED`; dense 601 samples check joint teleport. Real CI shows `BEAST_CLEARLINE_KNEE_BOB_RECOVERY_VISUAL_GAIT_GATES_PASS`, `BEAST_CLEARLINE_PORTABLE_34_TESTS_PASS`, `BEAST_CLEARLINE_NATIVE_4_TESTS_PASS` (38/38), exact six SVG source rerender+world foot contact PASS, official LibreSprite 1.3 bitwise ASE RGBA PASS, Godot 4.7.2 isolated 480px import PASS.

**Scope remains source QA, NOT gameplay acceptance**: artifact is still `FAIL_NOT_PRODUCTION_QUALITY`, `art_release=BLOCKED`, `gameplay_e2e=NOT_RUN`. No live-game motor collision verification, Web/Chromium tests, owner art signoff, native production cutover, Pages deploy or merge. No private artwork uploaded to PUBLIC repo or artifacts. The older #46047066962 32-test run remains historical; this 38-test run is the latest verified one. Follow exact PRIVATE checkpoint for next art revision.

**Trạng thái: PARTIAL — chưa hoàn tất.**


## Latest 2026-11-28 terminal source-browser QA (not deployed game E2E)

PUBLIC tested exact runner SHA `c68429c62d901f4035318446a9509b750f6acbff` with pinned PRIVATE art/SVG/tool SHA `08b3f6b512679e1227738723be56be1667c8e8ad`. [GitHub Actions #46049081789](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46049081789) **COMPLETED SUCCESS**, job `140675614164` SUCCESS. Official 38/38 Python source+native tests, original SVG/pose byte-perfect rerender, LibreSprite 1.3 native exact RGBA and Godot 4.7.2 480px isolated import still PASS.

**New**: install pinned Playwright 1.56/Chromium on the standard Ubuntu runner and exercise a PRIVATE source-only canvas preview. Browser renders all six original rig-derived 480px frames with distinct canvas bytes, steps Next/Previous across 6→1/1→6 correctly, reports no JavaScript errors. Logs `BEAST_CHROMIUM_6_SOURCE_FRAMES_VISIBLE_BUTTON_WRAP_PASS_GAMEPLAY_NOT_TESTED`. PRIVATE screenshot files remain transient in runner temp; they are **not uploaded to PUBLIC GitHub**. This is a source preview and **NOT** the Godot game E2E, production PCK, physics motor or a deployed Pages check.

Art remains `FAIL_NOT_PRODUCTION_QUALITY`, release `BLOCKED`, owner signoff absent; Private PR #18, Public Draft PR #17 still unmerged. The previous #46048568171 is historical (before browser gate). Next: actual game staging motor and Web/Playwright E2E only after new visual source quality review; do not claim source/browser smoke is game deployed.

**Trạng thái: PARTIAL — chưa hoàn tất.**


## 2026-11-28 v4 latest verified CI — oriented knee solution and rounded SVG forms

Exact PRIVATE tested original rig/Skill/art SHA `3d00e95bfcb31942840c8e990d5cf866e8a7be6a`, PUBLIC workflow tested SHA `a3a94c61942457fde3f2de9eb0b8899c26c6f9d8`; [GitHub Actions #46051334378](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46051334378) **COMPLETED SUCCESS**, job `140683111724` **COMPLETED SUCCESS**.

Observed root issue was a knee IK branch flip at the trailing ankle crossing hip height. The PRIVATE engine-neutral Skill now uses one oriented branch and tests the signed solution continuously, including a malicious external-pose wrong-side knee. Actual original artwork six editable 480px SVGs and 24 interpolated motion samples regenerated from the exact rig; fists and swing feet are smooth rounded curves rather than detached rectangles/fins. The new source manifest remains explicitly ART BLOCKED.

Actual runner logs: `BEAST_V4_ORIENTED_IK_REAR_KNEE_CONTINUITY_PASS`, `BEAST_CLEARLINE_PORTABLE_37_TESTS_PASS` plus `BEAST_CLEARLINE_NATIVE_4_TESTS_PASS` = **41/41** Python rig/native tests, six committed SVG byte parity, world visible support-foot lock, official pinned LibreSprite independent strict ASE RGBA source re-export PASS, isolated Godot 4.7.2 original 480px atlas import PASS, `BEAST_CHROMIUM_6_SOURCE_FRAMES_VISIBLE_BUTTON_WRAP_PASS_GAMEPLAY_NOT_TESTED` PASS.

PUBLIC workflow contains no PRIVATE SVG/PNG/ASE/GIF or screenshot artifact. This verifies **source/native/browser-source QA** only. Actual fighting-game motor/Web gameplay E2E, owner artist review, 8+ approved frame gameplay clip, Pages deploy/merge remain NOT DONE. PRIVATE `visual_self_review=FAIL_NOT_PRODUCTION_QUALITY`, `art_release=BLOCKED`. Older CI #46049081789 is superseded, not invalidated.

**NEXT:** Continue original rig-driven actual vector art review and eventually staged Godot fighter motor+Chromium in-game E2E, preserving public/private boundary. No unattended release of unfinished art.

**Trạng thái: PARTIAL — chưa hoàn tất.**
