
# Public Actions checkpoint — 2026-11-26 obstacle shaping retest

Status: **RETEST REQUIRED / FIRST RUN FAILED**.

- User asked for plausible Nekketsu-like obstacles with proper 2.5D forms
  and heights; Game source and rules:
  `docs/architecture/STAGE_OBSTACLE_DESIGN_STANDARD.md`.
- Game code includes `ArenaObstacleData`, projected 2.5D `ArenaObstacleView`,
  five per map, Y-sort/ground-foot anchors, physically independent collision.
- Public Actions `ci/playwright_smoke.py` now asserts 5 prop visuals,
  obstacle bodies and height metadata on both maps.
- Run https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45662885191
  FAILED in `Import project headlessly`: StageData non-@tool placeholder
  during `ArenaStage._draw` editor preview. Fix in Private:
  added `@tool` to `scripts/data/stage_data.gd`.
- Next step: check subsequent CI run (triggered by this PUBLIC docs push),
  inspect import/headless tests/Web export/Pages, then E2E screenshots.
  If any tests fail, fix root cause, rerun and update next checkpoint.
- Future: jump-vault height physics, hazards, equipment, AI pathfinding.
