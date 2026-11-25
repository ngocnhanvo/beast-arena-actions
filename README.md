# Beast Arena Actions (Public)

**AI / phiên chat mới: đọc [START_HERE](docs/START_HERE.md), [AGENTS.md](AGENTS.md) và [CI_PLAYWRIGHT_RUNBOOK](docs/CI_PLAYWRIGHT_RUNBOOK.md) trước khi sửa CI.** Trạng thái browser test có thể khác trạng thái Pages deploy.

This public repository runs Godot 4.7.2 tests and exports for the private project [beast-arena](https://github.com/ngocnhanvo/beast-arena).

- Push to this repository runs **token-free CI preflight**, then builds/tests the private Godot source on a PUBLIC runner when the read-only token is available, and publishes Pages.
- **Hourly scheduled check** on the PUBLIC repository reads the private `main` commit and rebuilds if the source SHA is new OR a successful Pages marker is missing (cache stores SHA only). No private-repository Actions minutes are used.
- Manual `workflow_dispatch` can force a build immediately after checking out private `main`.
- Exports: Web and Windows. Private releases are optional; public artifacts are off by default.
- **No build workflow runs in the private repository.**

## Chơi online qua GitHub Pages

Địa chỉ GitHub Pages đã triển khai thành công (ví dụ run #45652585969): https://ngocnhanvo.github.io/beast-arena-actions/

Bản Web **công khai**, có thể bị trích xuất tài nguyên. Chủ dự án đã phê duyệt xuất bản Web PUBLIC ngày 25/11/2026. Workflow tự triển khai khi repo Public push và kiểm tra lại theo lịch; chạy thủ công vẫn cần chọn deploy_pages=true. Xem [hướng dẫn](docs/SETUP.md).

## Setup

1. Create a *fine-grained* Personal Access Token with access to **only** `ngocnhanvo/beast-arena`, permission **Contents: Read**.
2. Add the PAT as `BEAST_ARENA_READ_TOKEN` in **this public repository's** Settings → Secrets and variables → Actions.
3. Go to [Build workflow](https://github.com/ngocnhanvo/beast-arena-actions/actions/workflows/build.yml), choose **Run workflow** to build now. The hourly public schedule then checks for new private commits automatically.
4. Optional private downloads: create a separate Contents Read/Write PAT for `beast-arena`, save as `BEAST_ARENA_RELEASE_TOKEN`. Builds are saved under the private repo's Releases.
5. Alternatively choose `publish_public_artifacts=true` manually **only if you intend to publish the exported binaries and embedded game data**.

See [detailed setup](docs/SETUP.md) and [security model](docs/SECURITY.md). Never add PATs to code, workflow YAML or conversation.
