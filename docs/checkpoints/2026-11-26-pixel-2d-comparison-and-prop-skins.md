# Public Actions checkpoint — visual-first dual presentation and authored physics props
Date 2026-11-26. **Overall: PARTIAL — chưa hoàn tất.**

## Canonical source handoff
- PRIVATE `ngocnhanvo/beast-arena/docs/checkpoints/2026-11-26-pixel-2d-comparison-and-prop-skins.md` is the authoritative latest checkpoint. Read AGENTS.md and both START_HERE docs, V3/V4 checkpoint and visual-first roadmap before edits.
- Original Physics0 source has new separately authored skins for all six native 3D physical obstacles; sprites and floor remain from same original pixel assets.
- Private `scripts/pixel_projection.gd` and `scripts/pixel_view.gd` create an OPTIONAL F5 2D visual projection from actual Godot 3D actor/floor Y: fixed horizontal X, 6.5 pixels/m depth for Z, 31 pixels/m physical elevation for Y; original sprite frames and map textures. No second gameplay/physics system, no changes to existing root P1.5 route, no forced F5 default.
- Private `scripts/demo.gd` reports `pixel_projection_mode` + actual draw counts; private new headless `pixel_projection_smoke.gd` validates world-axis/height map switch and 2v2 physical roster connection.
- Public `.github/workflows/build.yml` now runs headless `pixel_projection_smoke.gd`. Public `ci/playwright_physics_v2.py` toggles F5 in Chromium, screenshots `moss-nes-style-2d-preview.png`, asserts tile/character counts, nonflat pixels and restores original 3D preview.
- Pre-existing Public `ci/playwright_physics_v2.py` also requires `pixel_prop_skins=6` on Moss and Night Docks. This verifies native obstacle geometry is visually skinned, not merely created in code.

## Evidence (not a general completion claim)
- Godot build/Pages #45683483080 and Chromium #45683778280 SUCCESS. Real old pixel top-floor image visible but overly steep-looking wide map.
- Compact stage build/Pages #45684576424 and Chromium #45684936382 SUCCESS, private `08d99ab20437346e041c557f4294888c40e21772`; screenshot inspected: original texture detail visible but full-width 3D ramp still occupies too much of the frame, Nekketsu style NOT visually accepted.
- Prop skin build+Pages #45685202832 SUCCESS, checked-out PRIVATE source `549a33eedabb8b327dc511a6af6d887e2b53b137`, public pipeline `c2b6048236bea2770bcc72d8e849cfbb89b5108a`. Follow-up browser #45685557148 in progress at snapshot.
- Source pixel view last code PRIVATE `49ca27ea6e7729c9d35033f4420d2a70bf402cc0`; public CI test code last `ca30f9460e12b92f296cd558e1cb62d81d5e6300`.
- Build #45685585437 / queued #45685624341 will verify optional 2D renderer. **Not yet verified.** Never claim CI successful merely because pushed.

## Required next QA
1. Inspect latest public CI run and exact checkout SHA; repair Godot 4.7 parser/test/runtime failures if any.
2. Confirm Pages deployed and Chrome screenshot `moss-nes-style-2d-preview.png` from the SAME source SHA; compare both 3D and F5 2D mode, verify battle, ground height, silhouette, background and frame size. Check Night Docks through F5 as well before default change.
3. Keep visual acceptance open, no production root migration, no beast transformation until actual user-approved V0–V4 human/gameplay slice.

**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — Verified F5 release, visual feedback, stronger cross-map screenshot QA

