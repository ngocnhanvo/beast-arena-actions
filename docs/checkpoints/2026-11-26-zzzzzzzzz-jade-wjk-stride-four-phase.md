# Beast Arena Actions — W J K full-body sprites and 4-step actual-distance gait

Target PRIVATE source `fca9032d24dfce548930a9aaac596bbdc6356793`.

## Scope
Jade original user-approved sprite art remains `jade_approved_80f.png` (immutable). Private asset `jade_wjk_motion_pack_40.png` is a 160×200px original 5×4 sprite source, uploaded in corrected exact Git blob SHA `18af74665f6add4676124a638d5d2283187ee6d5`. The compositor scales to 80px and replaces ONLY W/JK frames. New native 3D `move_and_slide` actual XZ ground distance controls four distinct run poses per direction. No attack/collision/terrain/motor parameter is changed.

**Public E2E:** `ci/playwright_physics_v2.py` commit `31a91686` tests F7 approved player, W 4 phases and >0.9m actual travel, rear-facing J/K physically timed complete art screenshots `moss-jade-approved-W-J.png` and `moss-jade-approved-W-K.png`; old controls and browser/physics tests retained.

## Failed first attempt and mandatory revalidation
- Initial public CI [#45756722134](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45756722134) **FAIL** Godot PNG import; log `ERR_FILE_CORRUPT` on new asset, Pages **SKIPPED**.
- Root cause **VERIFIED:** GitHub uploaded blob `30ba16e...` had exactly two wrong base64 characters within IDAT; PNG CRC32 IDAT failure. IHDR/PLTE/tRNS/IEND intact. Corrected blob `18af74665f6add4676124a638d5d2283187ee6d5` exactly matches `git hash-object` local PNG, committed privately as `facdbdfe`. Hence next run must use the corrected exact source SHA.
- Next public pipeline must PASS all Godot parser/import ART-23/24 tests, physics 60Hz, 3D slopes, root P1.5, Web+Windows export, Pages, and automatically spawned real Chromium. Browser report must include W phase 0/1/2/3 and W J/K screenshots. Do not call PASS from green build alone. Any failures: inspect job logs, fix private/public source, rerun.

**Current checkpoint status: PARTIAL — chưa hoàn tất.**


## Second actual CI failure — fixed, rebuild required
- Corrected PNG import/CRC PASSED in build [#45756981894](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45756981894), but Godot ART-24 FAILED (`W did not alternate correct rear foot phase 0`), Pages SKIPPED.
- Actual test-fixture cause: 3D player starts 0.12m ABOVE floor; headless visual test attempted run immediately after scene load while `is_on_floor` was still false. Correct runtime selected airborne jump row5. PRIVATE fix `a4cfa3a481705cfa67acb48081c4b9d6a6911143` requires 20 REAL physics ticks for landing and verifies on-floor before gait frame assertions. No gameplay motor or combat rules modified; **do not suppress ART-24**.
- **NEW TARGET PRIVATE source:** `52751133013b5ad1cc59fb4163c73f8cf101180c`. This PUBLIC docs commit must trigger third Godot+Pages pipeline; then strict Chromium E2E with 4 foot phases and W J/K true source frame screenshot before any PASS claim.

**Trạng thái: PARTIAL — chưa hoàn tất**


### 2026-11-26 — WJK browser false-negative due Web test running off stage (verified)
- **Corrected-source Godot/Pages** [#45757152728](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45757152728) **PASS** compiling PRIVATE `52751133013b5ad1cc59fb4163c73f8cf101180c`. Real logs show `APPROVED JADE WJK PASS`, full-body J/K on all four facings, four unique run phases, preserved physics/combat/slopes, exports Web/Windows and Pages success.
- Auto browser [#45757397328](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45757397328) **FAIL** with `AssertionError: W did not alternate four distance-driven foot phases: {'phases': [], 'distance': 11.90024876594544}`. P1.5 browser PASS; `moss-jade-approved-rear-motion.png` screenshot successfully captured, user-facing hand-painted Jade rendering visible. **Verified cause:** new Python→Chromium 22× `snap(page)` loop held W long enough that the real 3D player crossed almost 12m and fell off the compact stage, so later snapshots all showed `gait=airborne`. This is test-induced extra motion, not evidence of no alternating steps.
- **E2E-only fix PUBLIC `a49a07a549b3eb09215a52a5e65bcefce0800c9b`:** collect every `requestAnimationFrame` debug state inside Chromium during an 850ms W stride, then require ALL 4 phases, correct rear facing and >0.9m native `move_and_slide()` ground distance. No physics speed, hitbox, gravity, stage bounds or source art changed. New public [Godot/Pages #45757669329](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45757669329) **PASS**; automatically triggered Chromium [#45757885478](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45757885478) **QUEUED** when checkpoint written, must be checked before Browser PASS claim.
- First two earlier failures remain documented: corrupt PNG IDAT base64 corrected with matched Git blob hash, and ART-24 fixture tried running before landing. All addressed with strict tests retained.
**Trạng thái: PARTIAL — chưa hoàn tất**
