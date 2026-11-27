# 2026-11-27 — Jade Codex ↔ ChatGPT API automatic bridge, PUBLIC pipeline boundary

## Scope
- Owner requested actual autonomous agent-to-agent exchange, not prompt copying. PRIVATE game repo now has [Jade Issue #1](https://github.com/ngocnhanvo/beast-arena/issues/1) and its own lightweight agent orchestration Actions workflow `.github/workflows/jade-agent-bridge.yml` installed at private `5dbbe4b2b4ef8f9f511748a1fe62d709f4dc` (docs follow-up `ae071b37648b099e4d9f31860c4540f7f956c720`).
- A manually owner-authorized run from PRIVATE repo Actions performs Codex source edit → independent GPT API review and Issue comment → Codex second edit → draft PR, bounded 2 Codex + 1 GPT call. No copy/paste needed after activating. NOT the same current ChatGPT conversation or interactive Codex Cloud account; uses OpenAI API under private GitHub secret.
- Workflow source/private Issue/PNG/ASE and owner MP4 MUST remain private. Public actions repo stays separate for compiled Godot/LibreSprite/Pages/Chromium; new PRIVATE bridge must NOT trigger public CI until human-authorized source integration.
- **Known blockers**: no evidence private Actions secret `BEAST_AGENT_OPENAI_API_KEY` configured, new bridge workflow run successful, ChatGPT delegate feedback or Codex draft PR. Owner must add separately billed API key and allow Actions-created draft PR, then press Run workflow (default Issue #1).
- Earlier compiled source `a1d7088` Godot+Pages #45869792252, pinned LibreSprite #45869792258, Chromium #45870099632 attempt2 PASS are OLD art. Latest public Godot #45885063773 PASS, browser #45885316036 FAIL pre-Jade Physics V2 J-key. Do not label the unstarted agent art visually accepted.
- After real PR and owner-approved preview integration, PUBLIC CI must verify exact private SHA, pinned source/toolchain, Pages and Playwright on only https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ . Art quality stays PENDING_OWNER_ART under autocheck:false.

**Trạng thái: PARTIAL — chưa hoàn tất.**
