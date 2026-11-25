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
