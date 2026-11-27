# 2026-11-28 — Exact FK/IK pose JSON to smooth-line SVG: terminal 24-test CI

## Actual source verification
PUBLIC isolated workflow `.github/workflows/motion-bound-vector-art.yml` tested exact source SHA `2b91543ba211dd1c5c7cf02c824240e18b313db1` against immutable PRIVATE code `72f11d02c6c715087b92837137b50acc9a7cd034` (PRIVATE branch `feat/motion-bound-vector-art-prototype`, Draft PR #17).

[Real Actions run #46044585625](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46044585625) **COMPLETED SUCCESS**. Job `140660530774` **COMPLETED SUCCESS**. Logs show `Ran 24 tests`, `EXACT_RIG_VECTOR_24_TESTS_PASS`, `VECTOR_6_SVG_24_INTERPOLATIONS_EXACT_POSE_HASH_BINDING_PASS_ART_BLOCKED`.

## What is actually tested
- Previous 15 original FK/IK tests, PLUS 9 renderer/source binding tests. The renderer uses the real pose-contract.json (no independent text-to-image prompts) to author six unique, editable smooth-line SVG cels.
- Actual SHA-256 of each source frame pose embedded as `metadata data-hash` in SVG; each frame has exactly one left+right arm and left+right leg element tag. The runner recomputes SHA from actual source JSON and compares all six.
- 24 contiguous vector/GIF frames rendered from the SAME continuous `motion_rig.pose_at(t)` function; physical-phase identity F2→F3, support labels, rigorous bone/stance checks pass.
- Negative/injected mislabel, toe lift, hand teleport, bone-length mutation and right stance leg teleport all fail **before vector export**.
- Exact actual artwork self-review is `FAIL_UNPOLISHED_ANATOMY` and release `BLOCKED`, asserted by the CI rather than overwritten as green aesthetic QA.

## Scope and lessons
Original smooth vector line art improves the pipeline provenance but the actor remains visually primitive and not production-quality. This is **source binding evidence, not owner artistic approval**, native Aseprite source, actual Godot 4.7.2 run, Web/Chromium E2E, or Pages deploy. Previous independent anime image generations did NOT apply the motion skill and must remain unverified. No PRIVATE raw SVG/PNG art uploaded to PUBLIC assets/Pages/artifacts. Both PRIVATE PR #17 and PUBLIC PR #16 stay Draft/unmerged.

Next: original vector shape/polish revision that preserves rigid anatomy identifiers and continuous poses; inspect actual loop visually and compare against the user's accepted clean-line style, then new native/game/Web checks and exact SHA CI. No production release until art accepted.

**Trạng thái: PARTIAL — chưa hoàn tất.**
