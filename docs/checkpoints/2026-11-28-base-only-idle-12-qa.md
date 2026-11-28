# 2026-11-28 — Base-only 12-frame fighter cutover: independent PUBLIC source QA (no deploy)

## Actual owner request
Owner explicitly retired Jade and all old visible fighters. PRIVATE branch `feat/base-only-idle-12-cutover` committed `4fc66fb8a24b4356bcab014eb3620d0524b20989` from previous game main `48dc2119981f26e9f010b279ff2520af99b2f99b`. All four active 2v2 fighter appearances use a single original bald/faceless/navy-short `base_human`, with new fixed-foot idle breathing 12×100ms, no alternate character toggle. Legacy data kept private for compatibility/rollback only. Other actions show static guard pending new art; physics/motor/combat unchanged.

## Security and verification boundary
Dedicated isolated PUBLIC workflow `.github/workflows/base-only-idle-12-qa.yml` pins exact PRIVATE source and tests: binary source foot bounds, Godot 4.7.2 import, actual four-fighter demo smoke, 60Hz physics and combat source regressions. Runner sees private source transiently and publishes NO raw source, art, build or Pages artifact. Art owner approval applies to prior *idle preview*, not new in-game frame-rate acceptance. This source QA is independent of the current main Pages.

Latest earlier GitHub Actions `#46105044735` had cache SUCCESS but Pages SKIPPED, E2E `#46105079522` SKIPPED; clean restart `#46107042607` 9/9 blueprint PASS only. NONE validates this Base-only integration.

## Next
- Inspect terminal current workflow job logs from exact PUBLIC SHA and PRIVATE `4fc66fb8`; fix Godot failures before release.
- Update PRIVATE checkpoint and this public checkpoint with actual run/job URL and test evidence.
- Only then consider merging PRIVATE safe cutover, trigger PUBLIC main Web build and Pages, wait for completion, inspect Chromium *actual screenshot* and runtime attack/health/foot displacement at one canonical `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/`.
- New walk/run/punch/kick/jump artwork remains `PENDING_ART`; do not report complete game animation.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## Verified terminal expanded QA (2026-11-28)
- [Source-pinned run #46118127900](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46118127900) COMPLETED **SUCCESS**, PUBLIC QA workflow SHA `6b19c05a2151666a664073758b68dd01b9ef3216`, PRIVATE tested `212db7a92e82427cab9a1ba75c29bef023bb1c13`.
- Actual Godot 4.7.2 log: import/parser PASS; 4/4 live actors `base_human`, 12/12 distinct authored native idle frames and planted-foot region; physics 60Hz/combos PASS; map editor 51.4px measured PASS; pixel projection, combat scene, hit effects, match state/scene, obstacle collision ALL PASS.
- Retired Jade-specific `visual_smoke.gd` and `three_quarter_preview_smoke.gd` are not game-active acceptance; new `base_only_idle_12_smoke.gd` replaces them in runtime build. Historic source remains recoverable; no destructive asset purge.
- Real public Pages and real Chromium remain **NOT_RUN for this release**. Prepared `ci/playwright_base_only.py` to exercise four Base actors, actual idle frame cycle, no old art toggles, movement and combat. Do NOT claim deployment from this QA alone.

**Trạng thái: PARTIAL — chưa hoàn tất.**
