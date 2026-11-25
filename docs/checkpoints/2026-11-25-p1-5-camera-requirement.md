
# Actions checkpoint — P1.5 camera / large map requirement — 2026-11-25

**Status: DOCUMENTED DESIGN, NOT IMPLEMENTED.**

- Game private doc commit: `574cb6497b9058c83d8756e9de0a05486c7b0828` (documentation only).
- Public Actions prior HEAD: `f39fbd06cc01707af179255b93a6a7cc15f4b390`.
- Product request: map extends beyond visible 960x540 viewport, smooth player-follow
  Camera2D limited to authored stage camera bounds. Camera follows player's
  ground XY, not sprite jump height Z. Walkable/collision/nav/hazard regions
  are separately editable over imported layered artwork.
- Verified existing build: CI #45657606670 SUCCESS; browser Playwright
  #45658080541 SUCCESS **on previous P1a only**.
- Next task after game implementation of P1.5a: add Playwright camera position,
  edge clamping, HUD, F2 overlay and screenshot assertions; see
  `docs/CI_PLAYWRIGHT_RUNBOOK.md`.
- Do not trigger CI solely for this documentation-only design decision.
- Read AGENTS.md / START_HERE.md / latest checkpoint in both repos before
  any code or workflow changes. Compare current HEAD and actual run logs.
