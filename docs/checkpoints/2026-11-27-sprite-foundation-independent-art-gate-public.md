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

**Trạng thái: PARTIAL — chưa hoàn tất.**