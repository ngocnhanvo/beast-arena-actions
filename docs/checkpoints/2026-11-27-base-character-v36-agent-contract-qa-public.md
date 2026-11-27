# 2026-11-27 — Base Character v3.6 deterministic agent-neutral source contract SUCCESS (art review still BLOCKED)

## Actual repo / run evidence
- PRIVATE source stacked on v3.5 Draft PR #9. New v3.6 branch `feat/base-character-v36-agent-neutral-contract` source code SHA `cbeb8d70d3b181fe8175400e7d0fa8c0600abf3e` (later checkpoint-only HEAD `16a1281f9b8d9cab7868d4424a7d883e495df3ed`). PRIVATE main source/game/Jade Draft PR #2 not changed. PUB main `c72335df77237580e88066749a3411b58b5494a6`; isolated CI `ci/base-character-v36-agent-contract`.
- Earlier PUBLIC [run #46023046511](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46023046511) **FAIL** on import because source is `src/sprite_contract.py` and tests live in `tests/` rather than the flat local package. Fixed module resolution in test setup and reran.
- PUBLIC workflow SHA `d6792c7f0c38ea65b9c874aee908e6995f06f247`, [run #46023248285](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46023248285), job `140587974169`: **COMPLETED SUCCESS**. Actual terminal log `Ran 16 tests / OK`, `V36_VISUAL_TRIAGE_FAIL_CLOSED_SOURCE_PASS`, `V36_AGENT_PACKET_VALID`, `V36_OWNER_ART_RELEASE_REMAINS_BLOCKED`.

## Deliverables / small-agent work protocol
- Source-only `tools/pose_lock/base_character_v36/src/sprite_contract.py`: zero AI/API requirements, deterministic `bootstrap/audit/task/apply/release`; immutable 6×80×80 source, nine item slots and per-frame approximated anchors, 80×80 edit allow masks, SHA pin on individual gear PNG, original sprite, manifest and contract, atomic single-slot apply.
- Full task packet: `task.json` + `layer.png` (ONLY editable) + `allowed_region.png` + read-only `original.png`/`current_skin.png`/`anatomy_part.png`. Agent edits one slot in one frame, code rejects stale edits, wrong source, random pixels, detached item, floor pen or wrong dimensions. Rebuild `--compose-only` retains authored hand corrections without touching original.
- Audit of owner-reviewed 4 Skyguard screenshots: hair cyan oversized, gold gloves and boots appear too large/inconsistent; source measurements produce 18 hair expansion warnings + 12 glove/boot area warnings (30 review observations, NOT independent confirmed art defects). These flags are NOT aesthetic judgment, and the tiny 3rd-frame `foot_far` region is estimated automatically, so may yield oversize false alarms.
- Full source and handoff in PRIVATE: `AGENTS.md`, `README.md`, `AGENT_HANDOFF.md`, formal `schema/agent_contract_v1.schema.json`, engineering lessons and private checkpoint. Owner-local review reports/PNG are not published to public CI.

## Hard boundary and next exact action
- `source_technical_status=PASS`, `owner_visual_status=PENDING_OWNER_ART`, release `BLOCKED`. **No new art was drawn or accepted**, no complete hidden anatomy, 6→1 owner motion acceptance, 8+ authored guard source, Godot gameplay/Pages/browser E2E. Do not interpret native LibreSprite v3.5 historical pass as approval of new Skyguard pixels. No game/main merge, Jade/physics untouched.
- Next: small agent or artist edits one Skyguard hair PNG via task, checkpoint hash, reruns v3.5 compositor, source QA, official LibreSprite. Check actual six-frame loops and owner signoff before extending to gloves, boots and other skin families. Preserve one canonical future game URL `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/`; `autocheck:false`.

**Trạng thái: PARTIAL — chưa hoàn tất.**
