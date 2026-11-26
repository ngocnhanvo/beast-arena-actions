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

## 2026-11-26 — Jade eight-phase source to be validated by real LibreSprite CLI
- New PRIVATE candidate jade_run_eight_right and jade_run_eight_left: eight individually authored 80px source frames, each 85ms, one run guard tag, PNG and editable .aseprite, foot y74 sidecar. Active candidates.json replaces old six-frame registered run tags; original six still archived. Public workflow automatically checks source tags, frame durations and pixel-exact roundtrip; any FAIL is a real exporter/ASE bug, not automatically art acceptance. User reviews only canonical https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . Owner aesthetic still PENDING_ART.

## 2026-11-26 — Jade 8-pose arm counter-swing source retouch (not owner-accepted yet)
- PRIVATE updated full 640x160 Jade source atlas; only 4 upper-body frames 2,3,4,5 are hand-repainted with near-arm guard counter-swing. Accepted shoes/legs are pixel-identical across ALL eight phases (source baseline `jade_run_eight_16_before_arm_retouch.png`, rows y55..79). Opposite LEFT sources mirror whole 80px frames, no limb component runtime manipulation.
- Active editable `.aseprite` sources and PNG exports regenerated for both 8-frame sides, 85ms per tagged cel. Private Godot `three_quarter_preview_smoke.gd` checks pixel-invariant legs and amended arm-only phases; PUBLIC real LibreSprite workflow validates full source PNG/ASE roundtrip.
- Owner `autocheck:false`; visual acceptance still pending. Inspect only https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ after exact SHA Pages deployment and browser Chromium test. Do NOT declare a source edit artistically successful solely from CLI PASS.

## 2026-11-27 — Pixel-exact rollback of broken Jade arm overpaint (requires real CI)
- User reported visibly broken eight-frame animation; true source problem found by comparing original 8+8 frames to four overpainted right-hand poses (2–5). Existing fist was not removed, oversized black glove polygons were drawn on top, not a valid original clean arm animation. Playwright video + rAF diagnostic #45864460748/#45865195144 confirms renderer selection does not certify browser-visible smooth motion; screenshot-heavy diagnostics itself causes stalls.
- PRIVATE `cd4b919d2e6da5ac550e59d0a852e316f424fc03` restores original full native 8+8 PNG and editable right/left ASE and PNG (old good sources), leaving the previously owner-accepted leg pixels unchanged. Source metadata now honestly labels hand cadence PENDING_ART. Original source baseline remains `jade_run_eight_16_before_arm_retouch.png`.
- Native smoke now asserts whole 16-cel exact PNG parity rather than merely all shoes: `JADE RUN ARM OVERPAINT ROLLBACK PASS`. Pin real LibreSprite CLI export and verify both eight-frame editable ASE files. Trigger build/Pages and exact Playwright without allowing the old overpaint to sneak through from cache.
- Owner checks only https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ after verified deploy. `autocheck:false` does NOT allow an automatic aesthetic acceptance of arm rhythm.

## 2026-11-27 — NEW 4+4 Jade running guard arm art, source-pixel acceptance gate
- PRIVATE `a1d7088747c06171f9e57b5a470095e082f50669` adds original AI-assisted complete native 8×80px right and eight whole-body mirrored left cels. Four distinct upper-body guard-arm shapes are staged in equal pairs F0=F7, F1=F6, F2=F5, F3=F4, with eight existing legs kept byte-identical at source y55–79 and original head/hair y0–36. The pairs create a continuous compact fist pump (retreat, middle, advance, full guard, reverse). No runtime limb components or overpainting of old gloves.
- Source PNG atlas 640×160 and `jade_run_eight_{right,left}.{png,aseprite}` need pinned real LibreSprite 85ms/tag export check. Native Godot source smoke now checks four distinct arm regions and exact symmetric 4+4 pairs + preserved leg/face pixel parity. No changes to physics, animation phase timing, collider, walking or maps.
- Actual Playwright screenshot/video and final art quality remain `PENDING_OWNER_REVIEW` (`autocheck:false`). Check the exact new build and E2E run IDs before declaring technical PASS; owner reviews only https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ .
