# 2026-11-28 — Clearline v6 real CharacterBody3D + Web Chromium gameplay E2E terminal PASS, art blocked

## Exact immutable evidence and secure scope
PRIVATE source/Skill/original SVGs tested SHA `4ad0ddcbcf1ec01b97a7b54ecafbb07ee612e353`; PUBLIC isolated workflow tested SHA `9334486c9a907842bfff16c4bcc662e32f12cb34`; [GitHub Actions #46056819234](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46056819234) **COMPLETED SUCCESS**, job `140701223640` terminal SUCCESS. Both PRs #18 PRIVATE and #17 PUBLIC remain DRAFT and unmerged.

Actual runner: `Ran 50 tests` (portable positive/adversarial original motion/SVG), `Ran 4 tests` (game-native), all 6 original Git SVG bytes match deterministic rig, world-space stance toe, official LibreSprite native 15 layers/6 original frames/14 blank gear strict RGBA and isolated Godot 480px source import PASS. **Workflow printed 41 portable tests (outdated name), but actual unittest count 50; record actual output, not stale label.**

## The missing bridge actually verified
PRIVATE staging builds a temporary **24-sample 6×4 480px** PNG+JSON from the exact 6 original rig-source SVG poses, with 18 derived inbetweens. Uses real `BeastPhysicsCharacter extends CharacterBody3D` and `BeastPhysicsStage` on actual colliders and real acceleration/braking. Headless motor: grounded 100 ticks, moving 99, all 24 source indices, 30/17 right/left stance samples, max quantized painted toe drift 0.055m, collider unchanged.

Runner creates an isolated Web export in temp, stages an alternate Physics V2 original Demo scene with clean-line unapproved `Sprite3D`, moves it from **actual** motor X distance rather than independent timer. Real Chromium Web game keyboard D drove X -11.30m→-4.43m, sampled 342 physics ticks, saw 24 frame indices, released key and motor stopped at 0m/s, captured 3 transient screenshots, zero JS page errors. Logged `BEAST_CLEARLINE_ACTUAL_GODOT_WEB_GAMEPLAY_CHROMIUM_MOTOR_PASS` and `BEAST_CLEARLINE_ACTUAL_GODOT_WEB_GAMEPLAY_E2E_PASS_NO_DEPLOY`. Godot `index.html`, `index.wasm`, `index.pck` export in temporary CI **not** Pages or game production.

## Actual failure lessons / no test bypass
- #46054144882 failed exact source because an oversized Files read only returned 5/16 files; fixed with smaller Git source groups.
- #46054395742 needed Godot `--editor --import --quit` for the project's global `class_name` registry.
- #46054979390, #46055542805, #46056036453 failed real Web `ready`; sanitized browser diagnostic proved Web booted but staging source JSON was missing; raw Image load also incompatible with export.
- #46056569063 failed when the headless motor CI step intentionally removed its staging assets; fixed by regenerating them ahead of Web export.
- #46056819234 PASS required exact source generation again, runner-only embedding of verified original JSON into temporary GDScript and Godot imported `Texture2D` atlas preload. PRIVATE source continues to fail closed, so absent staging pixels cannot accidentally become release assets.
No PRIVATE image or browser screenshot was uploaded to PUBLIC repo, Pages or Actions artifact. Publishing was NEVER triggered.

## Remaining release gates
`visual_self_review=FAIL_NOT_PRODUCTION_QUALITY`, `art_release=BLOCKED`, `owner_visual_acceptance=NOT_GIVEN`. Six original art cels are not 8+ actual independently-authored run cels; real Web motor E2E is only **staging** and not public production deployment or aesthetic acceptance. Preserve draft PRs and production Jade/Physics/Pages. Continue original 480px SVG artist shaping and all action/direction/skin QA, owner visual approval, authorized merge/deploy, and public game E2E after art accepted.

Next continue from current PRIVATE checkpoint `docs/checkpoints/2026-11-28-clearline-v6-real-motor-web-e2e-staging-pass-art-blocked.md`; PUBLIC `docs/START_HERE.md` must point here. Do not rerun completed v6 tests for documentation-only changes.

**Trạng thái: PARTIAL — chưa hoàn tất.**
