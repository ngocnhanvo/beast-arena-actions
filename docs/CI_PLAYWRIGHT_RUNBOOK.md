# CI/CD & Playwright — Runbook thực chiến

## Mục đích và boundaries
Ngocnhanvo/beast-arena-actions là PUBLIC, dùng standard hosted runners để import/test/export Godot từ repo game PRIVATE. Web được publish qua Pages PUBLIC theo quyết định người dùng ngày 25/11/2026. Không xuất raw source hoặc token; chỉ build artifact được chỉ định.

## Release chain và cách xác minh
1. Xác nhận main HEAD game và actions, workflow version đang chạy.
2. Public Actions build.yml: preflight → read-only private checkout → Godot 4.7.2 install/import → combat test → smoke test → Web/Windows exports → ZIP.
3. Optional Private release upload qua BEAST_ARENA_RELEASE_TOKEN: tag ci-<12 chars source SHA>. Nếu đủ 2 ZIP thì skip upload, tránh GitHub 500 khi clobber.
4. Pages upload artifact: chỉ game/build/web (PCK có thể lộ scripts/assets). Pages deploy: retry 4 lần; ghi successful Pages SHA cache.
5. Browser web-e2e.yml: Playwright Chromium mở Pages URL, đo canvas, test D movement, gửi J/K/Space/U, screenshots/results. Một bước Playwright FAIL phải được xử lý; không bỏ qua.
6. Chứng cứ minimum khi báo hoàn thành: source SHA + Actions SHA + run URL + từng job status + Pages URL status + E2E result/screenshot.

## Known problems và xử lý
### A. Run được yêu cầu nhưng website 404
- OBSERVED run 45650309237: build/export/upload Pages artifact PASS, deploy Pages HTTP 500.
- Root cause khi đó: GitHub Pages API không tạo được deployment (external server HTTP 500); không phải lỗi Godot compile.
- Fix đã áp dụng: Pages deploy retry theo 20/40/60s, hourly schedule cron 17 * * * * ở Public, cache riêng cho build + Pages.
- Verification: Pages job PASS ở run 45651281051. Luôn kiểm tra site HTTP sau deploy nếu có thể.
- CẢNH BÁO: GitHub UI 'workflow run was successfully requested' chỉ xác nhận đã nhận lệnh.

### B. Private release upload lại lỗi HTTP 500
- OBSERVED run 45649259196: gh release upload --clobber trả 500 với asset đã có.
- Fix: check 2 file ZIP ở Release có sẵn thì không clobber; thiếu thì retry/backoff.
- Verification: run 45649451401 PASS sau fix. Không thử xóa assets nếu chưa xác minh.

### C. Playwright 'Godot canvas too small'
- OBSERVED runs 45652872940, 45653213044: browser smoke FAILED. Screenshot artifact được upload dù test fail.
- Vị trí: ci/playwright_smoke.py, assert bounding_box().width > 400.
- Chưa xác định root cause: có thể viewport/CSS, Web engine init hay DOM. Không được mặc định là một trong số này.
- Chẩn đoán theo thứ tự:
  1. Tải artifact 'beast-arena-browser-screenshots' ở run 45653213044; mở failure.png và result.json.
  2. In page.url, HTTP statuses, canvas count, natural width/height + getBoundingClientRect + computed CSS + viewport; ghi lỗi JS và WebGL context.
  3. Kiểm tra screenshot nội dung: loading screen vs game vs 404; tách mạng/site readiness khỏi game readiness.
  4. Thử điều kiện chờ Web app ready; chỉ nới threshold nếu có chứng cứ, không che game canvas thật bị thu nhỏ.
  5. Khi test qua, thêm assert player actually moves và states/hit; màu placeholder chỉ là test tạm, thay bằng debug hook khi thay art.
- Test U trước khi Beast meter >=50 không chứng minh transform; test J/K chỉ dispatch key, không chứng minh gây damage.
- Browser headless SwiftShader có thể khác GPU người chơi; cần bổ sung manual browser test/Android về sau.

### D. GitHub write API gặp timeout / 409
- OBSERVED ReadTimeout, GraphQL error và 409 'Timed out validating the rule' khi commit.
- Sau lỗi phải **đọc HEAD và file path trước khi retry** để tránh duplicate/overwrite; chia commit nhỏ hoặc git blob/tree với expected_sha lease, không khẳng định push nếu chưa xác nhận.

## Bảo mật và chi phí
- Runners nặng chỉ PUBLIC repo; Private source repo không có workflow build nặng.
- Public Pages và Web PCK có thể bị xem/trích xuất; không bao giờ publish secrets, private source, unlicensed material.
- PAT chỉ quyền tối thiểu, lưu trong Secrets; không đưa full token vào log/script/artifacts.
- Phân biệt GitHub Actions cache/artifact và GitHub Releases; kiểm tra billing policy GitHub hiện tại nếu có thay đổi.
- GitHub Pages public availability phụ thuộc dịch vụ bên ngoài; bảo vệ bằng retries hữu hạn và checkpoint, không giả định mọi outage tự giải quyết ngay.

## Ghi sự cố mới
Date/Repo SHA/Actions run & job/Expected/Observed error/Verified vs hypothesis/Fix SHA/Tests PASS FAIL NOT TESTED/Remaining blocker.

## 25/11/2026 — verified new evidence & P1 gates
- Browser screenshot artifact run 45654797567 showed Godot splash/progress bar still loading; premature canvas-size check was wrong readiness criterion.
- Fix first waited for actual arena pixel content. Run 45656492064 PASS: Web game rendered and player moved +266.2 pixels after D.
- Updated game P1 emits opt-in public diagnostic snapshot only with query ?e2e=1 (window.__beastArenaDebug). Updated Playwright waits ready=true then checks obstacles=2, Space increments jump event with z>0, J increments attack event, D actually changes player world x, and screenshots.
- P1 Godot import/tests/export/Pages run 45656838908 PASS (before F2 source). Earlier run 45656654819: GDScript Rect2.translated unavailable; Godot import returned exit 0 despite SCRIPT ERROR and smoke failed. Changed Stage to Rect2(pos+offset,size) and importer CI step to inspect logs for SCRIPT ERROR.
- F2 overlay and docs private source are newer than 45656838908; require final full build and browser run before claiming latest version verified.
- When Playwright fails, download artifact result.json and failure.png and inspect state/DOM/JS errors; DO NOT silence assertion to paint it green.

## 2026-11-25 — Final verified P0/P1a browser outcome
- Godot engine build+Pages #45657432571 and #45657606670 SUCCESS; source e3d3b3f with F2 debug layer.
- Browser #45657791050 SUCCESS. JSON snapshot: player x before=210, after=437.5 (+227.5); jumps=1 with positive Z; attacks=2; collision_debug=true; obstacle count=2; no critical JS/WASM/PCK asset error. Screenshot artifact arena-debug-overlays.png visually confirms red collision outlines and yellow spawn points.
- Use opt-in ?e2e=1 and explicit Godot debug-state readiness; no assumptions about loading splash or pixel color.
- Next engineering task is P1b frame-accurate combat hitbox model, NOT reopening P0 without new evidence.

## 2026-11-25 — Future P1.5 scrolling-map camera acceptance (NOT IMPLEMENTED)

Product requirement is recorded in PRIVATE game repository
`docs/architecture/P1_5_IMAGE_FIRST_MAP_CAMERA.md`.

Once game source adds Camera2D/StageData world bounds, extend Public Playwright:
1. Open stage larger than 960x540 viewport (e.g. 3000x1500), wait for ready.
2. Read opt-in `?e2e=1` snapshot: player world XY, camera world XY,
   world bounds and camera bounds. Assert D movement past visible frame makes
   camera X increase (do not just inspect screenshot).
3. Assert camera clamps near both limits; screenshots show no blank outside
   background image and F2 collision graphics still align with obstacles.
4. Jump with Space; player height Z changes but camera Y does not bob solely
   because of Z. UI remains fixed while world scrolls.
5. Check collision and AI continue outside viewport; test return to spawn
   and teleports reset smoothing.
6. Capture screenshot evidence and result.json, preserve code SHA & run links.

Current P1a E2E runs are PASS, but this **new scrolling-map camera feature is
NOT TESTED and must never be represented as shipped**.

