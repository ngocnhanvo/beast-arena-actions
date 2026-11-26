# 2026-11-26 — WebGL six full-body Jade run pose hold / wrap gate

## Actual observed failure
- Exact prior Pages [#45846134771](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45846134771) SUCCESS, Chromium [#45846453321](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45846453321) FAIL in Jade A+A real sprint: rAF only observed [1,2,3,5], while Sprite3D selection bitmask 0x3F. P1.5/Physics/Arcade PASS. First earlier #45844648520 D+D missed pose 1. This is a **browser-visible-phase sampling failure**, not missing source cels.
- Owner reports unnatural last-frame leg reversal ("bị tật") and wants actual game repair, not detached sprites. A visual judgment remains owner PENDING_ART (`autocheck:false`).

## Scope
- Private source: generic `review_presented_run_phase` holds each 80px complete-body source cel >=85ms and >=2 true render updates, then advances exactly one sequential leg phase using 0.50m distance ticks. The 5→0 wrap must obey same hold; no motor/physics/map change.
- Original 480×160 Jade atlas has 6 original whole-body RIGHT and 6 fully mirrored LEFT cells; editable ASE source unchanged. Strict final >=8 authored run poses and punch/kick remain pending.
- Public `ci/playwright_jade_three_quarter.py` still observes all six real rAF displayed phases BOTH A+A and D+D, but allows up to 1850ms for low WebGL FPS source hold rather than racing six 85ms frames in 850ms. Stage/physical motion test still active.
- Native `three_quarter_preview_smoke.gd` explicitly tests two-render/minimum-duration frame gating, 5→0 seam, and six distinct cels; verify source SHA and actual test print.

## Evidence
- PRIVATE revisions: `7d73e6a`, `67f7119`, `018b06c`, `bfb07f8`; PUBLIC browser test `6f2c7c837a3ce68c082997058937fedad0b90b8d`.
- New triggered full [build #45848128995](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45848128995) was in progress at initial checkpoint. MUST check Godot/Windows/Web/Pages; exact subsequent Chromium E2E and art screenshots before claiming **technical** PASS.
- SINGLE reviewer URL: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ .

## Next
1. Fetch job steps/log for #45848128995 and exact `source_sha`; fix compile errors if any.
2. Inspect automatic browser workflow run. Require A+A/D+D six observed live phases, 5→0 native gate and 8-direction walk not regressed. Review screenshot artifact but do not self-sign-off art.
3. Ask owner to inspect actual source loop. If last->first anatomically still looks wrong, original extra whole-body transition art is required; never fake pose by cropping/shifting limbs. No alternative preview link.
4. Update both latest checkpoints and runbook with terminal result/next action.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## TERMINAL VERIFY 2026-11-26 22:27 ICT — technical PASS, owner visual PENDING
- PRIVATE source checked out by CI: `bfb07f867dcaaaae6c6ec38a4dd8250161bd5766`. PUBLIC exact build pipeline SHA `6f2c7c837a3ce68c082997058937fedad0b90b8d`.
- [Godot/Web/Windows/Pages #45848128995](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45848128995) **SUCCESS**, all 3 jobs including actual Pages deploy PASS. Godot log explicitly: `JADE SIX RUN FRAME HOLD PASS: source 85ms, >=2 render updates, sequential 5->0 seam`; 6 original native source frames each direction, 70px normalized character, eight-direction walk PASS. Native test warns about `Image.load_from_file` in a test-only audit path, not an export compile failure.
- [EXACT Chromium #45848462724](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45848462724) **SUCCESS**. P1.5 PASS (two maps/camera), Physics V2 PASS (2.17m climb, 2.35m descent), Arcade V2 PASS, `ONE CANONICAL /physics-v2/ JADE OWNER DESIGN SIX-POSE PASS`: strict browser E2E demands all six rAF phases for BOTH live A+A/D+D, source indices correct, idle and 8 walking directions unchanged. Artifact `beast-arena-browser-screenshots` ID 15133260807 was uploaded.
- OWNER ART: **PENDING_ART**. Six source cels exist, but draft `jade_run_owner_six_{right,left}.foot.json` currently has identical placeholder pivots x40/y75 for all six with `pivot_review_required:true`; do not pretend this proves believable grounded leg reversal. Full independent authored 8+ running poses, real punch/kick/idle source and owner gameplay visual acceptance remain pending (`autocheck:false`).
- NEXT: owner tests ONLY https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . If last→first still looks lame, correct native editable .aseprite whole-body contact keyframes/foot pivots, not a crop/shift-body-parts hack, then run same complete CI+Chromium.
**Trạng thái: PARTIAL — chưa hoàn tất.**
