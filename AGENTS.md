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

- **Physics V2 reuse-first (2026-11-26):** Trước khi build/đưa controller
  bên thứ ba vào Public pipeline, đọc PRIVATE
  `docs/architecture/OPEN_SOURCE_COMPONENT_AUDIT.md` và checkpoint
  `2026-11-26-physics-v2-oss-audit.md`.
  Chỉ lấy code có license/pin commit, không lấy asset CC-BY-NC-SA;
  cần thử Web Compatibility, không đè P1.5 Pages.

- Physics0 hiện có staging riêng `/physics-v2/`. Khi kiểm thử Web
  cần Godot state + Playwright hình ảnh pixel (map nền không đen).
  Lỗi GitHub Pages 503 tạm thời phải phân loại với lỗi không phục hồi;
  đừng lờ lỗi rendering khi movement vẫn hoạt động.
- Native Map Editor của Godot GridMap/CSG đã có test riêng, giữ Private
  nguồn và tài nguyên authored scenes; đọc checkpoint mới nhất trước khi
  triển khai hoặc gỡ các bước smoke.

- **Slope visual acceptance fix 2026-11-26:** never claim an incline visible just because PhysicsServer normals/data pass. The Web E2E must visibly traverse each incline using `R` then `D`, capture slope-entry and mid-traversal screenshots, verify +/- physical Y >=1.2m and floor angle >=10deg. See latest `docs/checkpoints/2026-11-26-visible-slopes.md` and PRIVATE `VISIBLE_SLOPE_ACCEPTANCE.md`.

- **AUTOCHECK MODE (owner 2026-11-26):** `autocheck: false` means do not autonomously iterate on visual-art signoff or pronounce the sprite aesthetically accepted. Build/publish only the scoped preview and let the user check real frames themselves. `autocheck: true` authorizes independent quality testing/repair loops with evidence. Always separate technical CI status from user's artistic judgment.

- **Animation source quality gate (2026-11-26):** Owner explicitly rejected current W/S Jade cut/paste arms/legs. Technical Godot/Chromium PASS is NOT visual PASS. New Public pipeline audits private editable .ase/.aseprite + tagged source with `PENDING_ART` (honest), never pretends sprite pixel hashes mean natural animation. Do not add autonomous style iterations while `autocheck: false`; see `docs/checkpoints/2026-11-26-zzzzzzzzzzzzzz-animation-v2-root-cause.md`.

- **Arcade V2 staged contract (2026-11-26):** `?controls=v2` (only) chooses 10 named clip intents, W/S both front-looking, A+A/D+D real sprint, F punch/G kick/F+G held chord jump/H guard. Legacy input remains default. PUBLIC browser `ci/playwright_arcade_v2.py` tests real 60Hz motor/attack inputs and exact deployed SHA; DO NOT label import-tag unit tests or browser green as owner-approved sprite animation. PRIVATE source-art audit PENDING_ART until ten editable full-body 80px clips. See `docs/checkpoints/2026-11-26-zzzzzzzzzzzzzzz-arcade-v2-ten-clips.md`.

- **Reusable guard fighter profile CI gate (2026-11-26):** Don't hardcode per-fighter atlas rows in pipeline. Public `ci/check_guard_profiles.py` validates PRIVATE `art/fighters/animation_profiles.json` and Web include_filter, build runs PRIVATE `tests/guard_animation_profiles_smoke.gd`, browser `ci/playwright_arcade_v2.py` verifies 4 guard profiles and actual motor/combat with exact SHA/run. Preserve separation **technical PASS vs PENDING_ART**; user `autocheck:false` decides visible guard-fist quality. Proven build #45791697419 and Chromium #45792314363 PASS, screenshots artifact #15103546473. Read latest guard reusable checkpoint.
2026-11-26 owner instruction: ALWAYS use one user-facing link https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ for Jade visual preview. No separate Pages paths or parameterized owner links. New six-frame 3/4 fighter source is a partial unapproved clip, technical CI/browser green is not artistic acceptance. Read latest checkpoint.