## 2026-11-25 — P1.5 two map/camera test observed PASS

- Public build https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45660505234 SUCCESS: checkout private source 226d413e683e, Godot import, combat/smoke/P1 core, **new P1.5 map test**, Web/Windows export, private ZIP release and Pages.
- Browser https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45660829632 SUCCESS: HTTP 200, no JS/WASM/PCK errors, readiness via opt-in `?e2e=1`, D moved +220.5 world units, Space/J/F2, stages switch with key 2, F3 far camera, F4 return.
- Snapshot values: Moss Temple world 2560x1440, far camera X=2080 Y=1140; Night Docks world 3072x1536, far camera X=2592 Y=1220, return X=480 Y=520. Test asserts camera never exceeds limit_right-viewport_width/2.
- Screenshots in public artifact `beast-arena-browser-screenshots`: `arena-ready.png`, `moss-temple-far-camera.png`, `night-docks-start.png`, `night-docks-far-camera.png`, `night-docks-return.png`.
- P1.5b editable polygons in Godot EditorPlugin and P1.5c props/characters are NOT IMPLEMENTED; the current demo offers `@tool` map texture/region Resource Inspector preview only.

## 2026-11-26 — Obstacle graphics / footprint validation

- User requirement: objects must have real recognizable shapes and plausible
  height, inspired by Nekketsu's staged hazards, not flat rectangles.
- Game source now uses `ArenaObstacleData` (kind/material/footprint/height),
  `ArenaObstacleView` with shaded projected form and y-sort alongside players.
  Five distinct obstacles per map, StaticBody2D physical footprint separate.
- Browser test `ci/playwright_smoke.py` now requires >=5 collision bodies,
  five actual visual props and meaningful height metadata per stage.
- First CI run #45662885191 **FAILED** during Godot headless editor import:
  Stage @tool called get_obstacles() on non-@tool StageData placeholder.
  Private fix: mark StageData @tool. Rebuild must confirm this and any further
  parser/scene errors before Pages deploy.
- If FAIL: inspect job log and screenshots; don't bypass importer gate.
  Check that actual F2 footprint overlays align after camera scrolling.
- Height data currently affects visual projection and asset contract.
  Jump-vault/platform physics, hazards and destructible props NOT implemented.

## 2026-11-26 — Obstacle models and deployment confirmed

- First import #45662885191 FAILED because the StageData resource class
  lacked @tool while ArenaStage._draw was @tool. Private source fixed.
- CI #45663247335 **SUCCESS**: source ff19f0253c9c, Godot import,
  combat/P1/P1.5 tests, Web/Windows export, Private Release and Pages.
- Browser #45663585488 **SUCCESS**: 5 physical+5 actual visual props per
  map. Moss height [105,142,66,126,32]; docks [134,72,80,164,130].
  D +213.5 world units, F2 overlay, jump/attack, map switch, far camera.
  Screenshots artifact `beast-arena-browser-screenshots`.
- CHECKED: browser run error-free critical network/JS; F2 screenshot
  demonstrates foot outline + vertical height marks separate from silhouette.
- No claim yet for jumping across low rails, elevated surfaces, damage hazards,
  destructible props or production-quality pixel art.

## 2026-11-26 — Physics V2 architecture spike (PLANNED ONLY)

The owner asked for one unified physics design before any more slope/height
patches. Private architecture documents:
- `docs/architecture/PHYSICS_FOUNDATION_V2.md`
- `docs/decisions/ADR_0002_UNIFIED_3D_PHYSICS.md` (PROPOSED, not ACCEPTED)
- `docs/testing/PHYSICS_V2_ACCEPTANCE_MATRIX.md`

The proposed technical proof uses Godot CharacterBody3D, real XZ ground/Y
elevation, floor slopes/materials and orthographic 2.5D rendering. Risks:
migration of current Node2D art/stage/camera, WebGL2 Compatibility renderer
and game performance. The proof must be implemented ISOLATED from the
current main scene to avoid breaking public playable demo.

When the experiment exists, introduce a separate CI stage:
1. Godot 4.7.2 headless test for PHYS-01..PHYS-08, PHYS-14 + negative tests,
   floor normals, acceleration, low/high obstacle sweeps and raised platform.
2. Web export in Compatibility renderer to SEPARATE route/artifact,
   not overwrite the production GitHub Pages entrypoint.
3. Playwright Chromium confirm 2.5D visuals, 60Hz input telemetry,
   3D position/slope/contact/landing, camera ground following, screenshots
   and reported frame timing on reference browser.
4. Record source SHA and exact failed/passed jobs and artifacts.
5. Only after successful gate and explicit ADR change begin migration,
   with old 2-map E2E regression tests preserved.

No physics V2 workflow/test has been created in this documentation-only
commit; do not claim Web/Windows Physics V2 PASS.

## 2026-11-26 — Use existing licensed engine/controllers before implementing Physics V2

- PRIVATE game source audit committed in
  `docs/architecture/OPEN_SOURCE_COMPONENT_AUDIT.md`.
  Original engine Godot is MIT; official 3D platformer and kinematic examples
  selected as reference, GDQuest MIT code (DO NOT COPY CC-BY-NC-SA art),
  SUCC MIT optional comparison but FPS-specific. Source SHA pins in audit.
- **No new Physics V2 controller code has been imported or tested**.
  Current CI and browser validations remain for the P1.5 2D prototype.
- When separate V2 spike exists, use Public runner, inspect licenses/manifests
  in Private, compare official baseline vs optional SUCC on identical
  slope, 0.2m step, low/high obstacle, landing and Web rendering fixtures.
- Godot built-in Jolt and GodotPhysics3D backends need measured test.
  Default Web export templates lack GDExtension support: do not add
  standalone Jolt extension automatically.
- Preserve current Pages root until go/no-go approval, capture all real
  job logs, screenshots, FPS and camera/position telemetry before claiming
  a successful migration.

## 2026-11-26 — Isolated Physics0 and Web image-quality regression gate

- Public CI now imports `game/experiments/physics_v2/`, runs
  `physics_smoke.gd`, `map_editor_smoke.gd`,
  `obstacle_collision_smoke.gd`, exports second Web under
  `game/build/web/physics-v2/`. Public Pages root remains P1.5, not V2.
- Browser `ci/playwright_physics_v2.py` uses opt-in
  `window.__beastPhysicsDebug`, verifies real CharacterBody3D Y jump,
  X movement in meters, maps/camera and screenshot. A separate
  Pillow pixel test catches a prior BUG where the 3D floor was completely
  black even though gameplay and assets had loaded. Use screenshots
  not just state assertions.
- CI #45667841114 and #45668117043 success for early Physics0 import,
  movement and export. CI #45669118019 success for native GridMap
  paint/erase/collision + art scale (55.8px at 960x540);
  browser #45668562257 PASS initial physics but floor black.
- Browser #45668868363 FAIL recorded a **transient** 503 response
  for index.pck; game nevertheless booted and moved +4.155m. 
  Updated test retains a `transient_asset_warnings` report when
  complete game/visual assertions pass rather than failing solely
  because an earlier retry got 503.
- Visual fix in PRIVATE stage material: unshaded image albedo, WHITE
  tint on authored image texture. New pixel acceptance test for Moss
  and Night Docks is mandatory and pending fresh Web run.
- Full V2 design matrix, native stage authoring usability and low/tall
  collider tests are still ongoing; do not mark production migration ready.

## 2026-11-26 — Retest Web CSG authoring colors after screenshot review

Godot Physics0 Playwright #45669821453 passed both physics and P1.5;
Pillow proof `moss_visible_floor_fraction=0.989`,
`docks_visible_floor_fraction=0.987`, D +4.097m.
Screenshots confirm original SVG floor textures now render correctly.
However some bare editor-created `CSGBox3D` geometry was black because
the editor blocks used default shaded material; added an original
`@tool BeastPaintableBlock` subclass that assigns unshaded authored
colors in both editor and Web. `map_editor_smoke.gd` now asserts
CSG material is unshaded and CSG collision stays enabled.
New public build is required to verify latest Private source, not to
replace production P1.5 (staging remains /physics-v2/).

## 2026-11-26 — Latest Physics0 native Godot/Pages run

