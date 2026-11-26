**NEW PENDING OWNER MANUAL REVIEW 2026-11-26 — JADE NATIVE-80PX ACTION ART:** User detected idle 80px vs 40px-upscaled action mismatch. PRIVATE source `jade_approved_motion.gd` now uses ONLY approved original 80px art for run/jump/J/K composites; ART-26 checks original source pixels. `autocheck: false` means user decides art quality; this is NOT yet new deployed Pages or user VISUAL_ACCEPTED. Latest previous verified #45764000051/#45764224828 predates this change. NEXT: validate single fresh build/export/deploy, then send owner `/physics-v2/?pixel=1&art=approved` to review. Read `docs/checkpoints/2026-11-26-zzzzzzzzzzz-jade-native-80px-manual-review.md`. **Trạng thái: PARTIAL — chưa hoàn tất.**

**LATEST VERIFIED 2026-11-26 — JADE W/J/K + REAL GROUNDED SHOES + DATA-DRIVEN 2D/3D FLOOR TEXTURES: SCOPED PASS.** Exact compiled PRIVATE `660093be13f55dae0aa30a8eb5d6a72818e87a56`, PUBLIC pipeline `da8094c23464457e50e350283565198ea14ab79d`. [Godot/Windows/Web/Pages #45764000051](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45764000051) ALL PASS. [ACTUAL Chromium #45764224828](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45764224828) PASS, exact build+pipeline assertion. [Real screenshots/report artifact #15091725487](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45764224828/artifacts/15091725487) downloaded and W, J, K PNGs visually inspected. W [0,1,2,3] run poses, 6.44m REAL ground travel/32 samples, 0px per-frame foot anchor mismatch, J row7, K row9, HP unchanged; both J/K camera-screen samples show 100% green walkable floor instead of an illusory vertical wall. Godot `BeastSpriteFootAnchor` aligns transparent margins in Sprite3D and PixelView; `BeastPhysicsMap.floor_texture_walkable_start_y_px` (Moss=64, Docks=80) governs both 2D and native 3D top-floor UV without per-map code, with PRES-15/16/17 and ART-25 tests. **Do not hide previous FAILs**: Chrome #45762495699 and #45762740141 each missed one ~83ms phase under slow software WebGL, #45763700972 fell off map because W fixture contaminated J. PUBLIC E2E `da8094c...` now samples up to three genuine W runs bounded by z=-7.5 and uses independent grounded J/K fixture; final PASS observed all four in one run. Mandatory read latest checkpoint `docs/checkpoints/2026-11-26-zzzzzzzzzz-jade-sprite-foot-pivots.md`, `docs/art/SPRITE_ATLAS_PIPELINE_STANDARD.md`, `docs/art/MAP_TEXTURE_SOURCE_STANDARD.md`, and engineering log/runbook. Preview https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved . **NEXT**: obtain user visual approval and create full editable Aseprite tagged 4-direction authored clips / Godot SpriteFrames import; map visuals and rest of physics/AI/combat/beast roadmap remain OPEN. Latest docs-only commits after compiled SHAs do not alter artifact. **Trạng thái: PARTIAL — chưa hoàn tất** (full game still incomplete).

**LATEST 2026-11-26 — approved Jade W/J/K FLOATING FEET recovery (NOT YET browser verified):** User supplied genuine screenshot showing shoes suspended above 3D ground on run frame. Verified original approved idle has 3 transparent px below shoes but new WJK run frames have 8–10px. New PRIVATE `scripts/sprite_foot_anchor.gd` caches per-cell visible-shoe baseline, `character.gd` uses grounded `Sprite3D.offset.y=-padding`, `pixel_view.gd` shares exact +padding in Canvas Y. `visual_smoke.gd` ART-25 40 grounded frames PASS; source PNG immutable, 3D collider/attack/motor unchanged. `docs/art/SPRITE_ATLAS_PIPELINE_STANDARD.md` records Aseprite/LibreSprite pivot tags, JSON metadata + Godot SpriteFrames; `tools/sprite_atlas_audit.py` audits future atlases. PUBLIC `ci/playwright_physics_v2.py` strict W/J/K real-floor test: first [Chromium #45759115851](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45759115851) FAIL because native grounded player remained idle and input W wasn't registered by test after T, not because foot pivot math failed (actual clearance 0.000147m, source pad3px, sprite offset-3px); fixture now forces canvas focus and waits for settled idle, actual native W velocity before sampling. [Godot/Web/Windows/Pages #45760063063](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45760063063) PASS with exact PRIVATE build `0ee84340ad5bb635b6acd43b2372c143842e157d`, PUBLIC pipeline `cbb8ea24762ea020838aeafcbb3b01b3bff98df7`; spawned [Chromium #45760290243](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45760290243) pending. Strict actual screenshot/HP/map/grounded+W gait not yet PASS, do not claim visually finished. **Read latest `docs/checkpoints/2026-11-26-zzzzzzzzzz-jade-sprite-foot-pivots.md`** in BOTH repos and engineering log / CI runbook. NEXT verify Chromium, diagnose real failure, update checkpoints and source. User wants an enduring sprite management workflow, not more ad hoc clip offsets. **Trạng thái: PARTIAL — chưa hoàn tất.**

**LATEST VERIFIED 2026-11-26 — AUTHENTIC JADE REAR-MOTION TECHNICAL PASS, ART SIGNOFF STILL OPEN:** Private built `3ba321b322918288dbe6baa402184319747fcba8`, PUBLIC `1442efc120d3de898da11588e0e86571769ce4d5`. [Godot, Web/Windows, Pages #45753711701](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45753711701) PASS; [ACTUAL Chromium #45753939789](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45753939789) PASS, genuine screenshot artifact 15086424989; 4 actual fighters, F7 approved 80px hero, back-facing run direction=3 row=4, unchanged HP/map, Moss uphill +2.08m, Docks downhill -2.41m. Original approved PNG untouched; back walk/run repaired by same-artist original-leg composites; rear prone/KO no longer standing. **Actual screenshot shows rear run leg silhouette still unnaturally extended sideways**: NOT fully painted hand-drawn animation, user visual acceptance still OPEN. First browser #45752879529 and second #45753426222 FAILED due newly added W fixture causing unjustified idle wait / contaminated older D-run test; third passed after T reset, no gameplay physics modified. Read latest `docs/checkpoints/2026-11-26-zzzzzzzz-approved-jade-rear-motion.md` (PRIVATE+PUBLIC) and PRIVATE `docs/art/APPROVED_JADE_ANIMATION_STANDARD.md`, plus engineering log. Next: personally illustrate authentic rear run/walk frames and side punch full-body contacts, review real PNG before map/beast work. Play https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved . **Trạng thái: PARTIAL — chưa hoàn tất.**

**LATEST VERIFIED 2026-11-26 — USER-APPROVED JADE ILLUSTRATION INTO REAL GAME:** PRIVATE compiled `03a34e696c1d48fe0910294637bcb98bfa8a59db`, PUBLIC build `5ba8919f938b54fae5a1eaaab6b98c3048a7204b`; [Godot+Pages #45751045283](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45751045283) PASS; [real Chromium #45751278124](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45751278124) PASS. Original transparent 320x1600 PNG 4x20×80px shows correct teal-haired red scarf ivory-vest fighter; source difference 17155 canvas pixels, HP/map parity; image artifact 15085976043 visually reviewed. Preview https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved (F7). Exact guide `docs/checkpoints/2026-11-26-zzzzzzz-approved-jade-web-verified.md`. Original body art accepted technically, **user visual signoff and other art/animation/map not done**. **Trạng thái: PARTIAL — chưa hoàn tất.**

**LATEST VERIFIED 2026-11-26 — ORIGINAL JADE 3-STYLE WEB A/B + PHYSICAL STAGE FLOOR DETAIL:** Read last section of `docs/checkpoints/2026-11-26-zzzzzz-jade-scarf-ab-preview.md` BEFORE older handoffs. PRIVATE exact compiled `4923704a1fa933300ea7e892582aced9733c43ed`, PUBLIC pipeline `b862d848a2ebc5c253de0aba523bad2a03757d61`; Godot Web+Windows+Pages [#45746214982](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45746214982) PASS and REAL Chromium [#45746420155](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45746420155) PASS. Real PNG artifact 15083925898 visually inspected: Classic versus vector Jade Scarf F6 (10190 changed screen pixels) versus original painted WebP Jade P (12369 pixels), same map/HP. Moss +2.155m and Docks -2.370m native 3D real slopes; 32/30 visible original floor details and 64px 2D hero; guard 1501 cyan pixels; P1.5 unchanged. Preview https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=painted. USER art signoff, unique 80 hand-drawn frames, grabs/throws, map art/editor, obstacle AI, device FPS, root migration and V5 beast forms STILL NOT COMPLETE. Source after this release may be docs-only; do not mistake later main HEAD for compiled SHA. **Trạng thái: PARTIAL — chưa hoàn tất.**

**2026-11-26 VERIFIED Web release — 60Hz human J/K chain + original Pixel 2D fixed far skyline:** PRIVATE game actually compiled `b06e131c955f09e50593d890244e8fbe47b44dc2`, PUBLIC build pipeline `441048d2dc92a4c477aa95a985f88c19317ff6c7`. [Godot/Web/Windows/Pages #45743279673](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45743279673) PASS; [real Chromium #45743526820](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45743526820) PASS, Moss +2.12m, Docks -2.39m, strict screenshot artifact 15082730310 examined. Gameplay preview https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1. Latest PUBLIC checkpoint `docs/checkpoints/2026-11-26-zzzzz-fixed-pixel-skyline-web-gate.md`, private latest `docs/checkpoints/2026-11-26-zz-human-art-web-verified.md`. USER art aesthetic signoff and V5 NOT COMPLETE. **PARTIAL — chưa hoàn tất.**

**LATEST 2026-11-26 USER ART REFERENCE (DOCS-ONLY):** Read last section of `docs/checkpoints/2026-11-26-zz-human-art-web-verified.md` and PRIVATE `docs/art/NEKKETSU_SPRITE_REFERENCE_2026-11-26.md`. Kunio sprite https://spritedatabase.net/file/19088 , related Stages https://spritedatabase.net/file/19107 used only as art/technical REFERENCES. Do not ship ripped art without true rightsholder license. No CI change and no new game deploy; last runtime #45735133772 Godot/Pages PASS, #45735342337 Chromium PASS. User art signoff and V5 remain OPEN. **PARTIAL — chưa hoàn tất.**

**MỚI NHẤT / 2026-11-26 — CHẶNG NHÂN VẬT PIXEL 2D ĐÃ NGHIỆM THU WEB:** Đọc `docs/checkpoints/2026-11-26-zz-human-art-web-verified.md` **TRƯỚC** các checkpoint cũ. Private source đã build `191842e4948d6f0a5a864a4c2c5815b240b2fd03`; Public Godot/Web+Windows+Pages #45735133772 PASS, Chromium #45735342337 PASS, đúng source+run. Bốn atlas 80-cell đã chỉnh 64 cell mới cho nhảy/nằm ngã/đứng dậy/KO; hoạt ảnh chạy/đấm theo vận tốc vật lý và timeline 60 Hz, có ảnh thật `moss-running-horizontal-pixel-2d.png` chứng minh F5 2D giữ đường chân trời ngang trong khi chạy trên dốc thực. Guard/HP/2v2/match/T và bản P1.5 cũ PASS. CI cache no-deploy skip branch chưa được kiểm chứng khi lịch tự chạy. **CHƯA XONG:** nghiệm thu mỹ thuật từ người dùng, bổ sung human animations/combos/grab/throw, editor/foreground/AI/performance, P1.5 migration và hóa thú V5 (chưa bắt đầu). **Trạng thái: PARTIAL — chưa hoàn tất.**

**LATEST VERIFIED 2026-11-26 — ORIGINAL SKYLINE + ACTUAL CYAN SHIELD:** Read last section of `docs/checkpoints/2026-11-26-pixel-2d-comparison-and-prop-skins.md` FIRST. Private source `e1e2c74853f1db1d5408b113062f1eacead115c9`; Public Godot+Pages #45730978934 PASS, actual Chromium #45731247515 PASS. Moss Temple now has distinct original shrine/gate/cedars/tower silhouettes; Night Docks warehouse/crane/tanks/containers. Real F5 0.5m slope 468/576 tile spans, four human fighters/portraits, guard cyan shield screenshot 1662 visible pixels, 2v2 match/round and T reset PASS. CI publication-gate #7dadcfd success branch PASS, scheduled no-deploy skip needs future actual verification. Original P1.5 remains separate; user art signoff, human animation/advanced combat, live editor, device FPS and V5 beast transformation are NOT complete. **Trạng thái: PARTIAL — chưa hoàn tất.**

**LATEST verified 2026-11-26 original impact FX:** Read `docs/checkpoints/2026-11-26-pixel-2d-comparison-and-prop-skins.md` final section. Build+Pages #45693164657 SUCCESS and Chromium #45693795373 SUCCESS, private source `4ab090e33e51822cc4639d6165ac8d4319a9be37`. Real 2v2 3D hit count=20 and authored original pixel visual event count=20, G/round/T/F5/screenshots regression PASS. Real cyan guard spark Chrome capture still pending, original art user review and advanced V4+V5 remain PARTIAL.\n\n**2026-11-26 LATEST VERIFIED HUMAN-ONLY PIXEL VERSION:** Read `docs/checkpoints/2026-11-26-pixel-2d-comparison-and-prop-skins.md` newest section and matching PRIVATE checkpoint. Source `d1a22bae199ba80296e6af850906e95241619f9b`; Godot+Pages [#45691649914](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45691649914) SUCCESS; Chromium [#45691975794](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45691975794) SUCCESS. Both actual pixel 2D Moss/Docks screenshots examined, finely sampled 0.5m physical incline (468/576 tiles), 4 original fighters/portraits, G guard, 60Hz 2v2 round/timeout, T restart all pass. Playable preview `/physics-v2/?pixel=1` ONLY; P1.5 root unmodified. Visual art user approval, V4 advanced combat/map editor and V5 beast form remain **PARTIAL — chưa hoàn tất**.

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
