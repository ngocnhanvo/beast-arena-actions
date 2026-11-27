# 2026-11-27 — Exact SHA repin for Jade Draft #2 native parser fix

- Previous isolated QA [#45936492263](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45936492263): Python independent PASS, pinned LibreSprite PASS (0 RGBA diffs), Chromium 8/8+9/9 PASS, Godot import/guard PASS but three_quarter_preview_smoke.gd parser FAIL. Diagnostic rerun [#45936854443](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45936854443) isolated duplicate `phase` declaration in same GDScript function.
- PRIVATE Draft PR #2 repaired only test loop name `counterphase_index`, SHA `51f3d8e12cb8d46071d9cdbd3ba0ab028b50aad7`. Public CI branch repins immutable source SHA, no deploy/merge/export/artifacts; all jobs must reach terminal status before technical signoff.
- NEXT: inspect real run/jobs/logs and if failures remain fix scoped cause; never report source art aesthetically accepted. `autocheck:false`.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## Final isolated QA evidence (verified from terminal Actions jobs)

- Source under test: PRIVATE `51f3d8e12cb8d46071d9cdbd3ba0ab028b50aad7`, CI pipeline `a1fd527f1db7b34f4ece96a1744ff4e77adc734c`; [run #45936962296](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45936962296) **completed SUCCESS**.
- Python verifier and pinned LibreSprite 1.3: PASS, both RIGHT/LEFT registered tagged ASE exports match PNG at all RGBA bytes, visible_diff=0 and transparent_rgb_diff=0.
- Godot 4.7.2: import exit=0, 0 script errors; `guard_animation_profiles_smoke.gd` exit=0 PASS; `three_quarter_preview_smoke.gd` exit=0 PASS, 0 script errors. Prior same-scope `phase` declaration parser failure is **resolved**.
- Chromium local GIF playback: PASS 8/8 run phases, 9/9 including idle source comparison, real 7→0 seam observed, unmatched_samples=0.
- NOT RUN: in-game Pages integration/E2E for new PR because draft must not merge/deploy. No owner visual acceptance or actual runtime run→idle transition assertion; these remain PENDING_OWNER_ART / separate idle transition scope.
- Reproducibility: test results apply to exactly PRIVATE source SHA `51f3d8e12cb8d46071d9cdbd3ba0ab028b50aad7`, not main or future docs-only branch HEAD. Public CI branch holds script and no private sprites/artifacts.

**Test result: PASS — isolated source technical QA.**

**Trạng thái: PARTIAL — chưa hoàn tất tổng thể do chưa được duyệt mỹ thuật và chưa tích hợp/deploy theo quy trình.**
