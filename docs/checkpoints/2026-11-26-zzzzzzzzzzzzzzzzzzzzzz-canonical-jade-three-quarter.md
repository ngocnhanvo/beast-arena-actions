# 2026-11-26 - Jade three-quarter view on ONE canonical Physics V2 URL

Owner wants gameplay on https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ only, with no alternate user-facing Pages links or query flags. New private editable art/drafts/jade_guard_34_walk_down.aseprite has six native 80x80 angled whole-body guard poses, updated 480x80 PNG, sidecar foot pivots and candidate manifest. NOT 10 full clips and NOT owner-accepted visuals.

Private scripts/fighter_animation_profile.gd + character.gd now allow a generic single-clip profile review path, without promoting PENDING_ART. Canonical no-query URL enables 2D PixelView, V2 controls and original Jade idle; S real-world movement selects the new 3/4 six-frame clip; rest of game keeps existing fallback. One Sprite3D frame and foot offset feeds 3D and pixel 2D; no runtime limb patching.

PUBLIC ci/playwright_jade_three_quarter.py checks the SAME Pages document with read-only internal ?review=1&e2e=1 diagnostics. It verifies published source SHA/run, floor and six-cel Sprite3D playback on actual S input. Never give diagnostic query link to user. PRIVATE native Godot three_quarter_preview_smoke.gd checks loaded 80px PNG source and six distinct original RGBA frames.

History: Godot/Pages #45803632632 SUCCESS, but compiled PRIVATE 0621ad... BEFORE the new image; does not prove new art deployed. #45803665391 FAIL in new Godot test: PackedByteArray.sha256_text missing from Godot 4.7.2. Private fix 9318d2... uses direct RGBA byte comparison instead. Fresh build and browser verification REQUIRED.

Next: inspect newest CI run actual private SHA, Godot smoke result, Pages deployment, exact browser screenshot; fix failures. Owner autocheck:false approves visual quality, no artificial visual PASS. Remaining nine authored clip sets, foot pivots, other fighters, beast and advanced game features pending.

Trạng thái: PARTIAL — chưa hoàn tất.

## FINAL real post-deployment verification
LibreSprite #45804294005 SUCCESS actual new 3/4 editable six-frame candidate. Build/Windows/Web/Pages #45804293992 SUCCESS on PRIVATE 9318d2c4eb5ebfb0b06fb603867f394c20089be4 and PUBLIC 9e349c2b672d45894efeed331d092a651f14ba6e. Godot native test JADE THREE-QUARTER PREVIEW PASS. Real Chromium #45804607930 SUCCESS: P1.5 dx210px, Physics V2 climb2.14m/descent2.41m and real floor angles, Arcade V2 attacks/runs, NEW canonical Jade 3/4 S animated clip/PixelView floor PASS. Screenshots artifact #15109780115.
Historical build #45803632632 compiled PRE-image source 0621ad, not proof that new source was published. #45803665391 FAIL due unsupported Godot PackedByteArray.sha256_text in regression test; fixed PRIVATE 9318d2 using actual byte-array comparison, latest exact build supersedes this technical failure.
Single user-facing game URL only: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/. Owner artistic acceptance still pending. Only 1 of 10 original guard actions supplied (six frames, shoe pivots draft); nine other original fighter clips and full Beast Arena roadmap OPEN.

**Trạng thái: PARTIAL — chưa hoàn tất.**
