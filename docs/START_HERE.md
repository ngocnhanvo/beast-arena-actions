# START HERE — Beast Arena Actions Public

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
