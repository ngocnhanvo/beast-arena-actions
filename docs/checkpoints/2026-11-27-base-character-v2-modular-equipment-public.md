# 2026-11-27 — Base Character v2 modular outfit source proposal, NO game deployment

## Baseline and proof
- PRIVATE `main` starting `48dc2119981f26e9f010b279ff2520af99b2f99b`; PUBLIC `main` starting `c72335df77237580e88066749a3411b58b5494a6`.
- PRIVATE isolated [Draft PR #4](https://github.com/ngocnhanvo/beast-arena/pull/4), source SHA `86bac78dca66d24300c15d8aa5818346cb7312b9`, adds `tools/pose_lock/base_character_v2/` and art-tool engineering checkpoint. Previous v1 code/art remains on the same isolated review branch.
- This proposal does not affect existing Jade [Draft PR #2](https://github.com/ngocnhanvo/beast-arena/pull/2), Issue #3, eight-direction walks, game motor/physics or production source. Previous [Jade isolated source QA run #45942733770](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45942733770) SUCCESS is for a DIFFERENT source SHA and is not Base v2 E2E proof.

## Local source-only validation
- Four source variants: `neutral` original six-pose art pixel exact; `aegis` distinct hair/armour/gauntlet/boots; `ranger` distinct hair/tunic/wrap/boots; `hybrid` mixing six equipment categories from other skins without changing the immutable 6-pose body.
- Nine native 80px RGBA editable layers with rear/front glove and hair, 6 frame-specific gear PNGs, provisional pose landmark manifest, 480×80 atlas, mirrored 480×160 left/right, six-frame GIF, OpenRaster and Aseprite authoring source.
- Local Python Pillow `python -m unittest discover -s tests -v`: **9/9 PASS**, including deliberate missing-item, glove drift (even with updated checksum), source hash tamper, recipe overwrite and path traversal checks.
- Aseprite file roundtrip tested by in-project binary reader only, not an independent editor; source PNG geometry tests do not imply natural animation. GIF is limited to 10ms increments, so requested 85ms appears as 80ms in preview GIF; interactive local HTML preview can use 85ms.
- **BLOCKED:** official LibreSprite 1.3 not installed in local environment; attempted pinned AppImage download resulted `curl: (6) Could not resolve host: github.com`. Public CI must perform independent editor and later Godot/Pages/Chromium checks separately.

## No public runtime or game deployment
No public workflows or game code were changed. No workflow triggered. This doc-only proposal remains Draft PR #1. No Pages deployment or actual browser/game validation, and no art owner visual approval (`autocheck:false`). The owner-facing live URL remains solely `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/`, unchanged by this proposal.

## Next exact action
Owner reviews 6-frame original Base Character v2 GIFs and new equipment shape; original art corrections recorded per-frame. Verify official pinned LibreSprite native RGBA roundtrip; after explicit owner integration authorization, register original asset in generic fighter profiles, run exact source/private SHA on public standard runner with Godot+Pages+Chromium, screenshot actual in-game skin-switch fidelity, then update both checkpoints. Never auto-merge Jade or this PR.

**Trạng thái: PARTIAL — chưa hoàn tất.**
