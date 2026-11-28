# 2026-11-28 — Calibrated 2.5D punch source art binding (PRIVATE-only assets)

- PRIVATE Draft source SHA `b2827035c547c6cb6217f5523d110de81ec6b53d`; PUBLIC workflow `41aa5d41d8752f76397b8be9ab9b67cc5e49f127` pins exact source and expects 95 tests. Inspect terminal run/job/log before citing PASS.
- True 3-axis analytic right-arm IK has fixed upper/forearm 60/65. Six actual annotated 480px **art** landmarks from GUARD and IMPACT (not self-derived IK coordinates) are inverse-projected with independently calibrated depths; right wrist world Z 40.2945→149.9601→40.2945 and projected original two key anchors agree <0.003px. 601 samples validated without teleport/bone stretch. Grounded right toe delta ~3.16px.
- Two unique high-res B2 art key images generate a 3-pose/25 sampled frame punched-depth GIF and 80px preview. Local 7/7 Python gates + actual Chromium interactive HTML canvas PASS (91497 changed pixels, no JS errors); owner review ZIP `Beast_Arena_2_5D_Punch_Review_Full.zip` in conversation. The image/ZIP are NOT GitHub assets and were NOT uploaded to PUBLIC CI, artifact or Pages.
- Scope: this is keyed combat-cel artwork, **not** finished full-body mesh skinning. Only RIGHT punching arm is anchored/calibrated to art; other parts are painted full-body keys. B1 user-approved source design is a separate reference and the new B2 art keys are NOT owner approved. No live Godot punch E2E; previous Web v10 gait result is unrelated. `art_release=BLOCKED`, no PR merge/main/production Pages.
- NEXT: separated editable B1 matching parts, continuous corrective arm/shoulder interpolation and real Godot punch, then owner art signoff.

**Trạng thái: PARTIAL — chưa hoàn tất.**
