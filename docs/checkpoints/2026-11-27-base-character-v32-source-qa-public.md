# 2026-11-27 — Base Character v3.2 six-frame local contour redraw, technical source QA PASS, visual/rights pending

## Status and source pins
PRIVATE main remains `48dc2119981f26e9f010b279ff2520af99b2f99b`. Clean isolated private branch `feat/base-character-v32-source-pose-lock` implementation SHA `bf71544cd0f4caa64a85ca329ef50c115da043c8`, later docs-only checkpoint SHA `6d29c99b6b5d9a9152bf4fe8461901dd1e29e22a`. Original v3/v3.1 rig source remains separate in Draft PR #5, previously visual FAIL, not merged. Jade Draft PR #2 and current gameplay unaffected.

PUBLIC main remains `c72335df77237580e88066749a3411b58b5494a6`. PUBLIC isolated source workflow branch `ci/base-character-v32-source-qa` commit `eefa729cee6b930bef3a4944a577be713207d9ce`. Exact [GitHub Actions #46008935382](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46008935382) **COMPLETED SUCCESS**, job `140539142884`; actual log inspected: `Ran 9 tests / OK` and `V32_SOURCE_QA_PASS__ART_RELEASE_BLOCKED`.

## Actual engineering change and important limits
- User explicitly requested repairing badly drawn v3.1 skeleton/body. Original v3.1 visually FAIL (6 silhouette IoUs ~0.50–0.60, 4/6 contact poses with 38 rendered below-ground ink pixels each).
- v3.2 is a **different method**: derive six native 80×80 frame silhouette masks from a locally user-supplied six-pose animation strip, then redraw RGB/palette **inside** mask, no invented IK joints. Output six individual cel PNGs, 480×80 and mirrored 480×160 atlases, GIF, visible-color 7-layer PNGs and local browser HTML. Six silhouettes match by construction, floor ink 0 after preview alignment. This does **not validate** rig/skeletal motion, unique original source anatomy, or arbitrary gear shape replacement.
- User-supplied reference is a third-party copyright-sensitive game sprite. No reference pixels / derived art were committed to PRIVATE or PUBLIC repositories or PUBLIC CI. Public Actions uses only a synthetic fake six-cel strip and verifies source tool semantics. All derived review art is local-only and **not rights-cleared for public release**.
- Local 9/9 unit tests PASS incl. missing frame, shifted mask, below-floor error, reconstructed 7 visible layers; preview JS syntax `node --check` PASS. Actual Chromium preview navigation blocked by host admin `net::ERR_BLOCKED_BY_ADMINISTRATOR` for file:// and localhost. This step **not** browser E2E/Godot game build/Pages deployment. No claim of production Base Character; owner `autocheck:false` art approval PENDING.

## Next exact step
Owner opens locally delivered v3.2 GIF/preview, reviews six poses and whether new appearance is acceptable, and can reject. If next goal is original commercial skin-ready character, independent authored anatomy/poses/cloth occlusion and license approval remain required. Only then integrate (existing run requires 8+ clips) in dedicated game build with exact SHA and real Chromium on canonical `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/`. Keep both branches/PR Draft and Jade unchanged.

**Trạng thái: PARTIAL — chưa hoàn tất.**
