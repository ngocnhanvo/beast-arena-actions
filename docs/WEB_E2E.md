
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

## 2026-11-28 — Actual organic-v8 art in real Godot Web staging (verified)

Previous #46090739701 compiled/checksummed v8 art but the real-game Web stage still used canonical v6; PASS did **not** prove v8 was visible. New isolated `--art-style organic-v8` generator exports the exact 24 original-rig time samples as a transparent 2880x1920 atlas and a manifest containing its PNG SHA-256. The stage embeds that JSON and preloads the actual Texture2D in the runner only; `clearline_web_staging.gd` rejects non-v8/missing SHA; Chromium checks v8 identity and identical hash while driving the real `CharacterBody3D` motor. Source/CI never uploads PRIVATE art/screen captures to PUBLIC artifacts or Pages.

[Run #46091560799](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46091560799) job `140813413017` **COMPLETED SUCCESS**, pinned PRIVATE `1f48ab01d21388c358b0974f97a25b44279c43e4`, PUBLIC `6c9c9f123ed80dbae40122a1b802166e74553ae7`. Actual `art_style=organic-v8-rig`, SHA `853bbc99dcad9184c42f6e79171f9511751669d4bea6f4aa20d09bfb6aa9b203`; 59/59 portable/native/screenshot controls plus v8 extra proof, real Web/Chromium E2E PASS: 24 frame indices, 264 physics ticks, X -11.30→-4.68m, braking, 3 screenshots, 122058 changed pixels in HUD-excluded world region, 0 JS errors. Output is a non-production staging draft. **ART FAIL_NOT_PRODUCTION_QUALITY / owner NOT_GIVEN**, six base rig cels +18 derived samples NOT 8+ original authored poses, Pages and main unchanged. Full handoff: `docs/checkpoints/2026-11-28-v8-actual-godot-web-art-integration.md`.

## 2026-11-28 — Folded-recovery v9 in actual transient Godot Web stage

v9 preserves the original motion_rig.py and its six canonical authored rig-based SVGs, and adds an isolated optical/anatomical recovery profile motion_organic_v9.py. F3 right and F6 left ankle are raised/retracted via the exact signed-branch IK solution; the 15/15 bones, planted world toe contact and arm FK are not altered. The staging exporter accepts --art-style organic-v9, generating 6x4 480px rig-frame atlases from v9 pose_at(t) and a blocked-release manifest with SHA, profile label and source identity. The actual Physics V2 Godot scene refuses older v8/old atlas identity; browser Playwright verifies the active sprite source SHA equals the generated PNG source. No public Pages assets or screenshots are uploaded.

Terminal [run #46092846821](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46092846821), PRIVATE exact SHA 4c9028deeabce733a17480db1ef22f8b448dc6e4, PUBLIC workflow e110f2727d15807c26a583b9d7d800591a01654b: **COMPLETED SUCCESS** with 56 portable +9 native/screenshot=65/65, strict LibreSprite, actual Godot motor, export Web and Chromium. Live v9 art style organic-v9-folded-recovery, atlas SHA eb39f675e5887aa22e9844529cc3591a929f904985f28448eb4b5047cc644812, 24 source samples, X -11.30 to -4.553m, 204 physics ticks, zero JS errors, HUD-excluded visual region 109312 changed pixels. This is neither 8+ independently authored art cels nor owner visual approval; original v6 and deployed production remain untouched. ART release BLOCKED; see docs/checkpoints/2026-11-28-folded-recovery-v9-actual-web-staging.md.
