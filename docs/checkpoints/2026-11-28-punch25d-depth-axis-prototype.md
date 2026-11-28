# 2026-11-28 — Technical 2.5D punch depth proof pinned in isolated PUBLIC CI

- Owner explicitly prioritized a **depth-axis punch** (three poses guard → thrust → recover) over further 2D running gait work, after confirming punch requires X/Y/Z spatial motion, perspective foreshortening and front/back layering.
- PRIVATE Draft PR #18 isolated source `tools/pose_lock/punch25d/punch25d.py` and `test_punch25d.py`, pinned exact SHA `2c89dd62211f35d5aacc1b708edf45534ffab82a`.
- 3D right/left arm FK/analytic 3D IK with constant bone lengths, world camera `+Z` depth projection, z-aware arm/torso occlusion and direction-sensitive rendered fist; 3 independent review poses plus 21 rig-generated time samples at 480px and 80px. Prototype does **not** reuse the pixels of owner-approved B1 reference and does not prove exact B1 art-to-skeleton binding.
- PUBLIC Draft PR #17 workflow source commit `b15b1bfbc5f81f14034b4ca9eea9a045709cadaa` pins PRIVATE SHA and runs 10 independently defined positive/negative rig cases plus 75 existing old-art tests = 85 expected controls. All SVG/PNG/GIF generated only in runner temp directory, never uploaded to PUBLIC artifacts, logs, Git or Pages.
- Exact workflow run awaiting terminal verification; inspect GitHub Actions job/log and update checkpoint with actual result before claiming PASS.
- Existing Godot E2E still displays old v10 **2D run** atlas and does NOT certify this new 2.5D punch in live game. New punch has **local 10/10 PASS** technical, but ART visually not equivalent to approved B1 design and owner B2 acceptance NOT_GIVEN. `art_release=BLOCKED`.
- NEXT: full B1-style layered/vector artwork with true per-bone binding and shoulder/elbow/fist corrective views, isolate only three punch poses, obtain owner review before game integration/production cutover.

**Trạng thái: PARTIAL — chưa hoàn tất.**
