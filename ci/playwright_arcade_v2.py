"""Beast Arena V2 controls: real Chromium keyboard -> Godot 60Hz state.

This is a functional control/pose-intent gate. Missing independently authored
Jade frames MUST remain PENDING_ART, not 'visual acceptance'. Never fake or
inject motor/combat state from JavaScript.
"""
import json
import os
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = ("https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/"
       "?e2e=1&controls=v2&art=approved&pixel=1")
OUT = Path("playwright-report/arcade-v2")
OUT.mkdir(parents=True, exist_ok=True)


def snap(page):
    return page.evaluate("window.__beastPhysicsDebug || null")


def expect_state(page, description, predicate, timeout=4000):
    page.wait_for_function(
        """(predicate) => {
            const s = window.__beastPhysicsDebug;
            return !!s && Function("s", "return (" + predicate + ")")(s);
        }""",
        arg=predicate, timeout=timeout, polling=40)
    current = snap(page)
    if not current:
        raise AssertionError(description + ": debug state absent")
    return current


def main():
    report = {"url": URL, "status": "NOT_RUN", "cases": {}, "pages": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--enable-webgl", "--use-gl=angle", "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader", "--disable-dev-shm-usage"
        ])
        page = browser.new_page(viewport={"width": 1200, "height": 800})
        page.on("pageerror", lambda err: report["pages"].append(str(err)))
        try:
            for attempt in range(6):
                response = page.goto(URL, wait_until="domcontentloaded",
                                     timeout=50000)
                if response is not None and response.status == 200:
                    break
                page.wait_for_timeout(5000)
            else:
                raise AssertionError("V2 arcade preview did not return HTTP 200")
            page.wait_for_function(
                "() => window.__beastPhysicsDebug?.ready === true",
                timeout=180000, polling=500)
            canvas = page.locator("canvas#canvas").first
            if not canvas.count():
                canvas = page.locator("canvas").first
            canvas.wait_for(state="visible", timeout=20000)
            canvas.click(force=True)
            start = snap(page)
            expected_source = os.getenv("BEAST_EXPECT_BUILD_RUN_ID", "").strip()
            expected_pipeline = os.getenv("BEAST_EXPECT_PIPELINE_SHA", "").strip()
            if expected_source and str(start.get("build_run_id")) != expected_source:
                raise AssertionError("V2 stale PCK build " + str(start.get("build_run_id")))
            if expected_pipeline and start.get("pipeline_sha") != expected_pipeline:
                raise AssertionError("V2 stale PCK pipeline " + str(start.get("pipeline_sha")))
            if not re.fullmatch(r"[0-9a-f]{40}", start.get("source_sha", "")):
                raise AssertionError("V2 missing private source commit")
            if (start.get("controls_v2_enabled") is not True
                    or start.get("animation_source_ready") is not False
                    or start.get("animation_clip_intent") != "idle_breathe_front"):
                raise AssertionError("V2 inputs or PENDING_ART signal missing: " + str(start))
            report["version"] = {x: start.get(x) for x in
                                 ("source_sha", "pipeline_sha", "build_run_id")}
            report["cases"]["source_art"] = "PENDING_ART, not visual acceptance"

            page.keyboard.down("w")
            up = expect_state(
                page, "W upward real world velocity / front appearance",
                "s.animation_clip_intent === 'walk_up_front_view' && "
                "s.player.vz < -0.4 && (s.human_sprite_frame % 4) === 0")
            page.keyboard.up("w")
            page.wait_for_timeout(350)
            page.keyboard.down("s")
            down = expect_state(
                page, "S downward real world velocity / front appearance",
                "s.animation_clip_intent === 'walk_down_front_view' && "
                "s.player.vz > 0.4 && (s.human_sprite_frame % 4) === 0")
            page.keyboard.up("s")
            report["cases"]["w_s"] = {
                "up_vz": up["player"]["vz"], "down_vz": down["player"]["vz"],
                "front_sprite": True}
            canvas.screenshot(path=str(OUT / "front-w-s-preview.png"))

            # A single press MUST stay walk, but release+A within 16 physics
            # ticks accelerates the true 3D motor and selects run_left.
            page.wait_for_timeout(400)
            page.keyboard.down("a")
            once = expect_state(
                page, "A single press must walk, not sprint",
                "s.animation_clip_intent === 'walk_left' && "
                "!s.sprint_requested && s.player.vx < -0.2")
            page.keyboard.up("a")
            page.wait_for_timeout(45)
            page.keyboard.down("a")
            left = expect_state(
                page, "A+A must activate true left sprint and run clip intent",
                "s.sprint_requested === true && s.sprint_direction === -1 && "
                "s.animation_clip_intent === 'run_left' && s.player.vx < -0.7")
            page.keyboard.up("a")
            page.wait_for_timeout(350)
            if snap(page).get("sprint_requested"):
                raise AssertionError("release A did not cancel sprint")
            report["cases"]["left_double_tap"] = {
                "walk_vx": once["player"]["vx"],
                "run_vx": left["player"]["vx"]}
            canvas.screenshot(path=str(OUT / "run-left-prototype.png"))

            page.keyboard.down("d")
            expect_state(page, "single D walk only",
                         "s.animation_clip_intent === 'walk_right' && !s.sprint_requested")
            page.keyboard.up("d")
            page.wait_for_timeout(45)
            page.keyboard.down("d")
            right = expect_state(
                page, "D+D must choose rightward run and actual motor",
                "s.sprint_requested === true && s.sprint_direction === 1 && "
                "s.animation_clip_intent === 'run_right' && s.player.vx > 0.7")
            page.keyboard.up("d")
            report["cases"]["right_double_tap"] = {"run_vx": right["player"]["vx"]}
            canvas.screenshot(path=str(OUT / "run-right-prototype.png"))

            # Real held key triggers a single authoritative attack after the
            # 7-tick F/G chord buffer; observe combat source, not just glyphs.
            expect_state(page, "stop after right sprint",
                         "abs(s.player.vx) < 0.2 && s.human_attack_id === ''",
                         timeout=5000)
            page.keyboard.down("f")
            punch = expect_state(
                page, "F must begin real punch with front clip selected",
                "s.human_attack_id === 'light_punch' && "
                "s.human_attack_frame > 0 && "
                "s.animation_clip_intent === 'punch_front'")
            page.keyboard.up("f")
            report["cases"]["f_punch"] = {"attack_id": punch["human_attack_id"]}
            expect_state(page, "punch recovery", "s.human_attack_id === ''",
                         timeout=6000)
            page.keyboard.down("g")
            kick = expect_state(
                page, "G must begin independent kick data, not heavy punch",
                "s.human_attack_id === 'front_kick' && "
                "s.human_attack_frame > 0 && "
                "s.animation_clip_intent === 'kick_front'")
            page.keyboard.up("g")
            report["cases"]["g_kick"] = {"attack_id": kick["human_attack_id"]}
            expect_state(page, "kick recovery",
                         "s.human_attack_id === '' && s.player.grounded",
                         timeout=6000)

            before_jump = snap(page)["player"]["jump_events"]
            page.keyboard.down("f")
            page.keyboard.down("g")
            chord = expect_state(
                page, "F+G must jump without punch or kick",
                f"s.player.jump_events > {before_jump} && s.player.vy > 0 && "
                "s.human_attack_id === '' && "
                "s.animation_clip_intent === 'jump_front'",
                timeout=5000)
            page.keyboard.up("g")
            page.keyboard.up("f")
            report["cases"]["fg_jump"] = {
                "jump_before": before_jump,
                "jump_after": chord["player"]["jump_events"],
                "attack_id": chord["human_attack_id"]}
            canvas.screenshot(path=str(OUT / "fg-jump-prototype.png"))
            if report["pages"]:
                raise AssertionError("browser script errors: " + str(report["pages"][:5]))
            report["status"] = "PASS_FUNCTIONAL_ART_PENDING"
            print("ARCADE V2 WEB PASS: W/S front, A+A/D+D sprint, F punch, G kick, F+G jump; visual PENDING_ART")
        except Exception as exc:
            report["status"] = "FAIL"
            report["error"] = str(exc)
            report["last_snapshot"] = snap(page)
            print("ARCADE V2 WEB FAIL: " + str(exc))
            raise
        finally:
            (OUT / "result.json").write_text(
                json.dumps(report, indent=2, ensure_ascii=False))
            browser.close()


if __name__ == "__main__":
    main()
