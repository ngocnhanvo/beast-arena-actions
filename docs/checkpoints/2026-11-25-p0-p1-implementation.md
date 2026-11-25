
# P0/P1a implementation checkpoint — 2026-11-25

This snapshot records work completed in this session; always inspect current HEAD and workflows before continuing.

Private source: ngocnhanvo/beast-arena on main. P1 source commits: 96e0929 (input/FSM/stage data), cc44b7a (fighter Z + collision), e200442 (main wiring and tests), b245323 (Rect2 fix), 9d92b64 (F2 debug overlay). Documentation was updated afterward; source HEAD may differ.

Public Actions: ngocnhanvo/beast-arena-actions on main. P0 Playwright fix 752ceb5; new state-based Playwright + P1 test wiring 7a3bd8e; strict script import step 47ff972.

Verified:
- P0 real-browser run #45656492064 SUCCESS (older source): rendered arena, D movement 266.2px.
- P1 Godot run #45656838908 SUCCESS: combat, stage smoke, FSM/spatial/collision test, Web/Windows exports and Pages. That run used source BEFORE F2 debug commit.
- Prior #45656654819 FAILED: Rect2.translated() not in Godot 4, leading to Stage script compile error. Fixed.
- New browser state-check workflow / final F2 source is not marked passed until corresponding run verifies.

What changed:
- InputCommand for intent, FSM idle/move/jump/attack/hitstun/KO, jump height Z independent ground XY.
- CharacterBody2D/STAGE StaticBody2D collision, StageData resources defining bounds, spawn and two wall obstacles.
- Combat height gap prevents ground punches hitting targets too far above (still range+facing P1 approximation).
- F2 visual collision markers, Stage spawn points and fighter circles.
- Web debug snapshot only with ?e2e=1 for browser testing, no private data.

Pending:
1. Run public CI on final private source and inspect exact source SHA in logs.
2. Verify Pages successfully deploys and new Playwright debug-state test PASS (including Space/J/D, screenshot).
3. If fail, inspect artifacts and log, fix in correct repo, rerun before reporting done.
4. Next phase P1b/P2: true per-frame hitbox/hurtbox/pushbox/grabbox, combo, guard, throw, AI pathfinding.
