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
