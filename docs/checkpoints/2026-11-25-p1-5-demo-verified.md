
# Actions checkpoint — P1.5 two playable large maps — 2026-11-25

**Verified P1.5a large-world Camera2D and 2 stage previews; other P1.5 scope partial.**

- PRIVATE functional source: `226d413e683ee30ea5e511a630e5ab96e6442e63`;
  subsequent private documentation-only commit `154bf525f3592239a432195d58c815e141b78e19`.
- PUBLIC Actions workflow+Playwright: `1dc3845e9769713e359da144c93a19e9fab4bc73`.
- Build/Pages: https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45660505234 **SUCCESS**; import, combat, smoke, P1, P1.5 test, Web/Windows exports, Private Release, Pages.
- Browser E2E: https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45660829632 **SUCCESS**; game ready, no page/asset errors, player D moved 220.5 world units, Space/J/F2 pass; map switch 2; F3/F4 far/home camera.
- Moss Temple camera far center (2080,1140) within 2560x1440 stage;
  Night Docks far (2592,1220) within 3072x1536; return (480,520).
  Screen is 960x540 game viewport, black bars in 1200x800 Playwright window
  are intentional aspect-ratio letterboxing, NOT out-of-map blank space.
- Public screenshot evidence in Playwright run artifact:
  `moss-temple-far-camera.png`, `night-docks-start.png`,
  `night-docks-far-camera.png` and `result.json`.
- Private release: https://github.com/ngocnhanvo/beast-arena/releases/tag/ci-226d413e683e
- Web game: https://ngocnhanvo.github.io/beast-arena-actions/
- Map StageData supports separate art/world/camera/ground bounds and
  independent collision wall geometry, but standalone interactive map editor
  with draggable polygons and props/equipment/character catalogs is NOT done.
  See PRIVATE `docs/P1_5_DEMO_HOW_TO_EDIT.md`.
- Next: P1.5b polygon authoring/editor, dynamic map catalog; P1.5c props/
  characters, then P1b combat hitboxes. Recheck both HEADs and live logs first.
