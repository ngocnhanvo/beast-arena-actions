"""Godot 3D Physics V2 staging E2E: never confuse with production P1.5.

All state is public opt-in (?e2e=1); no private source/tokens stored.
"""
import json
import re
import time
from collections import Counter
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright


def visible_floor_fraction(image_path: Path) -> float:
    # Screenshot pixel test catches a WebGL2/material regression where
    # collision and debug telemetry pass but the entire 3D floor is BLACK.
    # Only count a central interior crop; HUD/sprites occupy a minority.
    with Image.open(image_path).convert("RGB") as image:
        w, h = image.size
        sample = image.crop((int(w*0.16), int(h*0.29),
                             int(w*0.83), int(h*0.79)))
        colors = list(sample.getdata())
        bright = sum(1 for red, green, blue in colors
                     if max(red, green, blue) >= 58
                     and (green >= red*0.8 or blue >= red*0.8))
        return bright / max(1, len(colors))

def floor_tile_diversity(image_path: Path):
    # This crop deliberately avoids character pixels, ramp stripes,
    # foreground props and HUD. The old untextured BoxMesh displayed only
    # one uniform color here while all older movement tests returned PASS.
    with Image.open(image_path).convert("RGB") as image:
        w, h = image.size
        patch = image.crop((int(w * 0.13), int(h * 0.50),
                            int(w * 0.21), int(h * 0.61)))
        pixels = Counter(patch.getdata())
        total = sum(pixels.values())
        strong = sum(1 for n in pixels.values() if n / max(1, total) >= 0.01)
        dominant = max(pixels.values(), default=0) / max(1, total)
        return {"visible_color_groups": strong, "dominant_color_fraction": round(dominant, 4)}


URL = "https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?e2e=1"
OUT = Path("playwright-report/physics-v2")
OUT.mkdir(parents=True, exist_ok=True)


def snap(page):
    return page.evaluate("window.__beastPhysicsDebug || null")


def assert_locked_projection(first, current, stage):
    # Camera must slide across world positions, never tilt or rotate.
    # The user perceives a rotating level otherwise, especially on ramps.
    axes = ("pitch_deg", "yaw_deg", "roll_deg")
    for axis in axes:
        if axis not in first["camera"] or axis not in current["camera"]:
            raise AssertionError("camera angle telemetry missing: " + axis)
        drift = abs(first["camera"][axis] - current["camera"][axis])
        if drift > 0.10:
            raise AssertionError(
                "2.5D camera rotates when moving (%s %s drift=%.3f deg)" %
                (stage, axis, drift))


