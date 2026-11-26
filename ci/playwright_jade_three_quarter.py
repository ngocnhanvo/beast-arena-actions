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
            # BOTH directions are owner-requested. Native motor and visible
            # Sprite3D frame must follow actual W/S input on the SAME URL.
            for key, direction, tag, filename in [
                    ("s", "walk_down", "walk_down_guard_front", "walk-S"),
                    ("w", "walk_up", "walk_up_guard_front", "walk-W")]:
                page.keyboard.down(key)
                try:
                    vel = "s.player.vz > 0.35" if key == "s" else "s.player.vz < -0.35"
                    page.wait_for_function(
                        "() => {const s=window.__beastPhysicsDebug;"
                        "return s && s.review_preview_active "
                        "&& s.human_sprite_hframes === 6 "
                        "&& s.review_preview_action === '" + direction + "' "
                        "&& s.animation_clip_intent === '" + tag + "' "
                        "&& " + vel + ";}",
                        timeout=15000, polling=50)
                    page.wait_for_function(
                        "() => window.__beastPhysicsDebug?.review_preview_frame > 0",
                        timeout=15000, polling=40)
                    middle = state(page)
                    if middle.get("hero_atlas_frame_size") != 80:
                        raise AssertionError(key.upper() + " preview isn't native 80px")
                    # User visual bug: old and new 80px cells had DIFFERENT
                    # painted silhouette heights. Their figure heights must
                    # agree to <=1 screen pixel while W/S is actually moving.
                    reference = middle.get("review_reference_body_height_px", 0)
                    painted = middle.get("review_walk_painted_height_px", 0)
                    effective = middle.get("review_effective_body_height_px", 0)
                    scale = middle.get("review_visual_scale", 0)
                    if not (reference > 0 and painted > 0 and scale > 0
                            and abs(reference - effective) <= 1.0
                            and abs(painted * scale - effective) <= 0.01):
                        raise AssertionError(
                            "Sprite shrinks or grows on " + key.upper()
                            + ": baseline=" + str(reference)
                            + ", painted=" + str(painted)
                            + ", scaled=" + str(effective))
                    checked[key.upper()] = {
                        "clip": middle.get("animation_clip_intent"),
                        "native_cel_index": middle.get("review_preview_frame"),
                        "physical_vz": middle.get("player", {}).get("vz"),
                        "reference_figure_height_px": reference,
                        "native_source_figure_height_px": painted,
                        "normalized_figure_height_px": effective,
                        "uniform_visual_scale": scale,
                    }
                    canvas.screenshot(path=str(OUT / ("canonical-" + filename + ".png")))
                finally:
                    page.keyboard.up(key)
                page.wait_for_function(
                    "() => !window.__beastPhysicsDebug?.review_preview_active",
                    timeout=12000, polling=80)
            if set(checked) != {"S", "W"}:
                raise AssertionError("Both W and S must be verified")
            result.update({
                "status": "PASS_TECHNICAL_OWNER_ART_PENDING",
                "source_sha": start.get("source_sha"),
                "pipeline_sha": start.get("pipeline_sha"),
                "build_run_id": start.get("build_run_id"),
                "short_step_guard_directions": checked,
                "foot_pivot_px": 75,
                "full_source_status": "PENDING_ART",
            })
            print("ONE CANONICAL /physics-v2/ JADE CLOSE-STEP GUARD PASS: "
                  "real W AND S movements, 2 native 6x80px Sprite3D sources, "
                  "PixelView floor; owner visual review still pending")
        except Exception as exc:
            result["status"] = "FAIL"
            result["error"] = str(exc)
            result["last"] = state(page)
            raise
        finally:
            page.keyboard.up("s")
            page.keyboard.up("w")
            (OUT / "result.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2))
            browser.close()


if __name__ == "__main__":
    main()
