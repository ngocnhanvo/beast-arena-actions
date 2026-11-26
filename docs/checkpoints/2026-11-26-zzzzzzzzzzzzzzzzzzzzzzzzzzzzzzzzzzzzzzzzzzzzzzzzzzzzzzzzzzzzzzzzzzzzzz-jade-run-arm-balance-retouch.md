# 2026-11-26 — Jade run eight-frame hand counter-swing retouch (legs locked)

## Owner feedback
On actual /physics-v2/ game, owner accepted the 8-frame leg rhythm but rejected uneven running hand motion. Do not change the legs, run speed, camera, animation timing, eight walking directions, or other clips. The actual release source remains native 80px cels and one canonical review URL.

## Source modifications (PRIVATE)
- Original editable Jade 8x2 atlas `experiments/physics_v2/art/drafts/jade_run_eight_16.png` retains 8 RIGHT + 8 full-body mirrored LEFT, with source ASE/PNG re-exported.
- Repainted near-side bent guarded arm in complete-source native RIGHT frames indices **2,3,4,5**, yielding a continuous arm swing back→front→back paired (0,7), (1,6), (2,5), (3,4); mirrored entirety to LEFT (8..15), not a runtime limb animation system.
- Original accepted leg pixels archived in `jade_run_eight_16_before_arm_retouch.png`. Strict invariant: **all eight RIGHT lower-body blocks y55..79 are bit-for-bit equal** to prior approved leg cycle; all eight LEFT whole-body mirrors. Frame order 0..7, existing foot y74, stride 0.50m/pose, run source duration85ms and 2 GPU draw holds unchanged.
- Updated `jade_run_eight_{right,left}.aseprite`, `jade_run_eight_{right,left}.png` and source metadata `jade_run_eight_16.json`. `art/fighters/animation_profiles.json` records source arm pairing and immutable-leg baseline. `tests/three_quarter_preview_smoke.gd` asserts precise lower-body source parity and the intended changed 2,3,4,5 arm regions.
- No updates to physics/engine character animation core. Existing prior 8-pose source retained via archived PNG and Git history for rollback.

## Public verification in progress
- Public documentation triggered actual `Godot CI` run **#45862343065**, `LibreSprite Art Toolchain` **#45862342943** (PUBLIC SHA 5e030612b2f5a98a9bef1682c6fa46d87da29d4b). Check final jobs, actual PRIVATE source checkout SHA, native smoke and exact editable ASE/PNG roundtrip.
- Once Pages deploy succeeds, check automatically-triggered exact Chromium E2E. Requires right/left A+A/D+D post-draw 8-frame sequence/wrap, eight walking directions, P1.5 and physics. Avoid reusing old #45859142995 PASS: that covered pre-arm-retouch source.
- Review on *one* URL only: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . `autocheck:false`: owner must judge actual arm balancing; never auto-approve artistic quality.

## Open work
- Sprite upper-body quality/leg-counterphase **PENDING_OWNER_REVIEW**, this is a first native retouch, not visually accepted.
- Idle authored breathing, punch and kick independent source art still PENDING_ART in wider roadmap.
- Check actual run results and update this checkpoint plus engineering log with evidence. If owner dislikes arm pose, **revise original full-cel editable ASE art** without a cropped-limb runtime hack.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## FINAL TECHNICAL EVIDENCE — 2026-11-26
- PRIVATE actually compiled source `efe38067a00c9ff76d313f462062b5120ce8576d`; PUBLIC pipeline that deployed Pages `5e030612b2f5a98a9bef1682c6fa46d87da29d4b`. GitHub-run SHA after documentation updates does not imply new game asset changes.
- [Godot build/Windows/Web/actual Pages deploy #45862343065](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45862343065) **SUCCESS**, all three jobs. Log explicitly **JADE RUN ARM CADENCE SOURCE PASS: middle four hand-painted counter-swing frames 2..5; all eight original leg/sole cels EXACT**, plus all 8 pose/wrap checks.
- [Pinned real LibreSprite batch #45862342943](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45862342943) **SUCCESS**; editable right/left eight-frame ASE sources each pixel-exact to corresponding 640x80 PNG, 85ms timings and guard tag, with four registered candidate clips total.
- [Pinned full Chromium E2E #45862698015](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45862698015) **SUCCESS** (attempt1). P1.5 PASS; Physics V2 climb 2.15m/descent 2.43m PASS; Arcade V2 PASS; real Jade A+A / D+D eight GPU-drawn full-body poses and 7→0 seam PASS, eight walking directions and idle unchanged. Public screenshot artifact ID 15137984673.
- **What remains:** `autocheck:false` owner has not confirmed aesthetic quality of the hand rhythm after this version; this is PENDING_OWNER_REVIEW and does not become VISUAL_ACCEPTED from technical test success. Full original ten-clip production character art and independent punch/kick/idle remain PENDING_ART in overall roadmap. No remaining technical blocker in this scoped source/Pages/E2E deployment.
- Next conversation: owner opens ONLY https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ , tests real D+D/A+A and notes whether hand pump has correctly alternating rhythm; if user rejects, use existing editable ASE sources to repaint individual whole native cel arm poses without any runtime limb-slice hacks; preserve leg pixel regression and repeat full CI/E2E.
**Trạng thái: PARTIAL — chưa hoàn tất.**
