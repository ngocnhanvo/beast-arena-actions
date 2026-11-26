# Beast Arena Actions — four-phase opposing 80px arm-swing (2026-11-26)

## Scope
Owner directly requested fixing stiff hands during W/S running, which looks like dragging despite four stepping-foot frames. Both W/up and S/down must show the front face. User has set autocheck:false; user alone evaluates animation appearance, not an automated visual-quality loop.

## Source change to build
- PRIVATE scripts/jade_approved_motion.gd: from original approved 80px pixel cells, move two glove/forearm clusters in FOUR opposite stride phases; old arm pixels cleared before shifted placement to avoid ghost hands, red scarf and central face/vest preserved; true 80px source, not enlarged 40px.
- PRIVATE scripts/character.gd: four complete arm/leg phases for walking too, with the slower original physical-distance cadence preserved. No changes to 60Hz motor, physical Z direction, slopes, collisions or combat.
- PRIVATE tests/visual_smoke.gd ART-28: independent left/right arm-region differences, four unique poses each, opposite vertical swing, original central face/vest untouched. ART-29: four physical-distance phases for slow walking. ART-23/24/25/27 kept.
- PUBLIC existing Playwright still checks actual negative-Z W + front-facing image and four run phases, native grounded feet and J/K; it does not establish that arms look natural.

## Baseline and required next verification
Previous PRIVATE gameplay 96274aff26ad0e433709f6d1b25e7283664f7682 and PUBLIC pipeline daaae873bccce6cf950df12adee10b87b447b84e succeeded in Godot+Pages #45768105863 and real Chromium #45768366561, BEFORE the arm repair. These older PASS runs must NOT be used as evidence for the new arm patch.

NEXT: build current PRIVATE HEAD on current PUBLIC pipeline, verify ART-28/29 and exact source SHA, Web/Windows exports and Pages. Then ask owner to review live at https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved , testing W/S arm/leg opposition and F5, while original 80px face and grounded shoes remain clear. This source-native compositing bridge is not independently painted layered Aseprite animation; full content roadmap remains open.

**Trạng thái: PARTIAL — chưa hoàn tất** (at writing: new build/deploy and owner art review pending).

## New exact technical delivery VERIFIED
- PRIVATE actually compiled `eb2e32ae46b175e92f9ad12aa0567e85bcb6a932`; PUBLIC pipeline `cb53bf4fb94d6a01bc0c333c03f56c705c2f605b`.
- [Godot/Windows/Web/Pages #45770278285](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45770278285) **SUCCESS**, preflight, import/tests/export and Pages all completed. Real build job log asserts `APPROVED JADE 80PX COUNTER-SWING PASS: W/S same front, 4 shoe contacts, 4 opposite moving native-80px arm poses, source face/vest untouched, anchored feet; owner visual review pending` plus `All export checks passed.`
- Existing browser E2E auto-run [#45770517662](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45770517662) was IN PROGRESS on first note; check actual outcome and exact build/provenance before calling E2E PASS.
- Playable owner URL https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved . `autocheck:false` user reviews visual arm+leg swing himself; technical Web success is NOT artistic signoff. Rest of game roadmap remains incomplete.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## Verified 2026-11-26 browser J-press observation, robust event fixture
- [First actual Chromium #45770517662](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45770517662) **FAIL** (not art failure by itself). PRECISE evidence: test pressed J momentarily and sampled after fixed 55ms, saw `human_visual_gait=idle`, `human_sprite_frame=0`, `human_attack_frame=0`, player actually grounded with real clearance ~0.00084m, no damage, full source/pipeline match `eb2e32ae...` / `cb53bf4...`. P1.5 passed (224px move); Godot build #45770278285 already technically PASS. This snapshot cannot distinguish missed short keydown vs too-late frame capture; do NOT assert one particular cause.
- Browser fixture source `ci/playwright_physics_v2.py` [PUBLIC `5c68ec7c1d16996a526b7d49d18fb3e6b75f53ad`](https://github.com/ngocnhanvo/beast-arena-actions/commit/5c68ec7c1d16996a526b7d49d18fb3e6b75f53ad) corrects **technical event observation** without gameplay code or extra style/quality loops: focus real Godot canvas, hold one authentic Chromium J (then K) key-down until source Godot debug state proves `human_attack_frame>0` and visual row 7/8 (or 9/10), record exact observed attack data in JS at that moment, finally release key; wait actual attack/recovery end before K. This keeps failure strict on unresponsive keys, no manually injected debug/gameplay state or false positive from mere dispatch.
- The new PUBLIC build+Pages [#45770958180](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45770958180) has succeeded with exact compiled PRIVATE source `32b514546e6d2dec8d20381bd0cdcc204d1ce6f0`, PUBLIC `5c68ec7c1d16996a526b7d49d18fb3e6b75f53ad`; headless Godot ART-28/29 arm and 4-phase walk tests PASS. [Second Chromium #45771214382](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45771214382) was IN PROGRESS at first note. Check its final status independently; do not reuse old browser PASS to cover the new E2E.
- Owner autonomy: `autocheck:false`. Existing Chromium E2E checks engine functionality, not taste. Owner inspects real native 80px arm/leg counter-swing manually after publication; no art approval recorded.

**Trạng thái: PARTIAL — chưa hoàn tất** (new browser verdict and owner art approval pending).

## FINAL scoped technical verification 2026-11-26 — real Godot/Pages/Chromium PASS
- EXACT PRIVATE built source `32b514546e6d2dec8d20381bd0cdcc204d1ce6f0`, PUBLIC pipeline and real browser test `5c68ec7c1d16996a526b7d49d18fb3e6b75f53ad`. Later commits are docs-only and do not affect compiled game.
- [Build/Web/Windows/GitHub Pages #45770958180](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45770958180) **SUCCESS**: full Godot import/tests, ART-28 four source-native opposing arm poses independently for left/right and unchanged face, ART-29 four slow-walk phases, anchored shoes, exports and real Pages deploy.
- [EXACT real Chromium #45771214382](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45771214382) **SUCCESS**, expected pipeline `5c68ec7...` and expected build run `45770958180`. Browser P1.5 dx213.5px PASS, V2 physical ramp climb2.15m, descent2.43m, contact angles >=10deg, real dx12.55m PASS. J/K now confirmed via real focused Chromium held keydown + authoritative attack state. [Screenshot artifact #15094660972](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45771214382/artifacts/15094660972) exists.
- Preserve real earlier Chromium #45770517662 **FAIL** after 55ms J press/late snapshot returned idle; no proof of broken combat. PUBLIC `5c68ec7` corrected test real keydown/state acquisition with no game physics/combat/art changes. New exact browser pass supersedes old technical failure for that fixture, NOT the manual artistic check.
- **USER `autocheck: false`**: no autonomous appearance approval. Owner must play https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved and decide if the 80px left/right arm swing counter to shoe contacts looks natural W/S and if F5 views remain clean. This remains a native-pixel compositing preview, not authentic full hand-authored four-way Aseprite animation. Overall game roadmap remains open.

**Trạng thái: PARTIAL — chưa hoàn tất** (technical build/E2E PASS; owner graphic signoff + full roadmap not completed).
