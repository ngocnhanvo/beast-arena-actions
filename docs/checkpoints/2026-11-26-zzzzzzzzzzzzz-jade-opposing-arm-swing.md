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
