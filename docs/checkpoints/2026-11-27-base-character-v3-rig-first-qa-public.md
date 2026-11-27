# 2026-11-27 — Base Character v3 rig-first independent source CI strict PASS (no game deploy)

## Source, QA and terminal run
- PRIVATE `main` origin `48dc2119981f26e9f010b279ff2520af99b2f99b`. Final independent PRIVATE rig source SHA `43b77cd190ae95f8f1a12ba1a06a2b60ebd785ef` (new docs-only later SHA), [Draft PR #5](https://github.com/ngocnhanvo/beast-arena/pull/5). Does not depend on rejected v2 branch or alter Jade [Draft PR #2](https://github.com/ngocnhanvo/beast-arena/pull/2).
- PUBLIC `main` `c72335df77237580e88066749a3411b58b5494a6`, source-only branch `ci/base-character-v3-rig-source-qa` SHA `1ee88aada8e5c306d71ec237be1d7a4cf358d5c5`, [Draft PR #3](https://github.com/ngocnhanvo/beast-arena-actions/pull/3).
- Real terminal [Actions #46000054846](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46000054846) **COMPLETED SUCCESS**, job `140509086721` actual log checked: `Ran 20 tests`, four original diagnostic outfits `training/armor/tunic/hybrid`, six frame x 20 independent editable layered Aseprite per skin, official pinned LibreSprite 1.3 STRICT RGBA_DIFF=0 each; Godot 4.7.2 isolated Skeleton2D import and 12-frame diagnostic with 0 engine ERROR, not live game.
- Local offline Chromium **24/24 exact RGBA** 4 skins x 2 facings x 3 frame samples, zero JS errors, NOT real-game browser E2E.

## Important correction recorded
Initial CI #45999753730 wrongly displayed success while logs contained `ERROR: Condition "det == 0"` due to zero default `Bone2D.rest`. PRIVATE fix initialized `Transform2D.IDENTITY` before attaching bones and turned off autocalc during procedural creation. PUBLIC CI now fails on ANY Godot `ERROR:`, not just parser errors. Second CI #45999907263 passed corrected branch, then exact final independent-branch #46000054846 passed. This is a verified source+editor technical gate and does not signify owner visual acceptance.

## Scope and separate blockers
- New rig is AUTHORING only: anatomy underbody with independent leg/arm/head/hair/gear layers, IK source and fixed six-frame native export. Visual art remains stiff diagnostic quality, **PENDING_OWNER_ART**. Its six frames do NOT satisfy current game 8+ combat-guard-run requirement. No main merge, no Godot Web gameplay integration, no Pages deploy.
- Separate existing public production build #45997858112 SUCCESS; its browser E2E #45998186272 FAIL because J attack never entered Godot attack state. This is unrelated baseline gameplay and should not be misattributed to v3.
- Don't put private source/PNG/ASE in public logs/artifacts. Single canonical URL remains `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/` unchanged. Owner `autocheck:false` decides art quality and later authorizes integration.

## Resume
Keep independent v3 PR #5 and public CI PR #3 DRAFT. User checks offline preview and six-pose visual movement. If corrected art is needed, update immutable PRIVATE source SHA in isolated public CI and wait for terminal; only after explicit owner source acceptance and build authorization expand to 8+ proper guard clip tags, run exact Godot+Pages+Chromium gameplay and update both checkpoints.

**Trạng thái: PARTIAL — chưa hoàn tất.**
