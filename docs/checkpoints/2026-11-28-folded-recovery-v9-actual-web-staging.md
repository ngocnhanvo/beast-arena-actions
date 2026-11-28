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

## Terminal CI verified
- Actual [Actions #46092846821](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46092846821) job 140817491139, pinned PRIVATE 4c9028deeabce733a17480db1ef22f8b448dc6e4 and PUBLIC e110f2727d15807c26a583b9d7d800591a01654b: **COMPLETED SUCCESS**.
- Exact job logs: Ran 56 portable tests + Ran 9 native/screenshot = 65/65 PASS. BEAST_ORGANIC_V9_FOLDED_RECOVERY_600_DENSE_SAMPLES_6_SVG_24_GIF_PASS_ART_BLOCKED. Native official LibreSprite RGBA pixel exact PASS, Godot motor smoke PASS, transient Web export PASS.
- Real Web Chromium: BEAST_V9_ACTUAL_WEB_ATLAS_EXACT_SOURCE_SHA_AND_PIXELS_DIFFER_FROM_V6_PASS and BEAST_V9_ORGANIC_ATLAS_ACTUALLY_DISPLAYED_BY_GODOT_WEB_PASS_ART_BLOCKED. Active atlas SHA eb39f675e5887aa22e9844529cc3591a929f904985f28448eb4b5047cc644812, art_style organic-v9-folded-recovery, 24 sampled source indices, 204 physics ticks; X -11.300000 to -4.553435m, released D speed -0.030505m/s, 109312 world crop changed pixels (495 minimum), zero JS errors, 3 runner-temp screenshots.
- Technical PASS is not owner visual approval. Local preview uses older installed Skill, so the local contact sheet is illustrative; source code tested in runner pins the current v6 rig. Six original base rig poses plus 18 inbetweens do not satisfy required 8+ independently authored original cels. **ART FAIL_NOT_PRODUCTION_QUALITY / release BLOCKED; no merge, no Pages/production deployment.**
- Remaining next: inspect actual rig v6 sourced rendered art at both scales; improve torso/limb occlusion and natural run-to-idle; author 8+ original art cels, native source; seek owner visual acceptance.

Trạng thái: PARTIAL — chưa hoàn tất.