"""Godot 3D Physics V2 staging E2E: never confuse with production P1.5.

All state is public opt-in (?e2e=1); no private source/tokens stored.
"""
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/?e2e=1"
OUT = Path("playwright-report/physics-v2")
OUT.mkdir(parents=True, exist_ok=True)


def snap(page):
    return page.evaluate("window.__beastPhysicsDebug || null")


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
            canvas.screenshot(path=str(OUT / "moss-start.png"))

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
            page.keyboard.press("F3")
            page.wait_for_timeout(350)
            docks_far = snap(page)
            report["docks_far"] = docks_far
            if docks_far["player"]["x"] < 20.0:
                raise AssertionError("Night Docks cannot reach far world region")
            canvas.screenshot(path=str(OUT / "docks-far.png"))

            if report["page_errors"] or report["critical_asset_failures"]:
                raise AssertionError("3D Web has JS/PCK/WASM failures")
            report["status"] = "PASS"
            print("Physics V2 Web PASS: 3D character, jump, 2 editable maps, camera, dx=%.2fm" %
                  report["player_dx"], flush=True)
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
