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
