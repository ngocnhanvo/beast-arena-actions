# Beast Arena Public — Jade 80px source-only animation preview; owner manual review (2026-11-26)

The user identified a real art-quality problem: native 80px approved idle stayed detailed, but moving/punching poses came from a lower-resolution 40px sheet that was enlarged 2x by `INTERPOLATE_NEAREST`. Technical W/J/K physics+foot-pivot Pages/Chromium #45764000051/#45764224828 PASS were **not** checks that action art matched idle detail.

## Current PRIVATE source candidate
- Game source `ngocnhanvo/beast-arena/main`: in `scripts/jade_approved_motion.gd` removed 40px motion sheet import, used native original 80px source poses for W/side gait, recomposed high-detail rear leg motion and J/K upper/lower poses, and selected full-size jump illustration. 40px experimental PNG remains historical but no longer referenced at runtime.
- `tests/visual_smoke.gd`: new ART-26 native-art exact-pixel checks; existing full-body, 4-phase, foot-pivot and gameplay invariance remain. Camera, floor UV, physics, game damage, P1.5 main game unaffected.
- WARNING: rear/action composites are temporary and not truly hand-drawn complete four-way 80px clips. Owner may reasonably reject aesthetic results.

## Manual gate required
Owner explicitly set `autocheck: false`. **Do not build custom self-retrying screenshot style acceptance loops.** Existing compilation/export/publish CI is permitted to deliver a user-viewable preview; a browser automation success does not equal visual acceptance. Once Pages reflects the new exact PRIVATE SHA, owner checks `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved` (W/A/S/D, Space, J, K, F5). Report the updated build/source SHA and do not claim visually finished without their response. When `autocheck: true`, independently test the requested goal and iterate with documented evidence.

## Latest verified PREVIOUS source, not this change
- PRIVATE compiled `660093be13f55dae0aa30a8eb5d6a72818e87a56`, PUBLIC pipeline `da8094c23464457e50e350283565198ea14ab79d`.
- Build/Pages #45764000051 PASS; real Chromium #45764224828 PASS; those results predate native 80px art change.
- Current new build/deploy status: **PENDING until a new run actually proves it**, at document authoring time.

Next: PUBLIC build once from updated private `main`, inspect its exact SHA/build failure if any, publish preview, owner visual review. Continue editable Aseprite 80px source and broader game roadmap after approval.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## Fresh technical delivery verified, owner approval outstanding
- Exact built PRIVATE source `b681ef47e2054419028eb90e6136efae60b7eece`; PUBLIC pipeline `e40ca17cbc7df8a0beda782e6b77ed56229acbf7`.
- [Godot/Windows/Web/Pages #45766825513](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45766825513) **SUCCESS**. API verified preflight, Import/test/export and Pages jobs all concluded success. Real import/export job logs confirm checked-out PRIVATE SHA `b681ef47...`, `APPROVED JADE 80PX PASS` and `All export checks passed.`
- Preview: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved . Owner manual check for idle/run/jump/punch requested (`autocheck: false`). No custom autonomous style/screenshot acceptance loop has been run; Pages technical deploy ≠ aesthetic signoff. A normal `workflow_run` browser smoke may start automatically but does not supersede user approval.
- Next: owner tests W/A/S/D, Space, J/K, F5; collect user feedback before replacing fallback composites with fully authored native-80px animated clips. Rest of game still open.

**Trạng thái: PARTIAL — chưa hoàn tất.**
