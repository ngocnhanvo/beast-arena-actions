# Beast Arena Actions checkpoint 2026-11-25

Snapshot khi viết; chat/agent mới PHẢI kiểm tra GitHub runs mới nhất.

Source game Private commit nền trước docs: 9e140e8e93e1.
Actions Public commit nền trước docs: 7546acb611ed6772716dc32b88ed129eab12384a.
Godot CI+Pages: run 45652585969 PASS, 45651281051 PASS; Private Release ci-9e140e8e93e1 chứa Web/Windows ZIP.
Playwright E2E: FAILED run 45652872940, 45653213044, error Godot canvas too small. Bài test chưa đủ để kết luận playable hay gameplay bugs.
Next action: inspect screenshot and DOM canvas bounds of 45653213044; fix cause and reverify E2E actual movement; then stage/physics/hitboxes theo blueprint trong repo Private.
Lessons: release HTTP 500 clobber fixed via idempotent upload; GitHub Pages HTTP 500 fixed via bounded retries + hourly recovery; Github write API timeout/409 needs reread HEAD.
Docs precedence: AGENTS.md → START_HERE.md → CI_PLAYWRIGHT_RUNBOOK.md → latest checkpoint → workflow/code/logs.
