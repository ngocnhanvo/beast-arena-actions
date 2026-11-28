"""Real Chromium/SwiftShader gate for the Base-only twelve-frame fighter.

Tests true game inputs and visible pixels at the sole canonical Physics V2
game URL (query parameters are private CI instrumentation, not owner links).
Retired Jade-specific A/B assertions are intentionally not applicable.
"""
import json
import os
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/"
URL = BASE + "?e2e=1&controls=v2&pixel=1"
OUT = Path("playwright-report/base-only")
OUT.mkdir(parents=True, exist_ok=True)


def snap(page):
    return page.evaluate("window.__beastPhysicsDebug || null")


def until(page, description, predicate, timeout=7000):
    # Return the ACTUAL state that satisfied the predicate. Calling snap()
    # after wait_for_function would perform a second, asynchronous read:
    # the attack can finish in between and falsely record an empty attack ID.
    handle = page.wait_for_function(
        "() => {const s=window.__beastPhysicsDebug; return "
        "s && (" + predicate + ") ? s : false;}",
        polling=50, timeout=timeout)
    result = handle.json_value()
    if not isinstance(result, dict):
        raise AssertionError(description + ": matched state unavailable")
    return result


def main():
    report = {"url": BASE, "status": "NOT_RUN", "evidence": {}, "js_errors": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--enable-webgl", "--use-gl=angle", "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader", "--disable-dev-shm-usage"
        ])
        page = browser.new_page(viewport={"width": 1200, "height": 800})
        page.on("pageerror", lambda err: report["js_errors"].append(str(err)))
        try:
            for attempt in range(6):
                response = page.goto(URL, wait_until="domcontentloaded", timeout=50000)
                if response is not None and response.status == 200:
                    break
                page.wait_for_timeout(2500)
            else:
                raise AssertionError("Physics V2 Pages not HTTP 200")
            until(page, "Godot ready", "s.ready === true", timeout=180000)
            canvas = page.locator("canvas#canvas").first
            if not canvas.count():
                canvas = page.locator("canvas").first
            canvas.wait_for(state="visible", timeout=20000)
            canvas.click(force=True)
            start = until(page, "Base and real visible floor",
                          "s.base_fighter_count === 4 && "
                          "s.pixel_view_floor_tiles > 0 && s.player.grounded",
                          timeout=12000)
            expected_run = os.getenv("BEAST_EXPECT_BUILD_RUN_ID", "").strip()
            expected_pipeline = os.getenv("BEAST_EXPECT_PIPELINE_SHA", "").strip()
            expected_private = os.getenv("BEAST_EXPECT_PRIVATE_SHA", "").strip()
            actual_run = str(start.get("build_run_id", ""))
            if expected_run and actual_run != expected_run:
                if (actual_run.isdigit() and expected_run.isdigit()
                        and int(actual_run) > int(expected_run)):
                    report["status"] = "SUPERSEDED_BY_NEWER_PAGES"
                    report["expected_run"] = expected_run
                    report["actual_run"] = actual_run
                    return
                raise AssertionError("Stale Web PCK run " + actual_run)
            if expected_pipeline and start.get("pipeline_sha") != expected_pipeline:
                raise AssertionError("Stale Web PCK pipeline")
            if expected_private and start.get("source_sha") != expected_private:
                raise AssertionError("Private source SHA does not match release")
            if not re.fullmatch(r"[0-9a-f]{40}", start.get("source_sha", "")):
                raise AssertionError("Missing private source commit provenance")
            if not (start.get("actors") == 4
                    and start.get("base_fighter_count") == 4
                    and start.get("animation_profile_count") == 4
                    and start.get("animation_profile_id") == "base_human"
                    and start.get("animation_profile_stance") == "guard"
                    and start.get("base_idle_active") is True
                    and start.get("base_idle_frame_count") == 12
                    and start.get("base_idle_frame_duration_ms") == 100
                    and start.get("base_walk_attached_count") == 4
                    and start.get("base_punch_attached_count") == 4
                    and start.get("base_walk_frame_count") == 4
                    and start.get("base_walk_reference_frame_duration_ms") == 180
                    and start.get("visual_contract_schema") == 1
                    and start.get("visual_contract_clip") == "idle_guard_front"
                    and start.get("visual_contract_cell") == [80, 80]
                    and start.get("visual_contract_auto_fit") is False
                    and start.get("visual_contract_anatomy_pending") ==
                        "PENDING_ANATOMY_REAUTHOR"
                    and abs(float(start.get(
                        "visual_contract_meters_per_art_pixel", 0.0)) - 0.020) < 0.00001
                    and start.get("human_sprite_hframes") == 12
                    and start.get("human_sprite_vframes") == 1
                    and start.get("hero_atlas_frame_size") == 80
                    and start.get("original_hud_portraits") == 4
                    and start.get("animation_source_ready") is False
                    and start.get("review_idle_art_status")
                        == "BASE_12_AUTHORED_CELS_OWNER_APPROVED"):
                raise AssertionError("Old fighter or invalid Base texture: " + str(start))
            if abs(float(start.get("human_sprite_offset_y", 99)) + 4.0) > 0.01:
                raise AssertionError("Base planted-foot sprite offset has changed")
            if abs(float(start.get("human_physical_ground_clearance_m", 99))) > 0.25:
                raise AssertionError("Baseline real actor not grounded at sprite foot")
            report["version"] = {key: start.get(key) for key in
                                 ("source_sha", "pipeline_sha", "build_run_id")}
            report["evidence"]["pose_scale_contract"] = {
                "schema": start.get("visual_contract_schema"),
                "native_meters_per_pixel":
                    start.get("visual_contract_meters_per_art_pixel"),
                "auto_fit": start.get("visual_contract_auto_fit"),
                "known_legacy_anatomy_status":
                    start.get("visual_contract_anatomy_pending"),
            }
            canvas.screenshot(path=str(OUT / "base-idle.png"))
            seen = set()
            for _ in range(32):
                state = snap(page)
                if state and state.get("human_visual_gait") == "idle":
                    seen.add(int(state.get("human_sprite_frame", -1)))
                page.wait_for_timeout(110)
            if len(seen) < 5 or not seen.issubset(set(range(12))):
                raise AssertionError("Actual idle timer not selecting distinct cels: "
                                     + str(sorted(seen)))
            report["evidence"]["real_idle_frames_sampled"] = sorted(seen)

            # Obsolete A/B art hotkeys may not restore Jade or alter physics.
            for key in ("F6", "F7", "p"):
                page.keyboard.press(key)
            state = snap(page)
            if not (state.get("hero_art_concept_enabled") is False
                    and state.get("hero_art_painted_enabled") is False
                    and state.get("hero_art_approved_enabled") is False
                    and state.get("human_sprite_hframes") == 12
                    and state.get("base_fighter_count") == 4):
                raise AssertionError("Retired Jade art shortcut reactivated")
            report["evidence"]["retired_art_shortcuts"] = "BLOCKED"

            before = snap(page)["player"]
            walk_seen = set()
            page.keyboard.down("d")
            try:
                moved = until(page, "Real D movement selects owner 4-cel walk",
                              "s.player.vx > 0.30 && s.base_walk_active === true && "
                              "s.human_sprite_hframes === 4 && "
                              "s.animation_clip_intent === 'base_walk_4_approved' && "
                              "s.visual_contract_clip === 'base_walk_4_approved' && "
                              "s.visual_contract_auto_fit === false && "
                              "Math.abs(s.human_sprite_pixel_size - 0.020) < 0.00001")
                walk_seen.add(int(moved["human_sprite_frame"]))
                # Observe REAL game-originated pose indices and moving X.
                # 4 frames span 3.024m of real world travel; no browser
                # injection into velocity or animation timer is permitted.
                for _ in range(18):
                    page.wait_for_timeout(95)
                    state = snap(page)
                    if state and state.get("base_walk_active") is True:
                        if (state.get("human_sprite_hframes") != 4 or
                                state.get("human_sprite_offset_y") != -2 or
                                state.get("visual_contract_cell") != [80, 80] or
                                state.get("visual_contract_clip") != "base_walk_4_approved" or
                                abs(float(state.get("human_sprite_pixel_size", 0.0)) - 0.020) > 0.00001):
                            raise AssertionError("Walk atlas or shoe anchor changed")
                        walk_seen.add(int(state.get("human_sprite_frame", -1)))
                report["evidence"]["walk_ground_anchor_offset_px"] = -2
                canvas.screenshot(path=str(OUT / "base-walk-4-live.png"))
            finally:
                page.keyboard.up("d")
            if walk_seen != set(range(4)):
                raise AssertionError("Real world walk did not play all 4 "
                                     "owner poses: " + str(sorted(walk_seen)))
            current = snap(page)
            if float(current["player"]["x"]) <= float(before["x"]) + 1.0:
                raise AssertionError("D did not cause real 3D X movement")
            report["evidence"]["real_world_move_dx"] = (
                float(current["player"]["x"]) - float(before["x"]))
            report["evidence"]["walk_frames_sampled"] = sorted(walk_seen)
            idle_again = until(page, "Stopping restores 12 original idle poses",
                               "Math.abs(s.player.vx) < 0.2 && s.player.grounded && "
                               "s.human_sprite_hframes === 12 && "
                               "s.base_walk_active === false && "
                               "s.visual_contract_clip === 'idle_guard_front' && "
                               "Math.abs(s.human_sprite_pixel_size - 0.020) < 0.00001")
            if idle_again.get("human_sprite_offset_y") != -4:
                raise AssertionError("Idle must restore original foot anchor")
            canvas.screenshot(path=str(OUT / "base-idle-after-walk.png"))

            # A short 60Hz attack is faster than some 120ms Web snapshots.
            # Its ACCEPTED attack_instance and last_attack_id are durable real
            # Godot gameplay state, not synthetic browser counters.
            punch_history = []
            for hand, expected in (("right", {0,1,2}), ("left", {2,3})):
                before_punch_instance = int(snap(page)["human_attack_instance"])
                page.keyboard.press("f")
                punch = until(page, "Real F attack and rendered punch",
                              "s.human_attack_instance > " + str(before_punch_instance)
                              + " && s.human_last_attack_id === 'light_punch'"
                              + " && s.base_punch_hand === '" + hand + "'"
                              + " && s.base_punch_rendered_frames.includes(" + str(1 if hand=="right" else 3) + ")")
                canvas.screenshot(path=str(OUT / ("base-punch-"+hand+".png")))
                final = until(page, "Punch restores idle", "s.human_attack_id === '' && s.human_sprite_hframes === 12 && s.visual_contract_clip === 'idle_guard_front'")
                if not expected.issubset(set(final.get("base_punch_rendered_frames", []))):
                    raise AssertionError("Missing actual rendered punch frames: " + str(final.get("base_punch_rendered_frames")))
                punch_history.append({"hand": hand, "frames": final["base_punch_rendered_frames"], "instance": punch["human_attack_instance"]})
            report["evidence"]["real_punch"] = "light_punch"
            report["evidence"]["punch_history"] = punch_history
            before_kick_instance = int(snap(page)["human_attack_instance"])
            page.keyboard.down("g")
            try:
                kick = until(page, "Real G front kick event recorded",
                             "s.human_attack_instance > " + str(before_kick_instance)
                             + " && s.human_last_attack_id === 'front_kick'"
                             + " && s.human_sprite_hframes === 12")
                report["evidence"]["real_kick"] = kick.get("human_last_attack_id")
                report["evidence"]["kick_instance"] = kick.get("human_attack_instance")
                canvas.screenshot(path=str(OUT / "base-kick-physics.png"))
            finally:
                page.keyboard.up("g")
            if report["js_errors"]:
                raise AssertionError("Uncaught browser JavaScript errors")
            report["status"] = "PASS_BASE_IDLE_12_AND_WALK_4_PHYSICS"
            print("BASE_WALK_4_CHROMIUM_PASS: four Base fighters, idle 12, "
                  "all four original grounded walk cels, physical D/F/G, "
                  "old Jade retired; run/strike art pending")
        except Exception as exc:
            report["status"] = "FAIL"
            report["error"] = str(exc)
            try:
                report["last"] = snap(page)
                page.screenshot(path=str(OUT / "failure.png"), full_page=True)
            except Exception:
                pass
            raise
        finally:
            for key in ("d", "w", "s", "a", "f", "g"):
                try:
                    page.keyboard.up(key)
                except Exception:
                    pass
            (OUT / "result.json").write_text(
                json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            browser.close()


if __name__ == "__main__":
    main()
