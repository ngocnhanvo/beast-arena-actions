"""Test live Godot Web rendering and keyboard play via Playwright Chromium."""
import json
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

URL = "https://ngocnhanvo.github.io/beast-arena-actions/"
OUT = Path("playwright-report")
OUT.mkdir(exist_ok=True)

def blue_center(file):
    im = Image.open(file).convert("RGB")
    w, h = im.size
    pix = im.load()
    points = []
    for y in range(int(h * .25), int(h * .95), 2):
        for x in range(int(w * .08), int(w * .72), 2):
            r, g, b = pix[x, y]
            if 48 <= r <= 160 and 125 <= g <= 228 and b >= 180 and b-g >= 22 and g-r >= 44:
                points.append((x, y))
    if len(points) < 18:
        return None
    return sum(p[0] for p in points)/len(points), sum(p[1] for p in points)/len(points)

def main():
    report = {"url": URL, "assets_failed": [], "errors": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--enable-webgl", "--use-gl=angle", "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader", "--disable-dev-shm-usage"])
        page = browser.new_page(viewport={"width": 1200, "height": 800})
        page.on("pageerror", lambda err: report["errors"].append(str(err)))
        page.on("response", lambda r: report["assets_failed"].append(r.url)
                if r.status >= 400 and r.url.split("?")[0].endswith((".js", ".wasm", ".pck")) else None)
        try:
            for attempt in range(6):
                resp = page.goto(URL, wait_until="domcontentloaded", timeout=60000)
                if resp and resp.status == 200:
                    break
                page.wait_for_timeout(10000)
            assert resp and resp.status == 200, "Pages URL not HTTP 200"
            canvas = page.locator("canvas").first
            canvas.wait_for(state="visible", timeout=60000)
            assert canvas.bounding_box()["width"] > 400, "Godot canvas too small"
            canvas.click()
            before = None
            for _ in range(18):
                page.wait_for_timeout(1500)
                canvas.screenshot(path=str(OUT / "before.png"))
                before = blue_center(OUT / "before.png")
                if before: break
            assert before, "Player not rendered on canvas"
            page.keyboard.down("d")
            page.wait_for_timeout(900)
            page.keyboard.up("d")
            canvas.screenshot(path=str(OUT / "after-move.png"))
            after = blue_center(OUT / "after-move.png")
            assert after and after[0]-before[0] > 30, "D did not move player right"
            report["move_dx"] = after[0] - before[0]
            for key in ("j", "k", "Space", "u"):
                page.keyboard.press(key)
                page.wait_for_timeout(250)
            canvas.screenshot(path=str(OUT / "after-controls.png"))
            assert not report["assets_failed"], "Critical game resource HTTP failure"
            print("PASS: Godot scene rendered, player moved; attack/jump keys sent")
        except Exception as err:
            report["failure"] = str(err)
            page.screenshot(path=str(OUT / "failure.png"), full_page=True)
        finally:
            (OUT / "result.json").write_text(json.dumps(report, indent=2))
            browser.close()
    assert not report.get("failure"), report.get("failure")

if __name__ == "__main__":
    main()
