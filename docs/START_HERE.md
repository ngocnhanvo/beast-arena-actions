**NEWEST 2026-11-26 QA:** See `docs/checkpoints/2026-11-26-pixel-2d-comparison-and-prop-skins.md`. Direct original 2D stage `?pixel=1` and 4 pixel fighter portraits VERIFIED CI #45687946574 + Chromium #45688376830, source `9f27e53`. Browser #45688049122 failed stale build/test race, fixed Public `web-e2e.yml` `3cfa440` + strict SHA/run test `3b9b9a`, pending latest E2E check. New PRIVATE `0911450` has true Z-depth sprite/prop occlusion test NOT yet built. Root P1.5 intact, V5 deferred, VISUAL_ACCEPTED OPEN.

**LATEST 2026-11-26 F5 PIXEL-2D QA:** Read `docs/checkpoints/2026-11-26-pixel-2d-comparison-and-prop-skins.md` and matching PRIVATE checkpoint. Six real obstacle skins with original pixel-art textures: build+Pages #45685202832 PASS from source `549a33e`. New OPTIONAL F5 2D CanvasLayer view (SAME 3D physics) and public headless/Chromium test code `a04fc58`/`ca30f94` require new run and screenshot validation. Prior compact 3D Chromium #45684936382 PASS but aesthetic angled-stage issue is still OPEN. Do not announce new F5 screenshots/deployment until actual PASS.

**NEWEST HUMAN VISUAL+COMBAT SOURCE (2026-11-26) — NOT YET LIVE VERIFIED:** Read PUBLIC `docs/checkpoints/2026-11-26-v3-v4-human-combat-source.md` and PRIVATE matching checkpoint. New Physics0 code contains source-SHA stamped build, 2 original pixel stages, four original 80-frame colorway human atlases, opt-in `C` 2v2 AI + J/K actual hit damage, HP/KO, height-aware 60Hz attack resources. Public CI tests for V0-V4 and Chromium are authored but there is NO NEW verified build/Pages/Playwright run ID or screenshot. The old PASS #45676762869/#45677121093 predates all these changes. Never mark production migration or V5 complete.

**LATEST VISUAL-FIRST PRIORITY (2026-11-26):** User still perceives the whole arena as tilted and wants original pixel-art stages/fighters close in *style* to Nekketsu Kakutō Densetsu, **before** transformation. Read PRIVATE `docs/plans/NEKKETSU_VISUAL_FIRST_2026-11-26.md` and BOTH `docs/checkpoints/2026-11-26-visual-first-nekketsu-plan.md`. Angle-locked browser PASS #45677121093 is not a VISUAL acceptance; next pipeline must prove fixed world-line appearance, build ID and human screenshot approval. Do not include reference-game assets in Public builds.

# START HERE — Beast Arena Actions Public

**CAMERA TILT FIX VERIFIED 2026-11-26:** Godot CI/Pages #45676762869 PASS, browser #45677121093 PASS, Physics0 `camera_projection_locked=true` at fixed pitch -37.405°, yaw/roll=0. Read `docs/checkpoints/2026-11-26-camera-fixed-orientation.md`. Original P1.5 root remains unchanged.

**LATEST CAMERA FIX (2026-11-26):** Physics0 user sees whole map tilted during movement. Private game `d5bec34` locks 2.5D projection by removing per-frame camera `look_at`; Public test `e18cf413` rejects drift >0.10° on movement, ramps and map change. Read `docs/checkpoints/2026-11-26-camera-fixed-orientation.md`; check run #45676396568 and follow-up Chromium before reporting PASS.

**LATEST VERIFIED 2026-11-26:** Visible real slopes (isolated Physics0 only) built+deployed #45673586733 SUCCESS, Chromium #45673951103 SUCCESS: Moss +2.14m, Night Docks -2.39m real Y, screenshots checked. Read `docs/checkpoints/2026-11-26-visible-slopes.md`. Main P1.5 still separate.

**2026-11-26 PLAYER-VISIBLE SLOPE FIX:** read `docs/checkpoints/2026-11-26-visible-slopes.md` and PRIVATE `docs/architecture/VISIBLE_SLOPE_ACCEPTANCE.md`. The earlier V2 demo passed physics but slope was offscreen and nearly invisible. New source `22c3e80` plus Playwright `4fee8eb` require R ramp-entry screenshots and measured Y uphill/downhill on BOTH stages. GitHub CI #45672632606 started; do not assert final Web PASS until inspected.

