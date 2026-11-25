# Thiết lập GitHub Actions

## Secret đọc code (bắt buộc)

GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token.

Chọn **Only select repositories**: `ngocnhanvo/beast-arena`, và **Contents: Read-only**. Metadata read được cấp mặc định.

Trong **repo Public** `beast-arena-actions`, mở Settings → Secrets and variables → Actions → New repository secret và tạo `BEAST_ARENA_READ_TOKEN` chứa token vừa tạo.

Sau đó vào [Actions workflow](https://github.com/ngocnhanvo/beast-arena-actions/actions/workflows/build.yml) và chọn **Run workflow** (nhánh main) để build ngay. Ngoài ra Public Actions tự kiểm tra SHA của `beast-arena/main` mỗi giờ (phút 17 UTC) và chỉ build lại nếu chưa có marker build thành công cho SHA đó. Chỉ cache SHA, không cache source Private.

## Secret upload riêng vào Private (khuyến nghị)

Tạo một fine-grained token **riêng biệt** chỉ có quyền `Contents: Read and write` trên private `beast-arena`; lưu trong secret `BEAST_ARENA_RELEASE_TOKEN` của repo Public.

Workflow tạo một prerelease trong private repo theo tag `ci-<12 ký tự commit>`, upload ZIP Web + Windows; tải tại [Private releases](https://github.com/ngocnhanvo/beast-arena/releases). Không đặt token vào source hoặc chat.

Nếu không tạo token release, bản build được kiểm tra nhưng không có file tải về mặc định.

## Xuất artifact Public khi chủ động phát hành

Chỉ bật tùy chọn `publish_public_artifacts` nếu chấp nhận người khác tải binary từ repo Public. Godot export có thể chứa tài nguyên và mã script trong .pck.

## Vòng lặp phát triển

Push code vào private `beast-arena/main`; Public Actions tự kiểm tra mỗi giờ và build lại khi SHA thay đổi. Có thể kích hoạt workflow thủ công để build ngay. Public push chỉ chạy kiểm tra cấu hình; mọi build nặng đều ở repo Public, không cần workflow trên repo Private.
