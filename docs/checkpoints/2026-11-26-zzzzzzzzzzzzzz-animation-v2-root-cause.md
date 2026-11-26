# Beast Arena Actions — actual animation pipeline source audit (2026-11-26)

## Owner decision
Owner explicitly REJECTED current Jade run as very poor after artificial hand/foot pixel shifting. Do not misinterpret old technical PASS as owner visual signoff. A new original asset-production pipeline is needed, NOT further coordinate patches or a physics engine rewrite. User's `autocheck: false` remains in force.

## Verified prior source and CI
- Private HEAD at audit entry `4a769caf826a3e015ee5d8638d62e035102ace3e`, Public HEAD at audit entry `71082ae4c7ce83a39eaa89a27615736ddad9c5de`.
- Last modified legacy gameplay source `32b514546e6d2dec8d20381bd0cdcc204d1ce6f0`, pipeline `5c68ec7c1d16996a526b7d49d18fb3e6b75f53ad` had engine/Pages #45770958180 PASS and real Chromium #45771214382 PASS. This only showed functional 4-phase contacts, not natural body movement.

## Verified root cause
- Private repo has the 320x1600 approved Jade 4x20 80px PNG and 40px prototype pack, but no `.aseprite`/.ase editable animation source.
- Game `jade_approved_motion.gd` manually blits y>=53 shoes and shifts shoulder/arm pixel rectangles. Four hashed/different output frames do not represent independently drawn full-body actions.
- `character.gd` hardcodes atlas row selectors and `pixel_view.gd` reads Sprite3D row/column, tightly coupling animation authoring with two different renderers; transparency-derived pivot is a fallback only.
- Native Godot `SpriteFrames` and `AnimatedSprite3D` + Aseprite tagged sheet/JSON work on existing Godot stack, so missing genuine authored source is primary blocker, not a proven engine limit.

## Implemented source contract and public build audit
- Private `docs/architecture/ANIMATION_SYSTEM_V2.md`: full authored clip contract, 80px source geometry, named action/facing, frame durations, foot slices, one selected pose consumed by PixelView + Sprite3D, gameplay 60Hz unchanged, owner review gate.
- Private `experiments/physics_v2/art/animation_sources.json`: explicit Jade `REFERENCE_ONLY_NOT_ANIMATED`, no fabricated .aseprite/source frames, W/S visual direction front.
- Private `tools/animation_source_audit.py`: standard-library structural audit of editable .ase/.aseprite and Aseprite PNG+JSON tag/slice metadata. Non-strict status `PENDING_ART` permits ordinary technical CI while acknowledging not-ready art; `--strict` returns nonzero for incomplete art; status `READY_FOR_OWNER_REVIEW` still is NOT `VISUAL_ACCEPTED`.
- PUBLIC `.github/workflows/build.yml` now runs animation inventory on each real private checkout before Godot import. It must visibly disclose PENDING_ART in Actions summary, NOT report artistic PASS. Invalid source manifest fails.
- **No new graphical content or V2 runtime is shipped**. The deployed legacy Web player remains visually rejected; technical CI succeeding cannot convert it into an accepted preview.

## Initial actual GitHub Actions proof
- [PUBLIC build/Pages #45773624934](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45773624934) **SUCCESS**, built PRIVATE `1f165ac9d650bb043b1778d30460162c3c021f79`, pipeline `6c717f3be494d2690b757009ffbf8b4008e30117`. Real source audit log shows:
  `"status": "PENDING_ART"`,
  `"jade_human: no complete editable animation source + exported clips"`,
  `"visual_accepted": false`.
  Existing Godot counter-swing smoke and technical export also passed, but this does not fix the owner's visual rejection.
- [Real Chromium #45773861575](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45773861575) was IN PROGRESS at this checkpoint's authoring; check result separately. This is technical Web regression only, NOT animation approval.

## Real next steps and blockers
**BLOCKED_ART_SOURCE:** no six+ original independently drawn full-body run frames for Jade in editable timeline; no Aseprite tags, durations or true foot pivots. Next implement a real authored multi-frame front run set matching approved 80px idle; get owner to approve frame-by-frame contact sheet and motion loop; then author walk and left/right, jump/J/K and import tagged export as Godot SpriteFrames with a single pose/pivot feeding BOTH PixelView and Sprite3D. Do not fake art by shifting pixel fragments; do not silently replace current Web preview with unaccepted pose art. Full roadmap (beast/combat/map tools) remains OPEN.

**Trạng thái: PARTIAL — chưa hoàn tất.**
