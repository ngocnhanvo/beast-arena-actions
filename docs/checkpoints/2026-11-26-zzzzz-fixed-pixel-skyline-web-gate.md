# Beast Arena — Original Pixel 2D flat skyline on true slopes, new release gate

Date: 2026-11-26

**TARGET GAME SOURCE**: PRIVATE `b06e131c955f09e50593d890244e8fbe47b44dc2` (only docs updates since actual functional `8ae3fc37` skyline and `dc14a7b6` acceptance-test commits). PUBLIC pipeline must record exact build run and source SHA in Godot and Chromium telemetry.

## Problem / code correction
- Existing F5 pixel 2D `pixel_view.gd::_draw_facade()` previously set distant panel Y to `173.0 - (map.height_at(wx)-datum)*12`, tilting/stair-stepping the *distant* backdrop vertically as scenery crosses the actual slope. That contradicts the user's fixed horizontal Nekketsu-like skyline requirement despite a fixed 3D camera.
- Game source `8ae3fc37` now draws every original distant facade at `FACADE_SKYLINE_Y = 173.0`, independent of world-X ground elevation; keeps **true physical floor height, floor UV spans, retaining faces, player contact slopes, collision and 60Hz combat unchanged**. Background scroll remains X-only.
- `tests/pixel_projection_smoke.gd` `PRES-12` `dc14a7b6` asserts BOTH original maps (Moss uphill, Docks downhill) have >=1m real world-Y change while their pixel facade top stays equal at 173px.
- Also contains prior J/K player-only late recovery chained human attack from private source `0af48c8`.

## Prior VERIFIED actual CI/browser evidence — earlier source only
- V4 combo compiled PRIVATE `0af48c8`, build+Pages [#45742647411](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45742647411) SUCCESS on public `95281046`.
- Real Chromium [#45742922283](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45742922283) SUCCESS, *matching published PCK/build identity*: P1.5 PASS dx=213.5; Physics V2 PASS Moss climb 2.29m, Docks descent 2.37m, true contact angle >=10deg, dx=14.05m. Screenshot artifact ID 15082550219. Thus 60Hz combo + corrected E2E contract are in verified build. **That build does NOT include the new skyline correction.**
- Earlier #45742273520 browser FAILURE at a stale `human_visual_action` preview-only assertion; public test `95281046` switched to `human_visual_gait="attack"` + real `human_attack_frame` + pixel rows; full browser pass #45742922283 confirmed fix.

## Verification REQUIRED for this new commit
1. Trigger public Godot CI via this PUBLIC checkpoint push (with existing Pages opt-in), confirm PRIVATE compiled SHA equals `b06e131c955f09e50593d890244e8fbe47b44dc2`.
2. PASS strict import and `PRES-12` horizontal skyline test without disabling any P1.5, Physics V2, combat/visual/guard/round tests.
3. PASS Web + Windows exports and Pages deployment.
4. PASS automatic Chromium E2E against exact source SHA+build run ID; inspect genuine 2D screenshots `moss-nes-style-2d-start.png`, `docks-nes-style-2d-start.png`, `moss-running-horizontal-pixel-2d.png`, real ramps, humans, cyan guard and screenshot artifact. No image asset from actual NES game imported.
5. Record new run IDs, log and evidence; if any failure, fix before calling PASS.

## Remaining
Original pixel-style art user signoff; 2v2 throw/grab, obstacle-aware AI, foreground and map editor usability, device performance, P1.5 migration, V5 original beast forms. Main P1.5 production root remains intact pending parity.

**Trạng thái: PARTIAL — chưa hoàn tất**


## Final V4+flat-skyline pipeline acceptance — PASS (2026-11-26)

- Game functional source `b06e131c955f09e50593d890244e8fbe47b44dc2`, PUBLIC CI commit `441048d2dc92a4c477aa95a985f88c19317ff6c7`.
- [GitHub Actions Godot+Windows+Web export+Pages #45743279673](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45743279673) **SUCCESS**. Verified actual build-job log prints expected private SHA; `VISUAL SPIKE PASS`, `2D VISUAL ADAPTER PASS` including up/down map horizontal skyline `PRES-12`, `COMBO V4 PASS`, `All export checks passed` and `Isolated Physics V2 Web preview exported`.
- [Actual Chromium #45743526820](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45743526820) **SUCCESS**, strict EXPECT pipeline `441048d2`, EXPECT build run `45743279673`; P1.5 PASS dx=220.5, Physics V2 PASS Moss climb=2.12m, Docks descent=2.39m, real ground contact angle>=10deg, dx=11.41m.
- Downloadable screenshot/JSON artifact [ID 15082730310](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45743526820/artifacts/15082730310); actually downloaded ZIP, read `result.json` status `PASS` and visually examined both original `moss-nes-style-2d-start.png`, `docks-nes-style-2d-start.png` before/after 173px fixed skyline correction. Distant facade now horizontal across true slopes, while physical grade remains visible. Both 4 human fighters shown; 468 Moss tiles / 576 Docks tiles; original running sprite and live cyan guard screenshots PASS.
- Earlier `#45742273520` browser FAIL traced to stale `human_visual_action` preview expectation; PUBLIC fix `95281046` now checks physics-timed gait/attack frames, successfully retested Chrome `#45742922283` and final `#45743526820`. No Godot physics/attack tests removed to force a pass.
- **Web preview:** https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1 ; root P1.5 production still separate. This is validated Web tech preview, **NOT** user visual approval of final original NES-quality assets.
- Unfinished: detailed original fighter art fidelity/approved animation and stages, editor ergonomics, environmental props, human grab/throw, AI obstacle avoidance, device perf, main-route migration, V5 original beast. Continue from PRIVATE latest checkpoint before next source change.

**Trạng thái: PARTIAL — chưa hoàn tất**
