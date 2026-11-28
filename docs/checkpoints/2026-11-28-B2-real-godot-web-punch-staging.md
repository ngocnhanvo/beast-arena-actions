# 2026-11-28 — B2 actual Godot Web 2.5D punch stage / source proof (CI pending)

## Why
Previous #46101540323 proved a 3D arm + keyed source contract, but its real-Godot Web E2E still rendered **old V10 running artwork**, making it impossible to claim an in-game punch. Owner explicitly required a finished reviewable 2.5D punch rather than repeated unattractive sketches and misleading test counts.

## Implemented on DRAFT only
- PRIVATE Draft PR #18 source exact `022e9c2fff22036cbffa2b0d05253c0c1400feb6`: `tools/pose_lock/punch25d/punch25d_stage_export.py` now builds an isolated **actual 6×4 480px RGBA atlas, 24 punch samples** directly from `keyed_corrective_rig.pose_at(t)` and exactly two verifiable PRIVATE WebP key art sources (`assets/guard_impact_{0,1}_128.webp.b64`, expected SHA-256 `cc0de7c5f5e44ddfdee0fdcc5ae14405e3b5c7f914d96337d835457b0650250f`, `fa43a9f0b6d18e76cf256498e360edca5cbf1aad2306071ca8ded75d96466afe`). Owner B1 source reference remains separately tracked and no false pixel identity is claimed.
- The new `tools/pose_lock/punch25d/punch25d_web_staging.gd` reuses the **REAL Physics V2 CharacterBody3D** with an imported Sprite3D and listens for key **F** on the actual Godot Web canvas. Its animation time source is the 24-frame B2 punch atlas (NOT previous distance-driven v10 run). It publishes `window.__beastPunch` with active 3D wrist Z, source SHA, active/guard recovery and user approval blocked. It is copied only into the transient runner staging scene; private production assets and Pages are not modified.
- New `tools/pose_lock/punch25d/playwright_punch25d_real_game.py` captures guard → real keyboard F punch → recovered guard via Chromium/WebGL and compares actual HUD-excluded canvas world pixels while cross-checking the exact atlas SHA/source identity, minimum visited frame count and 3D wrist depth. It keeps screenshots only in runner-temp, not PUBLIC artifacts.
- Local atlas generated successfully from key source bytes: 2880×1920 RGBA, pixel SHA `52b4bd22497771141b1f3890109ef6b771816c7df7d30a0eb9bdca13263b92dc`, 19 guard cells + 5 impact cells, Z 40.29451–149.96007. Files **are in PRIVATE Git only** (base64 WebP asset bytes, source + tests), no graphics entered PUBLIC Git/Pages.
- PUBLIC Draft PR #17 workflow `fdeb9dfbdc0d76a8407ef8dbb0bde8f40fc1c8be` pins exact PRIVATE source, first retains original 95 native/old-Web gates, then builds the NEW B2 punch atlas, re-imports/re-exports a SECOND separate transient real Godot Web game and verifies Chromium F button/real sprite/return with independent screenshots. Run [#46104585623](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46104585623) was queued after an earlier source-run; **MUST check actual terminal result and logs** before PASS.
- No main, no owner-facing production Pages, no token/art leak.

## Honest remaining scope
- Two NEW hand-corrected raster art keys are **NOT** the specific B1-approved source pixels and are not full-body editable skinned layers; 24 samples are timing repeats of two keyed cels, not 24 independently painted frames. Their animation is intended *keyed impact*, not smooth interpolation; jerk risk at frame 9→10, 14→15 remains real and should be visually inspected after technical passes.
- `art_release=BLOCKED`, owner B2 signoff `NOT_GIVEN`. Even a real-Godot browser PASS demonstrates **in-game use of the new punch source**, not production-ready anatomy or globally reusable skinning.
- NEXT: inspect exact CI terminal export and 3 screenshot gates, fix any Godot import/Playwright failure, then create segmented/B1-matching art with corrective transitions, obtain owner visual acceptance before any merge/deploy. Do not return to running gait merely to rack up test counts.

**Trạng thái: PARTIAL — chưa hoàn tất.**
