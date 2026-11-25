
# Public Actions checkpoint — Physics0 + OSS Map Editor implementation

2026-11-26. **STAGING TECHNICAL SPIKE / PRODUCTION P1.5 STILL ACTIVE.**

## Source/CI
- Private game Physics0 source under `experiments/physics_v2`.
  Initial native 3D source passes earlier build #45667841114.
- Public Actions added stage import and test steps, export to
  `game/build/web/physics-v2/index.html`, Playwright staging test.
- Public build and Pages #45668117043 SUCCESS; #45669118019 SUCCESS
  (source 29fc83b9) including real native GridMap/CSG editor test,
  m-scale world, ramp/jump, 55.8px chibi art-size test.
- Browser E2E #45668562257 SUCCESS first movement/jump/switch,
  dx=4.11 meters, but its screenshot revealed black floor.
- Rendering bug FIXED later in Private source with unshaded WHITE-tint
  material on original SVG art. Playwright screenshot brightness test
  added with Pillow. Verification of fix pending in next browser run.
- Browser E2E #45668868363 failed due temporary 503 for index.pck;
  Web still loaded and moved +4.155m. Recovered transient asset status
  now warning, not an E2E failure if game/state/visual all PASS.
- Native obstacle low/tall clearance test added subsequently:
  `tests/obstacle_collision_smoke.gd`. Need inspect latest CI.
- Private `BeastMapCatalog` now adds maps by Inspector, with
  resources for original texture, authored scene and surface-grip zones.
- Latest Public code SHA before documentation:
  `98e0ff0ec7d89b0124c197479c90dbbab7c6cb45`.
  This documentation commit is NOT a gameplay source change.

## OSS map stack and legal
- Built-in MIT Godot `GridMap`/`MeshLibrary`/`CSGBox3D`
  (actual native editor, collision shapes); two authored runtime scenes
  are loaded through `PackedScene`.
- Cyclops Level Builder v1.5.2 MIT is OPTIONAL editor plugin; not
  vendored. Terrain3D GDExtension is not part of baseline Web export.
- Official MIT Godot 3D demo patterns cited by Private
  `third_party/SOURCES.md`; no restricted art imported.
- Reference docs PRIVATE
  `docs/architecture/MAP_EDITOR_OPEN_SOURCE_STACK.md`
  and `docs/architecture/PHYSICS_FOUNDATION_V2.md`.

## Pending
1. Run final Godot Physics0 stage+3D wall/rail/terrain material tests.
2. Real Chromium screenshot asserts art visible in BOTH maps and
   no uncaught errors; inspect actual artifact PNGs.
3. Measure performance and test remaining physics matrix; don't
   promote staging experiment over P1.5.
4. When verified update checkpoint in BOTH repos with code SHA,
   CI/Page and Playwright run, observations, known limitations.

## Rules
Read AGENTS, START_HERE and latest checkpoint in both repos before
any deployment. Keep PRIVATE source out of Public artifacts; only
already-approved compiled Pages export is public.
