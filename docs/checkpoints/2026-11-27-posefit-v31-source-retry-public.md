# 2026-11-27 - Six-pose running rig V3.1 reference-guided retry (ART PENDING)

Owner requested one real attempt to correct comical skeleton motion and expects an honest VISUAL_FAIL if movement is still wrong.
PRIVATE Draft PR #5 source implementation 5fa61627e0de17f2b9fdd12d6a04945b3dd8ed9f under tools/pose_lock/base_character_v3/pose_fit_revision/; base game and Jade unchanged.
Reopened user-provided original 242x60 six-pose running strip locally. Original third-party reference image and side-by-side stay LOCAL ONLY, no copied image pixels in PRIVATE/PUBLIC GitHub sources or CI artifacts.
New six artist-estimated pose landmarks (NOT automatically recovered joints), fixed two-bone IK, anti-flip bend hints, near/far counterphase, and actual world-space planted-ankle constraint in the solver for phase pairs 0/1 near and 3/4 far. Preview root-world stride assumed 5px per cel; NOT measured from reference or Godot motor.
Local tests 17/17 PASS incl. negative foot-slip, bad knee/elbow IK branch and 6->1 seam. Numerically: planted sole world drift 0px, worst pose-key joint jump 14.56px incl. 6->1, upper-arm max angular steps about 80 and 82 degrees; thigh max 103 and 93 degrees. Those large motions are STILL subject to user quality review.
Offline Chromium HTML preview verified slider, mirror, foot indicators and no JS exception; not real Godot gameplay E2E.
PUBLIC isolated workflow branch ci/base-character-v31-reference-fit and commit 2db1b44a23379561dead4ea7e59614583b340bf9, Actions run https://github.com/ngocnhanvo/beast-arena-actions/actions/runs/46005977392. At checkpoint writing status PENDING TERMINAL, verify end and logs before marking technical PASS.

Do not infer realistic gait from numerical correctness. LANDMARKS_ESTIMATED / VISUAL_PENDING_OWNER. If owner rejects GIF, mark VISUAL_FAIL and stop scaling outfits without artist-approved source poses; preserve main and Jade Draft PR #2. No merge, build, Pages deploy or actual game E2E. Owner autocheck:false.

Trạng thái: PARTIAL — chưa hoàn tất.
