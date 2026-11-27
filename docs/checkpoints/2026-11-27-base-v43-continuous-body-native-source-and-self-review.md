# 2026-11-27 — Base v4.3 continuous neutral body independent source QA

## Verified exact revisions
- PRIVATE source `ngocnhanvo/beast-arena` code `52c0676aaac5c89210396c387f2efd4f3eeeede4`; later docs-only branch commits do not change this source.
- PUBLIC isolated Actions workflow `965191f80d39aa41a06f1eb266f09fa45ba6804d`.
- [Actual GitHub Actions #46039131856](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46039131856) **COMPLETED SUCCESS**, exact real job `140642052381`, no pending jobs. Earlier #46038846471 was also PASS but did not yet enforce new self-visual rejection metadata.

## What was verified
12/12 source integrity/negative tests PASS: 6 unique 80×80 authored PNG cels, one continuous body part per cel, 14 empty independent gear slots, 15 layer native/ORA source, no override of edited body after initial authoring, new skins leave body byte-identical, path guards, forged approval guard.
Portable generic Sprite Foundation: source STRUCTURE PASS; source generator is labeled AI-assisted/procedural and requires independent art review, RELEASE BLOCKED.
External official LibreSprite 1.3 re-export exact RGBA: `V43_LIBRESPRITE_15_LAYER_STRICT_RGBA_PASS`.
Godot 4.7.2 isolated import: `V43_GODOT_SOURCE_IMPORT_PASS`, no runtime engine errors.

## Actual visual self-review (separate from machine tests)
- Original six-frame art is anatomically more coherent than the rejected disconnected v4.1 painted limbs, but opposite half-cycles remain too similar. Independent pixel analysis of full-body silhouette: (1,4) IoU 0.8825, (2,5) 0.7949, (3,6) 0.7806; second independent concept attempt similarly repeated half cycle.
- The PRIVATE exact testable source declares `self_visual_review=FAIL_REPEATED_HALF_CYCLE`, and CI proves the failure is not silently converted into approval: `V43_SELF_VISUAL_REVIEW_FAIL_HALF_CYCLE_LOCKED`, `V43_CONTINUOUS_BODY_SOURCE_PASS_ART_STILL_BLOCKED`.
- Foot world coordinates, planted-foot slip, six→one visual smoothness, owner acceptance, 8+ authored run poses, real game and Web Chromium E2E all remain UNVERIFIED/NOT DONE. **Do not call source CI SUCCESS art PASS.**

## Public/private security and continuation
Public repo contains workflow/read-only source checker and checkpoint only, no private PNGs, sprites, preview screenshots, GIF, ASA/ORA or raw game source. PRIVATE source under isolated Draft PR #15, PUBLIC CI under Draft PR #14. Production Jade PR #2 and public Pages `/physics-v2/` untouched.

Next: genuinely redraw the opposing 3 run phases (prefer original pixel/artist-authored anatomy, not shifting crop rectangles), self-review six frame contact and loop before any owner handoff, then rerun pinned independent CI on exact SHAs. Do not merge/release/produce outfit skins while ART FAIL.

**Trạng thái: PARTIAL — chưa hoàn tất.**
