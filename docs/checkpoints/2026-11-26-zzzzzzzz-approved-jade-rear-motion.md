# Beast Arena — approved Jade rear-motion repair (2026-11-26)

**Status on source commit: PARTIAL — CI/Chromium release gate still pending.**

## Exact scope and baseline
- Owner requested continued implementation of the **one exact expressive Jade** from the user-approved image; **no stage, HUD, physics, hitbox, AI, grab or beast-form feature changes** this iteration.
- Baseline PRIVATE compiled gameplay source `03a34e696c1d48fe0910294637bcb98bfa8a59db`, PUBLIC pipeline `5ba8919f938b54fae5a1eaaab6b98c3048a7204b`: Pages #45751045283 PASS, real Chromium #45751278124 PASS, artifact 15085976043. Last approved Web demo `?pixel=1&art=approved`, F7 toggle.
- Root cause **verified** against exact approved PNG with SHA256 `43b866e32d484e8d618f930f942c85ff1728159f79df1c0064dbe28ceedbd266`: rear-facing (direction 3) all 20 rows have identical standing pose, including walk/run/attack/KO. This is a sprite-source art gap, not faulty motion physics; current Godot selects proper pose rows.
- Source reference remains `experiments/physics_v2/assets/jade_approved_80f.png`: exact 320x1600 original 80px cells untouched, not replaced with low-detail vector blocks or third-party sprite rips.

## Narrow code fixes (PRIVATE)
- New `experiments/physics_v2/scripts/jade_approved_motion.gd` commit `3ef221bd`: runtime visual-only adapter builds a cached ImageTexture from original PNG, preserving its pixel style and all source non-rear rows. Rear walk1/walk2/run1/run2 retain authentic rear hair, scarf and jacket, but use original artist's moving legs below y=55; all four show visibly distinct legs (locally audited ~1000 altered pixels each). Rear jumping, punching, damage, knockdown, get-up, victory and KO temporarily use authentic action silhouettes from same illustration instead of standing idle.
- `demo.gd` commit `111e900d`: F7 and `?pixel=1&art=approved` select the cached visual-only atlas. Original PNG remains the source, 80px ×0.020m scale and HUD portrait match mode. Existing F6/P/classic modes unchanged; physical feet, 60Hz attack state, 3D hitboxes, damage, slope/camera, AI untouched.
- `visual_smoke.gd` commit `2c0bc2fc`: ART-22 requires changing all four rear gait rows, non-standing rear KO/fallen states and byte-identical original 60 non-rear pose cells. Retain ART-20/21 80 nonempty source cells/scale/physics parity.
- PUBLIC `ci/playwright_physics_v2.py` commit `ef1b42be`: while F7 is enabled press W in real Chromium, demand an actual rear-facing walking/running frame and 80px atlas, save screenshot `moss-jade-approved-rear-motion.png`, verify return to idle and original tests. This is an *actual Web game* gate, not a sheet screenshot substitute.

## Visual QA and limitations
- Developer inspected an original-source vs adapted-contact-sheet comparison; optional review artifact `/mnt/data/beast-jade-rear-motion-before-after.png`. The code preserves expressiveness of the approved head/scarf/body; **this is NOT 80 newly hand-drawn directional keyframes**. Missing artist-approved rear attack / jump / fall cells are displayed using temporary original side-on authored poses. Rows 8/10 contact art in the supplied image are smaller than adjacent windup poses; those still need real manual keyframe art. No claim of final art approval.

