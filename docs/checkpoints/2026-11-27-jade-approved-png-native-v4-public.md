# 2026-11-27 — Jade owner-approved PNG concept → native v4 isolated QA

- Source Draft PR #2 exact SHA `f0c1feab04649abd31cb899e6ca4e3074e4c8970` contains 8+8 edited native original ASE/PNG, strong rear fist back by hip and lead guard forward, 640x160 atlas, 85ms and foot/head/leg invariants. The illustrated PNG approval does not mean the 80px version is already visually signed off.
- Public isolated workflow `ci/jade-pr2-source-check` pins PRIVATE exact SHA using existing read-only token; Node22 uses v4 source and GIF check, independent Python with v4 guard landmarks, pinned LibreSprite1.3 RGBA, Godot4.7.2 import/guard/Jade smoke, Chromium local GIF playback.
- No source private pixels in public checkout artifacts or public logs beyond sanitized test counts. No merge/deploy or Pages export. The previous v3 [#45939974579](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45939974579) cannot verify this new v4.
- Check terminal run, reconcile all failures and update checkpoints and Issue/PR with actual evidence. Owner native visual remains pending, run-to-idle Issue #3 out of scope.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## Exact source v4 — isolated QA terminal evidence (2026-11-27)

- PRIVATE native source art SHA `f0c1feab04649abd31cb899e6ca4e3074e4c8970`, PUBLIC QA SHA `a3ae236ea2c7b4b4c0a68726cbbc0b53861590de`.
- [Workflow run #45942733770](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45942733770) **completed SUCCESS, 3/3 jobs passed**, not a game deploy.
- Pinned Node22: source ASE/PNG reconstruction 16 native cels PASS; reviewer GIF reproduction PASS, 16-frame 1360ms full two-cycle and 18-frame 2040ms run→idle comparison.
- Independent Python: native source verifier PASS, including accepted frozen face/feet, 8+8 whole-body mirror, metadata pivot Y74, timing 85ms, and rear/forward fist geometry.
- Pinned LibreSprite 1.3: RIGHT `visible_diff=0 transparent_rgb_diff=0`, LEFT `visible_diff=0 transparent_rgb_diff=0`.
- Godot 4.7.2: import script errors 0; guard profile native smoke PASS; three-quarter Jade smoke PASS, script errors 0.
- Chromium real GIF loop playback: 8/8 run frames, 9/9 run→idle source comparison, F7→F0 seam observed, unmatched=0.
- This certifies **exact source technical fidelity and local GIF playback only**; no main merge, no public Pages deploy, no in-game A+A/D+D E2E. User approved the illustrated 1254px concept, but has not separately seen/approved the reduced 80px native implementation; leave source visual approval pending.
- Issue #3 handles actual directional run→idle transition separately.
