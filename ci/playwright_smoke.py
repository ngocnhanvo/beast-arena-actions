"""Playwright end-to-end test for deployed Godot Web arena.

Waits for game content, not merely the loading-screen canvas. Captures DOM,
network, console and screenshots for diagnosing failures on public runners.
Does not check out private source and does not include secrets in artifacts.
"""
import json
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

URL = "https://ngocnhanvo.github.io/beast-arena-actions/?e2e=1"
OUT = Path("playwright-report")
OUT.mkdir(exist_ok=True)


def arena_pixels(path):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    p = img.load()
    stage = 0
    blue = []
    for y in range(int(h * .22), int(h * .96), 2):
        for x in range(int(w * .05), int(w * .91), 2):
            r, g, b = p[x, y]
            if 56 <= r <= 87 and 96 <= g <= 133 and 103 <= b <= 148:
                stage += 1
            if (int(w * .10) < x < int(w * .75) and
                    50 <= r <= 160 and 128 <= g <= 228 and
                    b >= 186 and b - g >= 25 and g - r >= 48):
                blue.append((x, y))
    center = None
    if len(blue) > 18:
        center = [sum(q[0] for q in blue) / len(blue),
                  sum(q[1] for q in blue) / len(blue)]
    return stage, center


def canvas_info(page):
    return page.evaluate("""() => [...document.querySelectorAll('canvas')].map(c => {
        const r=c.getBoundingClientRect();
        const s=getComputedStyle(c);
        return {id:c.id, width:c.width, height:c.height, x:r.x, y:r.y,
            css_width:r.width, css_height:r.height, display:s.display,
            visibility:s.visibility};
    })""")


def test():
    result = {"url": URL, "page_errors": [], "console_errors": [],
              "resource_errors": [], "navigation": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True, args=[
                "--enable-webgl", "--use-gl=angle", "--use-angle=swiftshader",
                "--enable-unsafe-swiftshader", "--disable-dev-shm-usage"
            ])
        page = browser.new_page(viewport={"width": 1200, "height": 800},
                                device_scale_factor=1)
        page.on("pageerror", lambda e: result["page_errors"].append(str(e)))
        page.on("console", lambda m: result["console_errors"].append(m.text)
                if m.type == "error" else None)
        page.on("requestfailed", lambda req: result["resource_errors"].append(
            {"url": req.url, "failure": req.failure}))
        page.on("response", lambda r: result["resource_errors"].append(
            {"url": r.url, "status": r.status})
            if r.status >= 400 and r.url.split("?")[0].endswith(
                (".pck", ".wasm", ".js")) else None)
        try:
            response = None
            for attempt in range(1, 7):
                try:
                    response = page.goto(URL, wait_until="domcontentloaded",
                                         timeout=45000)
                except Exception as e:
                    result["navigation"].append({"attempt": attempt,
                                                 "exception": str(e)})
                if response is not None and response.status == 200:
                    break
                result["navigation"].append(
                    {"attempt": attempt,
                     "status": response.status if response else None})
                page.wait_for_timeout(8000)
            if response is None or response.status != 200:
                raise AssertionError("Pages must return HTTP 200")
            result["status"] = response.status

            # Godot may display a full-page loading logo while the actual canvas
            # is still tiny or hidden. The canvas DOM existing is NOT game ready.
            started = time.monotonic()
            ready = False
            for attempt in range(1, 49):  # up to ~144 seconds after navigation
                page.wait_for_timeout(3000)
                result["canvas"] = canvas_info(page)
                canvas = page.locator("canvas#canvas").first
                if canvas.count() == 0:
                    canvas = page.locator("canvas").first
                if canvas.count() == 0:
                    continue
                box = canvas.bounding_box()
                if not box or box["width"] < 400 or box["height"] < 250:
                    continue
                canvas.screenshot(path=str(OUT / "arena-loading-or-ready.png"),
                                  timeout=15000)
                stage, center = arena_pixels(OUT / "arena-loading-or-ready.png")
                result["stage_pixels"] = stage
                result["player_center"] = center
                if stage > 350 and center is not None:
                    ready = True
                    break
                if attempt % 5 == 0:
                    print("Waiting for rendered arena, attempt %d/48; stage=%d"
                          % (attempt, stage), flush=True)
            result["startup_seconds"] = round(time.monotonic() - started, 2)
            if not ready:
                raise AssertionError(
                    "Godot game not ready after 144s; see screenshots and canvas diagnostics")
            canvas.click(force=True)
            canvas.screenshot(path=str(OUT / "before.png"))
            _, before = arena_pixels(OUT / "before.png")
            if before is None:
                raise AssertionError("Cannot find player before input")
            page.keyboard.down("d")
            page.wait_for_timeout(1000)
            page.keyboard.up("d")
            page.wait_for_timeout(250)
            canvas.screenshot(path=str(OUT / "after-move.png"))
            _, after = arena_pixels(OUT / "after-move.png")
            if after is None:
                raise AssertionError("Player not found after movement")
            dx = after[0] - before[0]
            result["player_movement_pixels"] = round(dx, 2)
            if dx < 28:
                raise AssertionError("D key failed to move player right: dx=%.1f" % dx)

            for key in ("j", "k", "Space", "u"):
                page.keyboard.press(key)
                page.wait_for_timeout(180)
            canvas.screenshot(path=str(OUT / "after-actions.png"))
            if result["resource_errors"]:
                raise AssertionError("Browser reported game asset network failures")
            if result["page_errors"]:
                raise AssertionError("Browser reported uncaught JS errors")
            print("PASS: real Godot arena rendered; D moved player %.1fpx" % dx)
        except Exception as exc:
            result["failure"] = str(exc)
            try:
                result["canvas"] = canvas_info(page)
                page.screenshot(path=str(OUT / "failure.png"), full_page=True,
                                timeout=12000)
            except Exception as capture_error:
                result["capture_error"] = str(capture_error)
        finally:
            (OUT / "result.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2),
                encoding="utf-8")
            browser.close()
    if result.get("failure"):
        raise AssertionError(result["failure"])


if __name__ == "__main__":
    test()