- **2026-11-26 REUSED 8-DIRECTION JADE GUARD WALK:** User accepts W/S compact shuffling guard and wants the SAME pose for A,D and all four diagonals. PUBLIC Chromium ci/playwright_jade_three_quarter.py checks all eight physical inputs (including mixed X/Z), correct semantic tags, reused W/S 6×80px source, left whole-body horizontal flip and 70px size parity. No fake per-direction art, no physical movement hacks. Only owner URL `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/`; `autocheck:false` means no autonomous art signoff. Build/Pages #45815352430 PASS; check real browser #45815615697. See latest eight-direction checkpoint.

- **2026-11-26 Jade pose-cadence parity:** Owner wants A/D and diagonals to step a little slower than W/S. Preserve physical 4.2m/s+diagonal normalization and real 70px sprite scale; only shared review pose distance W/S=0.30m, A/D=0.38m, diagonals=0.35m. Public browser test must validate all eight visual strides on SAME canonical /physics-v2/ Pages, not a test-only preview. #45819228268 Pages PASS; exact #45819571675 Chromium pending final signoff. Owner autocheck:false, no art VISUAL_ACCEPTED.

- **2026-11-26 owner idle/run/strike visibility:** Original front idle=[0] static, front punch sprites are idle copies, kick heavy-punch alias; F/G control PASS does NOT equal action art. Provisional 2s 3.5% grounded inhale and real sprint six-cel W/S guard reuse now present (source 07d5df; build #45823598975 PASS, browser #45823930933 still pending). Source-authored original 4+ idle, 8+ run, 4+ punch and 5+ independent kick are still PENDING_ART. Only /physics-v2/ game URL and manual owner autocheck:false acceptance. Read latest checkpoint.

- **2026-11-26 six native Jade run poses:** owner wants reference-like full body 6-phase running integrated into game, NEVER an unrelated generated drawing. Actual original Jade source atlas has left/right 80px complete-body poses rows [1,3,4,5,19,2], left col1/right col2, 70px normalized body/foot pivot; per-fighter `run_review` manifest and generic runtime, real A+A/D+D, no limb compositing. Public Playwright verifies both real sprints and retains 8 walking directions on ONLY /physics-v2/ URL. First CI #45827624972 failed unsupported test-only hash API; corrected; #45827898517 Godot+Pages PASS; final #45828107215/#45828220564 needs terminal proof. Artistic signoff autocheck:false, strict final 8-tag run original remains PENDING_ART.

- **2026-11-26 OWNER NEW JADE 6-FRAME RUN ACTUAL GAME:** Native 480×160 transparent owner-design, full-body right frames0..5 and left whole-body mirrors6..11, 80px editable .ase, profile-driven selection, stable70px body and original W/S/A/D walks. Godot/Pages #45837312371 PASS; pinned real LibreSprite #45837312555 attempt2 PASS. Browser test must prove ALL six live phases under real A+A/D+D in ≤850ms, not hold key against a real wall while falsely concluding animation failure. PUBLIC ddcd9d8 fix, build #45839072298 pending exact browser. Only /physics-v2/ URL and owner autocheck:false art signoff. See newest owner-six checkpoint.


- **2026-11-28 v6 real-game Web staging precedent:** separate source canvas Playwright from the actual Godot Web PCK + CharacterBody3D E2E. After pinned source test+official LibreSprite native reexport and Godot import, run real Physics V2 motor smoke and then opt-in isolated **transient** Web export using the real `clearline_web_staging.tscn`; verify Chromium keys, actual motor X/velocity, drawn 24-sample source atlas and braking, and never publish PRIVATE assets in PUBLIC artifacts/Pages. Fresh runner must `godot --headless --editor --import --quit` before typed SceneTree tests. Web export must regenerate deleted transient atlas/JSON and inject the exact verified JSON + preloaded Texture2D in TEMP staging script, since FileAccess/raw PNG isn't reliable in PCK. Terminal exact [Actions #46056819234](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46056819234) SUCCESS, PUBLIC tested workflow SHA `9334486c9a907842bfff16c4bcc662e32f12cb34`, PRIVATE source `4ad0ddcbcf1ec01b97a7b54ecafbb07ee612e353`. Staging E2E PASS does not mint owner art approval, original six cels still not full 8+ production clip, no merge/Pages. Check paired checkpoints.