Game code a39af14ac7fe51785d36778ea0af440d366d2d88, Actions code 3a7233a027a7d87676e6def2399944223a2a6200.
Godot/Pages #45670308588 SUCCESS, including real slope tests, native GridMap/CSG unshaded editor prop validation, real jump over low rail/tall wall block, 55.8px sprite scale and Web export.
Earlier real Chromium #45669821453 PASS with Moss floor fraction .989 and Docks .987; new browser #45670647655 pending at this writing to examine latest CSG material. Never infer browser pass from Godot import success.

## 2026-11-26 — FINAL Physics0 staging Web QA

Godot/Pages run #45670308588 SUCCESS, browser #45670647655 SUCCESS,
exact game source a39af14ac7fe51785d36778ea0af440d366d2d88,
action source 3a7233a027a7d87676e6def2399944223a2a6200.
Downloaded Playwright artifact: Moss floor fraction .989, Docks .987,
movement dx=4.175m, page errors 0, critical asset errors 0; screenshots
reviewed and CSG block colors no longer black.
Retain the Pillow screenshot gate; CI success alone previously missed
the black-floor rendering bug. Physics0 only STAGING, don't replace root.

## 2026-11-26 — User cannot see slopes despite previous green physics/Web tests

- OBSERVED: P0 Moss X[-7,+7] +2.4m/14m ~9.7deg and Docks -2.8m/18m; both mid-map. Spawn and far-camera snapshots skipped the actual ramp. Same texture across flat and slope. Existing Playwright only checked nonblack ground, not readable slope.
- Code fix PRIVATE game `22c3e80`: +3.6m/12m (~16.7deg) in both directions, contrasted ramp albedo, 11 cross-path tread lines, retaining face in side view, yellow floor borders, world-space height labels, player spawn/camera at ramp, R to teleport to slope entry.
- NEW browser acceptance `ci/playwright_physics_v2.py` PUBLIC `4fee8eb`: require ramp visuals >=25, angle >=14deg, screenshots of BOTH map slope entry/mid-traversal, measure actor actual world Y changes >=1.2m up/down after D held 2.6sec, contact floor angle >=10deg.
- Godot build run #45672632606 started, strict import and native 3D tests passed in preliminary logs. Check **final** CI/Pages+browser and screenshots before claiming slope visible. Original P1.5 page remains untouched; V2 stages under `/physics-v2/`.

## 2026-11-26 — post-verification HUD/sign legibility pass

- Visual slope traversal Web #45672998414 SUCCESS for initial corrected
  functional source `22c3e80`: Moss Y +2.21m, Docks Y -2.44m, real floor
  normal >=10deg, 4 slope screenshots both maps, legacy P1.5 regression PASS.
- Screenshot review: striped ramps and retaining walls clearly visible,
  but previous five-line white debug HUD overlapped the map's altitude
  signs near top of viewport. PRIVATE follow-up commit
  `8e7b163bf59a62fc886046c1d9908b0b5b52c39d` uses a compact dark
  HUD panel and moves billboard labels to near camera-side ramp edge.
- New PUBLIC push CI should build this exact commit and run Playwright;
  do not claim UI overlap fixed until actual screenshots reviewed.


## FINAL VERIFIED 2026-11-26 — SLOPE VISIBILITY ACCEPTANCE PASS

- Final PRIVATE game functional SHA `8e7b163bf59a62fc886046c1d9908b0b5b52c39d`. PUBLIC source for build `ad26866feb2d2779d5453cc9281edc980d8c9f8f`.
- CI / Godot import / native physics smoke / GridMap editing / low-rail vs high-wall collision / Web+Windows exports / Pages: **SUCCESS** https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45673586733 . Logs verify game source 8e7b163.
- LIVE Web Chromium: **SUCCESS** https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45673951103 . P1.5 legacy regression PASS (D +213.5px) and Physics0 ramp proof PASS: physical **uphill +2.14m Moss**, **downhill -2.39m Docks**, real floor normal 16.7deg, player D movement +3.82m.
- Playwright screenshots downloaded and visibly checked, new slopes with distinct stone treads, 3D retaining faces and START / UP or DOWN / END elevation labels are clearly seen on two maps. Compact dark HUD prevents overlaying 3D slope labels.
- Artifact name `beast-arena-browser-screenshots` in run #45673951103 includes `physics-v2/moss-slope-entry.png`, `physics-v2/moss-ramp-mid-climb.png`, `physics-v2/docks-slope-entry.png`, `physics-v2/docks-ramp-mid-descent.png`, `physics-v2/result.json`.
- Previous invisibility complaint is fixed **on staging** https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . Player: **R → D**, 1 uphill, 2 downhill.
- Original P1.5 root still does NOT have slope physics. V2 production engine migration and polished final art remain separate future work. No claims of full Physics V2 completion.

## 2026-11-26 — Fix unintended camera rotation in Physics0

- ROOT CAUSE inspected in `experiments/physics_v2/scripts/demo.gd`:
  `camera.global_position = camera.global_position.lerp(wanted,...)`
  together with `camera.look_at(dynamic_focus)` every frame.
  Translation follows with lag, look target instantly changes, so
  yaw/pitch appear to tilt whole map while moving or climbing/descending.
- NOT an intentional feature; 2.5D orthographic game should keep
  pitch/yaw/roll fixed while camera translates/clamps/follows terrain.
- PRIVATE patch SHA `d5bec34b89c406fe019d17fddfa0829fa7b14bd2`:
  fixed `CAMERA_OFFSET`, initializes camera orientation at reset only,
  removes per-frame `look_at` and exposes camera Euler angles in
  opt-in E2E snapshot.
- PUBLIC E2E patch SHA `e18cf4134e35fbba1774de60ba412ef61522485b`:
  Playwright checks camera rotation pitch/yaw/roll drift <=0.10°
  against initial frame after walk, Moss hill entry/climb, far teleport,
  Docks switch/downhill and far. Requires actual browser run (not
  only code assertion).
- New CI run started #45676396568. Must verify real private game
  source SHA on build, Pages deploy, follow-up Web browser result and
  screenshot; avoid claiming verified until tests PASS.

### Strict import regression found and corrected

First run #45676396568 FAILED in Godot Physics0 strict parser import:
`SCRIPT ERROR: Parse Error: Expected closing "}" after dictionary elements`
in demo.gd. Cause was a missing comma after the camera telemetry
dictionary; no Pages deploy occurred. PRIVATE source fix
`cf634df49426bdd893bdd674492424b4ef9d1121` restored the separator.
This public documentation push is intentional to trigger a new complete
public-runner build against the corrected PRIVATE source. Check new
run for exact game SHA and live Playwright camera lock, not assumed.


## FINAL VERIFIED — Camera no longer tilts the world (2026-11-26)

- PRIVATE game functional source SHA `cf634df49426bdd893bdd674492424b4ef9d1121`.
- PUBLIC Actions run head SHA `5b9fceb5b576b9c2a5910df869214271f62e8916`.
- First public build #45676396568 FAILED on syntax error in new game telemetry dictionary; detected strict Godot import. No Pages deploy. Patched missing comma in `cf634df`, then triggered fresh build.
- Godot import/physics/map/collision/export + Pages run **#45676762869 SUCCESS** on exact game SHA.
- Chromium browser tests **#45677121093 SUCCESS** for legacy P1.5 and new V2. Downloaded `beast-arena-browser-screenshots` and inspected `physics-v2/result.json`:
  - `status=PASS`, `camera_projection_locked=true`.
  - Camera reference pitch `-37.405356819751°`, yaw `0°`, roll `0°`; Playwright assertions guarantee drift <=0.10° at each walk/ramp/teleport/stage switch checkpoint.
  - Moss player climbed `2.137m`, Night Docks descended `2.476m`, flat dx `4.035m`. `page_errors=[]`, `critical_asset_failures=[]`.
- Staging https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ verified. Original P1.5 root remains unchanged.
- **CAMERA TILT REGRESSION CLOSED.** Smoothed camera POSITION is supported, per-frame angle changes are not. Preserve angle telemetry/acceptance tests.
- Evidence: https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45676762869 and https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45677121093


## 2026-11-26 — Visual-first Nekketsu acceptance: camera ANGLE PASS does not equal satisfactory 2.5D LOOK