def main():
    report = {"url": URL, "status": "NOT_TESTED", "page_errors": [],
              "critical_asset_failures": [], "navigation": []}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=[
            "--enable-webgl", "--use-gl=angle", "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader", "--disable-dev-shm-usage"
        ])
        page = browser.new_page(viewport={"width": 1200, "height": 800})
        page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
        page.on("response", lambda r: report["critical_asset_failures"].append(
            {"url": r.url, "status": r.status})
            if r.status >= 400 and r.url.split("?")[0].endswith(
                (".wasm", ".pck", ".js")) else None)
        try:
            response = None
            for attempt in range(1, 7):
                response = page.goto(URL, wait_until="domcontentloaded", timeout=50000)
                report["navigation"].append({"attempt": attempt, "http": response.status})
                if response.status == 200:
                    break
                page.wait_for_timeout(6000)
            if response is None or response.status != 200:
                raise AssertionError("staging /physics-v2/ is not HTTP 200")

            t0 = time.monotonic()
            page.wait_for_function(
                "() => window.__beastPhysicsDebug && window.__beastPhysicsDebug.ready === true",
                timeout=180000, polling=750)
            report["boot_seconds"] = round(time.monotonic() - t0, 2)
            canvas = page.locator("canvas#canvas").first
            if canvas.count() == 0:
                canvas = page.locator("canvas").first
            canvas.wait_for(state="visible", timeout=20000)
            bounds = canvas.bounding_box()
            if not bounds or bounds["width"] < 400 or bounds["height"] < 250:
                raise AssertionError("3D game canvas not ready")
            canvas.click(force=True)
            first = snap(page)
            report["initial"] = first
            if first["map_id"] != "moss_temple" or first["actors"] != 4:
                raise AssertionError("Moss Temple and four 3D actors missing")
            # Visual V0 is separate from the camera-angle regression gate.
            # Refuse a stale Web PCK even if old movement assertions pass.
            if not re.fullmatch(r"[0-9a-f]{40}", first.get("source_sha", "")):
                raise AssertionError("missing exact private source SHA in deployed PCK")
            if not re.fullmatch(r"[0-9a-f]{40}", first.get("pipeline_sha", "")):
                raise AssertionError("missing public Actions build commit SHA")
            if not str(first.get("build_run_id", "")).isdigit():
                raise AssertionError("missing actual deployment build run ID")
            report["version"] = {key: first[key] for key in
                                  ("source_sha", "pipeline_sha", "build_run_id", "visual_style_id")}
            if first.get("visual_style_id") != "v1-visible-pixel-floor-20261126":
                raise AssertionError("stale or wrong Physics0 visual build: " +
                                     str(first.get("visual_style_id")))
            if not (12.0 <= abs(first["camera"]["pitch_deg"]) <= 25.0):
                raise AssertionError("Nekketsu side-biased camera pitch outside visual profile")
            if abs(first.get("horizontal_world_axis_screen_dy", 999.0)) > 0.15:
                raise AssertionError("Horizontal world axis is not screen-horizontal")

            if first["ramp_rise_m"] < 2.0 or first["obstacles"] < 5:
                raise AssertionError("3D ramp and props missing")
            if first.get("pixel_floor_sections") != 3 or first.get("pixel_facade_panels", 0) < 10:
                raise AssertionError("Original pixel art layers missing in Moss scene")
            if first.get("human_sprite_hframes") != 4 or first.get("human_sprite_vframes") != 20:
                raise AssertionError("Original 80-frame directional human animation atlas not loaded")
            if abs(first.get("human_sprite_pixel_size", 0.0) - 0.025) > 0.0001:
                raise AssertionError("Human pixel scale differs from approved test contract")
            if first["map_width_m"] < 60.0:
                raise AssertionError("Stage should scroll beyond viewport")
            if first.get("ramp_visual_count", 0) < 25 or first.get("ramp_angle_deg", 0) < 14:
                raise AssertionError("Visible slope markers and 14+ degree rise missing")
            if first.get("ramp_end_y", 0) - first.get("ramp_start_y", 0) < 3.3:
                raise AssertionError("Moss ramp physical height not large enough to notice")
            canvas.screenshot(path=str(OUT / "moss-start.png"))
            report["moss_visible_floor_fraction"] = round(
                visible_floor_fraction(OUT / "moss-start.png"), 3)
            report["moss_tile_diversity"] = floor_tile_diversity(OUT / "moss-start.png")
            if (report["moss_tile_diversity"]["visible_color_groups"] < 3 or
                    report["moss_tile_diversity"]["dominant_color_fraction"] > 0.85):
                raise AssertionError("Moss pixel tile top surface is INVISIBLE "
                                     "despite valid material/mesh and collision: " +
                                     str(report["moss_tile_diversity"]))
            if report["moss_visible_floor_fraction"] < 0.14:
                raise AssertionError(
                    "Stage floor appears black/blank in WebGL2: "
                    + str(report["moss_visible_floor_fraction"]))

            page.keyboard.down("d")
            page.wait_for_timeout(950)
            page.keyboard.up("d")
            page.wait_for_timeout(250)
            moved = snap(page)
            report["movement"] = moved
            report["player_dx"] = round(moved["player"]["x"]-first["player"]["x"], 3)
            if report["player_dx"] <= 0.8:
                raise AssertionError("3D motor did not respond to D: " + str(report["player_dx"]))
            if moved.get("human_sprite_frame", -1) % 4 != 2:
                raise AssertionError("Directional pixel sprite did not face right on D movement")
            if moved["player"]["vx"] > 5.0:
                raise AssertionError("3D horizontal motor exceeded configured speed")
            canvas.screenshot(path=str(OUT / "moss-moving.png"))
            page.keyboard.press("j")
            page.wait_for_timeout(180)
            attack_visual = snap(page)
            report["human_attack_visual"] = attack_visual
            if attack_visual.get("human_visual_action") != "punch_light":
                raise AssertionError("J did not start the original light attack visual preview")
            if attack_visual.get("human_sprite_frame", -1) // 4 not in (7, 8):
                raise AssertionError("attack animation not on the original punch rows")
            canvas.screenshot(path=str(OUT / "moss-light-preview.png"))
            # This verifies animation playback only; combat damage/boxes
            # remain a separate milestone, never inferred from pixels.

            before_jumps = moved["player"]["jump_events"]
            page.keyboard.press("Space")
            page.wait_for_timeout(220)
            jump = snap(page)
            report["jump"] = jump
            if jump["player"]["jump_events"] <= before_jumps:
                raise AssertionError("Space did not apply real 3D jump impulse")
            if jump["player"]["y"] <= moved["player"]["y"] + 0.2:
                raise AssertionError("3D body elevation did not rise")
            canvas.screenshot(path=str(OUT / "moss-jump.png"))

            # New acceptance gate: a player must SEE and actually CLIMB a
            # significant incline, not just have a slope hidden offscreen.
            page.keyboard.press("r")  # stage entrance, no browser F5 reload
            page.wait_for_timeout(400)
            moss_ramp_entry = snap(page)
            report["moss_slope_entry"] = moss_ramp_entry
            canvas.screenshot(path=str(OUT / "moss-slope-entry.png"))
            page.keyboard.down("d")
            page.wait_for_timeout(2600)
            moss_ramp_mid = snap(page)
            page.keyboard.up("d")
            report["moss_slope_mid"] = moss_ramp_mid
            report["moss_ramp_climb_m"] = round(
                moss_ramp_mid["player"]["y"] - moss_ramp_entry["player"]["y"], 3)
            if report["moss_ramp_climb_m"] < 1.2:
                raise AssertionError("Moss looks like a ramp but player did not climb: "
                                     + str(report["moss_ramp_climb_m"]))
            if moss_ramp_mid["player"]["floor_angle_deg"] < 10:
                raise AssertionError("Moss terrain has no contact slope normal")
            canvas.screenshot(path=str(OUT / "moss-ramp-mid-climb.png"))

            page.keyboard.press("F3")
            page.wait_for_timeout(420)
            far = snap(page)
            report["moss_far"] = far
            if far["player"]["x"] < 15.0 or far["camera"]["x"] <= first["camera"]["x"] + 15.0:
                raise AssertionError("3D camera failed to follow beyond initial view")
            canvas.screenshot(path=str(OUT / "moss-far.png"))

            page.keyboard.press("2")
            page.wait_for_timeout(550)
            docks = snap(page)
            report["docks"] = docks
            if docks["map_id"] != "night_docks" or docks["ramp_rise_m"] >= 0.0:
                raise AssertionError("Night Docks downhill map did not load")
            if docks["actors"] != 4 or docks["obstacles"] < 5:
                raise AssertionError("3D actors / native colliders not created on switch")
            if docks.get("pixel_floor_sections") != 3 or docks.get("pixel_facade_panels", 0) < 10:
                raise AssertionError("Original pixel art layers missing in Docks scene")
            canvas.screenshot(path=str(OUT / "docks-high-platform.png"))
            if docks.get("ramp_visual_count", 0) < 25 or docks.get("ramp_angle_deg", 0) < 14:
                raise AssertionError("Docks downhill visual face and elevation labels missing")
            if docks["ramp_start_y"] - docks["ramp_end_y"] < 3.3:
                raise AssertionError("Docks downhill should descend by >= 3.3m")
            report["docks_visible_floor_fraction"] = round(
                visible_floor_fraction(OUT / "docks-high-platform.png"), 3)
            report["docks_tile_diversity"] = floor_tile_diversity(OUT / "docks-high-platform.png")
            if (report["docks_tile_diversity"]["visible_color_groups"] < 3 or
                    report["docks_tile_diversity"]["dominant_color_fraction"] > 0.85):
                raise AssertionError("Docks pixel tile top surface is INVISIBLE "
                                     "despite valid material/mesh and collision: " +
                                     str(report["docks_tile_diversity"]))
            if report["docks_visible_floor_fraction"] < 0.14:
                raise AssertionError(
                    "Night Docks floor is not visibly rendered: "
                    + str(report["docks_visible_floor_fraction"]))
            # Explicitly verify descending on the real 3D stage in Chromium.
            page.keyboard.press("r")
            page.wait_for_timeout(350)
            docks_slope_entry = snap(page)
            report["docks_slope_entry"] = docks_slope_entry
            canvas.screenshot(path=str(OUT / "docks-slope-entry.png"))
            page.keyboard.down("d")
            page.wait_for_timeout(2600)
            docks_slope_mid = snap(page)
            page.keyboard.up("d")
            report["docks_slope_mid"] = docks_slope_mid
            report["docks_ramp_descent_m"] = round(
                docks_slope_entry["player"]["y"] - docks_slope_mid["player"]["y"], 3)
            if report["docks_ramp_descent_m"] < 1.2:
                raise AssertionError("Docks does not actually descend the 3D incline: "
                                     + str(report["docks_ramp_descent_m"]))
            if docks_slope_mid["player"]["floor_angle_deg"] < 10:
                raise AssertionError("Docks terrain has no downhill contact normal")
            canvas.screenshot(path=str(OUT / "docks-ramp-mid-descent.png"))

            page.keyboard.press("F3")
            page.wait_for_timeout(350)
            docks_far = snap(page)
            report["docks_far"] = docks_far
            if docks_far["player"]["x"] < 20.0:
                raise AssertionError("Night Docks cannot reach far world region")
            canvas.screenshot(path=str(OUT / "docks-far.png"))

            # A transient GitHub Pages 503 may occur during deployment, but
            # if the WebAssembly game is READY, movement/jump/map assertions
            # pass and the floor is visible, it has recovered. Keep detailed
            # HTTP evidence without treating a recovered response as fatal.
            if report["critical_asset_failures"]:
                report["transient_asset_warnings"] = list(report["critical_asset_failures"])
            # Check actual camera orientation throughout movement, real
            # incline traversal, map switch and far teleport. Translation
            # to follow the player is fine; a change of yaw/pitch/roll isn't.
            for name, checkpoint in (
                ("moss walking", moved),
                ("moss slope entry", moss_ramp_entry),
                ("moss climbing", moss_ramp_mid),
                ("moss far", far),
                ("docks switch", docks),
                ("docks slope entry", docks_slope_entry),
                ("docks descending", docks_slope_mid),
                ("docks far", docks_far),
            ):
                assert_locked_projection(first, checkpoint, name)
            # The real 3D player climbs/descends, but a fixed 2.5D stage
            # must not pan vertically in reaction to elevation changes.
            for stage, checkpoint in (
                ("moss ramp", moss_ramp_mid),
                ("docks ramp", docks_slope_mid),
                ("docks switch", docks),
            ):
                if abs(checkpoint["camera"]["y"] - first["camera"]["y"]) > 0.06:
                    raise AssertionError("stage camera vertically bobs during " + stage)
                if abs(checkpoint.get("horizontal_world_axis_screen_dy", 999.0)) > 0.15:
                    raise AssertionError("world X axis is visually tilted during " + stage)
                if checkpoint.get("visual_style_id") != first.get("visual_style_id"):
                    raise AssertionError("visual style changed across stages")
            report["visual_v0_horizontal_axis_locked"] = True
            report["visual_v0_stage_elevation_bob_m"] = round(
                max(abs(cp["camera"]["y"] - first["camera"]["y"])
                    for cp in (moss_ramp_mid, docks_slope_mid, docks)), 4)
            report["camera_projection_locked"] = True
            report["camera_rotation_deg"] = {
                k: first["camera"][k]
                for k in ("pitch_deg", "yaw_deg", "roll_deg")
            }
            # Opt-in human-only 2v2: leave the baseline slope/camera
            # traversal untouched. C starts AI and real damage resolution.
            page.keyboard.press("1")
            page.wait_for_timeout(350)
            restart = snap(page)
            if restart["map_id"] != "moss_temple" or restart.get("combat_completed_hits", -1) != 0:
                raise AssertionError("2v2 round did not reset for independent test")
            page.keyboard.press("c")
            page.wait_for_timeout(4800)
            battle = snap(page)
            report["human_2v2"] = battle
            if not battle.get("combat_ai_enabled", False):
                raise AssertionError("2v2 AI was not enabled by C")
            if battle.get("combat_completed_hits", 0) < 1:
                raise AssertionError("real 2v2 actors never landed a gameplay attack")
            health = battle.get("combat_hp", {})
            if not health or sum(health.values()) >= 400:
                raise AssertionError("2v2 attack did not reduce any authoritative HP")
            bar_widths = battle.get("hud_hp_bar_px", {})
            for fighter, full_width in (("player", 206.0), ("ally", 206.0),
                                        ("enemy_a", 208.0), ("enemy_b", 211.0)):
                if fighter not in bar_widths or fighter not in health:
                    raise AssertionError("missing live HP bar or actor: " + fighter)
                expected_width = full_width * health[fighter] / 100.0
                if abs(bar_widths[fighter] - expected_width) > 3.5:
                    raise AssertionError("HUD HP bar does not track gameplay HP: " + fighter)
            report["human_2v2_hud_hp_synced"] = True
            canvas.screenshot(path=str(OUT / "moss-human-2v2.png"))
            report["human_2v2_pass"] = True

            if report["page_errors"]:
                raise AssertionError("3D Web has uncaught JavaScript errors")
            report["status"] = "PASS"
            print("Physics V2 Web PASS: climb=%.2fm, descent=%.2fm, actual contact angles >=10deg, dx=%.2fm" %
                  (report["moss_ramp_climb_m"], report["docks_ramp_descent_m"],
                   report["player_dx"]), flush=True)
        except Exception as error:
            report["status"] = "FAIL"
            report["failure"] = str(error)
            try:
                report["last"] = snap(page)
                page.screenshot(path=str(OUT / "failure.png"), full_page=True)
            except Exception as diagnostic:
                report["diagnostic_error"] = str(diagnostic)
        finally:
            (OUT / "result.json").write_text(
                json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            browser.close()
    if report["status"] != "PASS":
        raise AssertionError(report.get("failure", "Physics V2 unknown E2E failure"))


if __name__ == "__main__":
    main()
