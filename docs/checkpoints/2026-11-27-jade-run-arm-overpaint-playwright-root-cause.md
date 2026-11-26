# 2026-11-27 — Jade eight-pose running arm overpaint / Playwright real motion diagnosis

## Owner report
Owner reports "animate bị lỗi" after native eight-frame hand retouch and asks autonomous Playwright investigation. Owner previously accepted 8-frame LEGS; do not touch feet/motor/physics, one game link ONLY: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . `autocheck:false`: no automatic aesthetic acceptance.

## Verified root cause in source
- Recoverable original clean 640x160 native RGBA 8 RIGHT + 8 whole-body mirrored LEFT from source commit `b57eef3ad6ebff899d519249d7b33e1436d16d14`; verified all five original PNG/.aseprite blob SHAs.
- Latest editable source `jade_run_eight_16.png` after arm patch had additive black/skin brush strokes/polygons painted directly OVER original arms on RIGHT source frames 2,3,4,5, leaving underlying anatomy. Pixel byte diff compared to clean baseline, per frame: f2=578, f3=681, f4=652, f5=553 changed bytes; f0,f1,f6,f7 unchanged. Enlarged source comparison shows oversized dark rectangular gloves across torso. This is not a clean opposite-arm redraw and visually glitches. Regression was authored in offline `repair_jade_arm_cycle_v4.py` (NOT a native tagged clip).
- Old STRICT WebGL E2E #45862698015 PASS for 8 selected/GPU phases, but this did not check human arm anatomy, thus it falsely appears to validate art. Always distinguish technical E2E and visual inspection.

## Playwright real browser evidence
- New PUBLIC `ci/playwright_jade_motion_diagnostic.py` & `.github/workflows/jade-motion-diagnostic.yml` launched actual Chromium on canonical Pages, records real canvas per phase/ video and browser requestAnimationFrame telemetry, no state spoofing.
- Diagnostic #45864460748 SUCCESS collected artifact ID 15139676988: live screenshots only right phases [0,5], left [0,1,7] when synchronous canvas screenshots were taken, while engine GPU-history had whole [0..7]. Each screenshot could stall SwiftShader for seconds: sampling-induced freeze, **not proof** real owner GPU is similarly slow.
- Repeat uninterrupted-video/rAF diagnostic #45865195144 SUCCESS artifact ID 15140466496: browser rAF right phases [0,2,4,5,6,0,1], left [0,2,3,5,7,1,3,4]; max renderer rAF interval 1139ms/803ms respectively, with 20ms median: runner has severe software-renderer stalls. Godot internal history still covers [0..7] (right); do not claim screenshot tester validates continuous visual motion in normal GPU. These are runner conditions and require separate real-browser owner check. Script rerun #45864815819 FAIL was solely stale source SHA after docs-only rebuild, not a gameplay fail; diagnostic fixed to record current live SHA.

## Scoped fix already committed PRIVATE
- Source commit `cd4b919d2e6da5ac550e59d0a852e316f424fc03` atomically restores clean original native 8x2 atlas AND separate right/left PNG + both native editable ASEs (five binary original blobs), leaving intact every accepted 8-pose leg pixel and original whole-body mirrors. Removes malformed hand-overpaint (not runtime patch). This returns hands to last clean source, **not necessarily an approved final hand cadence**.
- `art/drafts/jade_run_eight_16.json`, `art/fighters/animation_profiles.json` accurately tag `OVERPAINT_REVERTED_HAND_CADENCE_REAUTHORING_REQUIRED`. New native `three_quarter_preview_smoke.gd` demands byte-for-byte restored 8+8 full-body PNG source equal to saved baseline and real 7→0/3→4 clip contracts, preventing black overpaint reintroduction. No motor/run gait or UI code touched.

## Required downstream verification
1. Trigger PUBLIC full Godot/Pages and real LibreSprite toolchain, prove game source SHA, successful export/deployment, and native `JADE RUN ARM OVERPAINT ROLLBACK PASS`. Check actual run IDs/logs.
2. Exact post-deploy Chromium E2E, confirm 8 directions/8 run drawn GPU phases, Arcade, slopes, camera. Distinguish transient Playwright software-renderer rAF stalls from reproducible game bug.
3. Owner inspects ONE canonical /physics-v2/ URL. No art acceptance implied by CI. If still uneven, commission/design genuinely independent whole-body arm counter-phase in editable ASE; no thick brush overpaint, cropped-hand patches, or physics tweaks.
4. Update both START_HERE, engineering/runbook and checkpoint with exact run evidence.

**Trạng thái: PARTIAL — chưa hoàn tất.**
