# 2026-11-28 — New clean animation source QA, no art or game deploy

Owner decided the prior 2D FK/IK → 2.5D rig-driven animation architecture and produced imagery do not meet natural-motion/visual quality requirements. Rather than deleting existing game/main/production, the restart uses **new source-only branches based exactly on main**:
- PRIVATE `feat/animation-keyframe-first-clean` based on `48dc2119981f26e9f010b279ff2520af99b2f99b`, clean motion source commit `900241f1641339ff30bf7c2b521a8a5aac0e390b`.
- PUBLIC `ci/animation-keyframe-first-clean` based on `c72335df77237580e88066749a3411b58b5494a6`, minimal new workflow commit `00faefd9dbb024edc8dacfa5d3265da44694da5c`.

The clean PRIVATE package `tools/animation_keyframe_first/` has a single six-beat normalized *storyboard motion blueprint*, standard-library validator and nine adversarial guard tests; **NO new renderer/rig/game asset is imported from previous 257 PRIVATE draft commits**. It declares `physics_simulation_status=NOT_RUN`, `visual_art_status=NOT_CREATED`, `owner_motion_approval=NOT_GIVEN`. Tests only verify internal planned beat ordering, right/left identity, contact and kinetic-chain constraints, with no false physical/art acceptance.

The NEW PUBLIC workflow `.github/workflows/animation-keyframe-first-clean.yml` pins the exact PRIVATE source commit, uses existing `BEAST_ARENA_READ_TOKEN` secret, runs **nine source-only structural tests** with Python 3.12, checks no old rig imports; does not build Godot, export PCK, publish Pages or leak private art/screenshots. **Must verify the terminal run and log; do not infer PASS from the workflow commit**.

Old PUBLIC `ci/rig-bound-clearline-v2-native-qa` is preserved but rejected. Existing `main`, Pages, Physics V2 and separate Jade work remain unchanged. The owner-approved B1 design reference SHA-256 `579784d916f5e2c6869061c945261c57bfa33d0f78c93a37af79340957f775c9` is a PRIVATE conversation source, not a PUBLIC CI artifact.

NEXT: produce six original rough hand-authored full-body punching key poses and visually check each transition before clean line or Godot. No owner art approval is implied by these nine unit tests.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## TERMINAL CI EVIDENCE (VERIFIED)
- [GitHub Actions #46107042607](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46107042607), job `140862016490`, PUBLIC workflow tested commit `00faefd9dbb024edc8dacfa5d3265da44694da5c`, pins PRIVATE source `900241f1641339ff30bf7c2b521a8a5aac0e390b`: **COMPLETED SUCCESS**.
- Job log confirms `CLEAN_SOURCE_NO_LEGACY_RIG_IMPORTS_PASS`, `Ran 9 tests`, `KEYFRAME_FIRST_9_BLUEPRINT_TESTS_PASS_ART_AND_PHYSICS_NOT_TESTED`. Machine output: `{"beat_count": 6, "motion_physics": "NOT_RUN", "owner_visual_approval": "NOT_GIVEN", "structure": "PASS"}`.
- This validates **ONLY** the NEW minimal storyboard contract and negative gates. No 6 original drawn poses or motion simulation exists yet. Do not claim animation, visual, Pages, Web game or author acceptance.
- Local 4-file source ZIP `/mnt/data/Beast_Arena_Animation_Clean_Restart.zip` (9,317 uncompressed bytes; SHA256 `8a1f17701bc4c491ea5634d220d1d55a84e1ad477ebb79f0ab63d9c22c37c234`). Re-ran 9/9 local tests. This is a conversation attachment, not a PUBLIC art asset.
**Trạng thái: PARTIAL — chưa hoàn tất.**
