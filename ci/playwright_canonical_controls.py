"""Owner-path regression: open EXACT canonical URL, no ?e2e or ?controls.

Measure ACTUAL WebGL/PixelView pixels around the human fighter. A
query-only debug hook or a synthetic gameplay counter cannot pass this test.
"""
import io
import json
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

URL = "https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/"
OUT = Path("playwright-report/canonical-g")
OUT.mkdir(parents=True, exist_ok=True)
REGION = (345, 275, 670, 505)


def changed_pixels(a, b, region=REGION):
    first = Image.open(io.BytesIO(a)).convert("RGB").crop(region)
    second = Image.open(io.BytesIO(b)).convert("RGB").crop(region)
    pa, pb = first.tobytes(), second.tobytes()
    return sum(
        1
        for i in range(0, len(pa), 3)
        if max(abs(pa[i + k] - pb[i + k]) for k in range(3)) >= 48
    )


def capture(canvas):
    return canvas.screenshot()


def main():
    result = {"url": URL, "status": "NOT_RUN", "idle_pixel_change": 0, "kick_peak_change": 0}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=[
            "--enable-webgl", "--use-gl=angle", "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader", "--disable-dev-shm-usage"
        ])
        page = browser.new_page(viewport={"width": 1200, "height": 800})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        try:
            for attempt in range(6):
                response = page.goto(URL, wait_until="domcontentloaded", timeout=50000)
                if response and response.status == 200:
                    break
                page.wait_for_timeout(1200)
            else:
                raise AssertionError("Canonical Pages HTTP 200 is required")
            assert page.url == URL, "Owner URL redirected or query flags added"
            canvas = page.locator("canvas#canvas").first
            if not canvas.count():
                canvas = page.locator("canvas").first
            canvas.wait_for(state="visible", timeout=120000)
            page.wait_for_timeout(3800)
            focus_tag = page.evaluate("document.activeElement && document.activeElement.tagName")
            result["focus_before_input"] = focus_tag
            if focus_tag != "CANVAS":
                raise AssertionError("Game failed to auto-focus the canvas for immediate G input: " + str(focus_tag))
            idle_images = []
            for _ in range(7):
                idle_images.append(capture(canvas))
                page.wait_for_timeout(65)
            idle_noise = max(changed_pixels(idle_images[0], b) for b in idle_images[1:])
            result["idle_pixel_change"] = idle_noise
            # Critically, DO NOT click canvas here: reproduce user's initial keypress.
            page.keyboard.press("g")
            kick = []
            for _ in range(15):
                kick.append(capture(canvas))
                page.wait_for_timeout(35)
            differences = [changed_pixels(idle_images[0], k) for k in kick]
            peak = max(differences)
            result["kick_peak_change"] = peak
            result["kick_changes"] = differences
            best_index = differences.index(peak)
            (OUT / "before-g.png").write_bytes(idle_images[0])
            (OUT / "after-g-most-changed.png").write_bytes(kick[best_index])
            if peak <= max(650, idle_noise * 1.55):
                raise AssertionError(
                    "No visible right-leg kick on canonical URL without canvas click: "
                    + "peak=" + str(peak) + ", idle=" + str(idle_noise)
                )
            if errors:
                raise AssertionError("Browser errors: " + repr(errors))
            result["status"] = "CANONICAL_G_VISIBLE_PASS"
            print("CANONICAL_G_VISIBLE_PASS: no query, auto-focus, real G, visual delta", peak, "idle", idle_noise)
        except Exception as exc:
            result["status"] = "FAIL"
            result["reason"] = str(exc)
            try:
                page.screenshot(path=str(OUT / "failure.png"), full_page=True)
            except Exception:
                pass
            raise
        finally:
            result["browser_errors"] = errors
            (OUT / "result.json").write_text(json.dumps(result, indent=2))
            browser.close()


if __name__ == "__main__":
    main()
