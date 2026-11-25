
# Beast Arena Web E2E — 2026-11-25

Workflow: .github/workflows/web-e2e.yml
Script: ci/playwright_smoke.py
Target: https://ngocnhanvo.github.io/beast-arena-actions/?e2e=1

Evidence P0: run 45656492064 PASS on older source — game rendered, D moved +266.2 pixels. Earlier runs failed because tests inspected Godot canvas during loading splash.

New test is NOT solely pixel-based: Godot Web publishes a minimal opt-in read-only snapshot window.__beastArenaDebug when URL includes e2e=1. Wait for ready=true after WASM startup; verify canvas visible, StageData obstacles=2, Space causes jump event and positive height Z, J starts attack, D causes world-space player X to increase >=28. Store screenshot, browser DOM, errors and state snapshots as PUBLIC artifacts.

Do not mark the latest P1 build passed until a new Browser Playwright workflow run succeeds. Pressing U with beast meter below 50 cannot prove transformation. F2 toggles collision/obstacle/spawn markers for manual tests.

## Verified browser status
- #45656492064 PASS on pre-P1 source after fixing loader wait (D +266.2px).
- #45657184814 PASS on P1 source, Space/J/D state changes, player +224 world units.
- #45657791050 PASS with F2 collision debug true, screenshot plus player +227.5 world units, no critical browser JS/WASM/PCK request errors.
- Images and result.json are GitHub Actions public artifacts. Re-verify on each new rendering/logic release; these runs do not test combos, throws, multiplayer, or Android.
