# 2026-11-27 - Base Character v1 modular skin pilot (private art source only)

PRIVATE game source branch feat/pose-locked-sprite-studio, Draft PR #4, now contains original native 480x80 six-pose transparent Base Character atlas plus reusable PNG source generator with six visual slot masks and three example palette skins. The full owner-side local bundle contains original concept art, 6x layered editable Aseprite and OpenRaster source, run GIFs, and 4 locally passing regression tests. No copied Nekketsu reference art is committed; the new six poses are independent designs and have not been proven joint-locked to the external reference.

PRIVATE main starting checkpoint 48dc2119981f26e9f010b279ff2520af99b2f99b; PUBLIC main starting checkpoint c72335df77237580e88066749a3411b58b5494a6. Existing Jade 8+8 Draft PR #2 remains separate; isolated source QA #45942733770 PASS does not cover this Base Character.

No PUBLIC pipeline source, workflow or Pages published game has been modified by this docs-only draft. Source-only local alpha-mask/multiple-color checks are not Godot, Playwright or owner visual signoff. The new char's native .aseprite authoring format still needs independent LibreSprite roundtrip. Recolor masks do not reconstruct anatomy under clothes or permit new jacket/armor shape automatically.

NEXT: owner review of Base Character loop, manually annotate true joints/feet, test real Aseprite/LibreSprite, and only after specific source/game integration approval build/deploy/test canonical https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/ with exact SHA and real Chromium screenshots. Owner autocheck:false; no autonomous merge.

Trạng thái: PARTIAL — chưa hoàn tất.
