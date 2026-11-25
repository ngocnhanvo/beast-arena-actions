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

## Chơi trực tiếp trên GitHub Pages

Địa chỉ dự kiến (chỉ hoạt động sau khi Pages được bật và triển khai thành công): https://ngocnhanvo.github.io/beast-arena-actions/

**Cần chủ repository bật Pages:** https://github.com/ngocnhanvo/beast-arena-actions/settings/pages → **Build and deployment → Source → GitHub Actions**.

Sau đó vào https://github.com/ngocnhanvo/beast-arena-actions/actions/workflows/build.yml → **Run workflow** → chọn `deploy_pages = true`. Workflow chạy trên public runner, đóng gói Web và đưa duy nhất `game/build/web` lên Pages.

Muốn mỗi bản build mới được tự động cập nhật trang, tạo Actions **repository variable** `AUTO_DEPLOY_PAGES=true` trong repo Public. Khi chưa có variable, workflow KHÔNG xuất bản Web ra Internet tự động.

**Cảnh báo:** Web build công khai, Godot `index.pck` có thể chứa và bị trích xuất script, tài nguyên và hình ảnh. Source Git vẫn Private, nhưng xuất bản Web KHÔNG đồng nghĩa giữ nội dung game bí mật. Không để token, dữ liệu riêng tư hoặc tài nguyên có bản quyền chưa được phép trong Web build.

Cấu hình hiện tại dùng WebGL2 Compatibility, Web export single-thread (không yêu cầu custom COOP/COEP headers). Điều khiển vẫn ưu tiên bàn phím PC; touch controls sẽ được phát triển sau.
