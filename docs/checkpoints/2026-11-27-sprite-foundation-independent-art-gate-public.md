# 2026-11-27 — Sprite Foundation cross-project reusable independent gate

PUBLIC repo contains **only original generic Python source, unit tests and
synthetic toy project pixels created at runtime**, no PRIVATE Beast Arena art.
Private adapter binds existing v4 author's 17 parts and 14 empty slots.
This is a shared package usable from any game/project with different number
of frames/canvas sizes, not a Beast Arena-specific art patch.

## Technical evidence

- Generic core uses Pillow only, path-sandboxing, composited PNG parity,
  inter-part pixel overlap/detachment, source/pose anchor drift, blank gear,
  optional per-project style ratios, independent owner-review SHA signature.
- Local original synthetic 32px/4-frame and 64px/8-frame tests PASS, incl.
  11 positive and negative tests that detect actual shifted masks and
  stale review fingerprint. New CI must verify exact commit/runner.
- PRIVATE owner-rejected Base v4 adapter expected to return
  `STRUCTURE PASS / VISUAL REJECTED / RELEASE BLOCKED` plus six optional
  head:torso ratio triage warnings. All six are provisional **review** flags,
  not independently signed biological proportions.
- Legacy #46028570106 LibreSprite/Godot source PASS is NOT art approval.

## Boundary and next step

No game Pages or general release. No PRIVATE raw image uploads, no secrets
in PUBLIC logs. CI must complete and read actual log before technical PASS.
Then owner creates a genuinely reviewed neutral silhouette and motion set;
public tool does NOT generate or beautify art. Future apps can import
`packages/sprite-foundation` and write only a thin project manifest adapter.


## Terminal source QA evidence

