# 2026-11-28 — v8 FK/IK continuous-joint source candidate, independent QA

- PRIVATE PR #18 v8 source commit `ec8e22379bcbd08d52486f94036c828626640c2d`; PUBLIC PR #17 workflow commit `6e6cb59c58fc513d61706739406b507b2d687012`.
- In addition to retained 59 base tests and official LibreSprite/Godot/isolated real Web Chromium, a new v8 test demands six genuinely different SVG/PNG raster outcomes against v7, 14 same-rig tagged joints, 24 sample animation and SHA source metadata integrity.
- Renderer uses continuous smoothly curved art envelopes through actual FK/IK knees/elbows; output remains an **isolated transient art candidate**, never committed to PUBLIC, uploaded to artifacts or deployed to Pages.
- [Run #46090739701](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46090739701) COMPLETED SUCCESS; job 140810800947 terminal logs verified.
- **Art remains blocked:** v8 visuals still lack convincing rear-flight and complete near/far occlusion, no 8+ new independently authored original production cels, no owner acceptance. Production main/Pages untouched. Next inspect run and fix failures then improve the actual art.
- **Trạng thái: PARTIAL — chưa hoàn tất.**

## REAL TERMINAL QA VERIFIED

- [PUBLIC GitHub Actions run #46090739701](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46090739701), job `140810800947`, **COMPLETED SUCCESS**, pinned exact PRIVATE `ec8e22379bcbd08d52486f94036c828626640c2d`, PUBLIC test workflow commit `6e6cb59c58fc513d61706739406b507b2d687012`.
- Logs: **Ran 50 tests** portable PASS; **Ran 9 tests** native/screenshot PASS; `BEAST_ORGANIC_V7_RIG_BOUND_STUDY_6_SVG_24_SAMPLES_PASS_ART_BLOCKED` and **`BEAST_ORGANIC_V8_EXACT_RIG_SHA_14_JOINTS_6_CHANGED_SVG_AND_24_SAMPLES_PASS_ART_BLOCKED`**.
- Original canonical SVG full rig byte parity PASS. LibreSprite real native RGBA pixel exact PASS. Godot real CharacterBody3D motor smoke PASS; transient Godot Web export PASS and Chromium actual keyboard/motor/screenshot PASS.
- Actual Web report: `sampled_frames=24`, 222 physics ticks, X -11.300000 → -4.616288m, stopped speed -0.030505m/s, 115849 world-region changed pixels vs required 495 (HUD excluded), zero JS errors, 3 screenshots. Stage generated on runner only, NOT Pages deploy.
- This proves generator and existing motor integration QA, **not** the new v8 art running inside gameplay, since the existing staging 24 atlas remains canonical v6. No owner aesthetic acceptance, no approved 8+ independently authored art, no merge. `art_release=BLOCKED`.

**Trạng thái: PARTIAL — chưa hoàn tất.**
