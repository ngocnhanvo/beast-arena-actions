# Beast Arena Actions — hướng dẫn AI/CI agent

TRƯỚC KHI THAY ĐỔI WORKFLOW:
1. Đọc docs/START_HERE.md và docs/CI_PLAYWRIGHT_RUNBOOK.md.
2. Đọc checkpoint mới nhất dưới docs/checkpoints/; đồng thời đọc docs/SETUP.md, SECURITY.md và WEB_E2E.md.
3. Đọc .github/workflows/build.yml, .github/workflows/web-e2e.yml, ci/playwright_smoke.py và helper scripts.
4. Kiểm tra main HEAD + GitHub Actions run/log gần nhất, Pages URL, Private Release; đối chiếu repo game PRIVATE/docs/START_HERE.md, checkpoint mới nhất.
5. Chỉ sửa phần đúng scope, commit/push đúng repo; khi lỗi Github API phải kiểm tra HEAD/path trước retry.
6. Ghi vào runbook/engineering log + checkpoint: triệu chứng, verified/hypothesis, run/job URL, commit, fix và kết quả.

QUY TẮC:
- Repo này PUBLIC; không đưa raw source PRIVATE, token, secrets, dữ liệu riêng tư, GitHub PAT vào commit/log/artifact.
- Game source ở ngocnhanvo/beast-arena (PRIVATE); build, Pages, Playwright ở đây (PUBLIC).
- KHÔNG suy ra game E2E PASS từ build PASS hay Pages deploy PASS.
- Các test chỉ gửi phím chưa chứng minh hành động xảy ra; gameplay cần trạng thái/screenshot.
- Nếu sửa workflow: cần check YAML, preflight và run thực tế. Không chỉ tạo workflow rồi kết luận đã chạy.
- Nếu asset upload/release gặp HTTP 500: phân biệt lỗi GitHub external, dùng retry idempotent, không loop vô hạn.
- Pages là PUBLIC đã được chủ repo đồng ý; PCK chứa scripts/assets export có thể bị trích xuất.
- Không sửa source ở repo Public và không chạy test build nặng trong Private.

- **2026-11-26 Physics V2 gate:** PRIVATE game now has
  `docs/architecture/PHYSICS_FOUNDATION_V2.md`,
  `docs/decisions/ADR_0002_UNIFIED_3D_PHYSICS.md` (PROPOSED) and
  `docs/testing/PHYSICS_V2_ACCEPTANCE_MATRIX.md`. Before creating
  new workflows for slope/3D gameplay, read these docs plus the newest
  Private checkpoint. No unapproved swap of public Pages main build.
