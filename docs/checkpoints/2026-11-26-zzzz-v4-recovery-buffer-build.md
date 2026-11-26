# Beast Arena Actions — V4 bounded human combo build verification (2026-11-26)

**TARGET PRIVATE SOURCE (must match exact runtime):** `0af48c861537b1f8dd1bc6ff7d791a588cf0c62c`.

## New behavior under test
- Human player input J/K: one late-recovery queued follow-up in last six 60Hz ticks; recovery and startup are never canceled, no extra early hitbox.
- Every linked attack starts with a new attack instance, target-hit registry and physics-timed sprite rows 9 (wind-up) / 10 (real heavy contact). Hitstun/KO clears pending input.
- AI behavior unchanged, original Pixel 2D horizon, two real ramps, 4 original human atlases, G guard and 2v2, P1.5 root kept separate.

## Acceptance sequence (NOT asserted PASS by this commit)
1. Public `.github/workflows/build.yml` push-triggered Godot 4.7.2 parser/import and existing `combat_v2_test.gd`, `visual_smoke.gd`, plus all P1.5/V2 smoke tests.
2. Only after tests pass: Web + Windows export and PUBLIC Pages publish (per existing owner opt-in).
3. Follow-on `.github/workflows/web-e2e.yml` strict published source SHA/run gate, actual Chromium, screenshot with ground and real human sprite on both maps. Check E2E report, not job color alone.
4. Record resulting build/Pages/Chrome run IDs, step logs and screenshot evidence in this checkpoint. If FAIL, diagnose in PRIVATE engineering log and fix source; do not loosen physics or remove tests.

## Previous verified evidence
- PRIVATE runtime baseline `191842e4948d6f0a5a864a4c2c5815b240b2fd03`.
- Last Pages build #45735133772 SUCCESS, Chromium #45735342337 SUCCESS.
- This checkpoint commit is a **CI trigger** for the new private source; it is NOT proof of deployment.

## Outstanding
NES-style original art quality and user signoff; grabs/throws/advanced combos; map props/editor UX, route AI, device FPS, P1.5 migration, original V5 beast forms.

**Trạng thái: PARTIAL — chưa hoàn tất**