**FINAL VERIFIED 2026-11-26:** Native Godot Physics0/map staging build+Pages run #45670308588 and Web Chromium run #45670647655 PASS on game code a39af14. Screenshot Moss + Docks + colored CSG proof reviewed. Read `docs/checkpoints/2026-11-26-physics0-oss-staging-passed.md`; staging is separate and not Physics V2 full migration.

**LATEST 2026-11-26:** See docs/checkpoints/2026-11-26-physics0-oss-staging-passed.md: Godot/Pages #45670308588 PASS for native 3D Physics0 + built-in GridMap/CSG. Chromium #45670647655 pending at documentation time. Staging /physics-v2/ is NOT production migration.

**LATEST 2026-11-26:** Physics0 is now implemented and verified in
a SEPARATE Godot 3D project on GitHub Pages at `/physics-v2/`, but it
is a prototype, NOT the production engine. Native Godot GridMap/CSG map
scenes, source art and material zones are in Private repo
`experiments/physics_v2/`. Read
`docs/checkpoints/2026-11-26-physics0-native-map-progress.md`.
Latest floor-visibility and obstacle-collision tests require checking
actual runs/screenshots before marking accepted.

**OSS REUSE REVIEW 2026-11-26:** PRIVATE
`docs/architecture/OPEN_SOURCE_COMPONENT_AUDIT.md` lists pinned,
licensed candidates (Godot official demos, GDQuest code, SUCC,
Stairs Character). Source review complete, **no plugin imported or
Physics V2 tests run**. New latest checkpoint:
`docs/checkpoints/2026-11-26-physics-v2-oss-audit.md`.
 
**IMPORTANT UPDATE 2026-11-26:** Physics V2 architecture-first decision.
Before new physics CI/Playwright work read PRIVATE
`docs/architecture/PHYSICS_FOUNDATION_V2.md`,
`docs/decisions/ADR_0002_UNIFIED_3D_PHYSICS.md`,
`docs/testing/PHYSICS_V2_ACCEPTANCE_MATRIX.md`, and newest checkpoints in
BOTH repos. ADR is PROPOSED and Physics V2 is NOT IMPLEMENTED.


Ngày lập: 2026-11-25. Hướng dẫn tiếp quản CI/CD và browser testing.

## Repo topology
- PRIVATE game: https://github.com/ngocnhanvo/beast-arena
- PUBLIC Actions: https://github.com/ngocnhanvo/beast-arena-actions
- LIVE GitHub Pages: https://ngocnhanvo.github.io/beast-arena-actions/
- Private Releases: https://github.com/ngocnhanvo/beast-arena/releases

Private source token BEAST_ARENA_READ_TOKEN (fine-grained Contents Read-only, one repo) và optional upload token BEAST_ARENA_RELEASE_TOKEN (Contents Read/write, one repo) nằm trong Actions secrets. Không in/đọc giá trị.

## Đọc theo thứ tự
1. AGENTS.md (repo này) → docs/CI_PLAYWRIGHT_RUNBOOK.md.
2. docs/SETUP.md, docs/SECURITY.md, docs/WEB_E2E.md, checkpoint mới nhất.
3. Workflow hiện tại .github/workflows/build.yml và .github/workflows/web-e2e.yml, các script trong ci/.
4. Repo game PRIVATE docs/START_HERE.md và docs/architecture/GAME_SYSTEMS_BLUEPRINT.md để hiểu scope.
5. Kiểm tra HEAD + workflow runs/logs thực tế; snapshot bên dưới có thể đã cũ.
6. Khi hoàn thành task, cập nhật docs/checkpoints + runbook với bằng chứng.

## Pipeline hiện tại
- Public CI chạy Godot 4.7.2, import và headless combat/smoke, export Web/Windows, tạo ZIP.
- Nếu có release token, lưu ZIP vào Private Release theo tag gắn với SHA source, không upload trùng không cần thiết.
- GitHub Pages là PUBLIC, tự deploy khi repo Actions push hoặc khi hourly recovery; manual build với deploy_pages=true.
- Workflow Pages retry tối đa 4 lần nếu GitHub API tạm trả HTTP 500; caches SHA build + Pages.
- Browser Playwright chạy từ workflow_run nếu CI completed successful hoặc workflow_dispatch; dùng headless Chromium/SwiftShader, screenshots/result JSON PUBLIC.

## Verified state as of 2026-11-25
- Godot CI + Web/Windows exports + Pages deploy: run 45652585969 SUCCESS; run 45651281051 SUCCESS.
- Private Release ci-9e140e8e93e1: 2 ZIP tồn tại.
- Playwright E2E: runs 45652872940 / 45653213044 FAILED với AssertionError Godot canvas too small. Chưa được nghiệm thu browser gameplay.
- Current workflow source snapshot trước docs: main commit 7546acb611ed6772716dc32b88ed129eab12384a. Verify new HEAD trước mọi lần chỉnh.

