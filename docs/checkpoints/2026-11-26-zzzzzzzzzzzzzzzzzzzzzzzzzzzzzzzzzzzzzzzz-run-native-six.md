# 2026-11-26 — Six ORIGINAL native full-body running poses, not short-step W/S reuse

## Owner reference and requirement
Owner supplied six running character frames and instructed IMPLEMENT IN GAME CODE, not generate/show unrelated drawing. Same sole owner Pages preview https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . `autocheck:false` means manual visual signoff.

## Source discovery + implementation
PRIVATE source content commit `97591b1c42808744bc73166460a0996f60875a36` (followed by docs-only `d831619857cb4f9acbe6ab861479c9268c9c57bb`). Existing actual original Jade RGBA 4×20 native 80px atlas has SIX distinct whole-body side-running silhouettes, rows **[1,3,4,5,19,2]** in original col1 for LEFT (atlas indices **[5,13,17,21,77,9]**) and original col2 for RIGHT (**[6,14,18,22,78,10]**). These original sprites preserve Jade hair/scarf/face/guard gloves/legs and longer sprints. No runtime limb cut/paste or fabricated image generated.

PRIVATE `art/fighters/animation_profiles.json` added optional `jade_human.run_review`; generic `fighter_animation_profile.gd` and `character.gd` validate six distinct full-body original native 80px frames, preserve 70px alpha-painted size/foot anchors, use actual left/right art on real A+A/D+D sprints, pace 0.50m/frame. The accepted eight walking directions, physical motor, slopes and combat unchanged. Source remains owner-review pilot; strict final 8-frame per-side independent run tags still `PENDING_ART`.

PUBLIC `ci/playwright_jade_three_quarter.py` now verifies BOTH live A+A and D+D physical sprint velocities, requested semantic tags, six original source row/column indices, six-frame progression, native-80px source, in-game screenshot of each, plus W/S/A/D/diagonal walk, idle breathing and map ground. Report actual screenshots; don't infer visuals from keyboard events alone.

## Actual Actions evidence
- Initial [#45827624972](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45827624972) failed because native TEST called unsupported `PackedByteArray.md5_text()`; source code was fine. Replaced test hash with `get_data().hex_encode().md5_text()`.
- [Native build/Pages #45827898517](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45827898517) **SUCCESS** after correction; real Godot log showed both sets of six original unique source cels, visible painted height70px and visual_scale1.0, unchanged 8-way walk.
- Latest public browser commit `0374aa6b785622c3323bc549368b6206ca31dfe2` adds LEFT A+A gate. New exact [Pages #45828107215](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45828107215) and [Chromium #45828220564](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45828220564) **IN PROGRESS at checkpoint creation**, must verify final status/source SHA/screenshot artifact. Do not declare final E2E PASS until verified.

## Handoff
Owner visually evaluates running in ACTUAL game at single canonical URL. Technical 6-distinct-cel source is built from pre-existing atlas poses, not newly authored independent final 8-pose sequences. User may still request art refinements. Punch/kick and other ten-tag authoring remain PENDING_ART. After runs final, record job outcomes/SHA and artifact in BOTH repos.

**Trạng thái: PARTIAL — chưa hoàn tất.**
