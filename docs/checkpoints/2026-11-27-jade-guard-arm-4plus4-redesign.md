# 2026-11-27 — Jade guarded arm running redesign, 4+4 counterphase, owner review

## User intent and previous incident
- Owner reports original hands looked unnatural despite legs being accepted; requested implementation in actual Beast Arena game, no separate illustration, same single canonical https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ .
- Read AGENTS.md, docs/START_HERE.md and latest source checkpoint in BOTH repos. Previous excessive black-glove overpaint failed on visible sprite, even though earlier Playwright frame coverage succeeded. Never patch limbs at runtime or declare visual acceptance from index checks.

## Source change (PRIVATE `a1d7088747c06171f9e57b5a470095e082f50669`)
- 8 whole-body native80 transparent RIGHT cells, 8 complete LEFT whole-body mirror cells, atlas 640x160, 85ms source per frame, 0.50m stride unchanged; no GDScript animation/motor/physics code changes.
- Re-authored readable compact guard fist poses on original AI-assisted source at four upper-body shapes, deliberately paired **(F0,F7), (F1,F6), (F2,F5), (F3,F4)**. 4+4 arc: hand back → through guard → forward → guard peak → return symmetrically, no oversized black glove painted over old fists. This is four different arm poses across eight full-body run frames, NOT eight independent arm designs.
- **Source pixel invariant:** all eight face/hair rows y0–36 and owner-accepted shoes/legs y55–79 remain exactly unchanged against `art/drafts/jade_run_eight_16_before_arm_retouch.png`; each LEFT whole 80px is exact mirror of corresponding RIGHT. No sprite shrinking, no hitbox/velocity changes.
- Editable originals `art/drafts/jade_run_eight_{right,left}.aseprite` have tagged 8×85ms full-body cels with corresponding PNG exports, complete atlas `jade_run_eight_16.png`. `art/drafts/jade_run_eight_16.json` explains the source/pairings/provenance. `art/fighters/animation_profiles.json` reads the same per-fighter profile; both directions unchanged indexes.
- Private Godot `tests/three_quarter_preview_smoke.gd` has new non-bypass gate: eight original legs/faces exactly equal to baseline; four unique upper-body source poses with exact symmetric pairs; mirror, 7→0 seam and 8 walking directions still enforced.

## Public CI
- Public docs source trigger `cd545a314ca966f6e31aac06e048bf54dc1afe11`, full Godot/Windows/Web/Pages build **#45869792252**, pinned actual LibreSprite workflow **#45869792258**. Check terminal job status, exact source SHA and logs. Once Pages deployment is confirmed, inspect automatic exact Chromium E2E and artwork screenshots. Do not use prior green #45865959570 to certify this new art.
- `autocheck:false`: CI verifies source, pixels, native Godot and real browser controls, NOT that arms satisfy owner aesthetically.

## Next steps
1. Confirm LibreSprite right/left tag, pixel-exact PNG exports, new source SHA, and Godot native `JADE RUN GUARD ARM COUNTERPHASE SOURCE PASS`.
2. Confirm Pages has newly built PCK and Chromium validates A+A,D+D all 8 actual rendered poses, 7→0, P1.5, Physics, Arcade and eight-direction walking; save screenshots.
3. Owner opens one canonical /physics-v2/ and reviews natural 4+4 guard-hand pump. If rejected, revise complete native cels in editable ASE without drawing over old fists, preserving accepted original legs.
4. Update both repo START_HERE, engineering notes and checkpoint with terminal run evidence.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## FINAL 2026-11-27 — exact new source build/Pages/LibreSprite/Chromium verified
- PRIVATE SOURCE SHA `a1d7088747c06171f9e57b5a470095e082f50669` built from PUBLIC pipeline SHA `cd545a314ca966f6e31aac06e048bf54dc1afe11`. These are the exact source IDs observed in E2E `jade-34/result.json` (not later docs-only HEAD).
- [Godot native, Windows/Web export and actual Pages deploy #45869792252](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45869792252) **SUCCESS all jobs**. Native log: `JADE RUN GUARD ARM COUNTERPHASE SOURCE PASS: four native upper-body guard shapes, 4+4 symmetric pairs; all eight accepted leg and face poses pixel-identical; whole-body mirrored LEFT; OWNER_ART_PENDING`. Also `JADE RUN EIGHT PHASE HOLD PASS`, sequential, 70px size and 8 walking directions PASS.
- [Pinned real LibreSprite CLI art roundtrip #45869792258](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45869792258) **SUCCESS**, both 8x80 original editable run RIGHT/LEFT tagged ASE sources exact PNG; four active candidate clips, no false ten-clip claim.
- [Exact Chromium Web E2E #45870099632](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45870099632) **SUCCESS attempt2**. Actual two-map/camera P1.5 PASS; Physics V2 climb2.21m/descent2.29m PASS; Arcade V2 PASS; Jade eight-way walking, idle, actual A+A/D+D same new atlas 8 full-body GPU-drawn phases [0..7] and 7→0 seam PASS. Browser artifact `beast-arena-browser-screenshots` ID **15141429141** from successful attempt. Browser telemetry confirms `source_sha=a1d7088`, `build_run_id=45869792252` and `pipeline_sha=cd545a3`. Godot drawn-phase mask 255 each direction and ordered history [0,1,2,3,4,5,6,7,0,1,2]. rAF samples observed [0,1,2,4,6] in SwiftShader: low-FPS sampling **does not certify visual smoothness on owner GPU**.
- **Recorded separate flaky fixture:** first E2E attempt FAIL before Jade at `J never entered real Godot attack state` in Physics V2, same as previous #45865959570 attempt1; retry passed with unchanged game source. Do not misclassify as source sprite or claim first attempt passed.
- **Technical scoped work PASS:** published correct new 4+4 source and native editable pipeline; old black glove overlap absent, original approved face+legs pixel intact, source is reproducible/editable. **Visual art status PENDING_OWNER_REVIEW** per `autocheck:false`: four paired guard-arm source poses may still need artistic adjustment after owner's real-game feedback. Other idle/punch/kick original fighter cels in broader roadmap still PENDING_ART.
- NEXT: owner opens ONLY https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ and tests D+D/A+A. If arm timing/shape is rejected, continue authoring **complete native cels** in editable ASE, retaining face/leg region invariants. Address flaky `J` fixture separately when relevant, not by disabling physics regression gates.

**Trạng thái: PARTIAL — chưa hoàn tất.**
