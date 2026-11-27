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
