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

## VERIFIED exact new source Web publish
- PRIVATE actually checked-out & compiled `96274aff26ad0e433709f6d1b25e7283664f7682`; PUBLIC pipeline `daaae873bccce6cf950df12adee10b87b447b84e`.
- [Godot 4.7.2/Windows/Web/GitHub Pages #45768105863](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45768105863) **SUCCESS**: preflight, import/test/export, Pages deployment all completed successfully. Actual GitHub job log contains `APPROVED JADE 80PX PASS: W/S same front view + 4 distinct native-80px left/right shoe contacts, physical foot pivots; owner art review pending` and `All export checks passed.`
- Older technical build #45767939805 on prior doc head and same functional code also SUCCESS but use **#45768105863** as authoritative newest source+pipeline release.
- Normal pre-existing browser smoke may run as an automatic `workflow_run`. No custom self-iterating screenshot acceptance loop is authorized while `autocheck: false`; owner visually decides whether the feet genuinely animate well.
- Owner preview: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved . W up and S down must both show front face and foot phases; test at own pace.

**Trạng thái: PARTIAL — chưa hoàn tất (technical Pages PASS; owner art approval pending).**

## 2026-11-26 — Latest actual Chromium result for front-facing W
- Exact PRIVATE compiled `96274aff26ad0e433709f6d1b25e7283664f7682`, PUBLIC pipeline `daaae873bccce6cf950df12adee10b87b447b84e`.
- [Godot/Windows/Web/Pages #45768105863](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45768105863) **SUCCESS**: preflight, import/test/export, Pages deploy all completed.
- [Actual Chromium #45768366561](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45768366561) **SUCCESS**, expected pipeline `daaae873...` and expected build run ID `45768105863` shown in job log. P1.5 browser dx 220.5px PASS; Physics V2 native uphill2.15m, downhill2.37m, angles >=10deg, horizontal dx9.83m PASS. [Screenshot artifact #15092424367](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45768366561/artifacts/15092424367) produced. Earlier Chromium #45768153673 also succeeded but used previous pipeline `ac640f...` and build #45767939805, so prefer newest exact pair.
- Browser asserts real W velocity -Z on ground with visual front-facing index0, four rendered shoe phases and unaffected physical combat; **technical PASS != appearance approved**. `autocheck: false`: no extra style-review automation, manual user signoff required. Original user screenshot of back-facing skating is obsolete for this new build, but current gait naturalness is still unverified by owner.
- Next: owner opens https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved and checks W/S front facing, alternation of stepping, side A/D, Space/J/K and F5. If unacceptable, replace temporary composites with native 80px individually authored, editable animation source.

**Trạng thái: PARTIAL — chưa hoàn tất (technical build/browser complete, owner art signoff and full roadmap open).**
