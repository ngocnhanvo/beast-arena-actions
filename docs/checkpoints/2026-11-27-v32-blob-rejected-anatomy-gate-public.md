# 2026-11-27 — User rejected v3.2 one-blob character; anatomy release gate now fails closed

## Verified actual root cause
Owner screenshot shows frame 4/6 as an unreadable one-color body mass. PRIVATE `tools/pose_lock/base_character_v32/src/locked_frame_art.py` paints all pixels inside one reference-based silhouette as skin and pastes constant shirt/pants polygons and glove ellipses. No independent near/far arms, hands, upper/lower legs, knees, or true per-frame z-order. Seven 'layers' from earlier prototype were partitions by palette, not anatomy. The 6-frame silhouette overlap 100% was TRUE BY CONSTRUCTION, but cannot certify interior anatomy or aesthetic fidelity; owner **VISUAL_FAIL**.

## New process code and isolated technical evidence
- PRIVATE [Draft PR #6](https://github.com/ngocnhanvo/beast-arena/pull/6), source revision `4ae39bc0b561335c9992253eb833842ee75d8664`; later docs-only checkpoint. Added `src/anatomy_gate.py` and `src/make_anatomy_template.py`, negative tests and anatomy authoring contract. This is SOURCE QA correction, **NOT a new finished character**.
- Anatomy gate requires 14 independently authored near/far head/torso/arms/hands/thigh/shin/feet ID maps for ALL six frames, twelve per-frame joint labels, realistic noncollapsed coordinates, per-frame visibility, provenance, z-order, partmap coverage and no floor penetration. Missing parts BLOCK; complete metadata only changes result to `STRUCTURE_REVIEW_REQUIRED`, never auto-accepts art.
- Synthetic 6×14 blank templates are generated only for an artist to draw the actual anatomy. Existing six full-body v3.2 PNGs are demonstrably `ANATOMY_INVALID` (no part layers). Owner must approve anatomically readable skeleton/body GIF before any costume expansion, merge or game deploy.
- PUBLIC workflow commit `1466ce618dd57232af1d00c635ea7c00ed416119`, actual [GitHub Actions #46010220531](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46010220531) **COMPLETED SUCCESS**, job `140543528719`; real logs read: `Ran 15 tests / OK`, `V32_SOURCE_QA_PASS__ART_RELEASE_BLOCKED` and `ANATOMY_INVALID_ART_BLOCKED_PASS`. This PASS means error detector correctly rejects the same bad art, NOT artistic completion.
- The original reference screenshot is third-party copyright-sensitive and stays LOCAL-only; no copied source / derivative sprite atlas in PUBLIC CI artifacts. Existing Jade Draft PR #2, PRIVATE main gameplay, PUBLIC game build and Pages were **not** changed.

## Remaining work
Real independent original/licensed anatomy drawings are **not complete**. Current artwork stays VISUAL_FAIL/ART_BLOCKED. No owner signoff, independent native LibreSprite reexport on a real anatomy source, Godot game export, Pages release or in-game Chromium E2E. No new deploy workflows were triggered. To resume, draw all six proper anatomy poses with credible hand/leg separation and annotate masks/joints; validate via new gate, then user visual approval, then source/engine QA. Do not simply tint reference alpha masks again.

**Trạng thái: PARTIAL — chưa hoàn tất.**
