# 2026-11-28 — Calibrated 2.5D punch source art binding (PRIVATE-only assets)

- PRIVATE Draft source SHA `b2827035c547c6cb6217f5523d110de81ec6b53d`; PUBLIC workflow `41aa5d41d8752f76397b8be9ab9b67cc5e49f127` pins exact source and expects 95 tests. Inspect terminal run/job/log before citing PASS.
- True 3-axis analytic right-arm IK has fixed upper/forearm 60/65. Six actual annotated 480px **art** landmarks from GUARD and IMPACT (not self-derived IK coordinates) are inverse-projected with independently calibrated depths; right wrist world Z 40.2945→149.9601→40.2945 and projected original two key anchors agree <0.003px. 601 samples validated without teleport/bone stretch. Grounded right toe delta ~3.16px.
- Two unique high-res B2 art key images generate a 3-pose/25 sampled frame punched-depth GIF and 80px preview. Local 7/7 Python gates + actual Chromium interactive HTML canvas PASS (91497 changed pixels, no JS errors); owner review ZIP `Beast_Arena_2_5D_Punch_Review_Full.zip` in conversation. The image/ZIP are NOT GitHub assets and were NOT uploaded to PUBLIC CI, artifact or Pages.
- Scope: this is keyed combat-cel artwork, **not** finished full-body mesh skinning. Only RIGHT punching arm is anchored/calibrated to art; other parts are painted full-body keys. B1 user-approved source design is a separate reference and the new B2 art keys are NOT owner approved. No live Godot punch E2E; previous Web v10 gait result is unrelated. `art_release=BLOCKED`, no PR merge/main/production Pages.
- NEXT: separated editable B1 matching parts, continuous corrective arm/shoulder interpolation and real Godot punch, then owner art signoff.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## Terminal pinned CI — independently verified after source patch

- [PUBLIC Actions #46101540323](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46101540323), job `140844870723`, source workflow SHA `41aa5d41d8752f76397b8be9ab9b67cc5e49f127`, pins PRIVATE `b2827035c547c6cb6217f5523d110de81ec6b53d`: **COMPLETED SUCCESS**, no failed steps.
- Actual logs: **56** portable rig tests, **5** B1 fail-closed tests, **9** native/screenshot tests, **5** legacy v10 art-key tests, **10** old prototype 3D IK tests, **10** new calibrated right-arm source/image anchor tests = **95/95 technical cases PASS**. Marker `BEAST_KEYED_25D_PUNCH_10_ART_CALIBRATED_SOURCE_TESTS_PASS_UNAPPROVED`.
- Exact code anchors GUARD and IMPACT from separately illustrated NEW B2 art; right upper/forearm remain constant 60/65 and 3D depth moves Z 40.2945→149.9601→40.2945. With actual two art-key 2D input landmarks, projected three anatomical joints each agree to <0.003px at key poses; 601 samples and loop continuity pass.
- Prior real Godot Web E2E also technically PASS **only for old organic-v10 run sprites**: 24 run sample frames, 234 game physics ticks, HUD-excluded world pixels 114747 changed, 0 JS errors. **This is NOT a running B2 punch in Godot.** Local newly produced B2 HTML Chromium canvas test separately PASS (91497 pixel changes, 0 JS errors), not a Godot scene.
- New 2-key art preview package is a current-chat artifact, not source art committed to PRIVATE Git; do not upload it or B1 approved photo to PUBLIC repository. New B2 image differs from specifically approved B1, so user art decision remains NOT_GIVEN. A valid 3D source mapping to two keyed full-body silhouettes does not prove full-body continuous skinning or finished animation.
- No merge into main and no production Pages deploy. `art_release=BLOCKED`, **Trạng thái: PARTIAL — chưa hoàn tất**.
