
# Beast Arena Actions checkpoint — Physics V2 plan — 2026-11-26

Status: DESIGN ONLY; 3D physics NOT IMPLEMENTED / NOT TESTED.

- PRIVATE Game base source HEAD before design `30ce9651ad361ad664afaf800a18b8c9eaf7b4f4`.
- PRIVATE architecture/docs committed to main at
  `0a15b38497be0f4430948a06a4767634a739568a` and
  `9d2a37db0deefe835ac93925616a0dbfd81d7cbc`.
- PUBLIC Actions original head prior this doc `28831970dbfc56572b0e0b635b7d0d6d8e582dc1`.
- Last verified P1.5 (OLD 2D/visual height) build & Pages:
  https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45663247335
  SUCCESS.
- Last verified P1.5 browser:
  https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45663585488
  SUCCESS.
- New user requirement: design a complete authoritative physics system
  before adding ramps, height, momentum, map, hazards and hitbox behavior.
- Preferred experimental direction: Godot 3D Physics source of truth with
  orthographic 2.5D art, XZ ground/Y up, meter units; preserve P1.5 demo.
- Mandatory PRIVATE docs: `PHYSICS_FOUNDATION_V2.md`,
  `ADR_0002_UNIFIED_3D_PHYSICS.md`,
  `PHYSICS_V2_ACCEPTANCE_MATRIX.md`.
- Next: isolated P-Physics0 spike, own headless tests + Playwright preview
  without replacing public main entrypoint, document GO/NO-GO and
  migration feasibility.
- Only docs changed; no new workflow run or 3D engine migration triggered.
- Future assistant: read AGENTS, START_HERE, newest checkpoint BOTH repos
  before changes; verify real latest GitHub HEAD/runs; update docs/logs.
