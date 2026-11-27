# 2026-11-28 — Original FK/IK sprite Skill, public read-only 15-test proof

## Exact source evidence
PRIVATE new `.agents/skills/beast-arena-motion-logic/` Skill and root AGENTS.md / ART_PIPELINE.md updates, tested code SHA `288a25acd1268d64fcc9a64658bc92057e72fe5b`. This Private Skill was developed independently and does not vendor third-party character art or source.

PUBLIC read-only workflow `.github/workflows/sprite-motion-logic.yml` tested exact SHA `c9f972ae83bca01aec0bc77a7a7888b840f8aea6` in [GitHub Actions #46042922208](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46042922208), **COMPLETED SUCCESS**, actual job `140654917257`.

Runner console `Ran 15 tests` / OK, `MOTION_IK_FK_15_ADVERSARIAL_TESTS_PASS` and `MOTION_RIG_6_PHASES_24_SUBFRAMES_STANCE_LOCK_PASS_ART_BLOCKED`.

## What is actually validated
- Six 80×80 deterministic mockup poses, 24 generated interpolated rig samples, JSON contact phase contract and 6-frame GIF produced in private runner temp only.
- 2-bone IK fixed-length legs, FK fixed-length arms, stable anatomical left/right identities and no silent knee-bend branch flip.
- RIGHT stance in frames 1/2 with exact world-space toe lock and rear toe-off at frame3; LEFT stance at frames4/5 and opposite toe-off frame6; crossing arm action and world-space 6→1 local wrap.
- Adversarial tests reject incorrectly relabeled stance, foot sliding, raised former stance leg in front, backwards swinging opposite leg, arm teleport, altered joint lengths and unreachable IK.
- Owner `autocheck:true` authorized self-QA, but **not** blanket game/art acceptance; code includes `visual_quality=NOT_REVIEWED`, `art_release=BLOCKED`, `gameplay_e2e=NOT_RUN`.

## Scope and next action
PUBLIC repo contains only the isolated workflow and this checkpoint. It does not publish private generated PNG/GIF/sprites or alter production Pages/Jade. Private Draft PR #16 and public Draft PR #15 remain unmerged. The new Skill is not production art; replace underpaint with original anatomically credible authored sprite on identical pose contract, self-review at 1× and zoom, separately validate LibreSprite/Godot/actual game Web foot trajectories, get owner art approval before release.

**Trạng thái: PARTIAL — chưa hoàn tất.**
