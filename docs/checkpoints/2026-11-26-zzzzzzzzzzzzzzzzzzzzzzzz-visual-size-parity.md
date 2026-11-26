# 2026-11-26 — W/S Jade apparent shrinking fixed on ONE canonical game link

## Report and source-confirmed root cause
User approved the short-step stance but observed that Jade becomes SMALLER specifically when pressing W/S compared with idle and running. Both sprites are native 80x80 cel grids, but the new 6-cel W/S painted figure occupies only 64 alpha-visible vertical pixels; the old approved idle/run reference is 70 opaque pixels. PixelView had always drawn a full 80px cell and Sprite3D retained old pixel_size; transparent padding caused the visible figure to contract. Not a physics/collider/movement bug.

## Implementation in PRIVATE
- PRIVATE compiled SHA 5c2eb9b810bb0430a853d94d803e629488b05b30.
- `scripts/sprite_foot_anchor.gd` adds reusable alpha-visible body bounds and uniform source-independent scale helper.
- `scripts/character.gd` computes one stable multiplier for each action from the approved fighter reference alpha height. W/S both get 70/64 = **1.09375×** uniform scale; Sprite3D graphic center re-anchors to the physical ground shoe level and restores nominal values on return to idle/run.
- `scripts/pixel_view.gd` draws the SAME clip at the matching scale in 2D. No change to authored pixels, frame order, rhythm, combat/hitbox, world physics, or renderer other actors.
- `tests/three_quarter_preview_smoke.gd` asserts both native 80px W/S sources produce matching opaque standing/side-running height; `scripts/demo.gd` exports source/body-scale metrics for browser telemetry.
- PUBLIC `ci/playwright_jade_three_quarter.py` asserts real W and S motor/clip and same effective 70px painted height, not merely 80px cel dimension.

## Actual technical proof
- [Godot/Windows/Web/Pages #45813542941](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45813542941) **SUCCESS**: PUBLIC 4ca52126f2d6ddd914ae0f23c2ac3eeede7bc70e, PRIVATE 5c2eb9b810bb0430a853d94d803e629488b05b30, native import and W/S visual-height test, Web exports, Pages deployment.
- Real log: `JADE-HEIGHT: action=walk_down standing/run=70 walk-paint=64 uniform-visual-scale=1.09375`; same for `walk_up`; native test `JADE THREE-QUARTER PREVIEW PASS`.
- [Chromium #45813823212](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45813823212) is triggered; check its terminal status, exact published SHA and screenshot artifact before saying Web E2E PASS.

## Handoff
- Owner checks ONLY https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . No new alternate demo route or user-facing query params.
- Browser run needs terminal check; if FAIL, inspect exact job log and repair; do not trust mere Pages success.
- Owner autocheck:false retains sole aesthetic signoff. Full ten-tag editable art source, eight other clips and visual approval remain PENDING_ART; not scope of the body-size fix.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## Terminal browser verification — 2026-11-26
- [Real Chromium #45813823212](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45813823212) **SUCCESS**, PUBLIC pipeline 4ca52126f2d6ddd914ae0f23c2ac3eeede7bc70e, deployed PRIVATE 5c2eb9b810bb0430a853d94d803e629488b05b30 from #45813542941. All test steps PASS: main P1.5, Physics V2 climb2.31m/descent2.39m, Arcade V2 controls, canonical real W/S preview with added painted-body-size parity assertions. Artifact #15113429395 contains new screenshots.
- Native Godot logs verify alpha-painted W/S=64px, old baseline idle/run=70px, corrected uniform scale=1.09375 in both directions. Public E2E checks effective height equals baseline within 1px during true input, in addition to source PCK SHA, physical input and PixelView floor.
- The bug fix is TECHNICALLY DONE and deployed at ONLY https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/; owner aesthetic confirmation still pending under autocheck:false. Full ten-tag fighter library/other Beast features are separately PENDING_ART.

**Trạng thái: PARTIAL — chưa hoàn tất.**
