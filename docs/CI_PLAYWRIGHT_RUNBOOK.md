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
