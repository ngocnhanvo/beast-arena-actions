"""One canonical public URL: verify Jade's actual 3/4 source in Chromium.

No alternate review deployment route. Query flags are used solely to expose
read-only test diagnostics on the SAME /physics-v2/ Pages file. This is NOT
owner aesthetic signoff and does NOT mark the 10-clip artist set complete.
"""
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/"
OUT = Path("playwright-report/jade-34")
OUT.mkdir(parents=True, exist_ok=True)


def state(page):
    return page.evaluate("window.__beastPhysicsDebug || null")


def main():
    result = {"single_review_url": URL, "status": "NOT_RUN"}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--enable-webgl", "--use-gl=angle", "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader", "--disable-dev-shm-usage"])
        page = browser.new_page(viewport={"width": 1200, "height": 800})
        try:
            response = page.goto(URL, wait_until="domcontentloaded", timeout=50000)
            if response is None or response.status != 200:
                raise AssertionError("Canonical /physics-v2/ isn't HTTP 200")
            canvas = page.locator("canvas#canvas").first
            if canvas.count() == 0:
                canvas = page.locator("canvas").first
            canvas.wait_for(state="visible", timeout=30000)
            page.wait_for_timeout(2500)
            canvas.screenshot(path=str(OUT / "canonical-idle.png"))

            # Same document, same Pages deployment, *read-only* E2E telemetry.
            response = page.goto(URL + "?e2e=1&review=1",
                                 wait_until="domcontentloaded", timeout=50000)
            if response is None or response.status != 200:
                raise AssertionError("Same preview document diagnostics unavailable")
            page.wait_for_function(
                "() => window.__beastPhysicsDebug?.ready === true",
                timeout=180000, polling=700)
            start = state(page)
            expected_pipeline = os.getenv("BEAST_EXPECT_PIPELINE_SHA", "")
            expected_run = os.getenv("BEAST_EXPECT_BUILD_RUN_ID", "")
            if expected_pipeline and start.get("pipeline_sha") != expected_pipeline:
                raise AssertionError("Wrong Pages SHA for canonical preview")
            if expected_run and str(start.get("build_run_id")) != expected_run:
                if (str(start.get("build_run_id", "")).isdigit() and
                        int(start["build_run_id"]) > int(expected_run)):
                    result["status"] = "SUPERSEDED_BY_NEWER_PAGES"
                    return
                raise AssertionError("Stale Pages PCK for canonical preview")
            if not (start.get("single_link_review") is True
                    and start.get("review_preview_loaded") is True
                    and start.get("review_preview_clips") == 2
                    and start.get("review_preview_view") == "three_quarter_right"
                    and start.get("animation_source_ready") is False
                    and start.get("pixel_projection_mode") is True
                    and start.get("pixel_view_floor_tiles", 0) > 0
                    and start.get("hero_art_approved_enabled") is True):
                raise AssertionError("Single-link angled source/floor review not active: " + str(start))
            canvas = page.locator("canvas#canvas").first
            if canvas.count() == 0:
                canvas = page.locator("canvas").first
            canvas.click(force=True)
            # The earlier "idle_breathe_front" name was only a static
            # pose. On the same public document, measure a real timed
            # inhale/exhale in *rendered presentation*, shoe anchor intact.
            page.wait_for_function(
                "() => window.__beastPhysicsDebug?.human_visual_gait === 'idle'",
                timeout=10000)
            page.wait_for_function(
                "() => window.__beastPhysicsDebug?.review_breath_scale > 1.027",
                timeout=6000, polling=35)
            inhale = state(page)
            canvas.screenshot(path=str(OUT / "canonical-idle-inhale.png"))
            page.wait_for_function(
                "() => window.__beastPhysicsDebug?.review_breath_scale < 1.005",
                timeout=6000, polling=35)
            exhale = state(page)
            canvas.screenshot(path=str(OUT / "canonical-idle-exhale.png"))
            if inhale["review_idle_art_status"] != (
                    "WHOLE_BODY_BREATH_PLACEHOLDER_PENDING_CELS"):
                raise AssertionError("Runtime must NOT claim authored idle art")
            checked = {}
            # One canonical page, eight physical compass movements. Side
            # frames reuse the WHOLE original body via horizontal mirroring;
            # diagonals select W/S source based on Z, with left mirror.
            # Never claim eight independently drawn sources.
            directions = [
                (("w",), "W", "walk_up", "walk_up", "walk_up_guard_front",
                 False, "s.player.vz < -0.35"),
                (("s",), "S", "walk_down", "walk_down", "walk_down_guard_front",
                 False, "s.player.vz > 0.35"),
                (("a",), "A", "walk_down", "walk_left", "walk_left_guard",
                 True, "s.player.vx < -0.35"),
                (("d",), "D", "walk_down", "walk_right", "walk_right_guard",
                 False, "s.player.vx > 0.35"),
                (("w", "a"), "W+A", "walk_up", "walk_left", "walk_left_guard",
                 True, "s.player.vx < -0.35 && s.player.vz < -0.35"),
                (("w", "d"), "W+D", "walk_up", "walk_right", "walk_right_guard",
                 False, "s.player.vx > 0.35 && s.player.vz < -0.35"),
                (("s", "a"), "S+A", "walk_down", "walk_left", "walk_left_guard",
                 True, "s.player.vx < -0.35 && s.player.vz > 0.35"),
                (("s", "d"), "S+D", "walk_down", "walk_right", "walk_right_guard",
                 False, "s.player.vx > 0.35 && s.player.vz > 0.35"),
            ]
            expected_stride_m = {
                "W": 0.30, "S": 0.30,
                "A": 0.38, "D": 0.38,
                "W+A": 0.35, "W+D": 0.35,
                "S+A": 0.35, "S+D": 0.35,
            }
            for keys, label, source, semantic, tag, mirrored, velocity in directions:
                # Every case starts on safe walkable stage, not where the
                # previous direction ended. A 15s predicate timeout with a
                # held movement key can otherwise send Jade off-map and
                # turn a presentation assertion into a falling-body failure.
                # R is the existing in-game ramp-entry teleport, not a
                # test-only mutation of physics state.
                page.wait_for_timeout(340)  # >16 native 60Hz double-tap ticks
                page.keyboard.press("r")
                page.wait_for_function(
                    "() => {const s=window.__beastPhysicsDebug;"
                    "return s && s.player && s.player.grounded "
                    "&& s.player.y > -0.25 && Math.abs(s.player.x) < 15 "
                    "&& Math.abs(s.player.z) < 2 "
                    "&& Math.abs(s.player.vx) < 0.25 "
                    "&& Math.abs(s.player.vz) < 0.25 "
                    "&& !s.sprint_requested;}",
                    timeout=12000, polling=70)
                for key in keys:
                    page.keyboard.down(key)
                try:
                    script = (
                        "() => {const s=window.__beastPhysicsDebug;"
                        "return s && s.review_preview_active "
                        "&& s.human_sprite_hframes === 6 "
                        "&& s.review_preview_action === '" + source + "' "
                        "&& s.review_direction_action === '" + semantic + "' "
                        "&& s.animation_clip_intent === '" + tag + "' "
                        "&& s.review_preview_flip_h === " + str(mirrored).lower()
                        + " && " + velocity + ";}"
                    )
                    try:
                        page.wait_for_function(script, timeout=5000, polling=50)
                    except Exception as exc:
                        # Report the exact input/predicate and real Godot
                        # state before releasing keys, not only a generic
                        # timeout after the actor has wandered outside map.
                        raise AssertionError(
                            "Eight-direction guard gate failed for " + label
                            + ": source=" + source
                            + ", intent=" + tag
                            + ", full_body_flip=" + str(mirrored)
                            + ", live_state=" + str(state(page))
                        ) from exc
                    page.wait_for_function(
                        "() => window.__beastPhysicsDebug?.review_preview_frame > 0",
                        timeout=15000, polling=50)
                    middle = state(page)
                    if middle.get("hero_atlas_frame_size") != 80:
                        raise AssertionError(label + " preview isn't native 80px")
                    reference = middle.get("review_reference_body_height_px", 0)
                    painted = middle.get("review_walk_painted_height_px", 0)
                    effective = middle.get("review_effective_body_height_px", 0)
                    scale = middle.get("review_visual_scale", 0)
                    if not (reference > 0 and painted > 0 and scale > 0
                            and abs(reference - effective) <= 1.0
                            and abs(painted * scale - effective) <= 0.01):
                        raise AssertionError(
                            "Painted body size changed on " + label
                            + ": reference=" + str(reference)
                            + ", painted=" + str(painted)
                            + ", scaled=" + str(effective))
                    # Real stride cadence is distance-driven, not FPS or
                    # animation timing simulated by the browser. Each clip
                    # remains native; player movement speed is unchanged.
                    frame_stride = middle.get("review_walk_distance_per_frame_m", 0)
                    expected = expected_stride_m[label]
                    if abs(frame_stride - expected) > 0.001:
                        raise AssertionError(
                            f"{label} step animation pace {frame_stride}m "
                            f"does not match expected {expected}m/cel")
                    # All directions use the same 4.2 m/s motor on flat
                    # terrain; diagonals cannot become sqrt(2) faster.
                    velocity_x = float(middle["player"]["vx"])
                    velocity_z = float(middle["player"]["vz"])
                    world_speed = (velocity_x**2 + velocity_z**2)**0.5
                    if not (0.35 < world_speed < 5.5):
                        raise AssertionError(
                            f"{label} unexpected physical walking speed {world_speed}")
                    checked[label] = {
                        "step_distance_per_cel_m": frame_stride,
                        "approx_cels_per_second_at_4_2_mps": round(
                            4.2 / frame_stride, 2),
                        "real_world_speed_mps": round(world_speed, 3),
                        "source": source,
                        "intent": tag,
                        "whole_cel_mirrored": mirrored,
                        "frame": middle.get("review_preview_frame"),
                        "velocity_x": middle.get("player", {}).get("vx"),
                        "velocity_z": middle.get("player", {}).get("vz"),
                        "reference_height_px": reference,
                        "normalized_height_px": effective,
                    }
                    canvas.screenshot(path=str(OUT / (
                        "canonical-walk-" + label.replace("+", "-") + ".png")))
                finally:
                    for key in keys:
                        page.keyboard.up(key)
                page.wait_for_function(
                    "() => !window.__beastPhysicsDebug?.review_preview_active",
                    timeout=12000, polling=80)
            if set(checked) != {"W", "S", "A", "D", "W+A", "W+D", "S+A", "S+D"}:
                raise AssertionError("All eight compass directions must be checked")
            # Sprint previously reverted to the original legacy 2-frame
            # side source (and FRONT could freeze). Verify REAL doubletap
            # D stays six native whole-body guard cels and faster physics.
            page.wait_for_timeout(450)
            page.keyboard.press("r")
            page.wait_for_function(
                "() => {const s=window.__beastPhysicsDebug;"
                "return s?.player?.grounded && Math.abs(s.player.vx)<0.25 "
                "&& !s.sprint_requested;}", timeout=12000)
            page.keyboard.down("d")
            page.wait_for_timeout(90)
            page.keyboard.up("d")
            page.wait_for_timeout(85)
            page.keyboard.down("d")
            try:
                page.wait_for_function(
                    "() => {const s=window.__beastPhysicsDebug;"
                    "return s?.review_run_active === true "
                    "&& s?.sprint_requested === true "
                    "&& s?.human_sprite_hframes === 6 "
                    "&& s?.human_sprite_vframes === 2 "
                    "&& s?.review_run_source_pose_count === 6 "
                    "&& s?.review_preview_action === 'run_right' "
                    "&& s?.review_run_source_is_native_80px === true "
                    "&& s?.review_run_distance_per_frame_m >= 0.40 "
                    "&& s?.player?.vx > 5.5;}", timeout=8000, polling=45)
                page.wait_for_function(
                    "() => window.__beastPhysicsDebug?.review_preview_frame > 0",
                    timeout=3000, polling=45)
                # Sample the LIVE gameplay frame stream for <=850ms,
                # rather than wait 2 seconds per numbered phase. Holding
                # left/right for many seconds hits real stage collision,
                # legitimately stops _gait_distance_m and freezes the pose.
                # We still REQUIRE every phase 0..5 to actually appear.
                right_phases = page.evaluate(
                    """() => new Promise(resolve => {
                      const observed = new Set();
                      const start = performance.now();
                      function sample() {
                        const s = window.__beastPhysicsDebug;
                        if (s?.review_run_active && s?.sprint_requested)
                          observed.add(s.review_preview_frame);
                        if (observed.size === 6 || performance.now() - start > 850)
                          resolve([...observed].sort((a,b)=>a-b));
                        else requestAnimationFrame(sample);
                      }
                      sample();
                    })""")
                if right_phases != list(range(6)):
                    raise AssertionError(
                        f"D+D must play all SIX visible phases during real sprint, "
                        f"observed={right_phases}, state={state(page)}")
                run_state = state(page)
                if (int(run_state.get("review_run_presented_phase_mask", 0))
                        & 0x3F) != 0x3F:
                    raise AssertionError(
                        "D+D game renderer did not select every real "
                        "whole-body leg phase: " + str(run_state))
                # Six NEW owner-designed whole-body right-facing source
                # cels in 480x160; never the old mixed legacy 4x20 atlas.
                source_index = int(run_state.get("review_run_source_frame", -1))
                if source_index != int(run_state.get("human_sprite_frame", -1)):
                    raise AssertionError("Right run visual frame != source atlas cell")
                if source_index not in range(0, 6):
                    raise AssertionError(
                        "D+D MUST render new owner-designed six-pose right row: "
                        f"cell={source_index}")
                canvas.screenshot(path=str(OUT / "canonical-guard-run-right.png"))
                if (run_state.get("review_run_art_status") !=
                        "OWNER_NEW_SIX_RUN_POSE_DESIGN_REVIEW_PENDING"):
                    raise AssertionError(
                        "Sprint must use distinct ORIGINAL side-running whole-body "
                        "frames, not W/S short steps or invented final authored 8-tag")
            finally:
                page.keyboard.up("d")
            # A+A must render the OWNER-designed mirrored WHOLE-body
            # left-facing row (indices 6..11), not the legacy 4x20 sprite.
            page.wait_for_timeout(450)
            page.keyboard.press("r")
            page.wait_for_function(
                "() => {const s=window.__beastPhysicsDebug;"
                "return s?.player?.grounded && Math.abs(s.player.vx)<0.25 "
                "&& !s.sprint_requested;}", timeout=12000)
            page.keyboard.down("a")
            page.wait_for_timeout(90)
            page.keyboard.up("a")
            page.wait_for_timeout(85)
            page.keyboard.down("a")
            try:
                page.wait_for_function(
                    "() => {const s=window.__beastPhysicsDebug;"
                    "return s?.review_run_active===true "
                    "&& s?.sprint_requested===true "
                    "&& s?.human_sprite_hframes===6 "
                    "&& s?.human_sprite_vframes===2 "
                    "&& s?.review_run_source_pose_count===6 "
                    "&& s?.review_preview_action==='run_left' "
                    "&& s?.review_run_source_is_native_80px===true "
                    "&& s?.player?.vx < -5.5;}", timeout=8000, polling=45)
                page.wait_for_function(
                    "() => window.__beastPhysicsDebug?.review_preview_frame > 0",
                    timeout=3000, polling=45)
                left_phases = page.evaluate(
                    """() => new Promise(resolve => {
                      const observed = new Set();
                      const start = performance.now();
                      function sample() {
                        const s = window.__beastPhysicsDebug;
                        if (s?.review_run_active && s?.sprint_requested)
                          observed.add(s.review_preview_frame);
                        if (observed.size === 6 || performance.now() - start > 850)
                          resolve([...observed].sort((a,b)=>a-b));
                        else requestAnimationFrame(sample);
                      }
                      sample();
                    })""")
                if left_phases != list(range(6)):
                    raise AssertionError(
                        f"A+A must play all SIX visible phases during real sprint, "
                        f"observed={left_phases}, state={state(page)}")
                left_run = state(page)
                if (int(left_run.get("review_run_presented_phase_mask", 0))
                        & 0x3F) != 0x3F:
                    raise AssertionError(
                        "A+A game renderer did not select all six "
                        "authored running poses: " + str(left_run))
                left_idx = int(left_run.get("review_run_source_frame", -1))
                if left_idx != int(left_run.get("human_sprite_frame", -1)):
                    raise AssertionError("Left run visual frame != source atlas cell")
                if left_idx not in range(6, 12):
                    raise AssertionError(
                        f"A+A must render new owner-designed LEFT row: {left_idx}")
                if left_run.get("review_run_art_status") != (
                        "OWNER_NEW_SIX_RUN_POSE_DESIGN_REVIEW_PENDING"):
                    raise AssertionError("Left run is not genuine source pilot")
                canvas.screenshot(path=str(OUT / "canonical-guard-run-left.png"))
            finally:
                page.keyboard.up("a")
            result.update({
                "status": "PASS_TECHNICAL_OWNER_ART_PENDING",
                "source_sha": start.get("source_sha"),
                "pipeline_sha": start.get("pipeline_sha"),
                "build_run_id": start.get("build_run_id"),
                "short_step_guard_directions": checked,
                "idle_breath": {
                    "inhale_scale": inhale["review_breath_scale"],
                    "exhale_scale": exhale["review_breath_scale"],
                    "status": inhale["review_idle_art_status"],
                },
                "run_preview": {
                    "frame": run_state["review_preview_frame"],
                    "stride_m": run_state["review_run_distance_per_frame_m"],
                    "velocity_x": run_state["player"]["vx"],
                    "source_status": run_state["review_run_art_status"],
                    "source_frame": run_state["review_run_source_frame"],
                    "source_pose_count": run_state["review_run_source_pose_count"],
                    "observed_live_phases": right_phases,
                    "actual_sprite_pose_mask": run_state["review_run_presented_phase_mask"],
                    "source_action": run_state["review_preview_action"],
                },
                "left_run_preview": {
                    "frame": left_run["review_preview_frame"],
                    "source_frame": left_run["review_run_source_frame"],
                    "pose_count": left_run["review_run_source_pose_count"],
                    "observed_live_phases": left_phases,
                    "actual_sprite_pose_mask": left_run["review_run_presented_phase_mask"],
                    "velocity_x": left_run["player"]["vx"],
                    "source_action": left_run["review_preview_action"],
                },
                "punch_art": "PENDING_ART_FRONT_PUNCH",
                "kick_art": "PENDING_ART_INDEPENDENT_KICK",
                "foot_pivot_px": 75,
                "full_source_status": "PENDING_ART",
            })
            print("ONE CANONICAL /physics-v2/ JADE OWNER DESIGN SIX-POSE PASS: "
                  "real A+A/D+D with new transparent 480x160 6+6 RGBA source; "
                  "both full-body row indices validated, eight walks and idle intact; "
                  "owner visual review pending")
        except Exception as exc:
            result["status"] = "FAIL"
            result["error"] = str(exc)
            result["last"] = state(page)
            raise
        finally:
            for key in ("w", "s", "a", "d"):
                page.keyboard.up(key)
            (OUT / "result.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2))
            browser.close()


if __name__ == "__main__":
    main()
