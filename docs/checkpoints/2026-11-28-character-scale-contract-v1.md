# 2026-11-28 — Pose-invariant scale contract V1 (owner-requested)

## Reason
Owner refuses workaround of forcing upright Walk to crouch like Idle. A character must preserve actual body proportions across upright, crouched, jump, knocked-down and future horizontal lying poses. A common canvas 80×80 is NOT a common character height. Current original Idle (12 frames) paints approximate head 26px, silhouette height 71–72px; original Walk (4 frames) paints head 29px, height 72–74px. 3px/29px = 10.3448% approximate head discrepancy. These pixel metrics are diagnostic, not an independently reviewed bone-length model.

## Exact source and original asset boundary
- PRIVATE work branch `feat/pose-invariant-character-scale-contract`, source code commit `00b8555a96b21b9080cb6fe6f76d9406a853e00b`, docs-only source release head pending.
- Original Idle SHA256 `ac395d4c108047538d0898033d10d6e785b10f6e84ba764304eb786b35caf954` and Walk SHA256 `cd4e482f5db5964f2b1906ea1ca72f3fbd6aae913f07290eec5bc43cbee6ce80`, unchanged. No fake redrawn art and no alpha-bounds auto-scaling.
- New `art/base/character_scale_contract.json`: fixed 0.020m per native art pixel; per-frame `cell_px`, `grid`, `foot_contact_px` and `foot_contact_kind` (semantic support could be shoulder/hip in future prone), original source hashes, explicit `PENDING_ANATOMY_REAUTHOR`.
- New shared `scripts/character_visual_contract.gd` used by Sprite3D and PixelView for native art cell/canvas, mirrored complete body and authored root placement. No changes to native 60Hz contact, collision capsule, speed, attack timing or damage; no pose-dependent stretch. Existing Idle12 and Walk4 retain same original y-center 0.8m and pixel offset -4.
- `tests/character_visual_contract_smoke.gd` verifies original 16 frame pivots and a synthetic 128×80 lying geometry support (86,68). The synthetic fixture does NOT mean an actual lying sprite was drawn or gameplay collider switched to prone.
- `tools/pose_scale_audit.py` and 3 Python unit tests verify source integrity; strict artist/source audit intentionally FAILS with expected code 3 until missing anatomical source is corrected. Never confuse a nonstrict technical PASS with owner-reviewed art.

## Independent source evidence
- [Isolated PUBLIC CI #46130611692](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46130611692) **COMPLETED SUCCESS** on PRIVATE source `00b8555a96b21b9080cb6fe6f76d9406a853e00b`. It verified original SHA/pivots, Pillow/3 unit tests, expected strict anatomy mismatch, Godot 4.7.2 parser import, real four actor Base scene, synthetic lying contact/mirror, unchanged Idle12 and Walk4, pixel projection, map, 60Hz physics and combat.
- Previous live production Pages [#46127709383](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46127709383), Chromium [#46127852101](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46127852101) PASS on OLD source; not proof that this new contract is deployed.

## Release steps pending
1. Update private main with exact QA-tested source and docs checkpoint.
2. Add public build checks for new pose contract and `ci/playwright_base_only.py` assertions of native source density 0.020, no auto-fit, frame/screen support, same source SHA and 4 active fighters.
3. Wait new full Godot/Web/Windows/Pages completion and real browser E2E; verify screenshot and state `PENDING_ANATOMY_REAUTHOR`, physics parity.
4. Next separate visual-art deliverable: create/approve ONE common body model sheet, redraw all whole-body Idle/Walk frames to that proportion, then rerun strict anatomy and owner visual review. Do not change pose by forced crouch or scale per-animation to fill bounding box.

**Trạng thái: PARTIAL — chưa hoàn tất.**
