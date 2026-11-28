# 2026-11-28 — Actual v8 art included in isolated Web staging, CI pending

- PRIVATE PR #18 source SHA `1f48ab01d21388c358b0974f97a25b44279c43e4`; PUBLIC PR #17 exact pinned CI workflow SHA `6c9c9f123ed80dbae40122a1b802166e74553ae7`.
- New v8-specific 24-frame Web atlas generated from `render_organic_v8_candidate.activate()` + `motion_rig.pose_at`, with RGBA 2880x1920 image, verified PNG SHA-256 in embedded JSON, `art_style=organic-v8-rig`, preserved 6 original rig keys and BLOCKED release.
- Compare full RGB v8 vs canonical v6 image; verify alpha dimensions, SHA, temporary Godot Web imported texture. Actual Godot scene refuses initialization if identity not v8, reports the SHA/selected style from `window.__beastClearline`, and browser asserts this matches the exact runner source JSON. Continue 59 rig/native/screenshot controls, official LibreSprite, Godot motor, and Web browser screenshot/movement tests.
- This fixes prior E2E scope: #46090739701 technically PASS but its Godot Web game displayed **canonical v6**, not organic v8. Do not cite it as v8 in-game proof.
- [Run #46091560799](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46091560799) initially QUEUED; read final job/log and update exact terminal evidence before declaring PASS.
- No PRIVATE art/asset/log/screenshots in PUBLIC repository or uploaded artifacts; no Pages or production changes. **Art release BLOCKED**: 8+ truly original authored poses, frame-to-frame anatomy F3/F6 and owner approval still missing.

**Trạng thái: PARTIAL — chưa hoàn tất.**
