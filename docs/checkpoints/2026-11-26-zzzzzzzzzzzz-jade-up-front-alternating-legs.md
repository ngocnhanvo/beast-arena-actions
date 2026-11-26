# Beast Arena Actions — W/up front-facing as S/down; explicit 80px alternate legs (2026-11-26)

## User manual review / new defect
The owner screenshot after the previous native-80px preview confirms **W moved north with an unconvincingly skating, back-facing fighter**. This is NOT a cosmetic PASS. Owner wants pressing W to preserve the face visible to the human viewer, just like pressing S. The user's review mode is `autocheck: false`: release a playable source change and let the owner judge movement art, no autonomous aesthetic/retry loop.

## Real source change
- PRIVATE `scripts/character.gd`: -Z and +Z world/combat directions remain distinct, but both map to **visual front column0**. A/D retain left/right visual orientation.
- PRIVATE `scripts/jade_approved_motion.gd`: front moving rows [3,4,1,2] alternate existing native-80px approved right/left stride shoe regions under native front upper art. No 40px upscaling or world/collider changes. Old rear frame composites remain compatibility-only; user will no longer see the back on W.
- PRIVATE `tests/visual_smoke.gd`: ART-27 verifies four distinct source 80px shoe regions, face unchanged, W/S same sprite index for identical phase while physics directions differ. ART-23/24/25 still require full-body, rows, correct grounded foot pivots.
- PUBLIC `ci/playwright_physics_v2.py`: W animation must physically travel negative Z, yet visually face index0; retains four genuine grounded-phase samples, pivot and J/K real-state assertions. New screenshot name `moss-jade-approved-up-front-motion.png`. This is an ENGINE/functional regression check, **not** user style approval.

## State before NEW release
Prior successful Pages [#45766825513](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45766825513) used a back-facing skating version; this is **not** validation of the current W/S correction. User has not signed off. Upon new source build, verify exact PRIVATE source SHA and PUBLIC pipeline commit in GitHub Actions; only then share https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved for owner W/S/legs/F5 check. Do not declare done from old PASS.

**Trạng thái: PARTIAL — chưa hoàn tất** (new build and owner visual signoff pending).
