"""Playwright E2E: confirm live Godot boot AND actual input/state transitions.

Uses a deliberately minimal, public, opt-in (?e2e=1) debug snapshot from game.
No source checkout and no private data in artifacts. Screenshots are PUBLIC.
"""
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "https://ngocnhanvo.github.io/beast-arena-actions/?e2e=1"
OUT = Path("playwright-report")
OUT.mkdir(exist_ok=True)


def debug_snapshot(page):
    return page.evaluate("window.__beastArenaDebug || null")


def dom_snapshot(page):
    return page.evaluate("""() => ({
      page: location.href,
      canvases: [...document.querySelectorAll('canvas')].map(c => {
        const r = c.getBoundingClientRect();
        return {id:c.id, width:c.width, height:c.height,
          css_width:r.width, css_height:r.height, x:r.x, y:r.y,
          display:getComputedStyle(c).display};
      })
    })""")


def main():
    report = {
        "target": URL, "navigation": [], "console_errors": [],
        "page_errors": [], "failed_assets": [], "status": "NOT_TESTED"
    }
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            "--enable-webgl", "--use-gl=angle", "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader", "--disable-dev-shm-usage"
        ])
        page = browser.new_page(viewport={"width": 1200, "height": 800},
                                device_scale_factor=1)
        page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
        page.on("console", lambda m: report["console_errors"].append(m.text)
                if m.type == "error" else None)
        page.on("response", lambda r: report["failed_assets"].append(
            {"url": r.url, "http": r.status}) if
            r.status >= 400 and r.url.split("?")[0].endswith(
                (".pck", ".wasm", ".js")) else None)
        try:
            page_response = None
            for attempt in range(1, 7):
                try:
                    page_response = page.goto(URL, wait_until="domcontentloaded",
                                              timeout=50000)
                    report["navigation"].append({
                        "attempt": attempt,
                        "http": page_response.status if page_response else None
                    })
                except Exception as e:
                    report["navigation"].append({
                        "attempt": attempt, "error": str(e)
                    })
                if page_response is not None and page_response.status == 200:
                    break
                page.wait_for_timeout(8000)
            if page_response is None or page_response.status != 200:
                raise AssertionError("GitHub Pages not HTTP 200")

            # The previous test hit Godot's partial loading splash; canvas
            # existed but wasn't sized/ready. Wait for the GAME signal instead.
            started = time.monotonic()
            page.wait_for_function(
                "() => window.__beastArenaDebug && window.__beastArenaDebug.ready === true",
                timeout=180000, polling=1000)
            report["boot_seconds"] = round(time.monotonic() - started, 2)
            report["dom"] = dom_snapshot(page)
            first = debug_snapshot(page)
            report["snapshot_before"] = first
            canvas = page.locator("canvas#canvas").first
            if canvas.count() == 0:
                canvas = page.locator("canvas").first
            canvas.wait_for(state="visible", timeout=20000)
            bounds = canvas.bounding_box()
            report["canvas_bounds"] = bounds
            if not bounds or bounds["width"] < 400 or bounds["height"] < 250:
                raise AssertionError("Actual game canvas too small after ready: %s" % bounds)
            if first["obstacles"] < 2:
                raise AssertionError("P1 stage missing collision obstacles")
            canvas.click(force=True)
            canvas.screenshot(path=str(OUT / "arena-ready.png"))

            # Real gameplay assertions use engine state rather than pixel RGB.
            jump_before = first["events"]["jumps"]
            page.keyboard.press("Space")
            page.wait_for_timeout(220)
            jumped = debug_snapshot(page)
            report["snapshot_jump"] = jumped
            if jumped["events"]["jumps"] <= jump_before:
                raise AssertionError("Space was pressed but jump event did not occur")
            if jumped["player"]["z"] <= 0:
                raise AssertionError("Jump event fired but player height Z not positive")

            attacks_before = jumped["events"]["attacks"]
            page.keyboard.press("j")
            page.wait_for_timeout(350)
            attack = debug_snapshot(page)
            report["snapshot_attack"] = attack
            if attack["events"]["attacks"] <= attacks_before:
                raise AssertionError("J was pressed but attack was not started")

            start_x = attack["player"]["x"]
            page.keyboard.down("d")
            page.wait_for_timeout(1000)
            page.keyboard.up("d")
            page.wait_for_timeout(200)
            movement = debug_snapshot(page)
            report["snapshot_movement"] = movement
            report["move_dx"] = round(movement["player"]["x"] - start_x, 2)
            canvas.screenshot(path=str(OUT / "arena-after-move.png"))
            if report["move_dx"] < 28:
                raise AssertionError("D did not move player right by >=28 world units")

            page.keyboard.press("k")
            page.keyboard.press("u")  # may not transform until meter >=50
            page.keyboard.press("F2")
            page.wait_for_timeout(250)
            overlays = debug_snapshot(page)
            report["snapshot_collision_overlay"] = overlays
            if overlays.get("collision_debug") is not True:
                raise AssertionError("F2 did not enable the collision/spawn debug overlay")
            canvas.screenshot(path=str(OUT / "arena-debug-overlays.png"))
            if report["failed_assets"]:
                raise AssertionError("Critical JS/WASM/PCK asset request failed")
            if report["page_errors"]:
                raise AssertionError("Uncaught browser page errors")
            report["status"] = "PASS"
            print("PASS P0: Godot ready; P1 stage and real Space/J/D input verified; dx=%.1f"
                  % report["move_dx"], flush=True)
        except Exception as exc:
            report["status"] = "FAIL"
            report["failure"] = str(exc)
            try:
                report["dom"] = dom_snapshot(page)
                report["last_debug"] = debug_snapshot(page)
                page.screenshot(path=str(OUT / "failure.png"), full_page=True)
            except Exception as diagnostic_exception:
                report["diagnostic_error"] = str(diagnostic_exception)
        finally:
            (OUT / "result.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            browser.close()
    if report["status"] != "PASS":
        raise AssertionError(report.get("failure", "Unknown browser test failure"))


if __name__ == "__main__":
    main()