- User continues to report `vẫn nghiêng` after source `cf634df`; the newly confirmed #45676762869 Godot+Pages SUCCESS and #45677121093 Web Chromium SUCCESS establish camera pitch/yaw/roll rotation drift <=0.10°, **not** satisfactory fixed 2.5D art composition. Existing camera pitch approx -37.405° may be visually too steep. Diagnose visually rather than weakening or removing the angle assertions.
- New plan in PRIVATE `docs/plans/NEKKETSU_VISUAL_FIRST_2026-11-26.md`: V0 camera/presentation → V1 original pixel-art system → V2 original stage → V3 human sprite → V4 human 2v2 → V5 transformation. Original main P1.5 and isolated `/physics-v2/` must remain separate.
- When implementing V0, add public diagnostic build/source ID on both routes, verify deployed PCK source SHA (watch Pages caching), capture idle/flat run/forward-depth run/ramp entry and middle/teleport/map-switch in identical viewport. Compare projected horizontal stage-axis and fixed landmarks before/after: **no world grid/skew rotation, no entire arena tilting as movement changes**, even while real physical Y of ramp varies.
- Review original authored pixel-art reference mockup versus actual browser screenshots: clean horizontal stage composition, 50–56px original fighters (960x540), nearest-neighbor pixel scaling, collision-foot anchors, foreground and obstacle occlusion. Visual status `VISUAL_ACCEPTED` requires human comparison and user approval; do not mark from telemetry alone.
- No proprietary Nekketsu sprite/ROM/map/audio extracted or published. Preserve source SHA, browser screenshot artifacts, JSON state, tests and review checklist in future checkpoint. New design/plan commits are DOCS-ONLY, not a new gameplay build claim.


## 2026-11-26 — V0/V1/V2/V3/V4 source test gate (new, not yet verified)

- PUBLIC workflow `.github/workflows/build.yml` now stamps exact `BeastBuildVersion.SOURCE_SHA`, public pipeline SHA and run ID into the isolated Godot project **before strict import**. Web diagnostics publishes those identifiers only with `?e2e=1`; Playwright requires 40-hex SHA and numeric run ID so stale PCK cannot accidentally pass new visual tests. These identifiers are not secrets.
- New strict Godot test chain in public runner: previous Physics0 native physics/map/obstacle checks, `tests/visual_smoke.gd` (shallow camera, art textures, floor UV, four original palette atlases), `tests/combat_v2_test.gd` (resource-driven 60 Hz startup/active/recovery, XY direction, Y elevation, one hit/window, KO), `tests/combat_scene_smoke.gd` (real 4-actor 2v2 team filtering and HP). No passing run on latest source confirmed.
- Public `ci/playwright_physics_v2.py` now asserts visual style ID, exact build provenance, camera angle and scene no-bob, two distinct original pixel tile/facade themes, 80-frame human sprite atlas, J real attack visualization, camera ramps + physical elevations, and a C-enabled 2v2 AI round with HP loss and screenshot `moss-human-2v2.png`. The Python preflight `ci/validate.sh` compiles both E2E scripts before expensive Godot import.
- Human gameplay remains experimental: G is only guard art; grabs, throws, frame-accurate hurtbox per body part, combo/cancel, terrain-aware AI navigation and multiplayer are NOT complete. V5 beast transformation intentionally deferred until V0–V4 accepted. No game P1.5 production swap.
- **NO NEW CI PASS CLAIM**: latest run IDs/logs/screenshot for these code commits were not available through current GitHub connector (only jobs-by-ID), and public Actions page fetch yielded DisabledError; terminal external network DNS unavailable. The known older successful runs #45676762869/#45677121093 apply ONLY to a previous functional source.
- Next: retrieve newest run ID manually from https://github.com/ngocnhanvo/beast-arena-actions/actions/workflows/build.yml or via future workflow-list tool; inspect strict Godot parser and headless/Pages jobs, then Chromium artifacts. Record exact PRIVATE SHA and new PUBLIC SHA, actual screenshot comparison and performance baseline; do not simply loosen tests to green. Current source milestone details in both repos `docs/checkpoints/2026-11-26-v3-v4-human-combat-source.md`.


### V4 HUD source-only extension — no live claim

- Source V4 now provides four original distinct-color player/ally/enemy HP bars on the fixed 960×540 CanvasLayer. Browser `ci/playwright_physics_v2.py` reads `combat_hp` and `hud_hp_bar_px` and must verify all four rendered widths match actual HP after 2v2 combat. `moss-human-2v2.png` must be inspected for visible contrast and overlapping labels.
- Private source through `da1313e`; public test commit `9167503`. **NOT VERIFIED** in new Godot/Chromium. See latest matching checkpoint in both repos.


### 2026-11-26 — Image material visibly absent despite green Physics0 E2E

