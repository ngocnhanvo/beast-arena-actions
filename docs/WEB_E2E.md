
# Beast Arena Web E2E — 2026-11-25

Workflow: .github/workflows/web-e2e.yml
Script: ci/playwright_smoke.py
Target: https://ngocnhanvo.github.io/beast-arena-actions/?e2e=1

Evidence P0: run 45656492064 PASS on older source — game rendered, D moved +266.2 pixels. Earlier runs failed because tests inspected Godot canvas during loading splash.

New test is NOT solely pixel-based: Godot Web publishes a minimal opt-in read-only snapshot window.__beastArenaDebug when URL includes e2e=1. Wait for ready=true after WASM startup; verify canvas visible, StageData obstacles=2, Space causes jump event and positive height Z, J starts attack, D causes world-space player X to increase >=28. Store screenshot, browser DOM, errors and state snapshots as PUBLIC artifacts.

Do not mark the latest P1 build passed until a new Browser Playwright workflow run succeeds. Pressing U with beast meter below 50 cannot prove transformation. F2 toggles collision/obstacle/spawn markers for manual tests.

## Verified browser status
- #45656492064 PASS on pre-P1 source after fixing loader wait (D +266.2px).
- #45657184814 PASS on P1 source, Space/J/D state changes, player +224 world units.
- #45657791050 PASS with F2 collision debug true, screenshot plus player +227.5 world units, no critical browser JS/WASM/PCK request errors.
- Images and result.json are GitHub Actions public artifacts. Re-verify on each new rendering/logic release; these runs do not test combos, throws, multiplayer, or Android.

## Live P1.5 verification

On 2026-11-25, run https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45660829632 succeeded against published Web build. The script now also verifies two map IDs, both world sizes exceed 960x540, F3 far-side camera follow/clamp, switching to map 2 with key 2 and F4 return camera reset. Images and `result.json` are stored as Public Actions artifact; the asset and player state debug hook is only enabled by `?e2e=1`.

This verifies a preview, NOT fully interactive map editor functionality.

## 2026-11-26 — Obstacle visual smoke

Playwright run #45663585488 PASS for P1.5b ground-foot obstacle visuals.
Tests actual five visual models and five physical obstacles/map and height
metadata; captures screenshots on both large maps. The first CI build
#45662885191 failed in Godot editor due to missing @tool; corrected and
reverified build #45663247335 PASS. Remaining E2E plans:
height-aware vault and character-to-obstacle occlusion pixels.

## Physics0 new staging route and visual QA

New scene: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/
Built from PRIVATE `experiments/physics_v2` and exported to a nested
subfolder without modifying main P1.5 URL. Browser Playwright
`ci/playwright_physics_v2.py` exercises camera, 2 maps, World 3D
jump/acceleration and original image floor. Pillow checks floor brightness,
not only Godot readiness, to catch black WebGL material regressions.
Early browser #45668562257 PASS movement (+4.11m) but showed black floor;
later browser must confirm corrected art.


## 2026-11-28 — Actual original clear-line Physics V2 staging Web game E2E (separate from production)

- Code: PRIVATE `experiments/physics_v2/scenes/clearline_web_staging.tscn`, `scripts/clearline_web_staging.gd` inherits the real `scripts/demo.gd` and retains the existing `CharacterBody3D` with unchanged capsule, stage and motor. Dynamic visual layer is 24 source-time samples from one FK/IK original 6-cel vector art rig. Web Playwright keyboard motor test: `tools/pose_lock/vector_clearline/staging/playwright_actual_game_staging.py`.
- PUBLIC isolated `.github/workflows/rig-bound-clearline-native.yml` on exact source SHA `4ad0ddcbcf1ec01b97a7b54ecafbb07ee612e353`, workflow SHA `9334486c9a907842bfff16c4bcc662e32f12cb34`. [Actions #46056819234](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46056819234) **COMPLETED SUCCESS**, real Chromium Web PCK gameplay canvas, not an HTML source sheet: keyboard D drove real motor X -11.30→-4.43m, saw all 24 source frames, sampled 342 physics ticks, released D and verified speed 0, three staging screenshots and no JS errors. No public Pages deploy.
- **Runtime export trap:** Godot Web does not expose arbitrary raw staging JSON/PNG to `FileAccess` / `Image.load_from_file` reliably. Generate transient assets again after headless motor test cleanup, verify motion JSON & `art_release=BLOCKED`, insert exact JSON as temporary base64 GDScript String and import the transient 6×4 source atlas as typed `preload` Texture2D in runner-only scene; do NOT modify permanent production script/preset. Browser fail-closed diagnostic reports `window.__beastClearline` status and errors if Web state missing. Earlier runs #46054979390/#46055542805/#46056036453/#46056569063 failed and were fixed without bypassing checks.
- **Scope:** this is a genuine opt-in staged version of the original Physics V2 game, **NOT** production deployed Pages, artist-approved artwork, or a finished 8+ authored pose library. Only six original cels exist, 18 inbetweens derived. Art status `FAIL_NOT_PRODUCTION_QUALITY`, release blocked, owner acceptance absent, source PRs remain draft. PRIVATE images/screenshots remain ephemeral runner temp; no PUBLIC raw asset/Pages upload. Read current checkpoint `docs/checkpoints/2026-11-28-clearline-v6-real-web-game-e2e-source-qa-pass.md`.

## 2026-11-28 — Web screenshot HUD-only false-positive regression (isolated clearline Draft)

- **Test design issue, not proven gameplay bug:** the earlier stage check using nonempty screenshot/colors could greenlight only a colorful HUD or background. New PRIVATE `tools/pose_lock/vector_clearline/staging/screenshot_gate.py` checks actual screenshot region excluding top HUD, rejects flat scenes and requires meaningful changed pixels across before/moving/stopped real Godot Web canvases. Five independent synthetic controls reject black WebGL, HUD-only, static scene, and mismatched dimensions.
- [Terminal PUBLIC run #46059102869](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46059102869), PUBLIC workflow SHA `680ff794895566a45285e281fe2876b0b3e13bfd` pinned PRIVATE source SHA `265975f977f6b787a41ac6298302502ad63ab1ab`: **COMPLETED SUCCESS**, 50 portable plus 4 native plus 5 screenshot adversarial = **59 tests PASS**; LibreSprite native RGBA, Godot headless real motor, transient Web export and Chromium E2E also PASS.
- Real browser state: X -11.3000 to -4.6163m, all 24 frame indexes, post-key-up speed -0.0305m/s, 216 physics samples, 3 staging screenshots, 0 JavaScript errors. HUD-excluded crop [77,184,883,491] measured 114149 changed pixels, required 495; contrast 48.3/49.3.
- **Limit:** pixel delta can also arise from the world/camera, not necessarily the fighter art; this does not certify exact fighter silhouette, natural choreography, physical toe contact or aesthetic owner approval. PRIVATE raw images/screenshots stayed in ephemeral runner, never posted to PUBLIC artifacts/Pages. `art_release=BLOCKED` and owner signoff `NOT_GIVEN`; source/CI PRs stay Draft and Pages production is unchanged.
- NEXT: independently gate fighter-specific visible sprite pixels/phase identity in staging, then independently author/review genuine smooth 8+ run cels. Details: `docs/checkpoints/2026-11-28-clearline-real-web-screenshot-gate-59-pass-public.md`.
