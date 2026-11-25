
# Actions checkpoint — 2.5D obstacle shapes and heights VERIFIED — 2026-11-26

## Baseline and evidence
- PRIVATE built game SHA `ff19f0253c9ca649da3465cf5a45a1cf50b15616`;
  subsequent Private docs-only SHA `30ce9651ad361ad664afaf800a18b8c9eaf7b4f4`.
- Public test source SHA `2ec02d0d1f656411735014de13439030345156a1`.
- First CI #45662885191 FAIL, `ArenaStageData` placeholder in @tool editor.
- Corrected build+Pages #45663247335 SUCCESS:
  https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45663247335
- Browser E2E #45663585488 SUCCESS:
  https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45663585488
  5 colliders+5 2.5D y-sorted visuals per map, heights [105,142,66,126,32]
  and [134,72,80,164,130], F2/debug, +213.5 world X, camera clamp,
  both stage switches, no critical browser asset errors.
- Private Web/Windows release:
  https://github.com/ngocnhanvo/beast-arena/releases/tag/ci-ff19f0253c9c
- Play online: https://ngocnhanvo.github.io/beast-arena-actions/
- Private game standard:
  `docs/architecture/STAGE_OBSTACLE_DESIGN_STANDARD.md`.

## Implemented versus unfinished
- Implemented: per-object kind/material/footprint/height; original shaded
  projected 2.5D drawings, Y-sorted foot anchors, body collision only at
  footprint, map Data resources/Inspector preview.
- Not implemented: proper low obstacle jump clearance/platform landing,
  destructible props, hazard damage, AI navigation, advanced EditorPlugin,
  production pixel-art assets.

## Next actions
Read AGENTS.md + START_HERE.md + newest checkpoint BOTH repos, inspect
actual HEAD, GitHub Actions and logs, then continue feature work per roadmap;
after each code change update engineering log and checkpoint.
