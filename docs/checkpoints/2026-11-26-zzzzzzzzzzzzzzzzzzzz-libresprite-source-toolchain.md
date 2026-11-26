# LibreSprite v1.3 source toolchain for Beast Arena — 2026-11-26

Owner asked us to install/use LibreSprite ourselves, stop requiring manual setup. `autocheck:false`: owner alone approves visual quality.
Preflight: read AGENTS.md, docs/START_HERE.md, latest checkpoints and real GitHub Actions/logs in both repos.

## Verified real toolchain
- Upstream official v1.3 Linux x86_64 AppImage 98,089,464 bytes, SHA256 fd90bddda8135fe00f4a9a9c8c9ebd48f9b07e8782ab269be5c9efb1a851af30.
- Public ci/setup_libresprite.sh installs SHA-pinned binary via FUSE-free extraction, SDL dummy headless wrapper; no binary distributed to user.
- Public .github/workflows/libresprite-art.yml uses secure actions/checkout private token, no public art/source artifacts.
- Public ci/libresprite_roundtrip_smoke.py proves actual source .ase editable layer, 4 cels, PNG and JSON tags/durations/pixels.
- Public ci/libresprite_full_export_smoke.py proves real PRIVATE tools/libresprite_export.py with 58 TEST-ONLY 80px frames, ten guard tags and explicit per-frame foot pivot source; no test art shipped.
- GitHub Actions #45796842259 SUCCESS and secure checkout #45797269317 SUCCESS; real logs include LIBRESPRITE FULL GUARD EXPORT PASS and PENDING_ART for genuine Jade.
- Historical FAIL #45796083150 and #45796479653 were malformed test-only ASE reserved-byte escapes, now fixed.

## PRIVATE code and contract
- PRIVATE tools/libresprite_export.py exports actual FULL native 80px guards from editable .ase/.aseprite and per-frame authored .foot.json; LibreSprite v1.3 does NOT support reliable --list-slices. Export merges pivot slices then validates Godot format.
- PRIVATE tools/export_animation_sources.py delegates to this exporter; PRIVATE art/animation_sources.json and tools/animation_source_audit.py now enforce consistency with fighter guard 10-clip shared profile.
- Details PRIVATE docs/art/LIBRESPRITE_SOURCE_WORKFLOW.md and PUBLIC docs/LIBRESPRITE_RUNBOOK.md.

## FIRST Jade graphical source DRAFT
- Current chat generated 6 distinct complete-body original front-facing Jade combat-guard WALK-DOWN keyframes, native 80x80, 100ms; raised fists, teal hair, red scarf.
- Created actual editable ASEprite binary with six RGBA full-body cels, one tagged walk_down_guard_front (frames 0..5), PNG 480x80, GIF, draft .foot.json and preview strip.
- Independently parsed ASE header/chunks (magic 0xA5E0) and decompressed all six cels; pixel data matches exported PNG exactly. This is a DRAFT clip, not quality approved.
- Available as current conversation artifact BeastArena_Jade_guard_walk_down_SOURCE_DRAFT.zip / REVIEW.png in /mnt/data. NOT committed to private GitHub repo; no unsupported path assumption.
- This is ONE of TEN required clips. It does NOT qualify as final Jade art; do not enable it in-game or remove PENDING_ART. Draft foot y=76 needs artist checking.

## Remaining / next steps
- Produce 9 other complete 80px high-guard clips, refine entire 58+ frame source, verify foot contacts, combine into editable layered 10-tag ASEprite asset in PRIVATE repo.
- Run real LibreSprite exporter, strict source audit, Godot SpriteFrames importer and staging preview; only owner visual-accepts under autocheck:false.
- Technical toolchain proven PASS, actual final game animation NOT READY; later full game roadmap open.

**Trạng thái: PARTIAL — chưa hoàn tất.**