
# Public Actions checkpoint — visible real up/down slopes (2026-11-26)

Status: **IN PROGRESS / WAIT FINAL PAGES + WEB E2E**, not yet fully verified at this checkpoint creation.

- User sees no slopes; source confirmed center-only hidden ramp and very gentle uniform art. Previous PASS covered motion physics but never screenshot of slope.
- PRIVATE corrected GAME code SHA: `22c3e80b36e698c7fedb63a9c8afad0c4ed096f6`.
- PUBLIC corrected Playwright code SHA: `4fee8eb73c67b18bc31a5af09d99211146551b00`.
- Official Godot motor remains same; slope collider remains one tilted `StaticBody3D`. Moss rises +3.6m in12m, Night Docks descends -3.6m in12m, angle ~16.7deg. No simulated height hack.
- 11 cross-path tread markers, 2 start/end seam markings, 12 camera-side retaining-face segments, 3 elevation labels per stage. All derive from real stage resource; render-only, no extra collision.
- Initial spawn now near ramp; camera lookahead toward it; R takes player to ramp entry. Screenshots from R then holding D must show actual climb/descent.
- New Godot headless test verifies visual nodes and angle as well as real 3D floor normals and jump; legacy 2D P1.5 tests remain.
- New Playwright captures `moss-slope-entry.png`, `moss-ramp-mid-climb.png`, `docks-slope-entry.png`, `docks-ramp-mid-descent.png`; measures actor world Y difference >=1.2m and angle >=10deg while on ramp; screen color checks remain.
- CI run: https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45672632606 . Import, Physics0 and Map/Obstacle tests SUCCESS early; Pages deployment pending at document write. Browser after deployment must be queried and images inspected.
- Original P1.5 root is not migrated; stage prototype is `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/`.
- Follow-up: verify exact source SHA, CI+Pages conclusion, browser run and measurements, download screenshot artifact, inspect ramp visually, update both checkpoints. No premature VERIFIED claim.
