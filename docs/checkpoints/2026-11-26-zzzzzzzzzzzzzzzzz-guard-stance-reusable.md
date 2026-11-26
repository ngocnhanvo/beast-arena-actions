# Beast Arena Actions — reusable combat guard animation framework (2026-11-26)

## Scope / acceptance standard
Owner requested every fighter keep raised fists in standing, walking and running, as in owner-supplied guard sprite reference; all four characters must reuse ONE animation codebase, no patched per-character hand/leg offsets. `autocheck:false` = manual owner art verdict. Reference is illustrative, not an imported/licensed sprite.

## Actually verified preceding GitHub evidence
- PRIVATE initial HEAD `ebdd56a9e3fc9a5c441e9598ab34d6c122916ac2`, PUBLIC initial HEAD `495b6decc9859dbfa653483561774e2adee86713`; read AGENTS.md, docs/START_HERE.md and both newest checkpoints before implementing.
- Previous Pages [#45786335073](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45786335073) SUCCESS but [Chromium #45786635605](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45786635605) FAIL due Physics V2 `wait_for_function` 10-second timeout, after P1.5 PASS (dx227.5). Do not reuse older Chromium PASS to claim new art accepted.
- New [build #45790727518](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45790727518) **FAIL** mandatory new `guard_animation_profiles_smoke.gd`: exactly `GUARD-PROFILE: only native 80px sources are supported` and `GUARD-203` on Jade. Proven root cause: Godot JSON Variant numeric array comparison to GDScript literal [80,80] is not type-stable. PRIVATE `d2f3b4fc89beda4770b8b3f77dbceab65ec3d190` fixes elementwise numeric checks. Must run fresh CI to verify; older #45790694776 technically SUCCESS but did not run mandatory new guard test.

## Implemented code / workflow
- PRIVATE `art/fighters/animation_profiles.json`: one 80×80 `stance=guard` ten-clip contract and distinct media per Jade, ally, rival A, rival B. Has 7 required guard locomotion tags and punch/kick/jump; distinct W/S front-facing, separate left/right walk and run, original 80px authored foot slices, PENDING_ART_GUARD_FRAMES for all.
- PRIVATE `scripts/fighter_animation_profile.gd` validates each roster member's data, unique ten tags, min frames and named guard stance. `scripts/animation_intent.gd` picks generic input/velocity action without atlas rows. Existing `named_animation_library.gd` now imports ten clip tags *from the fighter profile*; `character.gd` and `demo.gd` assign/reuse correct profiles for all four actors, source-readiness never faked.
- Web PCK `export_presets.cfg` explicitly includes `art/fighters/*.json`: otherwise new fighter catalog is invisible on Pages.
- PRIVATE `tests/guard_animation_profiles_smoke.gd` is mandatory in PUBLIC `.github/workflows/build.yml`, tests all four profile mappings, ten logical commands, true 80px Aseprite frame metadata importer and real Sprite3D shared foot pose using **test-only synthetic pixels** never shipped as game art.
- PUBLIC `ci/playwright_arcade_v2.py` expects exact current Pages build SHA/run + 4 loaded profiles, Jade `guard` stance, new guard-named clip intentions and old physical movement/punch/kick/jump state. A codebase PASS is NOT visual-quality PASS.
- Existing physics 60Hz, W/S physical axis, collisions, map slopes and combat remain unchanged. The only new artwork requirement is native ORIGINAL *full-body high-guard frames* (not limb shifting).

## Next exact steps
1. Trigger fresh Public build for newest PRIVATE HEAD using mandatory guard test; inspect logs, source SHA, Actions and Pages. Fix genuine failures, preserve failure run IDs.
2. Run real Chromium against same built Pages PCK to prove four profiles included in Web export and guard clip intents, W/S front, A+A/D+D side running, F/G attacks and F+G jump. Preserve technical failures from prior #45786635605; only exact verified Web run can supersede them.
3. Source independent original editable human-fighter Aseprite full-body stance frames with arms up for every idle/walk/run keyframe, including 2 different front-facing W/S loops; satisfy 10 clips and per-frame foot slice. Source audit remains `PENDING_ART` until authentic source and owner signoff. Do NOT silently publish old graphic behavior as fixed.

**Trạng thái: PARTIAL — chưa hoàn tất.**
