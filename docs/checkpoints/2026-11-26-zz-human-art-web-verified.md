# Beast Arena Actions — HUMAN-ART final verified handoff (2026-11-26)

## Strict matching build/run
- PRIVATE exact compiled source: `191842e4948d6f0a5a864a4c2c5815b240b2fd03` (later Private HEAD may have documentation-only changes). PUBLIC exact pipeline code `a8f49cc62dfde3a3b5514fb10d41f1035eee3a82`.
- [#45735133772](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45735133772): **SUCCESS** preflight, Godot 4.7.2 strict import, physics/3D ramps/obstacle editor, original four 80-cell human SVG atlases, screenshot/presentation tests, 60Hz team combat/guard/VFX/match, Web+Windows export, Pages deploy. Root P1.5 separate.
- [#45735342337](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45735342337): **SUCCESS** actual Chromium with matching source SHA and run ID, artifact `beast-arena-browser-screenshots`, real `physics-v2/result.json.status=PASS`.
- New actual image `physics-v2/moss-running-horizontal-pixel-2d.png` downloaded/visually inspected. `original_2d_running_art_pass=true`: **horizontal background while actor runs on a genuine rising 3D incline**. The earlier image `moss-running-real-speed.png` used 3D comparison mode (appears tilted), so it is NOT a valid proof of NES-style F5 art. User-facing intended staging URL: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1
- `physics_driven_run_art_pass=true`: physical XZ velocity ≈4.2m/s drives authored run row3 / frame14; `original_human_jump_pose_pass=true` at actual airborne Y0.855m with row5. All four original human atlases were edited in 64 cells total (4 poses × 4 facings × 4 fighters): jump/prone KO/getup/defeat. Imported alpha silhouette tests PASS. Moss=468 and Docks=576 floor image spans with 4 fighters each; HP, hit counter, G guard, 90s round and T restart PASS.
- `real_guard_contact.blocks=1`, HP97, `visible_cyan_pixels=1388`. `?e2e=1&capture_guard=1` **explicit test-only** holds a real already-confirmed 3D guard frame for headless screenshot. Normal gameplay 0.55s art lifetime and collision/damage remain unchanged; unit test protects this. Do not claim the held screenshot reflects the full natural VFX animation.

## Incident and follow-up
- #45732537827/#45732600754 failed ART-10 at not-yet-grounded spawn, fixed by real physics-floor wait `82b94b`; #45732775052 Godot+Pages PASS.
- #45733022775 failed fixed 250ms idle assertion; real inertia/render requires waiting actual vx+animation; fix PUBLIC `1198ce3`.
- #45733685336 and #45734022726 failed intermittent cyan screenshot pixels=0 after short-lived effect expired; code/game counters were real. Opt-in capture fix PUBLIC `156e6d8`, PRIVATE `191842e`; #45734623244 and #45735342337 full E2E PASS without weakening visible-pixel minimum.
- Previous scheduled source/Pages cache hit #45728104476 skipped deploy; downstream #45728174303 erroneously failed STALE_PAGES. `web-e2e.yml` PUBLIC `7dadcfd` publication-gate skips E2E if Pages job is skipped and fails closed on unknown status; real deployed branch proved #45730089391. **Scheduled skip branch still not observed**; verify next natural schedule without forcing a misleading pass.
- Remaining: final NES-like original visual polish and user approval, new human combos/grab/throw, map props/editor UX, AI navigation, cross-device FPS, production P1.5 parity/migration, original V5 beast abilities **not yet started**. Preserve true 3D-only physics authority and original artwork. After each change rerun public build + strict screenshot QA and document exact SHA.

**Trạng thái: PARTIAL — chưa hoàn tất**
