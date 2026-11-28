
# Sprite-release fastlane (2026-11-28)
- Public pushes in ci/ carry exact private-source SHA in ci/sprite-release-source.sha; mismatch blocks deployment before import.
- Public docs-only changes do not trigger a new Godot build. Full coverage still available on hourly schedule and manual workflow_dispatch.
- Fastlane retains Godot 4.7.2, native Base Idle/Walk/Punch/Kick actual scene tests, source scale audit, combat timing/pixel projection, isolated Web export, Pages deployment, actual Chromium E2E. Skips unrelated root P1/P1.5/Windows export/map-grid tests and private release upload only on fastlane; scheduled/full runs retain these.
- Verification MUST include a separate browser test at EXACT canonical no-query URL: ?e2e=1 is a distinct instrumented environment and its PASS does not certify the user's experience.
- Open issue: no-query G unresponsive for owner, even after diagnostic test PASS. Source fix private d7ec67d3068179bc2bedda5c33ee25be93b2237d standardizes Web controls and uses _input instead of _unhandled_key_input, but only exact successful build and owner-url E2E can confirm.

Baseline last verified before fix: Private 842f3c1876e44e851d1d47753ee00f418ff17e7c public 3c9d68c656bdbc8536cab67188b99938db5ca61a Godot/Pages #46162967616 PASS, Chromium #46163162919 PASS only on query-specific environment. New source d7ec67... requires exact fresh runs. **Trạng thái: PARTIAL — chưa hoàn tất.**

### Repair after first fastlane run
Build #46163994715 PASS including native BASE_KICK_G_INPUT_PASS and Pages. Browser #46164132268 FAIL in the **legacy root P1.5 route** with GitHub Pages not HTTP 200, before canonical G test. Verified root cause in new workflow: fastlane exported only /physics-v2/ and Pages upload replaced entire site; root / index missing. Corrective workflow imports/exports the root Web route on sprite fastlane, preserves two routes, still skips Windows, unrelated map tests, private release. Must rerun exact root and /physics-v2/ E2E; no source/art changes.

### Canonical browser probe repair (2026-11-28)
Private source 131d77eb84149b7d89eb1c90ecac98497b19010d exposes minimal read-only G keydown count, accepted real kick, PixelView drawn frames on exact no-query URL. Prior run #46164495394 failed screenshot-delta test (idle pixel changes 3073 vs peak 3046), because 22 synchronous SwiftShader screenshots were slower than the whole kick and sampled Idle, not the short impact. Browser fastlane now checks root route HTTP 200, no-query canvas autofocus, real G key event, accepted front_kick and actual PixelView drawn [0,1], and then captures one screenshot. Push fastlane skips unrelated P1.5/full-Base browser suite; scheduled and manual full suite still run unchanged. No test or private asset is removed. Await exact build, Pages and Chromium verification; PARTIAL until PASS.
