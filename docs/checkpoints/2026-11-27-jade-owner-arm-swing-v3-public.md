# 2026-11-27 — Owner-provided reference drives Jade v3 isolated test

- PRIVATE [Draft PR #2](https://github.com/ngocnhanvo/beast-arena/pull/2) exact source **`89e85277189eb5ea406ef91f0b8aef6e1d8124d3`**. Original owner six-pose orange runner reference translated only to rhythm; no reference pixel copied. 8 native Jade right/left source cels changed; same frozen face/legs and foot/timing.
- Public isolated QA branch `ci/jade-pr2-source-check` only: checkout exact private SHA using existing read-only secret, pinned Node22 to reproduce original native ASE/PNG and GIF/media, independent Python verifier with new arm-sweep checks, LibreSprite1.3 native roundtrip, Godot4.7.2 headless smoke, Chromium local two-cycle GIF playback. No private art uploaded, no build export, no Pages, no merge or deploy.
- Prior 3/3 run [#45936962296](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45936962296) applied to v2 only. **Do not claim v3 PASS until actual new run reaches terminal success.** Owner art approval still pending; separate Issue #3 handles running→idle.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## Terminal exact-SHA CI evidence (2026-11-27)

- PRIVATE Jade v3 art/test SHA: `89e85277189eb5ea406ef91f0b8aef6e1d8124d3`, PUBLIC isolated QA pipeline `3faf0c09131f18f127e461585734b401c864d7c0`.
- [GitHub Actions #45939974579](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45939974579): **completed SUCCESS, 3/3 jobs PASS**. No merge, no export, no public artifact, no Pages deployment.
- Pinned Node22: `node tools/jade_run_guard_swing_v3.js --check` PASS for 16 complete native cels, immutable face/leg pixels, mirrored LEFT and original tag/85ms; `node tools/jade_run_review_media_v3.js --check` PASS with 16-frame 1360ms GIF and 18-frame 2040ms source-cut GIF.
- Independent Python verifier: PASS with guard swing amplitude and opposite-phase contract.
- LibreSprite1.3: RIGHT/LEFT strict RGBA export `visible_diff=0`, `transparent_rgb_diff=0`.
- Godot4.7.2: import `IMPORT_SCRIPT_ERRORS=0`; guard profile smoke PASS; three-quarter Jade native smoke PASS; zero script errors.
- Chromium GIF replay: 8/8 running phases, 9/9 including idle comparison; F7→F0 observed, unmatched samples=0. This is local GIF playback, not in-game Web/Pages E2E, nor owner aesthetic acceptance.
- Owner art review PENDING: supplied reference stresses full front/back counter-swing; manual owner decides style. Run→idle facing mismatch is separate Issue #3.
