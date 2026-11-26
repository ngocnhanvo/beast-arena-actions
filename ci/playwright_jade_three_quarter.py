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
            result.update({
                "status": "PASS_TECHNICAL_OWNER_ART_PENDING",
                "source_sha": start.get("source_sha"),
                "pipeline_sha": start.get("pipeline_sha"),
                "build_run_id": start.get("build_run_id"),
                "short_step_guard_directions": checked,
                "foot_pivot_px": 75,
                "full_source_status": "PENDING_ART",
            })
            print("ONE CANONICAL /physics-v2/ JADE 8-DIRECTION PACE PASS: "
                  "W/S=0.30m/cel, lateral=0.38m/cel, diagonals=0.35m/cel; "
                  "motor preserved, 6x80px cels, PixelView visible; "
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
