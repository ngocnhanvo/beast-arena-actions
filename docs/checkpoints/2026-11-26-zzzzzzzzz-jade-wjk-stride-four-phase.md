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
