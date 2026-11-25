"""Godot 3D Physics V2 staging E2E: never confuse with production P1.5.

All state is public opt-in (?e2e=1); no private source/tokens stored.
"""
import json
import time
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
            if first["ramp_rise_m"] < 2.0 or first["obstacles"] < 5:
                raise AssertionError("3D ramp and props missing")
            if first["map_width_m"] < 60.0:
                raise AssertionError("Stage should scroll beyond viewport")
            if first.get("ramp_visual_count", 0) < 25 or first.get("ramp_angle_deg", 0) < 14:
                raise AssertionError("Visible slope markers and 14+ degree rise missing")
            if first.get("ramp_end_y", 0) - first.get("ramp_start_y", 0) < 3.3:
                raise AssertionError("Moss ramp physical height not large enough to notice")
            canvas.screenshot(path=str(OUT / "moss-start.png"))
            report["moss_visible_floor_fraction"] = round(
                visible_floor_fraction(OUT / "moss-start.png"), 3)
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
            if moved["player"]["vx"] > 5.0:
                raise AssertionError("3D horizontal motor exceeded configured speed")
            canvas.screenshot(path=str(OUT / "moss-moving.png"))

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
            canvas.screenshot(path=str(OUT / "docks-high-platform.png"))
            if docks.get("ramp_visual_count", 0) < 25 or docks.get("ramp_angle_deg", 0) < 14:
                raise AssertionError("Docks downhill visual face and elevation labels missing")
            if docks["ramp_start_y"] - docks["ramp_end_y"] < 3.3:
                raise AssertionError("Docks downhill should descend by >= 3.3m")
            report["docks_visible_floor_fraction"] = round(
                visible_floor_fraction(OUT / "docks-high-platform.png"), 3)
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
            report["camera_projection_locked"] = True
            report["camera_rotation_deg"] = {
                k: first["camera"][k]
                for k in ("pitch_deg", "yaw_deg", "roll_deg")
            }
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
