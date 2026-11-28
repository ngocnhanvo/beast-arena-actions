# 2026-11-28 — Folded recovery v9, F3/F6 ankle and knee profile

- PRIVATE PR #18 pinned source SHA: 4c9028deeabce733a17480db1ef22f8b448dc6e4.
- PUBLIC pinned workflow SHA: e110f2727d15807c26a583b9d7d800591a01654b.
- PRIVATE source adds motion_organic_v9.py: isolated IK rear ankle target -13/27 during F3/F6 (previous -14/22), with signed knee IK branch, fixed thigh/shin 15/15, preserved stance toe world-lock and arm FK. Does not alter original motion_rig.py or six canonical SVG source files.
- PRIVATE source adds render_organic_v9_candidate.py: six 480px transparent rig-bound SVG frames, 24 deterministic time samples and review contact sheet. Six original gait keys +18 inbetweens are NOT 8+ authored original production frames.
- Added six independent v9 tests, verified locally with older installed Skill: 601 samples and loop/stance/limb/negative shin gates PASS. Exact repository-v6 validation needs public CI.
- Opt-in staging build_24_frame_atlas.py --art-style organic-v9 produces 6x4 480px Web image and SHA manifest; Godot runtime fails closed without organic-v9-folded-recovery; real Chromium Playwright checks the same SHA. Production game and Pages unchanged.
- Run https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46092846821 initially IN_PROGRESS. Inspect terminal logs; do not claim success before conclusion.
- Art still FAIL_NOT_PRODUCTION_QUALITY pending full 480px/80px review, 8+ genuinely authored run frames, action/direction clips and owner signoff. No PR merge/deploy.

Trạng thái: PARTIAL — chưa hoàn tất.