# 2026-11-27 — Base Character v2 isolated source QA terminal SUCCESS, game not deployed

## Verified exact proof
- PRIVATE [Base Character v2 Draft PR #4](https://github.com/ngocnhanvo/beast-arena/pull/4), isolated source SHA **`86bac78dca66d24300c15d8aa5818346cb7312b9`** (separate later docs-only checkpoint).
- PUBLIC isolated workflow at `2dd6a61d097fca9457119a054102c48e2aba9d0a`, [run #45995267834](https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/45995267834) **COMPLETED SUCCESS**. Job `140492965654` terminal run and actual log inspected.
- Pinned SHA verified; `Ran 9 tests / OK`; 4/4 original Neutral/Aegis/Ranger/Hybrid equipment source manifests and mirror/anchors PASS; official SHA256-pinned LibreSprite 1.3 downloaded on runner, **STRICT RGBA_DIFF=0** for each of the four independent editable nine-layer 6-cel native Aseprite sources. No art uploaded to public artifacts or copied to public source.
- The earlier local editor download failed DNS but actual isolated CI resolved and completed; **independent native QA now PASS**, replaces any earlier note calling that gate BLOCKED.

## Technical scope, not owner/game acceptance
- The six 80×80 body poses and root position are immutable; separate whole-frame gear layers (9 transparent sublayers) make real hair/armor/glove/boot silhouette replacement possible. Neutral source matches v1 exactly, hybrid combines six source item families. Source-only local tests also PASS 9/9, including invalid drift/manifest/path tests.
- No runtime Godot code was changed, no Pages was deployed, no real gameplay Chromium E2E and no owner art approval (`autocheck:false`). Previous unrelated Jade #45942733770 PASS does not authorize merging Jade PR #2 or this Base proposal.
- GIF 85ms request is stored at 80ms playback due centisecond format; separate offline HTML demo uses 85ms. Approximate landmark/pivot annotations do not claim accurate joint physics or planted-foot identity.

## Resume
Keep PRIVATE PR #4 DRAFT, PUBLIC documentation PR #1 DRAFT, PUBLIC isolated CI branch for source validation separate. Owner reviews four GIF loops; any art edits require new native CI with pinned private SHA. After explicit integration approval, use generic fighter profile and public Godot+Pages+Chromium exact SHA validation on **only** canonical `https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/`. Do not auto-merge/deploy.

**Trạng thái: PARTIAL — chưa hoàn tất.**
