# 2026-11-27 — Base v4.1 independent original neutral source QA terminal

Public workflow is **read-only source QA** for private art, not an art release.
No private PNG/ASE/GIF is placed in the PUBLIC repo, log, artifact or Pages.
PUBLIC isolated [Draft PR #13](https://github.com/ngocnhanvo/beast-arena-actions/pull/13)
stacks on reusable portable foundation Draft PR #12. PRIVATE authored
[Draft PR #14](https://github.com/ngocnhanvo/beast-arena/pull/14)
stacks on rejected v4 adapter Draft PR #13; existing Jade Draft PR #2
is untouched.

## Pinned final source evidence

- PUBLIC workflow code SHA `fcdc8352cc2464cacee7aa32c20b6a75368e7c75`
- PRIVATE source and portable adapter code SHA
  `5c6e62cadc93eeb64876803aa4282df401b8df1b`
- [Actual Actions run #46034356147](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46034356147)
  **COMPLETED SUCCESS**, job 140625874955.
- Actual console: Python eight positive/adversarial source tests PASS;
  `V41_PORTABLE_STRUCTURE_PASS_OWNER_ART_BLOCKED`, no technical errors
  or warnings, three explicit approval blockers;
  `V41_AUTHORED_6FRAME_31LAYER_LIBRESPRITE_PASS` (pinned official
  LibreSprite 1.3 exact six-cel RGBA output);
  `V41_SOURCE_INDEPENDENT_GODOT_IMPORT_PASS` (4.7.2 isolated import).
- Earlier run #46034253424 SUCCESS only on eight Python/native/Godot
  gates before the shared portable adapter was added. Do not confuse
  it with the final full gate.

## Architecture lesson / boundaries

The new actual v4.1 body uses separately hand-authored original polygons
on all 6 run poses, not the rejected v4 procedural limb capsules. Renderer
merely bakes 17 editable body source parts + 14 empty gear layers per
80×80 frame to 31-layer ASE/ORA/PNG/GIF, with source editing preserved.
The generic Sprite Foundation is reusable by any project; game-specific
topology and provenance are provided by the private adapter.

Passing source/editor/engine checks cannot validate aesthetics. On v4.1
the correct status is **STRUCTURE PASS / VISUAL PENDING / RELEASE BLOCKED**
because no independently reviewed six-pose body, real foot contact,
6→1 loop motion proof or externally signed approval exists. Preserve
owner autocheck:false. Do not merge draft, publish Pages, build costumes
on an unapproved body, or claim game Web E2E. Source/body review next,
then independent motion and signed approval, then skins/game integration.

**Trạng thái: PARTIAL — chưa hoàn tất.**