## Acceptance / next turn
1. Public build [#45752674592](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45752674592) started with Public `ef1b42be`; verify precise PRIVATE compiled HEAD against `2c0bc2fc9612538c5a25779aaf802fb2e23be44f`.
2. Inspect all Godot headless tests including ART-22, P1.5/2D/3D slopes, combat and AI. If failing, fix source and record job log. Then Web+Windows and Pages must be successful.
3. Verify auto Chromium Web E2E with exact source+pipeline+build ID and `moss-jade-approved-rear-motion.png` screenshot, not just green Actions status.
4. After pass, inspect real image with rear animation at in-game scale and link preview. Owner has not explicitly approved the last version's visual result yet; advance unique source animation frames only after authentic art review.
5. Remaining roadmap still open: full independently illustrated 4-facing animations (especially punch contact and fall/recover), matching scene paint/foreground, AI/navigation, throws, device QA, root game migration, V5 beast form.

**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — FINAL VERIFIED Jade rear gait release (SUCCESS, art still not approved)

- **Authoritative functional asset implementation:** `jade_approved_motion.gd` `3ef221bd`; `demo.gd` `111e900d`, `visual_smoke.gd` ART-22 `2c0bc2fc`. Original expressive user-approved `jade_approved_80f.png` source is UNMODIFIED; 60 non-rear cells byte-identical, four rear walk/run rows animated, rear prone/KO no longer upright. Provisional rear attack rows still use same artist's side silhouettes. Physics, speed, hitboxes, HP and original stages untouched.
- **EXACT PRIVATE GAME compiled into verified release:** `3ba321b322918288dbe6baa402184319747fcba8` (docs-only changes after functional source); **PUBLIC CI commit** `1442efc120d3de898da11588e0e86571769ce4d5`.
- **FINAL strict Godot, Web, Windows export and GitHub Pages:** [#45753711701](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45753711701) **PASS**; actual log contains `APPROVED JADE ART PASS: source-preserved 80 PNG cells, fixed rear gait/KO, unchanged 3D foot and HP`, `VISUAL SPIKE PASS`, `2D VISUAL ADAPTER PASS`, `COMBO V4 PASS`, `All export checks passed`.
- **FINAL REAL Chromium** [#45753939789](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45753939789) **PASS**, strict EXPECT pipeline `1442efc1`, EXPECT build ID `45753711701`. Browser log `PASS P1.5 ... dx=210.0`; `Physics V2 Web PASS: climb=2.08m, descent=2.41m, actual contact angles >=10deg, dx=8.84m`. Real downloaded [screenshot/report artifact 15086424989](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45753939789/artifacts/15086424989). `physics-v2/result.json.status=PASS`; `user_approved_jade_rear_motion={active:true,direction:3,pose_row:4,gait:"run"}`; approved F7 80px changes 16061 actual canvas pixels with identical HP and map; 4 fighters, 32 visible Moss and 30 Docks ground details. Actual real WebGL image `physics-v2/moss-jade-approved-rear-motion.png` personally inspected.
- **Do not hide earlier FAILS.** First Chrome #45752879529 failed AFTER capturing rear-run image because added test improperly waited for instantaneous idle speed on actual physics slope; fixed public E2E `fbe363e7`. Second Chrome #45753426222 failed old D-run gate (`gait=airborne`, vx=4.2) due to NEW W sprite fixture contaminating real Z/airborne state before the next test; fixed `1442efc1` by invoking existing T reset after W capture. Third Chrome #45753939789 PASS. No physics tests weakened/removed.
- **Critical visual honesty:** In actual Chromium screenshot, Jade's leg silhouettes extend sideways, making W rear-running look unusually horizontal/airborne. The repair eliminates frozen rear gait but is NOT final visually acceptable authored back-running animation. The original user art reference is approved direction, not final animation signoff. Next artist task MUST draw authentic rear 4+ walk and run keyframes from the approved style, full-body punch contact rows 8/10 at consistent size and back-facing take-hit/knockdown/get-up, not crop/translate/fake source silhouettes. Then test real Web PNGs. Do NOT prematurely polish map/beast/AI before user sees finished one fighter.
- **Play:** https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved ; hold W for rear movement, F7 toggles original classic vs approved illustration, F5 toggles 2D/3D. Root P1.5 unchanged.

**Trạng thái: PARTIAL — chưa hoàn tất**
