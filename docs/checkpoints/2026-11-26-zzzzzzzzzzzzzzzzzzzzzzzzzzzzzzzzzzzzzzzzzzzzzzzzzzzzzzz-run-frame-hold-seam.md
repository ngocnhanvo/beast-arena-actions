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
