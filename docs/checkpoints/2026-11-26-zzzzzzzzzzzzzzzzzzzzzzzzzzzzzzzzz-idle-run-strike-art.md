# 2026-11-26 — Jade idle breathing and sprint visual pilot, authentic punch/kick still missing

## Owner report and source evidence
Owner says idle breathing invisible, punch/kick/run visuals not okay. On actual PRIVATE game, `HUMAN_VISUAL_CLIPS["idle"]=[0]` means static, FRONT punch rows 7..10 are copied from a FRONT idle cel in `jade_approved_motion.gd`, and kick uses heavy punch fallback; F/G state tests are NOT proofs of animated strikes. Review six-cel native W/S Jade strip previously activated only while walking, so sprint fell back to static-front/two-frame legacy.

## Code changes (do not mislabel artwork)
- PRIVATE source `07d5dfb453815ecc221b0f62712c4ea540483e4c`. Shared 2s 1.0→1.035→1.0 whole-body micro breathing when truly idle, physical shoe contact anchored in BOTH Sprite3D and PixelView. Does NOT invent native painted inhale/exhale poses.
- Real sprint now samples existing W/S six complete 80px guard cels at 0.48m/pose forward, 0.56 side, 0.52 diagonal under existing 60Hz doubletap physical sprint; true run semantic tags continue, but original eight-cel run art remains PENDING_ART.
- No cropped limb or false generated punch/kick visuals. Exact debug statuses `WHOLE_BODY_BREATH_PLACEHOLDER_PENDING_CELS`, `REUSED_WALK_ART_PENDING_RUN`, `PENDING_ART_FRONT_PUNCH`, `PENDING_ART_INDEPENDENT_KICK`.
- PUBLIC `ci/playwright_jade_three_quarter.py` measures inhale/exhale, captures screenshots, verifies real doubletap sprint and native full-body six-cel review, still checks eight walking keys and size/tempo. Read-only debug flags use SAME canonical game document.

## Evidence
- [Actual Godot/Windows/Web/Pages #45823598975](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45823598975) **SUCCESS**, compiled PRIVATE `07d5dfb453815ecc221b0f62712c4ea540483e4c`, PUBLIC `8568d1516dfd1ce64f0a8557e42e3bfb136092aa`; native check printed `JADE IDLE/RUN PILOT PASS`, unchanged physics/combat regressions and Pages deploy.
- [Real browser #45823930933](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45823930933) is **IN PROGRESS at initial checkpoint**; inspect exact terminal status and screenshots; NEVER claim Chromium PASS from Pages success.

## User-facing and handoff
- Only demo link: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . User `autocheck:false` visual acceptance still required.
- The scoped pilot improves visibility of idle and run, but does NOT complete user's request for proper art: MUST independently author/tag full-body Aseprite/LibreSprite Jade `idle_guard_front` ≥4, `run_left_guard` and `run_right_guard` ≥8 each, `punch_front` ≥4, `kick_front` ≥5 native 80px frames with real startup/impact/recovery, planted-foot pivots. Never use punch frame to fake kick or image crop/paste body parts. No tool/library available currently creates accurate authentic art by magic; actual drawings remain necessary.
- Finish with terminal source/job checks, root cause log, owner review; original 10-tag all fighters/Beast remain separately pending.

**Trạng thái: PARTIAL — chưa hoàn tất.**
