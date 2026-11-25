# Actions checkpoint — Physics0 native editor & Web staging — 2026-11-26

Status: GODOT CI / PAGES PASS, final Chromium after latest CSG color change pending. 3D Physics0 not migrated to P1.5 production.

- GAME functional source SHA a39af14ac7fe51785d36778ea0af440d366d2d88.
- ACTIONS test source SHA 3a7233a027a7d87676e6def2399944223a2a6200.
- GitHub Actions #45670308588 SUCCESS https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45670308588 : strict import, Physics0 motor/ramp/jump, native GridMap 5 collision brushes and CSG unshaded prop material, 55.8px character, walk blocked by rail / jump over rail / tall wall blocks, Windows/Web and staging Pages.
- Older browser #45669821453 PASS real Physics0 and original P1.5 game. Screenshot floor-color check: Moss 0.989, Docks 0.987.
- New browser #45670647655 pending at time of this checkpoint, must inspect screenshots after CSG color change.
- Previous browser #45668868363 failed for temporary Pages HTTP 503 PCK while game ready; now report recovered network warnings separately, never suppress actual screen/color or runtime errors.
- Staging game: https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/
- Main P1.5 game (unchanged): https://ngocnhanvo.github.io/beast-arena-actions/

OSS map tools: built-in GridMap, MeshLibrary, CSGBox3D Godot 4.7.2; actual authored scenes and map catalog / surface-grip zones stored in PRIVATE. MIT Godot demo patterns studied, source in third_party/SOURCES.md. Cyclops optional only; Terrain3D extension not used.

NOT DONE: full physics/combat 2v2 migration, animation, props/hazards, AI navigation, complete level editor, performance approval. ADR still PROPOSED. Check actual GitHub run logs and latest checkpoint in BOTH repos.