## Next priority
1. Lấy artifact screenshots + result.json của E2E fail run 45653213044; xác minh canvas CSS bounds/natural size/WebGL before fixing.
2. Fix Playwright hoặc Godot Web loader theo evidence; rerun E2E, xác nhận character actually moves.
3. Bổ sung game debug hooks (ở Private repo) để test state attack/jump/beast, không dùng pixel placeholder lâu dài.
4. Bảo đảm CI không rebuild chỉ vì docs-only update nếu đã tách workflow; cân nhắc tối ưu trong phase sau, không làm ảnh hưởng deploy.
5. Mỗi sự cố bổ sung runbook/checkpoint, không dán secret vào chat.

**Một dòng nhớ:** BUILD PASS != PAGES PASS != PLAYWRIGHT PASS.

## P0/P1a live update 2026-11-25
- Playwright older source was fixed by waiting for rendered scene; run 45656492064 PASS and D moved +266.2px.
- Godot P1 headless import, combat, smoke, spatial FSM and wall collision tests + Web/Windows + Pages PASSED in run 45656838908 (pre-F2 overlay source).
- New P1 Web smoke test now uses ?e2e=1 read-only game snapshot to check ready, Space jump Z/event, J attack event, D movement and screenshot. Verify newest run before claiming PASS.
- Latest private source has F2 debug circles, walls and spawn points. New build required after source commit; do not confuse prior CI success with latest source.
- Always read newest checkpoint in both repos and verify live runs.

## Final verified P0/P1a (2026-11-25)
See docs/checkpoints/2026-11-25-p0-p1-verified.md. Public CI/Pages 45657432571 and 45657606670 SUCCESS; browser E2E 45657791050 SUCCESS with J/Space/D gameplay state, F2 collision overlay and screenshot. Source functional SHA e3d3b3f; later private docs-only head may differ. Full per-frame combat engine is NOT implemented.

## P1.5 follow-up design — camera and image-first stages

Owner approved maps larger than viewport with Camera2D following player,
camera clamp, independent playable/world/image boundaries and layered
image-first art with editable collision/walkable/navigation polygons.
See PRIVATE `beast-arena/docs/architecture/P1_5_IMAGE_FIRST_MAP_CAMERA.md`
and PRIVATE checkpoint `2026-11-25-p1-5-camera-requirement.md`.
Public test acceptance is in `docs/CI_PLAYWRIGHT_RUNBOOK.md`.
**This is a PLAN, not implemented.**

## Verified P1.5a two wide-map preview — 2026-11-25

PRIOR P1.5 'not implemented' notes are historical. The user can now play
two larger-than-viewport maps on public Pages:
Moss Temple 2560x1440, Night Docks 3072x1536, bounded/smoothed Camera2D.
Private functional SHA `226d413e683ee30ea5e511a630e5ab96e6442e63`.
Public workflow/test SHA `1dc3845e9769713e359da144c93a19e9fab4bc73`.
Build+Pages #45660505234 SUCCESS; browser #45660829632 SUCCESS, screenshot
artifact has both maps near/far, jump/attack/movement, F2 and camera clamp.
Read latest checkpoint `docs/checkpoints/2026-11-25-p1-5-demo-verified.md`.
Interactive polygon map editor/character/equipment tools remain TODO.

## 2026-11-26 — 2.5D obstacle shaping follow-up

PRIVATE game docs/architecture/STAGE_OBSTACLE_DESIGN_STANDARD.md defines:
footprint(world XY), height_px, shape/material, shadow/top/side faces, Y-sort,
solid collision and limits. Both map demos now use 5 authored model instances.
Read newest obstacle checkpoint in both repos; first CI #45662885191
failed due to StageData @tool placeholder and source fix was committed.
Do not claim deployment before latest build, Pages and Playwright verify.

## 2026-11-26 — Verified 2.5D obstacle model preview

Previous "retest required" note is historical. CI/Pages #45663247335
and browser #45663585488 PASSED for Private game source FF19F025.
Both maps feature five original modeled obstacle visuals with ground-foot
collider, separate height and F2 overlays. See latest Public checkpoint
`docs/checkpoints/2026-11-26-obstacles-verified.md` and Private standard
`docs/architecture/STAGE_OBSTACLE_DESIGN_STANDARD.md`.
Vaults/platforms/hazards/destructible props are NOT implemented.