- PUBLIC generic package tested at workflow SHA `4db7a95b5b760ecf0230a7c376498eb42e318fda`, PRIVATE v4 adapter immutable SHA `a57a723088595e2153a6304aa1c4f17c631d41c5`, [GitHub Actions #46031026676](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46031026676) **COMPLETED SUCCESS**. Job `140614548571` actual log `Ran 11 tests / OK` + `SPRITE_FOUNDATION_GENERIC_11_TESTS_PASS`, independent project fixtures 32×32×4 and 64×64×8. Job `140614654175` actual log `Ran 1 test / OK` + `V40_OWNER_REJECTED_ART_HARD_BLOCK_SOURCE_VALID`, six original v4 frames source checked without publishing any private art files.
- First workflow #46030876976 failed YAML pre-validation because unquoted step name colon. Quoted YAML name and reran full pipeline. The final `SUCCESS` proves the validator *correctly blocks owner-rejected art*, not that actual mannequin artwork has improved.
- v4 source audit `STRUCTURE PASS / VISUAL REJECTED / RELEASE BLOCKED`, 6 provisional style-ratio review warnings and 5 explicit gates. No auto-sign, no uploaded private image, no merge, no Pages release or Godot game E2E. Visual body anatomy still needs reauthoring and explicit owner approval.

**Trạng thái: PARTIAL — chưa hoàn tất.**

## 2026-11-27 continuation: source-contract approval v2 (pending terminal CI)

Observed security/quality defect in public v0.1: approval v1 signed ONLY
final flattened RGBA output. Repainting a source body layer that is hidden by
another layer could preserve the final frame hash and reuse a stale owner
signature. Furthermore, changing the manifest motion claims could leave a
v1 signature valid. This is NOT acceptable for reusable cross-project agent
workflows where generated source and independently approved evidence must not
share authority.

Change in this draft branch:
- `audit.py`: include a canonical SHA-256 fingerprint of the ENTIRE manifest,
  individual body/neutral-gear RGBA layers, frame order and final frames.
  HMAC v2 signs that fingerprint and final hashes, and v1 is fail-closed.
- `cli.py`: human-only owner-sign signs report's v2 source contract.
- `tests/test_foundation.py`: three additional adversarial tests for invisible
  source-layer modification, manifest change and legacy signature rejection.
- Package README explains invalidating old approval and human-only re-signing.
- No new artwork, no renderer, Jade, game physics, Pages or main merge.

The code commits are `adcccde`, `a107f58`, `f71e7a6` and docs `7fc851c`.
The branch workflow is triggered automatically by package modifications.
Do not mark new revision PASS until actual terminal Actions run and job logs
show full 14/14 generic tests and v4 rejected-source adapter gate.

Next: inspect terminal CI, then update this checkpoint with exact run and SHA.
Keep PRIVATE v4 rejected, owner art signoff required. No deployment.

**Trạng thái: PARTIAL — chưa hoàn tất.**


## Terminal verified continuation — approval-v2

**PUBLIC CI #46033318504 COMPLETED SUCCESS** at exact workflow/code SHA
`39e451b7abdc98757c9b6e6b71d05894c7a8049b`. Real job IDs:
- `140622346341`: Generic 14/14 adversarial tests PASS, including three
  new attacks against signed hidden body, manifest mutation, and legacy HMAC.
- `140622503783`: PRIVATE immutable v4 adapter/source regression 1/1 PASS;
  correctly outputs `V40_OWNER_REJECTED_ART_HARD_BLOCK_SOURCE_VALID`.
- Prior complete code revision #46033190502 also SUCCESS; one intermediate
  partial commit #46033147416 failed and some queued superseded pushes were
  cancelled. Do not use those as release evidence.

Code/docs on this PUBLIC draft only. Source SHA pin for PRIVATE adapter
remains `a57a723088595e2153a6304aa1c4f17c631d41c5`.
The neutral v4 ART is still **REJECTED_BY_OWNER**, not repaired; no actual
new skin, no live game QA, no merge or Pages release. Approval v2 is a
fail-closed technical security/quality contract, not art/aesthetic acceptance.

Next: separately author and obtain owner review of an anatomically sound
neutral six-pose source and real running loop, then test its exact source
under the generic validator; do not auto-sign from an agent.

**Trạng thái: PARTIAL — chưa hoàn tất.**


## Continued 2026-11-27 — reusable model-neutral motion diagnostics verified

REQUIREMENT: Do not let low-cost agents infer natural running or grounded
feet from a self-produced vector/pixel animation. Added reusable
`sprite_foundation.motion` and `sprite-foundation motion-diagnose`
across arbitrary frame counts/canvas sizes. It reads actual RGBA renders
and reports per-frame alpha silhouette bounds/centroid, lowest filled pixel
row, adjacent pixel-change fractions and a measured final→first seam
relative to internal median. It **does not infer ground contact, world
trajectory, smooth motion or visual owner acceptance**.

**PUBLIC exact CI #46035667624 COMPLETED SUCCESS**, tested SHA
`31991e608ed58f93341d215d3ad515b712ae1a73`:
- Generic job `140630471824`: `Ran 19 tests` / OK, including five
  independent synthetic motion cases for 32px/4 and 64px/8, duplicate
  frames, bottom-pixel ambiguity, empty and missing frames.
- PRIVATE old rejected v4 source job `140630659505`: `Ran 1 test` / OK;
  `V40_OWNER_REJECTED_ART_HARD_BLOCK_SOURCE_VALID`.
- Earlier interleaved pushes' runs were superseded/cancelled. Use the
  exact successful run above, not the old 14-test run.

**PRIVATE real v4.1 diagnostic** executed through independently pinned
PUBLIC isolated [#46035739118](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46035739118)
on runner SHA `232a95356100d12cc2fd6cee3e3cdf70502d9478`,
private source SHA `d363b7ae89940d9e7f3c52f443190c10140c9197`.
Measured `seam_vs_internal_median_ratio=1.0928`, painted lowest
rows `[72,72,71,72,72,72]`, NOT physical foot contacts;
`ground_contact_status=UNVERIFIED`,
`loop_art_review_status=UNVERIFIED`,
`release_authorization=NONE`. Concurrent v4.1 16/16 original
source tests, strict LibreSprite 31-layer RGBA and isolated Godot import
also PASS.

No art/style QA can be auto-approved from metrics. No owner visual review,
no game E2E, no new Pages deployment or merge. Next: actual owner review
of neutral body, then independently authored/verified motion and owner
source-contract signoff; only then enable skin and game integration.

**Trạng thái: PARTIAL — chưa hoàn tất.**