- Verified historical/current Web run [#45682788253](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45682788253) PASS on private SHA `9e0a30b`: all physics, camera, teams/HP and asset nodes PASS. However screenshot artifact manually inspected showed **untextured flat green/blue floor**. Exact Moss interior crop `x=.13–.21w, y=.50–.61h` contained *one RGB color* `(100,141,116)` over 8,448 pixels; prior `visible_floor_fraction` (bright fraction .988) gave false confidence.
- Current `ci/playwright_physics_v2.py` additionally samples that same stage-safe crop on BOTH Moss and Docks. `floor_tile_diversity()` reports counts of dominant (>1%) RGB groups and largest-color share. Fail if groups <3 or largest >0.85. It also requires `visual_style_id=v1-visible-pixel-floor-20261126` to prevent stale Pages PCK pass.
- Underlying PRIVATE fix `9360b449` reverses ArrayMesh face winding, texture material disables backface culling and raises art plane; fixes distracting ramps and uses F2 to gate large debug labels. PRIVATE `b84f7994` checks 2-sided material and actual texture presence in Godot.
- Godot import/Pages [#45683483080](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45683483080) SUCCESS. Browser [#45683778280](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45683778280) pending at documentation time. Download artifact and inspect real floor colors/screenshots; a green build without this browser visual test is not a visual PASS.


## 2026-11-26 — New optional F5 pixel-2D stage presentation gate

- Private source `scripts/pixel_projection.gd` and `scripts/pixel_view.gd` are a **visual adapter** to SAME 3D world: screen X=480+(physicalX-focusX)*32, screen Y=339+(Z-focusZ)*6.5-(physicalY-stageDatumY)*31. 3D input/collision/ramp/motor/hitboxes/HP untouched. Existing 3D view remains default until visual acceptance.
- Public `build.yml` added `tests/pixel_projection_smoke.gd` to assert X-horizontal, true physical Y and Z-depth, correct two-map/4-actor link; no fake height is introduced. Public `ci/playwright_physics_v2.py` now presses F5 after traditional physics+2v2 traversal, checks `pixel_projection_mode`, >60 drawn original tiles and at least 2 fighters, screenshots `moss-nes-style-2d-preview.png`, checks visible tile colors, then toggles F5 back to 3D.
- Independently, `pixel_prop_skins=6` asserted on both Moss and Docks; each actual native collider has original pixel-art material (public source `c2b6048`). Build+Pages #45685202832 PASS. Browser #45685557148 and newer F5 builds #45685585437/#45685624341 had not been verified when this note was written.
- Explicit user visual acceptance REQUIRED after viewing screenshots. CI green for 2D mapping cannot by itself establish Nekketsu look and feel. No P1.5 migration or beast form V5 until gates pass. See latest checkpoint in both repos.


## 2026-11-26 — F5 browser result actually verified, next screenshot comparison

- Current PASS for optional physics-backed Pixel2D view: Build/Pages #45685585437 on private `49ca27ea`, Chromium #45685984297. Screenshot/JSON downloaded, `pixel_2d_overlay_pass=true`, 221 tiles, 4 actors, 25 combat hits, original camera still stable. This proves runtime but does NOT approve visuals.
- Visual QA FINDING: screenshot is closer to Nekketsu 2D orientation but sky blank and step/front gaps. Source `40f0cce` adds original parallax temple/harbor skylines plus world-height brick/metal risers, and private unique 80-frame silhouette additions. `ci/playwright_physics_v2.py` public `79f33d5` adds screenshots `moss-nes-style-2d-start.png` and `docks-nes-style-2d-start.png` before combat; keep after-combat F5 screenshot too. Review both maps and actual 3D physics matches.
- New private headless alpha silhouette test `67c1ac8` must be included in a later Godot CI run. Never mark `VISUAL_ACCEPTED` from pixels-per-frame test alone or migrate P1.5. See latest matching checkpoint.


## 2026-11-26 — Fix browser build/script race from verified FAIL
- OBSERVED #45688049122 FAIL `Four authored human portrait badges are missing` while new Test expected four portraits from source `9f27e53` but Page PCK still previous `3f088fc`. Correct source build #45687946574, Chromium #45688376830 PASS after Pages caught up, with visually verified four original portraits and `pixel_direct_url_pass=true`.
- FIX `web-e2e.yml` `3cfa440` pins scripts to `github.event.workflow_run.head_sha`; Physics0 E2E `3b9b9a` requires `first.pipeline_sha==BEAST_EXPECT_PIPELINE_SHA` and `first.build_run_id==BEAST_EXPECT_BUILD_RUN_ID`. Thus false positives/negatives from different build revisions show clear `STALE_PAGES`. #45688176577 build SUCCESS on `3b9b9a`, browser #45688659887 running when documented. A screenshot is still required to visually approve.
- New original pixel art renderer `BeastPixelView` now depth-sorts 3D native obstacle sprites and human body positions together, preserving occlusion with real Z. PRIVATE headless `pixel_projection_smoke.gd` enforces wall-in-front/back order and Public CI must check source after `0911450`. Do not claim PASS based on older #456881.

## 2026-11-26 — Latest actual Web verified 0.5m ramp and round result proof
- Godot+Pages [#45691649914](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45691649914) SUCCESS source `d1a22bae199ba80296e6af850906e95241619f9b` PUBLIC `df8f1ff7ee145bf88f327a05bcadfd6eaa913011`; `tests/pixel_projection_smoke.gd` and the scene `match_scene_smoke.gd` PASS.
- Chromium [#45691975794](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45691975794) SUCCESS with actual screenshot artifact. `result.json` statuses: P1.5 and Physics0 PASS, direct pixel URL same source, Moss start 468 tiles, Docks start 576 tiles (old 234/288), both 4 fighters, no runtime page error. F5 2D surface tessellation now 0.5m along real 3D inclines and unchanged 2m plain spans; screenshots confirm smoother slopes. G guard and 90s round / T reset confirmed from snapshot. SHA and run identity live in `?e2e=1` and F2 UI; display does not scatter developer diagnostics over ordinary play.
- Do not mark artistic approval automatically. Old Web screenshot before/after mosaic assembled locally for human review. Future must measure performance on multiple devices, add level art and full human combat before P1.5 migration/beast form. **PARTIAL**.


## 2026-11-26 — VERIFIED original 8-bit contact feedback on live browser

- **CI/Pages/Web SUCCESS:** [#45693164657](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45693164657), source `4ab090e33e51822cc4639d6165ac8d4319a9be37`, PUBLIC SHA `59a244842d3b45345f892fc7ea66cc1305e8383d`. All Godot strict import, new `hit_effects_smoke.gd`, real 2v2 hit-to-one-FX test, pixel 0.5m real ramps, 60Hz match/G guard, Web+Windows export and Pages deploy PASS.
- **Chromium SUCCESS:** [#45693795373](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45693795373), actual screenshot ZIP `beast-arena-browser-screenshots` downloaded, `physics-v2/result.json.status=PASS`; `pixel_combat_fx_events_pass=true` and real 3D 2v2 hits=20, original pixel render contact events=20. Direct `?pixel=1`, exact source SHA, all 4 fighters, AI/HP, G press/release, 90s round/KO/T restart, headless 0.5m physical ramps and P1.5 existing route PASS. Actual `moss-nes-style-2d-preview.png` looked at: human sprites, 4 portraits, shallow horizontal perspective, fine incline remain legible.
- Art/VFX: original amber damage burst and cyan block burst, 0.20sec finite lifetime, 24 event bounded queue; visual-only `BeastHitEffects` projected from true world XYZ. **Unverified:** browser battle had `pixel_guard_fx_total=0` (no real front block in that particular battle) and screenshot after 2v2 may not contain the transient 0.2sec visual spark. Do NOT claim a real captured cyan-block screenshot or final artwork approval. Model tests for guard event pass; next agent should stage actual guard hit + screenshot.
- **Not complete:** visual user signoff and original fighter animation polishing, map/foreground variety, advanced combo/grab/throw and obstacle-aware AI, robust editor, mobile performance, P1.5 root migration and V5 original beast transformation remain. Use private matching checkpoint as authoritative; do not trigger beast early.

**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — Fix scheduled-cache browser false FAIL; stronger live cyan shield screenshot proof

- **Evidence:** Scheduled public CI #45728104476 SUCCESS but its `Publish Web game to GitHub Pages (PUBLIC)` job SKIPPED (source+Pages successful cache hit). Follow-up browser #45728174303 FAIL after P1.5 PASS, with exact `STALE_PAGES: loaded PCK run 45694618558 instead of triggering build 45728104476`. This was a false E2E deployment assumption, not a gameplay regression; unchanged PCK was not redeployed and cannot carry new run ID.
- **Fix:** `.github/workflows/web-e2e.yml` commit `7dadcfd01c4630d3bbf3166398d15142e368b726`: new `publication-gate` queries GitHub run jobs under read-only `actions:read`; only release E2E when the exact triggering Pages job concluded SUCCESS. If Pages is SKIPPED, downstream `browser-smoke` job is SKIPPED with notice. Missing/failed job status causes gate FAILURE rather than silently asserting PASS. Direct manual browser dispatch stays supported. Existing exact pipeline-SHA/build-run-ID test remains STRICT for real deployments.
- **Verified LIVE success branch:** GitHub build+Pages #45729838736 SUCCESS; new downstream browser #45730089391 SUCCESS. `publication-gate` job log explicitly shows `Pages deployed by triggering run 45729838736`; no test bypass on actual deploy. **Skipped branch NOT YET directly verified**; next scheduled no-change run is its required gate.
- **Pixel art visual QA upgrade:** PRIVATE source `f94dbe484068ad891b1620e306ecc6193d1e1a00` extends truly blocked-hit cyan shield artwork to 0.55s (normal amber contact 0.20s), original brighter shield border/spokes, and a new active-cyan-only diagnostics counter. Godot import/tests, export and Pages #45730152150 SUCCESS, PUBLIC `ci/playwright_physics_v2.py` commit `b62c92265db0fd62afe558d51d96feab4cf32a27` requires at least 40 cyan-looking pixels in actual PNG `moss-cyan-guard-contact.png` while real blocking happens; prior screenshot did NOT actually capture color despite counters.
- **Next:** inspect Chromium #45730411190; check `physics-v2/result.json` and PNG itself, repair from real screenshot/log if FAIL. Do NOT claim cyan art screenshot PASS merely because guard event counter >0 or prior browser PASS. Update private matching checkpoint. This is still visual-first Nekketsu-like original asset prototype, root P1.5 unchanged, V5 not started.

**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — Confirmed four original pixel skyline variants on BOTH stages

- PRIVATE exact source `e1e2c74853f1db1d5408b113062f1eacead115c9`, PUBLIC build source `a20aa6c6090d476e68f072b78d7bc738f8d743fb`. [Godot+Web+Windows+Pages #45730978934](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45730978934) SUCCESS, with strict parser/3D physics/0.5m visual ramps/guards/2v2 hit effects/team rounds all PASS.
- [Chromium E2E #45731247515](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45731247515) SUCCESS, real `publication-gate` + P1.5 + Physics0 tests all PASS, screenshot ZIP downloaded and inspected: `physics-v2/moss-nes-style-2d-start.png` displays original shrine/torii/trees/pagoda (468 tile spans, 4 fighters), `physics-v2/docks-nes-style-2d-start.png` displays original warehouse/crane/tank/container silhouettes (576 tile spans, 4 fighters). Fixed horizon and physical inclines remain; no cloned one-shape skyline. Human-first graphics are still prototype and require user visual review.
- Real cyan blocking and screenshot pixel check continue PASS on the new stages: `real_guard_contact.blocks=1`, `real_guard_contact.visible_cyan_pixels=1662`, HP=97, real 3D contact feedback count matches visual VFX; `round_restart_pass`, direct pixel URL and 2v2 HP PASS.
- The **scheduled SHA-cache no-deploy branch** for `publication-gate` remains to be proven by next natural cached scheduled workflow. Its real deployed build branch already passed #45730089391. Never mislabel #45728174303 stale-run failure as a game rendering defect.
- Next user-visual acceptance, richer original human poses/props/editor, grab/throw/combos and obstacle-aware team AI; benchmark mobile hardware. Keep root P1.5 separate; do not begin V5 beast art until human map gameplay approved.

**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — 64 distinct human poses and physics-speed animation verified in real Web

- EXACT PRIVATE game source built `191842e4948d6f0a5a864a4c2c5815b240b2fd03`; PUBLIC pipeline `156e6d86c2fa7914ef5224dca77e437e73a3dbac`. Godot+Web+Windows+Pages [#45734392214](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45734392214) **SUCCESS** incl. four imported 80-cell original human SVG atlases, 64 changed jump/knockdown/getup/KO cells and strict `visual_smoke.gd` pose geometry gate plus real 60Hz combat, physics, slope, maps, AI, guard/round tests.
- Real Chromium [#45734623244](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45734623244) **SUCCESS**, actual ZIP screenshots + JSON downloaded and inspected: `status=PASS`, `physics_driven_run_art_pass=true` (actual physical vx≈4.2, original running row3), `original_human_jump_pose_pass=true` (row5 at physically airborne Y=0.855m), both Moss 468 and Docks 576 floor spans with 4 fighters, 2v2 hit/HP/AI, fixed camera, T reset and P1.5 legacy route all PASS.
- Test-timing repairs based on actual FAIL: first #45732537827/#45732600754 `ART-10` tried to verify gait before spawned body had landed, private test `82b94b` waits actual Godot contact. Browser #45733022775 prematurely demanded idle at fixed 250ms while real motor retained inertia; script `1198ce3` waits for both true speed<0.20 and displayed idle. Later Chrome pass verifies.
- Intermittent #45733685336 and #45734022726 `visible_cyan_pixels=0` were screenshot timing (0.55-second spark had expired), despite real front blocks and HP. Private capture opt-in `?e2e=1&capture_guard=1` holds only the artwork frame of a genuinely resolved block, keeping combat independent and normal playing duration intact; Godot unit tests verify opt-in semantics. Chrome #45734623244 screenshot now **1501 vivid cyan pixels**, true front block=1, HP=97. Real game without `capture_guard` retains natural VFX duration.
- **UNVERIFIED NEXT visual evidence:** PUBLIC `ci/playwright_physics_v2.py` `a8f49cc` adds *actual F5 horizontal 2D running screenshot* `moss-running-horizontal-pixel-2d.png` after observing older screenshot `moss-running-real-speed.png` was taken in intentionally oblique 3D comparison mode. Public build #45735133772 was running when documented. Confirm Godot+Pages+Chromium and inspect original 2D snapshot before marking screenshot PASS. Keep root P1.5 unchanged.
- User art quality acceptance still OPEN; human grab/throw/combos, editor foreground, obstacle AI, mobile FPS and V5 beast transformation still pending. `PARTIAL` not full game completion.

**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — V4 visual timeline: stale E2E assumption confirmed

- **Actual new combo source built & Pages:** private `0af48c861537b1f8dd1bc6ff7d791a588cf0c62c`, public pipeline `8a151d2ad42968549344ebc2999f163f725a984e`, build+Pages [#45742050996](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45742050996) **SUCCESS**. Godot log explicitly `COMBO V4 PASS`, `VISUAL SPIKE PASS`, both Web+Windows export success.
- **New Chrome failure #45742273520:** P1.5 PASS `dx=210.0` but V2 failed `AssertionError: J did not start the original light attack visual preview`. **Verified cause (source+assertion):** the authoritatively timed physical attack now clears old optional `human_visual_action` preview to avoid stale art past recovery; obsolete E2E was asserting preview string rather than true attack frame/pose. This is a **test expectation mismatch**, not evidence of broken 3D hitbox or map geometry. Do not ignore the failure.
- **Fix PUBLIC** `ci/playwright_physics_v2.py` commit `95281046c042f9ce214aee716590ef8ae59494e5`: require genuine `human_visual_gait == "attack"`, positive physical 60Hz `human_attack_frame`, and original sprite row 7/8. Keep the early-press and pixel screenshot requirements. Test method must not require a deprecated art preview flag.
- **Revalidation target:** [#45742647411](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45742647411) Godot+Pages, then automatically spawned Chromium run matching exact pipeline/source/build IDs. Verify both actual statuses/logs/artifacts before labeling PASS. A separate PRIVATE physical-up/down backdrop skyline fix is underway and needs its OWN later build/visual acceptance.
- **Regression lesson:** A reference implementation's presentation debug field can be deleted/changed while fixed-tick combat stays correct. Read `human_attack_frame` + rendered row, not a display-only preview flag, for strict Web E2E. Human art approval and V5 are still open.

**Trạng thái: PARTIAL — chưa hoàn tất**


## Final V4+flat-skyline pipeline acceptance — PASS (2026-11-26)

- Game functional source `b06e131c955f09e50593d890244e8fbe47b44dc2`, PUBLIC CI commit `441048d2dc92a4c477aa95a985f88c19317ff6c7`.
- [GitHub Actions Godot+Windows+Web export+Pages #45743279673](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45743279673) **SUCCESS**. Verified actual build-job log prints expected private SHA; `VISUAL SPIKE PASS`, `2D VISUAL ADAPTER PASS` including up/down map horizontal skyline `PRES-12`, `COMBO V4 PASS`, `All export checks passed` and `Isolated Physics V2 Web preview exported`.
- [Actual Chromium #45743526820](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45743526820) **SUCCESS**, strict EXPECT pipeline `441048d2`, EXPECT build run `45743279673`; P1.5 PASS dx=220.5, Physics V2 PASS Moss climb=2.12m, Docks descent=2.39m, real ground contact angle>=10deg, dx=11.41m.
- Downloadable screenshot/JSON artifact [ID 15082730310](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45743526820/artifacts/15082730310); actually downloaded ZIP, read `result.json` status `PASS` and visually examined both original `moss-nes-style-2d-start.png`, `docks-nes-style-2d-start.png` before/after 173px fixed skyline correction. Distant facade now horizontal across true slopes, while physical grade remains visible. Both 4 human fighters shown; 468 Moss tiles / 576 Docks tiles; original running sprite and live cyan guard screenshots PASS.
- Earlier `#45742273520` browser FAIL traced to stale `human_visual_action` preview expectation; PUBLIC fix `95281046` now checks physics-timed gait/attack frames, successfully retested Chrome `#45742922283` and final `#45743526820`. No Godot physics/attack tests removed to force a pass.
- **Web preview:** https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1 ; root P1.5 production still separate. This is validated Web tech preview, **NOT** user visual approval of final original NES-quality assets.
- Unfinished: detailed original fighter art fidelity/approved animation and stages, editor ergonomics, environmental props, human grab/throw, AI obstacle avoidance, device perf, main-route migration, V5 original beast. Continue from PRIVATE latest checkpoint before next source change.

**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — Verified after PRES-13 recovery: 64px humans + anchored ground art on real Chromium

- **Exact PRIVATE compiled game:** `7a661ab099cca2b13753614bb456d8413c9d2ffb`; **PUBLIC pipeline:** `100b417a41c42028853506e79cac036604c86db8`.
- [Actual Godot 4.7.2, Web + Windows export, Pages #45745650475](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45745650475) **SUCCESS**: `PRES-13` reverified with Moss 66/Docks 78 world-space floor anchors after 3.0m authored spacing, `PRES-14` requires 64px pixel-view fighter cell; original 60Hz combat, V4 chains/guard, two real 3D ramps and P1.5 regression still pass.
- [Actual published Chromium #45745833887](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45745833887) **SUCCESS**, strict linked build/source. Parsed `physics-v2/result.json` **PASS**: Moss visible 32 original ground details / 468 floor strips, Docks visible 30 / 576; physically uphill +2.19m and downhill -2.50m; F6 Jade Scarf real pixel screenshot comparison `changed_visible_pixels=10894` with same HP/map, true G guard snapshot PASS.
- [Screenshots artifact ID 15082749502](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45745833887/artifacts/15082749502) downloaded; directly inspected actual `moss-jade-scarf-concept.png`: sprite visibly larger/clearer, ground has new small moss tuft/stone accents on actual slope and plains without changing far horizontal skyline or collider silhouettes. User's visual art approval is still **OPEN**; this proves rendered feature not final aesthetic quality.
- First failed run #45745395296 `PRES-13` Moss 57 anchors <60 remains documented; subsequent fix `84a6bd89` not weakened acceptance and full browser pass is proof.
- **New independent SOURCE still UNVERIFIED:** later `jade_concept_atlas.gd` original painted image-generated 80-cell draft and `P` compare mode currently undergoing its OWN strict CI from PRIVATE later HEAD (do not attribute it to #45745833887). Next verify new source, P-mode headless decode and Chromium screenshot before claiming high-detail sprite mode delivered.

**Trạng thái: PARTIAL — chưa hoàn tất**

## 2026-11-26 — Final Paint Jade artwork A/B from ACTUAL Web + Chromium, verified

- **Game exact compiled source**: PRIVATE `4923704a1fa933300ea7e892582aced9733c43ed`; PUBLIC exact pipeline E2E `b862d848a2ebc5c253de0aba523bad2a03757d61`. New private documentation-only commits after source do not affect the deployed PCK.
- **Build+Pages**: [#45746214982](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45746214982) **SUCCESS**, Godot 4.7.2 strict import and all headless P1.5/Physics V2/Pixel View + ART-17/18 (loaded real original WebP image 256×1280, 80 nonblank 64px cells, painted portrait + physics/HP invariant), V4 60Hz combo, slope/obstacle/guard/round, export Web+Windows and deployed Pages.
- **Real Chromium browser test**: [#45746420155](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45746420155) **SUCCESS**, exact pipeline `b862d848...` and build run ID `45746214982` checked against embedded source SHA `4923704a...`; actual `physics-v2/result.json.status=PASS`.
- **Real screenshot artifact [15083925898](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45746420155/artifacts/15083925898)** downloaded and unpacked; images inspected: `physics-v2/moss-nes-style-2d-start.png`, `moss-jade-scarf-concept.png`, `moss-jade-painted-concept.png`, `docks-nes-style-2d-start.png`, `moss-running-horizontal-pixel-2d.png`, and `moss-cyan-guard-contact.png`. Generated truthful 3-way original Web comparison `/mnt/data/beast-arena-jade-three-variants-chromium.png` locally to show owner, **not** third-party NES art.
- **Measured REAL screenshot changes**: Painted Jade P toggle `original_jade_painted_art_comparison.changed_visible_pixels=12369`, vector Jade Scarf F6 toggle `...changed_visible_pixels=10190`. Both tests confirm **same combat_hp and same map**, 4 real fighters, physical Moss up +2.155m, Docks down -2.370m and contact angle >=10°; 468/576 2D ground strips, 32/30 on-screen original floor details; real blocked hit shield `visible_cyan_pixels=1501` with real block=1/HP=97, P1.5 unchanged, original true 2D running/horizontal horizon screenshot pass.
- **User-facing preview**: `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=painted` and `?pixel=1&art=concept`; **P** toggles Painted vs Classic, **F6** toggles vector Scarf vs Classic, **F5** switches 2D/oblique 3D comparison. Prototype visible size 64px source cells; native 3D physics is still sole authority.
- **Visual judgment is NOT user acceptance:** Painted variant has noticeably better original expressive facial/hair silhouette compared with flat SVG placeholder at actual 64px; levels retain blocky placeholder geometry; 80 atlas logical cells are **NOT 80 individually polished keyframes** (some poses mirrored/reused and floor anchors prone/KO need hand-authoring). User pixel-art signoff remains OPEN. Do not mark V5 beast, grab/throw, navigational AI, foreground art or production migration done.
- **Prior actual FAIL and fix preserved:** #45745395296 `PRES-13` FAILED (57 original Moss floor markers below 60), fix `84a6bd8921` => 66 Moss/78 Docks physical anchors, then #45745650475 Pages and #45745833887 Chromium PASS. Continue only from this exact checkpoint.

**Next**: solicit/record user art preference between Classic / Scarf / Painted in real game; refine ONE original approved human silhouette and unique animation loops (walk/run/attack/get-up) at 64px; make foreground/props/stages higher visual fidelity (physical Y respected). Then complete grab/throw, obstacle-aware AI, editor, device FPS, P1.5 parity before V5 original beast transformation.

**Trạng thái: PARTIAL — chưa hoàn tất**

## 2026-11-26 — Approved illustration real PNG A/B visual gate PASS

- PUBLIC pipeline `5ba8919f938b54fae5a1eaaab6b98c3048a7204b` built PRIVATE `03a34e696c1d48fe0910294637bcb98bfa8a59db`. [Build/Pages #45751045283](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45751045283) SUCCESS and [Chromium #45751278124](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45751278124) SUCCESS.
- `ci/playwright_physics_v2.py` takes real A/B canvas captures `moss-nes-style-2d-start.png` and `moss-jade-approved-exact-art.png` after pressing F7; asserts flag, actual 80px atlas cell, same HP/map, >=700 visibly different pixels. Real result: **17,155** changed pixels, all previous P1.5/V2/2v2/guard/slopes tests pass. GitHub Actions screenshot artifact [15085976043](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45751278124/artifacts/15085976043); both comparison images downloaded and visually inspected.
- Learned: a visual-art requirement must be validated against **the exact approved source image** as imported asset and actual rendered game screenshot; do not substitute source-level texture loading, pixel count alone, or AI-generated concept page. Existing maps/roster still stylized blocky by scoped user direction; do not widen feature work until 1-fighter approval.
**Trạng thái: PARTIAL — chưa hoàn tất.**


## 2026-11-26 — approved Jade rear movement screenshot gate: timeout corrected

- PRIVATE code source `2c0bc2fc9612538c5a25779aaf802fb2e23be44f` adds presentation-only original-art rear motion repair; front/side 60 cells unchanged and knockout uses the original artist's fallen pose rather than a standing back silhouette. Godot validates via ART-22, physical Y/HP/60Hz combat still independently tested.
- First PUBLIC build+Pages [#45752674592](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45752674592) **PASS**; real Chromium [#45752879529](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45752879529) **FAIL**, not a silently skipped test. Source+published build matches. Artifact `15086207295` contains `moss-jade-approved-rear-motion.png` **successfully captured** and displays visually distinct rear-running original sprite with stage visible. Old P1.5 browser smoke independently PASS.
- Verified failing statement: NEW fixture required speed <0.2 AND `visual_gait=idle` within 6s AFTER releasing W on an actual slippery/uphill 3D map. This condition is NOT part of the new rear animation acceptance and can be delayed by authentic physics. Failure in Playwright `Page.wait_for_function: Timeout 6000ms exceeded`, not Godot import or asset decoding. Do not disable existing physical-stop or slope tests lower in the script.
- Public test fix `fbe363e73c26112625c12ee9919654ba35ff14f5`: keep hard assertion while W held (`human_sprite_frame %4 ==3`, walk/run gait, 80px atlas, screenshot captured), release W + short UI settle, no false strict idle requirement; old physical movement/stop/slope tests remain. Build+Pages retest [#45753203544](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45753203544) **SUCCESS**; spawned Chromium [#45753426222](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45753426222) QUEUED at this note — its result must be checked before Browser PASS claim.
- Takeaway: tests should prove WHAT the new feature promises and must not impose an unrelated instant motor-stop contract on real slope contact. Compare genuine PNG screenshot to approved user illustration separately from headless state checks. Keep `result.json` and exact source SHA/build/run identity in acceptance.

**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — FINAL VERIFIED Jade rear gait release (SUCCESS, art still not approved)

- **Authoritative functional asset implementation:** `jade_approved_motion.gd` `3ef221bd`; `demo.gd` `111e900d`, `visual_smoke.gd` ART-22 `2c0bc2fc`. Original expressive user-approved `jade_approved_80f.png` source is UNMODIFIED; 60 non-rear cells byte-identical, four rear walk/run rows animated, rear prone/KO no longer upright. Provisional rear attack rows still use same artist's side silhouettes. Physics, speed, hitboxes, HP and original stages untouched.
- **EXACT PRIVATE GAME compiled into verified release:** `3ba321b322918288dbe6baa402184319747fcba8` (docs-only changes after functional source); **PUBLIC CI commit** `1442efc120d3de898da11588e0e86571769ce4d5`.
- **FINAL strict Godot, Web, Windows export and GitHub Pages:** [#45753711701](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45753711701) **PASS**; actual log contains `APPROVED JADE ART PASS: source-preserved 80 PNG cells, fixed rear gait/KO, unchanged 3D foot and HP`, `VISUAL SPIKE PASS`, `2D VISUAL ADAPTER PASS`, `COMBO V4 PASS`, `All export checks passed`.
- **FINAL REAL Chromium** [#45753939789](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45753939789) **PASS**, strict EXPECT pipeline `1442efc1`, EXPECT build ID `45753711701`. Browser log `PASS P1.5 ... dx=210.0`; `Physics V2 Web PASS: climb=2.08m, descent=2.41m, actual contact angles >=10deg, dx=8.84m`. Real downloaded [screenshot/report artifact 15086424989](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45753939789/artifacts/15086424989). `physics-v2/result.json.status=PASS`; `user_approved_jade_rear_motion={active:true,direction:3,pose_row:4,gait:"run"}`; approved F7 80px changes 16061 actual canvas pixels with identical HP and map; 4 fighters, 32 visible Moss and 30 Docks ground details. Actual real WebGL image `physics-v2/moss-jade-approved-rear-motion.png` personally inspected.
- **Do not hide earlier FAILS.** First Chrome #45752879529 failed AFTER capturing rear-run image because added test improperly waited for instantaneous idle speed on actual physics slope; fixed public E2E `fbe363e7`. Second Chrome #45753426222 failed old D-run gate (`gait=airborne`, vx=4.2) due to NEW W sprite fixture contaminating real Z/airborne state before the next test; fixed `1442efc1` by invoking existing T reset after W capture. Third Chrome #45753939789 PASS. No physics tests weakened/removed.
- **Critical visual honesty:** In actual Chromium screenshot, Jade's leg silhouettes extend sideways, making W rear-running look unusually horizontal/airborne. The repair eliminates frozen rear gait but is NOT final visually acceptable authored back-running animation. The original user art reference is approved direction, not final animation signoff. Next artist task MUST draw authentic rear 4+ walk and run keyframes from the approved style, full-body punch contact rows 8/10 at consistent size and back-facing take-hit/knockdown/get-up, not crop/translate/fake source silhouettes. Then test real Web PNGs. Do NOT prematurely polish map/beast/AI before user sees finished one fighter.
- **Play:** https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1&art=approved ; hold W for rear movement, F7 toggles original classic vs approved illustration, F5 toggles 2D/3D. Root P1.5 unchanged.

**Trạng thái: PARTIAL — chưa hoàn tất**


### 2026-11-26 — WJK browser false-negative due Web test running off stage (verified)
- **Corrected-source Godot/Pages** [#45757152728](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45757152728) **PASS** compiling PRIVATE `52751133013b5ad1cc59fb4163c73f8cf101180c`. Real logs show `APPROVED JADE WJK PASS`, full-body J/K on all four facings, four unique run phases, preserved physics/combat/slopes, exports Web/Windows and Pages success.
- Auto browser [#45757397328](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45757397328) **FAIL** with `AssertionError: W did not alternate four distance-driven foot phases: {'phases': [], 'distance': 11.90024876594544}`. P1.5 browser PASS; `moss-jade-approved-rear-motion.png` screenshot successfully captured, user-facing hand-painted Jade rendering visible. **Verified cause:** new Python→Chromium 22× `snap(page)` loop held W long enough that the real 3D player crossed almost 12m and fell off the compact stage, so later snapshots all showed `gait=airborne`. This is test-induced extra motion, not evidence of no alternating steps.
- **E2E-only fix PUBLIC `a49a07a549b3eb09215a52a5e65bcefce0800c9b`:** collect every `requestAnimationFrame` debug state inside Chromium during an 850ms W stride, then require ALL 4 phases, correct rear facing and >0.9m native `move_and_slide()` ground distance. No physics speed, hitbox, gravity, stage bounds or source art changed. New public [Godot/Pages #45757669329](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45757669329) **PASS**; automatically triggered Chromium [#45757885478](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45757885478) **QUEUED** when checkpoint written, must be checked before Browser PASS claim.
- First two earlier failures remain documented: corrupt PNG IDAT base64 corrected with matched Git blob hash, and ART-24 fixture tried running before landing. All addressed with strict tests retained.
**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — Sprite pivot drift / genuine physical air separation

- **Source screenshot user `image(7).png` confirmed visible Jade boots off ground** on Pixel 2D Moss. Review of original PNG cell bounds verified root art problem: approved idle bottom opaque y=76 of 80 (3px transparent), W rear run bottom ~70–71 (8–9px transparent), side run bottom ~69–70 (9–10px), J/K rear bottom y=76 (3px). The previous `Sprite3D` and `PixelView` both placed the opaque artwork as if every PNG cell were filled to y=79. Changing W/J/K poses therefore changed visible foot height even with identical physical actor world Y.
- **Engine source fixes** `sprite_foot_anchor.gd` (`80a24b8`), `character.gd` (`0fa8f8b`), `pixel_view.gd` (`1b1952d`): lazy cached per-frame opacity scanning, shared physical shoe-pivot from Sprite3D.offset.y=-padding (Godot Y UP) and PixelView rect +padding (Canvas Y DOWN). Grounded only; jumps continue using actual native CharacterBody3D height. No world/collider, HP, attack timing, slope or AI changes.
- `visual_smoke.gd` ART-25 (`0d493fd`) checks 40 grounded cells four directions incl W J/K guard/idle, both viewport pivot equations, actual Sprite3D offset on 4 physical W gait phases. `demo.gd` (`a55620b`) exports opt-in telemetry `human_sprite_foot_padding_px`, `human_sprite_offset_y`, `human_sprite_grounded`, `human_physical_ground_clearance_m`; public E2E `aed5cda` resets genuine grounded spawn before sampling W 4 distance-driven phases and asserts real native floor contact + screen pivot, takes real W/J/K screenshots.
- **Standard authoring tools:** Aseprite/LibreSprite slice foot pivot+animation tag + PNG/JSON export; native Godot SpriteFrames/AnimatedSprite3D for eventual authored animation migration, no unknown addon installed. Doc `docs/art/SPRITE_ATLAS_PIPELINE_STANDARD.md`; private `tools/sprite_atlas_audit.py` flags transparent shoe padding and exports JSON for artists before any import.
- **Observed prior FAIL** real Chromium [#45757885478](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45757885478): zero grounded W samples after extended test; must distinguish true airborne actor from PNG gap. Do not hide the failure or clamp sprites down while physically airborne.
- **NEW Godot+Web/Windows+Pages #45758868968 PASS** compiling exact private gameplay `a55620bee0a78f6b974c897b4abe7d703d6b5fff` with public `aed5cda897a32ce64ae46efc1c37d7608347aa54`; actual log `APPROVED JADE WJK PASS: 4 foot phases + shared physical shoe pivots for W/J/K...`, `VISUAL SPIKE PASS`, `2D VISUAL ADAPTER PASS`, `COMBO V4 PASS`, exports PASS. Automatic strict Chromium [#45759115851](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45759115851) underway at time of this log; cannot claim Browser PASS yet.
- **NEXT:** inspect real Chromium status, debug sample array (including physical grounded/world height) and actual W/J/K screenshots. If W transitions into genuine airborne without jump, investigate native motor floor contact separately (see unified 3D physics ADR); correct that physical issue instead of hiding it in art. If screenshots only show planted feet, update both checkpoints with exact art/physics verification and seek user approval.
- **Remaining roadmap:** full editable Aseprite source with authored 4-direction clips, map art quality, editor, AI, grabs, V5 beast and P1.5 migration not complete. This update is a scoped repair, not an assertion of a finished game.

**Trạng thái: PARTIAL — chưa hoàn tất**