- VERIFIED PUBLIC Godot+Pages [#45685585437](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45685585437) SUCCESS, actual PRIVATE source `49ca27ea6e7729c9d35033f4420d2a70bf402cc0`, PUBLIC pipeline `a04fc583d3af6392154f619868451e4fd68d3d60`. Headless physical 3D tests + independent `pixel_projection_smoke.gd` passed.
- VERIFIED browser Chromium [#45685984297](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45685984297) SUCCESS. Artifact screenshot `physics-v2/moss-nes-style-2d-preview.png` downloaded & visually inspected; result has `pixel_2d_overlay_pass=true`, 221 tile draws, four real fighter renderings, 25 3D combat hits, 9 distinct visible color groups, F5 returns to original view.
- Human visual QA: the whole map no longer feels like a single tilted 3D plane, but F5 sky has too much empty space and raised stair tiles lack connected supporting walls. Thus **VISUAL_ACCEPTED=FALSE / USER REVIEW PENDING**; don't conflate this with technical browser PASS.
- PRIVATE new code `40f0cce` adds original sky parallax and pixelated physical retaining walls; unique hair/scarf/armor variants `330f3ce`, `7395afc`, `659e3b4`; source visual test `67c1ac8` checks distinct alpha silhouettes. PUBLIC `ci/playwright_physics_v2.py` commit `79f33d5` captures **both Moss and Docks F5 start** images BEFORE combat in addition to original F5 post-2v2 image.
- **NOT YET VERIFIED** at documentation time: build [#45686677550](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45686677550) and follow-up screenshot runs for new sky/retaining wall/F5 two-map captures. `67c1ac8` alpha test may be newer than that source checkout and must be re-built. Preserve old P1.5 and no V5 deployment.

**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — Actual latest Godot/Chromium verification, direct pixel URL and CI provenance

- Build+Pages #45686677550 PASS source `40f0cce`; E2E #45687005195 PASS, both originally authored Moss and Docks `moss-nes-style-2d-start.png`, `docks-nes-style-2d-start.png` downloaded/inspected. Original parallax sky and physical-height stone/steel risers visible. Godot still sole XYZ collider; F5 horizontal screen composition avoids entire tilted 3D slab.
- Build+Pages #45687678619 PASS source `3f088fc`: direct URL query `/physics-v2/?pixel=1` boots pixel view without F5, P1.5 unaffected.
- Build+Pages #45687946574 PASS source `9f27e53c06da78779b85a42cceb0cbe440d0b008`, pipeline `fb8f5fc32856df6591ffcd98ff79615667c21db2`; Chromium #45688376830 PASS. Actual artifact `result.json` confirms `pixel_direct_url.enabled=true`, 234 Moss floor tiles, 288 Docks tiles, 4 actors and 4 original visible pixel HUD portraits; `moss-direct-pixel-url.png` screenshot inspected. Pixel art prototype remains subject to user visual acceptance.
- Browser #45688049122 FAIL with `Four authored human portrait badges are missing`: newer browser code ran against **stale Pages image** before #456879 deployment, NOT a confirmed missing portrait code. Public source `web-e2e.yml` commit `3cfa440` pins test checkout to producing run `head_sha`; `ci/playwright_physics_v2.py` commit `3b9b9a` checks exact `BEAST_EXPECT_PIPELINE_SHA` and `BEAST_EXPECT_BUILD_RUN_ID` against deployed PCK. Public build+Pages #45688176577 PASS and browser #45688659887 was IN PROGRESS at entry; verify identity test before claiming its success.
- NEW private source `c79731a` / `5890143` / `0911450`: physically correct Z ordering of humans/real 3D props under optional F5 renderer, with headless test that raises wall Z in front/behind fighter. **Not yet built/deployed**; latest private code head before docs `0911450f906e1e3622363e800501fe515cd2b1fb`. Next Public push without [skip ci] must validate this source.
- Next: inspect newest source SHA checked out, headless `pixel_projection_smoke.gd`, Web/Pages, Chromium #? and screenshots. If a stale build mismatch occurs do not mask it as PASS; retry only after correct deploy. USER VISUAL ACCEPTANCE still OPEN, root P1.5 unchanged, V5 not started.

**Trạng thái: PARTIAL — chưa hoàn tất**

### Immediate rebuild gate for new physical Z occlusion

- Confirmed #45688659887 Chromium PASS on Public pipeline exact-SHA E2E after fix #45688176577 CI+Pages PASS. This validates prior source `9f27e53`, **not** the latest physical prop/fighter occlusion source.
- This public docs commit triggers a new Godot CI to check PRIVATE latest head `b9586fae69f...` including actual code `c79731a`, `5890143` and test `0911450`. Need verify Godot import and pixel projection test, Pages, then Chromium screenshot. **Requested/triggered is NOT success**.

## 2026-11-26 — V4 human guard verified and real 60 Hz match results in repair cycle

- PRIVATE directional guard code `46cf5fad` + PUBLIC guard browser `12837ad` verified: build+Pages [#45689560800](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45689560800) SUCCESS and Chromium [#45689891139](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45689891139) SUCCESS. G hold/release and actual gameplay guard animation checked.
- NEW source PRIVATE `439ab5a` (`BeastMatchState`, 60Hz timer, team-KO and timeout/draw results), `d45d6e3` unit test; `558ed1b` integrated 4-player match HUD + C start/T restart, `446904f` real 4-actor scene fixture. PUBLIC workflow `3e72352` added unit+scene jobs and browser `9f1d1fe` tests authoritative countdown/true T reset.
- **OBSERVED FAIL** build [#45690255618](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45690255618): strict Godot import, old physical/visual/combat tests and new round 60Hz UNIT test PASS; new `match_scene_smoke.gd` fails `ROUND-12: real UI doesn't reflect gameplay team victory`. Earlier in same test, `match_state.outcome == TEAM_1_WIN` was PASS. This is likely `SceneTree.process_frame` firing before `Node._process`, so the victory label had not been redrawn yet; no Pages deployment happened.
- PRIVATE fix `c19b31d89532a60e5eba25f91402055e05791fa6` waits one more actual render frame after physical KO/restart, improves the failure log. This **PUBLIC DOCS COMMIT intentionally triggers NEW CI** (not skip-ci). Verify exact private source SHA, all stages and Chromium; don't claim new match V4 PASS until run and browser evidence.
- Do NOT move human-beast transformation ahead of visual-first acceptance; gameplay core still incomplete (combo/grab/throw/navigation/editor) and root P1.5 not migrated.

**Trạng thái: PARTIAL — chưa hoàn tất**


## 2026-11-26 — Exact 2v2 round E2E PASS, trigger fine-grained original slope render gate

- **VERIFIED:** Public Godot+Pages #45690550928 SUCCESS with private SHA `732d652392b21d4ec2b30a73a98b85dbfcc30d50`, pipeline SHA `9d36afd9a634e414d6838c10cbd555c1d85e0d0f`. Original art/physics/guard and NEW 60Hz `match_state_smoke.gd` and `match_scene_smoke.gd` PASS.
- **VERIFIED:** Chromium [#45690919676](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45690919676) SUCCESS. Real artifact `physics-v2/result.json` inspected: ACTIVE round timer 5106/5400, HUD `ROUND 1  86`, T restart PASS (all four HP=100, 5400 ticks, no active AI or hits), exact direct pixel URL source SHA, legacy P1.5 PASS. Screenshot `moss-direct-pixel-url.png` inspected; original 2D level and four portraits still visually render; not artist-approved.
- **SOURCE ONLY / NEXT:** Private `BeastPixelProjection.floor_x_strips` `758d420` and `BeastPixelView` `5a84826` draw true physical 3D uphill/downhill with finer 0.5m X image tessellation, avoiding visually chunky 2m staircase bands. Private `tests/pixel_projection_smoke.gd` `1dd00ce` asserts map-wide seamless coverage and <=0.5m visible ramp columns on Moss and Docks. Private `scripts/demo.gd` `4041d63` removes large visible SHA strip for original arcade controls while keeping F2 exact diagnostics and opt-in Web SHA.
- This PUBLIC docs commit intentionally triggers new full public CI/Pages+Chromium against PRIVATE HEAD (verify exact checkout SHA). **Do not claim deployment or live screenshot PASS for new ramp/HUD until new run and screenshot inspected.** Root P1.5 still separate; user original Nekketsu-like artwork acceptance OPEN; no beast form V5.

**Trạng thái: PARTIAL — chưa hoàn tất**

## 2026-11-26 — ACTUAL FINE-RAMP PAGES+CHROMIUM PASS; art approval still open

- PRIVATE source `d1a22bae199ba80296e6af850906e95241619f9b`; PUBLIC pipeline `df8f1ff7ee145bf88f327a05bcadfd6eaa913011`. [Build+Pages #45691649914](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45691649914) **SUCCESS** on exact source: strict import, all physical slopes, original stage materials, `pixel_projection_smoke.gd` 0.5m continuous columns, guard/round, human 2v2, Web+Windows export and Pages.
- [Chromium #45691975794](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45691975794) **SUCCESS**. Actual `beast-arena-browser-screenshots` artifact downloaded; `physics-v2/result.json.status=PASS`, no page errors, source SHA matches. Moss `moss-nes-style-2d-start.png` tile count=468; Night Docks `docks-nes-style-2d-start.png` tile count=576, both 4 visible pixel fighters. Previous old images had 234/288 much coarser stage steps. Visually inspected new two-map screenshots: slope edges materially smoother, level horizon fixed, UI cleaned (controls instead of full CI SHA string); true 3D physics unchanged.
- Chrome also verifies C starts actual 60Hz timer, real HP/team hits/AI, player G guard, T rematch resets all 4 HP to 100 and 5400-tick timer, source/run exactness and P1.5 legacy route. Demo URL: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?pixel=1
- **NOT DONE:** user art approval and complete original hand-drawn Nekketsu-era character frames, varied map decorations/navigation/better editor, advanced 2v2 human combo/grab/throw, production migration/perf/ADR approval and all beast transformations. Root P1.5 still isolated. This is technically PASS for the milestone, but **overall PARTIAL**.

NEXT: source HEAD/run check, improve original human animation and stage art, add damage feedback/advanced combat/level editor; after each change rerun Godot+Pages+Chromium, inspect screenshots and update this latest checkpoint. **Trạng thái: PARTIAL — chưa hoàn tất**
