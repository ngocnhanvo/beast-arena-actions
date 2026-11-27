# 2026-11-27 — PRIVATE six-pose sprite-studio tooling in separate draft branch (no public CI modification)

## Starting baseline
PUBLIC `main` `c72335df77237580e88066749a3411b58b5494a6`; PRIVATE `main` `48dc2119981f26e9f010b279ff2520af99b2f99b`.
Read both AGENTS.md, START_HERE, newest checkpoints, PUBLIC build.yml and web-e2e.yml. Existing Jade native PR #2 remains DRAFT; isolated source 3-job CI #45942733770 PASS for PRIVATE art `f0c1feab04649abd31cb899e6ca4e3074e4c8970`. Source-only QA != game Pages or Chromium in-game E2E.

## New isolated effort
Owner supplied a six-frame run reference strip (242x60) and requested a repeatable pose-preserving sprite preparation system. PRIVATE branch `feat/pose-locked-sprite-studio` contains `tools/pose_lock/pose_studio.py`, README, synthetic tests and separate technical checkpoint. Standalone `beast-arena-sprite-studio` Skill was delivered in chat and passed independent validation and three local tests.

Reference images remain outside BOTH GitHub repositories and must not be published as unlicensed game assets. No changes to public build scripts, pages, game runtime or current native Jade 8+8 art. No workflow/deploy was triggered by this docs-only branch.

## Status and next steps
PRIVATE feature branch source test must be validated in its own right; source extraction defaults to 80px cells, approximate y73 ink-bottom pivot, provisional 85ms (not source timing), numeric IoU/centroid QA, NOT anatomical rig or artistic acceptance. Review private draft PR, annotate joint positions and contacts, source-author original new native art only with explicit owner review. Existing Jade PR #2 and run-to-idle Issue #3 remain separate. Any later build must use exact pinned private SHA, Pages and real Chromium tests and sole canonical `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/`, keeping user `autocheck:false`.

**Trạng thái: PARTIAL — chưa hoàn tất.**
