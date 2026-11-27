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


## Terminal continuation: safe one-pose/one-part source updates

PRIVATE exact code `d363b7ae89940d9e7f3c52f443190c10140c9197`
adds per-contour SHA metadata, fail-closed stale-polygon detection and
`apply-contour --frame --part`. One agent cannot edit a polygon in
`pose_shapes.json` and silently rebuild unchanged PNGs; it must
explicitly apply the ONE intended contour. Other sources remain pixel
unchanged and forged motion/owner-review metadata is rejected.

PUBLIC [Actions #46035363712](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46035363712)
**COMPLETED SUCCESS**, workflow tested SHA
`bfaf56cc5e9df4992b938aacdc3eeff14b7a9704`,
job `140629380489` actual log:
- `Ran 16 tests` OK (original eight + eight scoped editing tests).
- `V41_PORTABLE_STRUCTURE_PASS_OWNER_ART_BLOCKED`, source 0 errors,
  0 warnings; 3 pending independent motion/owner gates.
- `V41_AUTHORED_6FRAME_31LAYER_LIBRESPRITE_PASS`.
- `V41_SOURCE_INDEPENDENT_GODOT_IMPORT_PASS`.

Earlier intermediate workflow #46035339603 FAIL (15/16) because
the negative test expected the old approval error string despite
the correct stricter `UNTRUSTED_SOURCE_METADATA` exception.
The test was updated to assert the real stronger guard, followed
by full terminal PASS. No falsified art approval or altered source
was used to make CI green. Public repository still contains no
PRIVATE raw source or rendered artwork. No gameplay, Pages, merge.

**Trạng thái: PARTIAL — chưa hoàn tất.**


## Final independently pinned real v4.1 pixel-motion diagnostic

PUBLIC shared `sprite-foundation` motion tool
`31991e608ed58f93341d215d3ad515b712ae1a73`
was validated in [generic Actions #46035667624](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46035667624)
COMPLETED SUCCESS (19/19 synthetic/adversarial core tests and one
real old owner-rejected v4 blocking adapter test).
The tool produces objective raster/frame statistics without
pretending to prove world-space planted feet or artistic acceptance.

Independent actual v4.1 pipeline [#46035739118](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46035739118)
COMPLETED SUCCESS on exact public SHA
`232a95356100d12cc2fd6cee3e3cdf70502d9478`,
private authored v4.1 SHA
`d363b7ae89940d9e7f3c52f443190c10140c9197`,
job `140630554884`. Runtime logs:
- 16/16 authored source and scoped one-part editing negative tests PASS.
- Portable source integrity STRUCTURE PASS, owner visual PENDING,
  release BLOCKED.
- Source `motion-diagnose` reports seam/internal median pixel-change
  ratio 1.0928, bottom painted y rows [72,72,71,72,72,72].
  Explicit `GROUND_CONTACT=UNVERIFIED`,
  `LOOP_ART_REVIEW=UNVERIFIED`, `release_authorization=NONE`.
- Pinned official LibreSprite 1.3 native strict RGBA PASS
  for 6 editable 31-layer cels; isolated Godot 4.7.2 import PASS.
No new PRIVATE sprite art persisted in PUBLIC repo/artifacts/Pages.
No auto-merge, no game build or gameplay Chromium E2E.

**Trạng thái: PARTIAL — chưa hoàn tất.**
