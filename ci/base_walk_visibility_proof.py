"""Capture actual published Physics V2 WALK motion to audit visibility, not just debug frame IDs.

No source checkout, hacks, altered playback, injected Godot state or new preview URL.
This captures a short public-canvas VIDEO while genuine D input moves the actor.
"""
import json
import os
import shutil
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/"
URL = BASE + "?e2e=1&controls=v2&pixel=1"
OUT = Path("playwright-report/walk-visible")
OUT.mkdir(parents=True, exist_ok=True)


def snapshot(page):
    return page.evaluate("window.__beastPhysicsDebug || null")


def until(page, predicate, timeout=30000):
    h = page.wait_for_function(
        "() => {const s=window.__beastPhysicsDebug; return s && (" +
        predicate + ") ? s : false;}", polling=50, timeout=timeout)
    return h.json_value()


def main():
    report = {"url": BASE, "status": "FAIL", "walk_seen": [], "samples": [],
              "js_errors": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--enable-webgl", "--use-gl=angle", "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader", "--disable-dev-shm-usage"])
        ctx = browser.new_context(
            viewport={"width": 1200, "height": 800},
            record_video_dir=str(OUT),
            record_video_size={"width": 1200, "height": 800})
        page = ctx.new_page()
        page_open = time.monotonic()
        page.on("pageerror", lambda err: report["js_errors"].append(str(err)))
        video = page.video
        try:
            for _ in range(6):
                response = page.goto(URL, wait_until="domcontentloaded", timeout=55000)
                if response is not None and response.status == 200:
                    break
                page.wait_for_timeout(2200)
            else:
                raise AssertionError("canonical Pages not HTTP 200")
            state = until(page, "s.ready === true && s.base_fighter_count === 4 && "
                          "s.player.grounded && s.pixel_view_floor_tiles > 0", 180000)
            for key, expected in [
                ("build_run_id", "46127709383"),
                ("source_sha", "8aa79c18825904203e08a7a760cf00b9a2cb7d43"),
                ("pipeline_sha", "fd4003ee10380f6f150d754fcf85597b7b57eb3b")]:
                if str(state.get(key)) != expected:
                    raise AssertionError("Pages stale version for " + key +
                                         ": " + str(state.get(key)))
            report["version"] = {k: state.get(k) for k in
                                 ("build_run_id", "source_sha", "pipeline_sha")}
            canvas = page.locator("canvas#canvas").first
            if not canvas.count():
                canvas = page.locator("canvas").first
            canvas.wait_for(state="visible", timeout=20000)
            canvas.click(force=True)
            until(page, "s.human_sprite_hframes === 12 && s.player.grounded")
            canvas.screenshot(path=str(OUT / "before-walk.png"))
            report["movement_start_seconds"] = time.monotonic() - page_open
            before_x = snapshot(page)["player"]["x"]
            seen = set()
            page.keyboard.down("d")
            try:
                for _ in range(72):
                    page.wait_for_timeout(75)
                    s = snapshot(page)
                    if not s or not s.get("base_walk_active"):
                        continue
                    if (s.get("human_sprite_hframes") != 4 or
                            s.get("animation_clip_intent") != "base_walk_4_approved"):
                        raise AssertionError("real walk atlas not active")
                    idx = int(s.get("human_sprite_frame", -1))
                    if not 0 <= idx < 4:
                        raise AssertionError("frame out of range " + str(idx))
                    seen.add(idx)
                    if len(report["samples"]) < 160:
                        report["samples"].append({
                            "sec": round(time.monotonic() - page_open, 3),
                            "frame": idx,
                            "world_x": s["player"]["x"],
                            "world_vx": s["player"]["vx"],
                            "hframes": s["human_sprite_hframes"]})
                    if idx == 1 and not (OUT / "walk-phase-1.png").exists():
                        canvas.screenshot(path=str(OUT / "walk-phase-1.png"))
                    if idx == 3 and not (OUT / "walk-phase-3.png").exists():
                        canvas.screenshot(path=str(OUT / "walk-phase-3.png"))
            finally:
                page.keyboard.up("d")
            after_x = snapshot(page)["player"]["x"]
            report["world_move_dx"] = float(after_x) - float(before_x)
            report["walk_seen"] = sorted(seen)
            until(page, "s.human_sprite_hframes === 12 && "
                        "s.base_walk_active === false && "
                        "s.animation_clip_intent === 'idle_guard_front'", 20000)
            page.wait_for_timeout(400)
            canvas.screenshot(path=str(OUT / "after-walk.png"))
            if seen != set(range(4)):
                raise AssertionError("walking visually sampled only: " + str(sorted(seen)))
            if report["world_move_dx"] < 1.0:
                raise AssertionError("no physical player movement")
            if report["js_errors"]:
                raise AssertionError("JS errors: " + str(report["js_errors"]))
            report["status"] = "PASS_LIVE_WALK_4_VIDEO_PHYSICAL_MOVEMENT"
            print("WALK_4_REAL_VIDEO_PASS: frames 0,1,2,3 seen on published "
                  "canonical game, actual world distance "+str(report["world_move_dx"]))
        except Exception as ex:
            report["error"] = str(ex)
            print("WALK_4_REAL_VIDEO_FAIL: " + str(ex))
            raise
        finally:
            report["capture_end_seconds"] = time.monotonic() - page_open
            (OUT / "walk-live-evidence.json").write_text(
                json.dumps(report, indent=2), encoding="utf-8")
            ctx.close()
            try:
                video_file = Path(video.path())
                if video_file.exists():
                    shutil.copyfile(video_file, OUT / "base-walk-gameplay.webm")
                    print("CAPTURED_PUBLIC_CANVAS_WEBM " +
                          str((OUT / "base-walk-gameplay.webm").stat().st_size))
            except Exception as e:
                print("VIDEO_ARTIFACT_WARNING: " + str(e))
            browser.close()


if __name__ == "__main__":
    main()
