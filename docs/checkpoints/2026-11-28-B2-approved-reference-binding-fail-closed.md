# 2026-11-28 — B2/6 approved reference binding negative result and fail-closed CI

B1: OWNER APPROVED the exact smooth-line neutral base fighter raster (PRIVATE conversation attachment). B2: experimental F2→F3 raster global mesh deformation **visually failed** even when four fixed-length 2D chains and pre-toe-off contact passed 101 local samples. Lower leg, toes and forearm distorted. Interpolating the two separate figure images from the original sheet also ghosted contours; neither proves layered rigged animation.

Private experimental reference, PNG, GIF, keypoint screenshots and ZIP are **NOT** uploaded to PUBLIC GitHub. Source-only negative gate added to PRIVATE Draft PR #18 `tools/pose_lock/approved_b1/b2_reference_gate.py` + `test_b2_reference_gate.py`: assert exact approved SHA-256/dimensions when reference available and preserve fail-closed owner approval semantics. Five synthetic negative tests run without private pixels.

PUBLIC Draft PR #17 pins PRIVATE `c286efe70d3e02b7d0d3bbc95f5d6e0e4aebad2b`; new workflow SHA `8c896b716079229a60a0d0738e07847122a1a7ae`, [run #46097045152](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46097045152). Must check terminal status, job and logs before declaring technical PASS. Previous 70/70 v10 art test run doesn't validate the approved raster artwork.

NEXT: B2 still blocked; create **layered** per-bone master from *same approved design*, weight/transform each segment with elbow/knee corrective shapes, independently review 480px +80px F2→F3 silhouette, then owner visual approval. No main/Pages merge/deploy. Never claim B2 passed merely because source negative tests passed.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## Terminal exact-pin technical CI result — verified separately from art
- [PUBLIC Actions run #46097045152](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46097045152), job `140830693202`, exact PUBLIC workflow SHA `8c896b716079229a60a0d0738e07847122a1a7ae`, exact PRIVATE pinned SHA `c286efe70d3e02b7d0d3bbc95f5d6e0e4aebad2b`: **COMPLETED SUCCESS**.
- Actual runner logs: 56 pre-existing portable tests PASS; 9 independent native/screenshot controls PASS; 5 old v10 style-key tests PASS; **5 new B1/B2 reference identity and approval fail-closed tests PASS** = 75 tests total. Output marker `BEAST_B1_OWNER_VISUAL_APPROVAL_BOUNDARY_5_TESTS_PASS_B2_ART_REMAINS_BLOCKED`.
- Old v10 transient Godot Web/Chromium motor test also PASS, `art_style=organic-v10-eight-key-study`, atlas SHA `3e3f8dde093fae43ad376996b9720c5b0cbf68910a7a240b88a47a93725a8802`, 24 source sample indices, 270 ticks, X -11.300000 to -4.490603m, 122829 changed HUD-excluded world pixels, zero JS errors. This is HISTORICAL OLD ART source regression, **not** approved B1 artwork live-game QA.
- The new owner-approved artwork is NOT a layered rig and was NOT uploaded to CI/GitHub. The offline B2 approved-original visual experiment FAILED. CI SUCCESS here **only proves fail-closed boundaries and old code are safe**. Owner B2 approval remains NOT_GIVEN, `B2_visual_binding=FAIL`, release BLOCKED; no production Pages, no PR merge.

**Trạng thái: PARTIAL — chưa hoàn tất.**
