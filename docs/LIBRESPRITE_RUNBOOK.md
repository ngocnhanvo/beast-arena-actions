> 2026-11-26 FINAL: New 3/4 Jade original six-cel art/drafts candidate is verified with REAL LibreSprite #45804294005 and published canonical Physics V2 by #45804293992. Real Chromium #45804607930 PASS on same Pages document and visible S animation in 2D, screenshot artifact #15109780115. One link for owner ONLY: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/. 9 clips PENDING_ART; manual owner signoff still required.

2026-11-26 UPDATE: Private candidate art/drafts/jade_guard_34_walk_down.aseprite and PNG/foot sidecar supersede the rejected face-on Jade candidate in the generic candidates.json manifest. This source must pass the real pinned LibreSprite batch workflow before claiming source technical PASS. The ONLY user-facing live preview is https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/; no alternate path. Owner artwork review pending, nine other clips still missing.

> **Current verified art status (2026-11-26):** A real six-frame Jade original AI-assisted candidate .aseprite source has NOW been committed to the PRIVATE art/drafts folder with tagged PNG, provisional foot pivots and owner-review PNG. The PUBLIC LibreSprite workflow tests it via PRIVATE generic manifest reader; [#45800285146](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45800285146) SUCCESS on actual CLI and pixel identity. The earlier chat-only draft described below remains historical; the new committed draft does not complete the 10-clip fighter library. Strict tag/atlas/pivot coverage with eight negative regression cases and Godot/Pages #45800285101 both PASS. The draft is not in Pages or the game; full source is PENDING_ART and autocheck:false means human visual review.

# Beast Arena LibreSprite 1.3 — CI operator and privacy runbook (2026-11-26)

## Real deployment and verified binary
- **Official upstream:** https://github.com/LibreSprite/LibreSprite/releases/tag/v1.3
- **Linux file:** `libresprite-v1.3-linux-x86_64.AppImage`, size 98,089,464 bytes
- **Trusted upstream SHA-256:** `fd90bddda8135fe00f4a9a9c8c9ebd48f9b07e8782ab269be5c9efb1a851af30` (GitHub official release API). Do not replace with `latest` or an unverified mirror.
- **Installed by:** `ci/setup_libresprite.sh`, downloads with retries, verifies SHA-256 and extracts AppImage with `--appimage-extract` (no FUSE or interactive desktop); wrapper uses `SDL_VIDEODRIVER=dummy`. Binary is transient in `RUNNER_TEMP`, not committed, never forwarded to users.
- **Workflow:** `.github/workflows/libresprite-art.yml`, job `install-and-validate`. Actual `libresprite --version` prints `LibreSprite 1.3`.
- **Security:** PUBLIC repo holds ONLY pipeline scripts and numeric metadata test pixels. PRIVATE repo is checked out with `actions/checkout`, `persist-credentials:false` and `BEAST_ARENA_READ_TOKEN`; never print token or attach PRIVATE art to public Actions artifacts. Workflow does NOT deploy Web or mutate the private repository.

## Verified real integration tests
1. `python3 ci/libresprite_roundtrip_smoke.py` generates a disposable **original-test-only** native 80x80 4-frame layered ASE, opens it with the ACTUAL LibreSprite binary, exports `--format json-array` PNG metadata and checks 4 original RGBA pixels, frame dimensions, frame durations and tag name.
2. `python3 ci/libresprite_full_export_smoke.py --game private-game --binary libresprite` generates a disposable **58-frame** editable source with **all ten** fighter guard tags and a per-frame foot source sidecar. Calls PRIVATE `tools/libresprite_export.py` as implemented, then validates real exported PNG **4640×80 RGBA8**, full tagged JSON and 58 explicit foot-anchor keys. Test drawings are NOT Jade, not shipped and not `VISUAL_ACCEPTED`.
3. `python3 private-game/tools/animation_source_audit.py` remains `PENDING_ART` until the actual Jade original editable full-body guard source is created. The CI may SUCCESS while `PENDING_ART` is present: this means tool infrastructure PASS, not creative quality PASS.

## Foot pivot interoperability fix
Official LibreSprite v1.3 supports `-b --list-tags --sheet-type horizontal <source>.ase --sheet output.png --data output.json --format json-array`. Do **not** use legacy `--list-slices`; LibreSprite 1.3 is missing guaranteed newer Aseprite slice metadata.

Source pivot must be independently authored and checked at 80px resolution in a sibling `<name>.foot.json`:
```json
{
  "schema_version": 1,
  "source_frame_count": 2,
  "foot_pivots": [
    {"frame": 0, "x": 40, "y": 76},
    {"frame": 1, "x": 39, "y": 77}
  ]
}
```
Each original frame requires its own explicit key. The private exporter merges these into `meta.slices=[{name:"foot_anchor",keys:[...]}]` after LibreSprite, without moving/cropping any pixels, and runs strict existing native 80px PNG/source/tag validator. It never fabricates unpainted body poses. These example pivots are for schema demonstration, NOT Jade ground truth.

## Private authoring and adding fighters
- Private path: `experiments/physics_v2/art/source/<fighter>.aseprite` and `<fighter>.foot.json`.
- Profile: `experiments/physics_v2/art/fighters/animation_profiles.json`. Ten tags: idle_guard_front, walk_up_guard_front, walk_down_guard_front, walk_left_guard, walk_right_guard, run_left_guard, run_right_guard, punch_front, kick_front, jump_front; minimum original frames 4/6/6/6/6/8/8/4/5/5. Source .aseprite is **80×80 RGBA8 per frame**, manually redrawn FULL BODY with high-guard arms for each idle/walk/run frame, not cropped limbs, 40px upscaling or row/column guessing.
- Export:
```sh
python3 tools/libresprite_export.py --fighter jade_human \
  --source experiments/physics_v2/art/source/jade_human.aseprite \
  --foot experiments/physics_v2/art/source/jade_human.foot.json
```
- For all fighters, change only profile source names, art and sidecar. Game motor/selection is shared; no Jade-only code path is required.
- No release to owner as **complete animation** until real visual loops are reviewed with `autocheck:false`.

## Actual runs and failure history
- [Art toolchain #45795749806](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45795749806) SUCCESS for first real 4-frame .ase roundtrip.
- [#45796083150](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45796083150) FAIL: test fixture encoded reserved ASE bytes as literal `\\0` rather than NUL; fixed.
- [#45796479653](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45796479653) FAIL: same malformed tag fixture produced invalid UTF-8 metadata; fixed actual binary header and reserved bytes, never muted an art validator.
- [#45796842259](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45796842259) **SUCCESS**, proves 4-frame actual CLI roundtrip + full **58-frame private exporter** + all 10 tags/pivots with original public test pixels.
- [#45797269317](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45797269317) **SUCCESS**, same tests with secure private `actions/checkout` rather than PAT in git command, PRIVATE SHA `fda05cf6698338ab7ecbee2bcdf23ff6b2bc01d7`; true SOURCE status `PENDING_ART`. Later PRIVATE manifest/old exporter synchronization commits need new exact source verification after this run.

**Trạng thái: PARTIAL — chưa hoàn tất** (LibreSprite CLI and 58-frame code pipeline PASS; authentic 10-clip guard artwork, private committed ASE and owner aesthetic approval not done).

## 2026-11-26 — Jade user-designed six-pose running candidate (not full final art)

The owner requested replacing the visibly incorrect old mixed 4×20 run with the newly designed six whole-body Jade poses *inside the canonical game*. PRIVATE `art/drafts/jade_run_owner_six_12.png` is a native transparent 6×2 atlas, right=frames 0..5, left=6..11 mirrored as **whole body**. Its editable sources are `jade_run_owner_six_right.aseprite`, `jade_run_owner_six_left.aseprite`, matching single-row PNGs and `.foot.json` draft pivots. `candidates.json` now registers both source tags, in addition to unchanged W/S walk candidates. The raw 2172×724 AI design included black/gray stage effects, removed by chroma-guided foreground extraction; no limbs were manipulated. Final owner aesthetic verdict remains PENDING_ART.

Native Godot, Pages export, Chromium and a REAL pinned LibreSprite CLI source re-export are distinct verification gates. `tests/draft_animation_sources_smoke.py --binary libresprite` must round-trip both six-frame editable sources to identical transparent PNG/frames and validate each tag/foot sidecar. This public runbook commit triggers the LibreSprite art workflow; record the resulting run SHA/status in the next checkpoint. Six review poses are not the strict 8+ separate-frame running minimum; the full ten-tag fighter catalog, strike art and owner `autocheck:false` approval remain pending.

**Trạng thái: PARTIAL — chưa hoàn tất.**
