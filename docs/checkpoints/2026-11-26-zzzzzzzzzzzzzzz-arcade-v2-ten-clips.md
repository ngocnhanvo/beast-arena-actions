# Beast Arena Actions — opt-in Arcade V2 ten clip/input staging checkpoint (2026-11-26)

## Owner-specified scope and non-negotiable art gate
10 separately authored actions expected: idle breathing, W/S front-facing but
separate walk loops, A/D side walk, A+A/D+D side running, F punch, G kick,
simultaneous F+G jump. `autocheck:false`: user alone judges art. Current
original 80px Jade atlas is still a pre-existing, **visually rejected**
cut-and-paste prototype. No ten actual editable full-body clips exist yet.
Do not equate successful test frames with artistically complete sprites.

## SOURCE changes now present in PRIVATE
- `scripts/arcade_input.gd`: fixed 60Hz buffered 16-tick horizontal
  double-tap, 7-tick overlapping simultaneous F+G chord only; OS auto
  repeat and two separate F/G taps do not count as a chord.
- `scripts/named_animation_library.gd`: Godot native SpriteFrames +
  AtlasTexture import of Aseprite RGB PNG and --format json-array full
  untrimmed 80px frames, ten tags with min counts, source duration and
  foot_anchor slice. Runtime 1x1 pose shared between Sprite3D and
  PixelView; no 4x20 legacy index on an authored clip.
- `scripts/demo.gd` & `character.gd`: opt-in Web query
  `?controls=v2&art=approved&pixel=1`; W/S look front, A+A/D+D
  3D physical sprint, F light punch, G independent kick attack data,
  overlapping F+G jumps without emitting attack; H guards.
  Debug `animation_clip_intent` separate from
  `animation_source_ready=false`. User-facing HUD warns PENDING_ART.
- `art/animation_sources.json` now requires ten original tags, including
  W and S separate but both front-looking. `export_presets.cfg` includes
  future `art/export/*.json`; `tools/export_animation_sources.py`
  is local-only strict Aseprite/LibreSprite PNG+JSON exporter, returns
  PENDING_ART until genuine editable source exists. Unit-test-only in-memory
  RGBA frame sheet exercises real JSON/tag/foot data parser.
- `tools/animation_source_audit.py` now validates untrimmed original
  80×80 RGBA8 source, pivot slice coordinates, durations and bounds.
  **No real .aseprite and no original clip export exists yet.**

## PUBLIC workflow / tests
- `.github/workflows/build.yml` runs mandatory isolated Godot V2
  headless `res://tests/arcade_animation_v2_smoke.gd` without replacing
  standard combat, slopes or map smoke.
- `.github/workflows/web-e2e.yml` includes
  `ci/playwright_arcade_v2.py` in normal real Chromium E2E;
  strict source+pipeline+build provenance, real W/S velocities, one-step
  walk vs A+A/D+D sprint, F/G combat attack state and F+G real airborne
  motion. Existing P1.5/PhysicsV2 suites remain.
- Browser concurrency now cancels superseded runs. Newer Pages may
  replace older PCK mid-test: older run must be marked
  SUPERSEDED_BY_NEWER_PAGES, never falsely PASS or STALE if newer.
- First browser run #45779061468 FAILED because E2E source expected
  old run ID while Pages had already deployed a newer build (verified
  log `V2 stale PCK build 45778853589` vs 45778804465).
  #45779338957 FAILED after P1.5 and PhysicsV2 PASS with test-only
  JavaScript typo `ReferenceError: abs is not defined`. Public
  commit `9dea165f...` fixes to `Math.abs`. These are real failures
  and must not be concealed, even though functional source worked.
- Public Godot/build #45778200911 SUCCESS with early V2 framework.
  Public Godot/Pages #45778853589 SUCCESS compiled PRIVATE
  `a31406c05e0a0905c386eb819a145ca8f42d43b6`, PUBLIC `88cc51...`,
  headless `ANIMATION V2 FOUNDATION PASS`.
  Most recent exact PUBLIC run [#45780007709](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45780007709)
  SUCCESS compiled PRIVATE `73e1b8062f5976a1a8a088cf67722b5456012e83`
  on PUBLIC `9dea165f12761c91bad39695736ebfa282bd4206`;
  log confirms ten named imported-tag tester, PENDING_ART warning,
  Web/Windows export and Pages. PRIVATE subsequent docs-only reference
  `8c43d49...` does not modify runtime.
- Real Chromium [#45780479922](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45780479922)
  was still running when this document was first created; inspect
  actual final conclusion before claiming arcade V2 E2E PASS.

## Remaining and next
- **BLOCKED_ART_SOURCE:** actual ten clips with individually drawn
  editable .aseprite/.ase frames (4/6/6/6/6/8/8/4/5/5), RGB PNG+JSON
  export, true foot anchor and manual owner's art signoff.
- User requested completing whole feature, but code+input/CI and live
  prototype are only a technical milestone, not full animation.
- Read PRIVATE `docs/checkpoints/2026-11-26-zzzzzzzzzzzzzzz-arcade-v2-ten-clips.md`
  and `docs/art/JADE_TEN_CLIP_ANIMATION_PRODUCTION_2026-11-26.md`.
- Next: verify new exact Chromium, fix any genuine controls/input issues
  with log evidence; then produce full authored 80px action poses, run
  strict source gate, user approves complete sequences, only then
  switch the live V2 sprite source from legacy to authored.

**Trạng thái: PARTIAL — chưa hoàn tất.**
