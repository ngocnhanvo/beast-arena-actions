# 2026-11-26 — real Jade editable source draft, reusable LibreSprite art CI

## Verified HEAD / runs
- PRIVATE asset source b800b636bde28c6ca4d3353877391ffe7922ae86: six AI-assisted original native 80x80 poses, 100ms, single walk_down_guard_front tag and true .aseprite binary, private art/drafts only.
- PRIVATE tests use candidate manifest at experiments/physics_v2/art/drafts/candidates.json; no art committed to public repo or Pages.
- PRIVATE strict audit rejects invalid overlapping/untagged/out-of-order 10 clip ranges, duplicate source atlas rectangles, missing/incorrect pivot keys. 8 intentional negative regression cases.
- PUBLIC workflow 1bfeaabbdc83ca8b3bf6b0280e4fa9c61d3f126f automatically runs generic PRIVATE tests/draft_animation_sources_smoke.py, not actor-specific public code.
- SUCCESS LibreSprite #45800285146: real candidate .ase opened, six frames and PNG pixel identity verified; 58 test-only 10-tag exporter and strict regressions PASS; full game source audit reports PENDING_ART.
- SUCCESS Godot/Windows/Web/Pages #45800285101 on latest 1bfeaab pipeline. This release does not ship draft character art.
- FAIL previous-browser #45800283677: P1.5 PASS, isolated Physics V2 wait_for_function timeout. Older expected SHA was 8b7d16, and Pages was concurrently updated, so exact root cause requires later stable-run verification.
- New browser #45800631688 must be read for actual final status; at checkpoint not assumed PASS.

## Remaining / next step
- ONE of TEN original guard clips is a candidate. Nine remaining (at least 52 frames), authentic reviewed foot pivots, merged 58+ frame editable private source, strict full-export, Godot preview, and owner's visual signoff are NOT finished.
- With owner autocheck:false, never turn a technical CI PASS into visual acceptance. Add new clips to PRIVATE candidate manifest and the same generic CI tests them; follow game source roadmap, keep PUBLIC Pages art unchanged until authorized.
- Status: PARTIAL — chưa hoàn tất.
