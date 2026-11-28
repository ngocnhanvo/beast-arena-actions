"""Verify real G input and all four actually drawn Kick4 frames on the user's EXACT no-query URL."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

OWNER = "https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/"
ROOT = "https://ngocnhanvo.github.io/beast-arena-actions/"
OUT = Path("playwright-report/canonical-g")
OUT.mkdir(parents=True, exist_ok=True)

def await_proof(page, predicate, timeout=12000):
    fn = "() => {const s=window.__beastCanonicalInputProof; return s && (" + predicate + ") ? s : false;}"
    return page.wait_for_function(fn, polling=50, timeout=timeout).json_value()

def main():
    report = {"url": OWNER, "status": "NOT_RUN", "steps": []}
    with sync_playwright() as pw:
        options = {"headless": True, "args": [
            "--enable-webgl", "--use-gl=angle", "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader", "--disable-dev-shm-usage"]}
        if os.environ.get("BEAST_PLAYWRIGHT_CHANNEL"):
            options["channel"] = os.environ["BEAST_PLAYWRIGHT_CHANNEL"]
        browser = pw.chromium.launch(**options)
        page = browser.new_page(viewport={"width": 1200, "height": 800})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        try:
            root = page.request.get(ROOT, timeout=20000)
            if root.status != 200:
                raise AssertionError("Fastlane must preserve existing root Pages: " + str(root.status))
            report["steps"].append("root_http_200")
            for _ in range(6):
                response = page.goto(OWNER, wait_until="domcontentloaded", timeout=50000)
                if response and response.status == 200:
                    break
                page.wait_for_timeout(1200)
            else:
                raise AssertionError("Owner Physics V2 Pages is not HTTP 200")
            if page.url != OWNER:
                raise AssertionError("User URL changed or gained query parameters")
            canvas = page.locator("canvas#canvas").first
            if not canvas.count():
                canvas = page.locator("canvas").first
            canvas.wait_for(state="visible", timeout=120000)
            start = await_proof(page, "s.ready === true && s.controls_v2 === true", 120000)
            expected = os.environ.get("BEAST_EXPECT_SOURCE_SHA", "")
            if expected and start.get("source_sha") != expected:
                # Pages CDN can be briefly stale; retry the SAME unmodified URL.
                for retry in range(3):
                    page.wait_for_timeout(1200)
                    page.reload(wait_until="domcontentloaded", timeout=50000)
                    start = await_proof(page, "s.ready === true && s.controls_v2 === true", 120000)
                    if start.get("source_sha") == expected:
                        break
                if start.get("source_sha") != expected:
                    raise AssertionError("Stale Pages source: " + str(start.get("source_sha")) + " != " + expected)
            report["start"] = start
            if start.get("kick_native_cell_height") != 80:
                raise AssertionError("Kick must use native 80px frame height: " + str(start.get("kick_native_cell_height")))
            if start.get("kick_native_frame_count") != 4:
                raise AssertionError("Kick4 must have four 120x80 source frames: " + str(start.get("kick_native_frame_count")))
            focus = page.evaluate("document.activeElement && document.activeElement.tagName")
            report["focus"] = focus
            if focus != "CANVAS":
                raise AssertionError("Canvas not focused for user G: " + str(focus))
            # No click, no ?e2e=1, no synthetic Godot command.
            page.keyboard.press("g")
            got = await_proof(page, "s.g_keydown_count > " + str(start["g_keydown_count"]))
            report["input"] = got
            report["steps"].append("real_G_received")
            attack = await_proof(page,
                "s.accepted_kick_count > " + str(start["accepted_kick_count"])
                + " && s.last_attack_id === 'front_kick'")
            report["attack"] = attack
            report["steps"].append("real_kick_accepted")
            drawn = await_proof(page, "s.kick_drawn_frames.includes(0) && s.kick_drawn_frames.includes(1) && s.kick_drawn_frames.includes(2) && s.kick_drawn_frames.includes(3)")
            if not all(i in drawn.get("kick_presented_frames", []) for i in (0, 1, 2, 3)):
                raise AssertionError("Kick4 was drawn but not all four phases presented")
            report["drawn"] = drawn
            report["steps"].append("four_right_leg_kick_cels_actually_drawn_by_PixelView")
            page.screenshot(path=str(OUT / "after-g.png"), full_page=True)
            if errors:
                raise AssertionError("Browser errors: " + repr(errors))
            report["status"] = "PASS_CANONICAL_G_REAL_INPUT_AND_DRAW"
            print("CANONICAL_KICK4_REAL_INPUT_AND_DRAW_PASS: no query, no click, actual G, ALL four kick poses drawn")
        except Exception as exc:
            report["status"] = "FAIL"
            report["reason"] = str(exc)
            try:
                page.screenshot(path=str(OUT / "failure.png"), full_page=True)
            except Exception:
                pass
            raise
        finally:
            report["browser_errors"] = errors
            (OUT / "result.json").write_text(json.dumps(report, indent=2))
            browser.close()

if __name__ == "__main__":
    main()
