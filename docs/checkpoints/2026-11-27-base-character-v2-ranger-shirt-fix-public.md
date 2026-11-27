# 2026-11-27 — Base Character v2 Ranger/Hybrid shirt corrected; native source CI PASS

## Root cause
Owner screenshot showed HYBRID/LEFT/frame5 green top hiding arms. PRIVATE equipment authoring `draw_top` had Ranger garment polygon too wide and long (hip+8), rendered above source arm pixels while gloves were on top. HYBRID references Ranger top, so it inherited the defect. This was a source-art occlusion error, **not** Godot physics or animation timing.

## Fix and independently validated evidence
- PRIVATE source change `0be70455dc7cbc439ab21459c8e22c2134983a71`, checkpoint-only newer branch HEAD `b1403c8c4db26b02d18e33cde3dd981767cbe4f8`. Existing PRIVATE Draft PR #4 stays DRAFT and unmerged; Jade Draft PR #2 remains untouched.
- New fitted Ranger upper-body vest, protected original arms/skin with 1px outline, hem no lower than hip+4, unchanged six original body poses. Hybrid inherits its corrected top automatically. Dedicated `validate_tunic_occlusion` guard rejects old oversized tunic even with rehashed manifest and atlas.
- Actual isolated [GitHub Actions #45996680515](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45996680515) **COMPLETED SUCCESS**, exact PRIVATE source pin `0be70455dc7cbc439ab21459c8e22c2134983a71`: **11/11** Python tests and official pinned LibreSprite v1.3 independent RGBA export for Neutral/Aegis/Ranger/Hybrid, 6 cels x 9 layers, **RGBA_DIFF=0**.
- PUBLIC workflow updated metadata only (old 9->11) and was re-run at [#45996751870](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45996751870): **COMPLETED SUCCESS** (confirm exact current run job logs if further triage).
- Locally Chromium canvas source-preview 4 skins x right/left = **8/8 exact pixel** comparisons, 0 JS errors; cannot equate to Godot Web gameplay E2E. Offline preview updated and delivered to owner.

## Boundary / pending
Only source art / CI. No actual Godot profile integration, production Pages game deployment, human owner art acceptance, or in-game browser E2E. Owner `autocheck:false` visually decides art. Keep one canonical eventual live game URL `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/`. Next: owner reviews Ranger/Hybrid loop, then exact game build only after explicit approval. Do not auto-merge.

**Trạng thái: PARTIAL — chưa hoàn tất.**
