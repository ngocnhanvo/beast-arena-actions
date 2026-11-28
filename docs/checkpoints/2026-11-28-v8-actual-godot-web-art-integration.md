# 2026-11-28 — Actual v8 art included in isolated Web staging, CI pending

- PRIVATE PR #18 source SHA `1f48ab01d21388c358b0974f97a25b44279c43e4`; PUBLIC PR #17 exact pinned CI workflow SHA `6c9c9f123ed80dbae40122a1b802166e74553ae7`.
- New v8-specific 24-frame Web atlas generated from `render_organic_v8_candidate.activate()` + `motion_rig.pose_at`, with RGBA 2880x1920 image, verified PNG SHA-256 in embedded JSON, `art_style=organic-v8-rig`, preserved 6 original rig keys and BLOCKED release.
- Compare full RGB v8 vs canonical v6 image; verify alpha dimensions, SHA, temporary Godot Web imported texture. Actual Godot scene refuses initialization if identity not v8, reports the SHA/selected style from `window.__beastClearline`, and browser asserts this matches the exact runner source JSON. Continue 59 rig/native/screenshot controls, official LibreSprite, Godot motor, and Web browser screenshot/movement tests.
- This fixes prior E2E scope: #46090739701 technically PASS but its Godot Web game displayed **canonical v6**, not organic v8. Do not cite it as v8 in-game proof.
- [Run #46091560799](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46091560799) initially QUEUED; read final job/log and update exact terminal evidence before declaring PASS.
- No PRIVATE art/asset/log/screenshots in PUBLIC repository or uploaded artifacts; no Pages or production changes. **Art release BLOCKED**: 8+ truly original authored poses, frame-to-frame anatomy F3/F6 and owner approval still missing.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## TERMINAL RESULT / EXACT SOURCE IMAGE IN GAME VERIFIED

- [PUBLIC Actions run #46091560799](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46091560799), job `140813413017`, workflow exact SHA `6c9c9f123ed80dbae40122a1b802166e74553ae7`, pins PRIVATE art+staging source SHA `1f48ab01d21388c358b0974f97a25b44279c43e4`: **COMPLETED SUCCESS**, all steps terminal.
- Logs: Ran 50 portable tests, Ran 9 native/screenshot tests; organic v8 six changed rig-bound SVG + 14 joint identity +24 samples PASS; official LibreSprite strict RGBA PASS; real Godot CharacterBody3D motor PASS; transient Web PCK and Chromium PASS.
- **New v8-in-game proof:** `BEAST_V8_ACTUAL_WEB_ATLAS_EXACT_SOURCE_SHA_AND_PIXELS_DIFFER_FROM_V6_PASS`; `BEAST_V8_ORGANIC_ATLAS_ACTUALLY_DISPLAYED_BY_GODOT_WEB_PASS_ART_BLOCKED`. PNG atlas SHA-256 `853bbc99dcad9184c42f6e79171f9511751669d4bea6f4aa20d09bfb6aa9b203`, identical to JSON manifest and browser-reported active sprite. Web imported actual transient Texture2D with 6x4 frames, not old canonical v6. The screenshot source controls and browser runtime prove integration, not owner aesthetic acceptance.
- Browser real Physics V2: `art_style=organic-v8-rig`, X -11.300000 → -4.679103m, 264 physics ticks, 24 visited visual source indices, stopped X speed -0.030505m/s, 122058 changed scene pixels (495 minimum; HUD excluded), three screenshots, no JS errors.
- Corrected previous gap: #46090739701 only ran v8 source generation separately while Web displayed canonical v6; this NEW run actually stages and renders v8. No source/asset/screenshot uploaded to PUBLIC artifacts/Pages. Main untouched and both PRs still Draft.
- **Remaining:** Art self-review `FAIL_NOT_PRODUCTION_QUALITY` (rear-flight F3/F6 anatomy/occlusion); only six reused rig keys plus 18 samples, not final 8+ independently authored source poses; all actions/directions, neutral overlays and owner aesthetic signoff missing; production deployment/merge BLOCKED. Next improve source art geometry, iterate at 480px/80px, then original authored run cels and revalidate real game.

**Trạng thái: PARTIAL — chưa hoàn tất.**
