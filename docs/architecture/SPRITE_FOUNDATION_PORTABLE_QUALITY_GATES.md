# Cross-project Sprite Foundation v1 — Architecture, migration, and engineering lesson

Date: 2026-11-27. Status: SOURCE QA prototype / art acceptance remains external.

## Verified cause of v4 false-green

The owner rejected the v4 bald mannequin in supplied frames 1/6 and 2/6. The
old `BaseCharacterV4Tests` checked **29 source/export invariants** such as
nonempty per-part layers, fixed pivot, gear blank, Aseprite/LibreSprite RGBA
parity and Godot import. The underlying v4 renderer creates stylized 2D
capsules from the same joints that its metadata tests accept. This creates a
**self-referential validation trap**: 29/29 PASS means files round-trip, not
that head/neck, shoulder, hands, shin and overall gait are aesthetically
plausible. Previous versions 3.1–3.7 repeatedly moved the error between pose
geometry, clothing and mask layers without an independent approved gold art
reference.

## Design correction

The production pipeline must have FOUR explicitly separate decisions:

1. **SOURCE** — format, PNG dimensions, required independent layers, topology
   connections, no blank/detached body, per-slot immutability, actual PNG
   composition, symlink/path safety.
2. **ANATOMY / POSE** — artist-authoritative independent landmarks and approved
   silhouettes; special rules for near/far occlusion and project style. A
   generator's own joints may detect drift, but **cannot certify its own art**.
3. **MOTION** — clip edges, 6->1 seam, planted-foot world-space drift,
   consistent body scale and stance. A source file cannot prove ground contact.
4. **RELEASE** — owner approval keyed to **exact RGBA frame hashes** and an
   independently managed signing secret. Game/engine/Web tests follow and
   cannot be substituted by any art-source gate.

Sprite Foundation owns only the reusable QA implementation; every game
supplies its own `sprite_manifest.json` adapter and independently approved
reference art. No project-specific `80px`, `6 poses`, human proportions,
Beast Arena repo paths or Godot APIs appear in the library.

## Working examples

- Test project A: 32x32, 4 frames, original synthetic 3-part actor.
- Test project B: 64x64, 8 frames, independent synthetic 3-part actor.
- Real PRIVATE Beast Arena: 80x80, 6 frames, 17 body parts, 14 empty gear
  slots, 16 declared anatomical connections, six provisional head/torso ratio
  warnings; `structure_status=PASS`, `visual_review_status=REJECTED`,
  `release_status=BLOCKED`. This is **not** a repaired artwork.
- Negative cases: part detached while final PNG is recomposited to match,
  stale frame, part missing, gear in neutral, unapproved source/secret,
  out-of-range anchor, path traversal, changed pixels after owner approval.

## Acceptance rules for future cheap agents

- An agent receives one independently versioned pose+part+gear work packet.
- The agent cannot change acceptance criteria or secretly re-sign approval.
- Missing external reference or explicit owner rejection is **blocking**, not
  just a warning. No fake accepted reference may be synthesized from bad art.
- Pose and painter are separate; body art first, clothes later.
- Each art change invalidates previous pixel approval. Reviewer/owner
  acceptance is granted only on the actual artifact the user saw.
- Reuse common Python CLI across new games; do not duplicate the engine in
  each project. Only the adapter/profile changes.

## Immediate follow-up (not art-complete)

1. Owner/artist creates six true neutral poses with readable head-neck, shoulders,
   elbows, pelvis, knees and bare feet from an independently reviewed style sheet.
2. Add a project-approved body-ratio profile, per-frame front/back occlusion
   and leg-foot world-space contact track (currently unverified).
3. Re-run generic structure QA, owner six-frame loop acceptance, signed exact
   source approval and then one independent gear stress test.
4. Only then consider >8 individually authored clip compatibility and
   actual game/Web E2E. Jade, gameplay, Pages stay untouched now.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## Implementation lesson — external approval must cover editable source

The original approval v1 HMAC bound only the visible flattened RGBA cels,
not the hidden anatomy layers or independent motion and topology contract.
A cheap/automated agent could edit an occluded part without affecting final
PNG bytes and retain a previously signed approval. Changing manifest claims
would similarly avoid invalidation. This is **source-provenance failure**,
not an art generator problem.

**Verified code fix:** owner-approval-v2 seals `source_contract_sha256`
derived from full ordered source layer RGBA, exact composite frame hashes
and the canonical manifest (including project geometry and motion claims).
V1 signatures are rejected, not silently grandfathered. Three adversarial
tests simulate hidden-source edits, metadata edits and a valid legacy HMAC.
The tool remains engine/model/project independent; no visual aesthetic
judgment is invented by hashes. The signing operation stays human-owned
and is never invoked by CI.

Future migration: replace prior approval only after the actual artist has
reviewed the current revision; require frame/loop/foot contact evidence, and
tie any final gameplay integration to exact repo revisions. The protected v4
source remains visually rejected and unreleased.
