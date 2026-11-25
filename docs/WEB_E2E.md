# Beast Arena Web E2E

Workflow: .github/workflows/web-e2e.yml
Script: ci/playwright_smoke.py
Target: https://ngocnhanvo.github.io/beast-arena-actions/

Uses Playwright/Chromium + SwiftShader on PUBLIC runner. Expects Pages 200, visible canvas, screenshot of blue placeholder fighter, D moves right at least 30px, J/K/Space/U keys dispatched. Stores before/after screenshots and result JSON, public artifacts (7-day retention).

IMPORTANT: as of 2026-11-25, runs 45652872940 and 45653213044 are FAIL, AssertionError: Godot canvas too small. Browser gameplay is NOT verified. Read docs/CI_PLAYWRIGHT_RUNBOOK.md, download screenshots and inspect DOM/loader; do not simply suppress the assertion. Sending J/K/U does not prove an attack/hit/transform occurred (U needs enough Beast meter). Update this document after verified passing run with exact run ID and image evidence.
