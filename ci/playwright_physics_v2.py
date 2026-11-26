"""Godot 3D Physics V2 staging E2E: never confuse with production P1.5.

All state is public opt-in (?e2e=1); no private source/tokens stored.
"""
import json
import os
import re
import time
from collections import Counter
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

def floor_tile_diversity(image_path: Path):
    # This crop deliberately avoids character pixels, ramp stripes,
    # foreground props and HUD. The old untextured BoxMesh displayed only
    # one uniform color here while all older movement tests returned PASS.
    with Image.open(image_path).convert("RGB") as image:
        w, h = image.size
        patch = image.crop((int(w * 0.13), int(h * 0.50),
                            int(w * 0.21), int(h * 0.61)))
        pixels = Counter(patch.getdata())
        total = sum(pixels.values())
        strong = sum(1 for n in pixels.values() if n / max(1, total) >= 0.01)
        dominant = max(pixels.values(), default=0) / max(1, total)
        return {"visible_color_groups": strong, "dominant_color_fraction": round(dominant, 4)}


def walkable_moss_green_fraction(image_path: Path) -> float:
    # At 1200x800 exported Godot canvas resolution this small unoccupied
    # ground patch is BEHIND Jade after holding W, not on the physical
    # retaining wall. The old `map_moss.svg` sampled the first 64px
    # GREY WALL source band here, making grounded W/J/K look suspended.
    # Real floor must look grass-green at this playable world Z.
    with Image.open(image_path).convert("RGB") as img:
        w, h = img.size
        region = img.crop((int(w * 0.45), int(h * 0.63),
                           int(w * 0.50), int(h * 0.68)))
        pixels = list(region.getdata())
        green = sum(1 for red, g, blue in pixels
                    if g > red + 23 and g > blue + 9)
        return green / max(1, len(pixels))


def visible_cyan_guard_pixels(image_path: Path) -> int:
    # Require actual WebGL2 screenshot evidence, not just a gameplay
    # telemetry counter. Palette is intentionally high-saturation aqua;
    # ordinary Moss stage/human colors have zero matching pixels.
    with Image.open(image_path).convert("RGB") as image:
        return sum(1 for red, green, blue in image.getdata()
                   if red <= 165 and green >= 215 and blue >= 210
                   and blue > red + 45)


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
            # Visual V0 is separate from the camera-angle regression gate.
            # Refuse a stale Web PCK even if old movement assertions pass.
            expected_pipeline = os.environ.get("BEAST_EXPECT_PIPELINE_SHA", "").strip()
            expected_build_run = os.environ.get("BEAST_EXPECT_BUILD_RUN_ID", "").strip()
            if expected_pipeline and first.get("pipeline_sha") != expected_pipeline:
                raise AssertionError(
                    "STALE_PAGES: loaded PCK public SHA %s but triggering CI used %s" %
                    (first.get("pipeline_sha"), expected_pipeline))
            if expected_build_run and str(first.get("build_run_id")) != expected_build_run:
                raise AssertionError(
                    "STALE_PAGES: loaded PCK run %s instead of triggering build %s" %
                    (first.get("build_run_id"), expected_build_run))
            if not re.fullmatch(r"[0-9a-f]{40}", first.get("source_sha", "")):
                raise AssertionError("missing exact private source SHA in deployed PCK")
            if not re.fullmatch(r"[0-9a-f]{40}", first.get("pipeline_sha", "")):
                raise AssertionError("missing public Actions build commit SHA")
            if not str(first.get("build_run_id", "")).isdigit():
                raise AssertionError("missing actual deployment build run ID")
            report["version"] = {key: first[key] for key in
                                  ("source_sha", "pipeline_sha", "build_run_id", "visual_style_id")}
            if first.get("visual_style_id") != "v2-compact-pixel-stage-20261126":
                raise AssertionError("stale or wrong Physics0 visual build: " +
                                     str(first.get("visual_style_id")))
            if not (12.0 <= abs(first["camera"]["pitch_deg"]) <= 25.0):
                raise AssertionError("Nekketsu side-biased camera pitch outside visual profile")
            if abs(first.get("horizontal_world_axis_screen_dy", 999.0)) > 0.15:
                raise AssertionError("Horizontal world axis is not screen-horizontal")

            if first["ramp_rise_m"] < 2.0 or first["obstacles"] < 5:
                raise AssertionError("3D ramp and props missing")
            # Real obstructions are authored meshes, not flat colored cubes.
            # A skin must decorate each physical prop on both stages.
            if first.get("pixel_prop_skins") != 6:
                raise AssertionError("Moss stage is missing original textured obstacle skins")
            if first.get("pixel_floor_sections") != 3 or first.get("pixel_facade_panels", 0) < 10:
                raise AssertionError("Original pixel art layers missing in Moss scene")
            if first.get("original_hud_portraits") != 4:
                raise AssertionError("Four authored human portrait badges are missing from NES-style 2v2 HUD")
            if first.get("human_sprite_hframes") != 4 or first.get("human_sprite_vframes") != 20:
                raise AssertionError("Original 80-frame directional human animation atlas not loaded")
            if abs(first.get("human_sprite_pixel_size", 0.0) - 0.025) > 0.0001:
                raise AssertionError("Human pixel scale differs from approved test contract")
            if first["map_width_m"] < 60.0:
                raise AssertionError("Stage should scroll beyond viewport")
            if not (25.0 <= first.get("map_depth_m", 0.0) <= 28.0):
                raise AssertionError("Moss stage depth loses compact horizontal brawler composition")
            if first.get("ramp_visual_count", 0) < 25 or first.get("ramp_angle_deg", 0) < 14:
                raise AssertionError("Visible slope markers and 14+ degree rise missing")
            if first.get("ramp_end_y", 0) - first.get("ramp_start_y", 0) < 3.3:
                raise AssertionError("Moss ramp physical height not large enough to notice")
            page.keyboard.down("g")
            page.wait_for_timeout(380)
            guard_on = snap(page)
            if guard_on.get("player_guarding") is not True:
                raise AssertionError("Hold G must activate authoritative facing guard")
            if guard_on.get("human_visual_action") != "guard":
                raise AssertionError("G guard animation not synchronized with combat state")
            page.keyboard.up("g")
            page.wait_for_timeout(250)
            if snap(page).get("player_guarding") is not False:
                raise AssertionError("G release must stop authoritative guard")
            report["player_guard_input_pass"] = True
            canvas.screenshot(path=str(OUT / "moss-start.png"))
            # Record visual-first art before the fighters take any damage.
            page.keyboard.press("F5")
            page.wait_for_timeout(480)
            moss_pixel = snap(page)
            if (not moss_pixel.get("pixel_projection_mode") or
                    moss_pixel.get("pixel_view_fighters") != 4 or
                    moss_pixel.get("pixel_view_floor_tiles", 0) < 60 or
                    moss_pixel.get("pixel_floor_details", 0) < 15):
                raise AssertionError("Moss F5 2D start scene is missing map/4 humans")
            canvas.screenshot(path=str(OUT / "moss-nes-style-2d-start.png"))
            report["moss_pixel_2d_start"] = {
                "tiles": moss_pixel["pixel_view_floor_tiles"],
                "floor_details": moss_pixel["pixel_floor_details"],
                "fighters": moss_pixel["pixel_view_fighters"],
                "colors": floor_tile_diversity(OUT / "moss-nes-style-2d-start.png")}
            # Artist A/B must visibly differ IN THE REAL CANVAS, not
            # merely change an internal flag. F6 changes ONLY the hero atlas,
            # while preserving 3D feet, hitboxes and the fixed world skyline.
            hero_before = snap(page)
            page.keyboard.press("F6")
            page.wait_for_function(
                "() => window.__beastPhysicsDebug && window.__beastPhysicsDebug.hero_art_concept_enabled === true",
                timeout=7000, polling=75)
            hero_after = snap(page)
            if (hero_after.get("combat_hp") != hero_before.get("combat_hp") or
                    hero_after.get("map_id") != hero_before.get("map_id") or
                    not hero_after.get("pixel_projection_mode")):
                raise AssertionError("F6 art comparison changed human gameplay state")
            page.wait_for_timeout(180)
            art_compare_path = OUT / "moss-jade-scarf-concept.png"
            canvas.screenshot(path=str(art_compare_path))
            with (Image.open(OUT / "moss-nes-style-2d-start.png").convert("RGB") as
                    baseline_image, Image.open(art_compare_path).convert("RGB") as concept_image):
                if baseline_image.size != concept_image.size:
                    raise AssertionError("F6 artist mode modified pixel viewport dimensions")
                changed_pixels = sum(1 for old, new in zip(
                    baseline_image.getdata(), concept_image.getdata()) if old != new)
            report["original_jade_scarf_art_comparison"] = {
                "active": True, "changed_visible_pixels": changed_pixels,
                "same_hp": True, "same_level": True}
            if changed_pixels < 50:
                raise AssertionError("F6 concept artist sprite is not visibly different in actual 2D canvas")
            page.keyboard.press("F6")
            page.wait_for_function(
                "() => window.__beastPhysicsDebug && window.__beastPhysicsDebug.hero_art_concept_enabled === false",
                timeout=7000, polling=75)
            # The separately authored, image-generated original 80-cell
            # character atlas must also work in the ACTUAL Godot WebGL
            # runtime. The P key swaps only art, never the authoritative
            # 3D CharacterBody3D, combat state, HP or floor projection.
            page.keyboard.press("p")
            page.wait_for_function(
                "() => window.__beastPhysicsDebug && window.__beastPhysicsDebug.hero_art_painted_enabled === true",
                timeout=8000, polling=70)
            painted_snapshot = snap(page)
            if (painted_snapshot.get("combat_hp") != hero_before.get("combat_hp") or
                    painted_snapshot.get("map_id") != hero_before.get("map_id") or
                    not painted_snapshot.get("pixel_projection_mode")):
                raise AssertionError("P high-detail character art changed physics/HP/level")
            page.wait_for_timeout(160)
            painted_path = OUT / "moss-jade-painted-concept.png"
            canvas.screenshot(path=str(painted_path))
            with (Image.open(OUT / "moss-nes-style-2d-start.png").convert("RGB") as
                    baseline_image, Image.open(painted_path).convert("RGB") as painted_image):
                if baseline_image.size != painted_image.size:
                    raise AssertionError("P high-detail sprite altered Web viewport")
                painted_pixels = sum(1 for old, new in zip(
                    baseline_image.getdata(), painted_image.getdata()) if old != new)
            if painted_pixels < 300:
                raise AssertionError("Original WebP painted 80-frame Jade is invisible in Chromium: "
                                     + str(painted_pixels))
            report["original_jade_painted_art_comparison"] = {
                "active": True, "changed_visible_pixels": painted_pixels,
                "same_hp": True, "same_level": True}
            page.keyboard.press("p")
            page.wait_for_function(
                "() => window.__beastPhysicsDebug && window.__beastPhysicsDebug.hero_art_painted_enabled === false",
                timeout=8000, polling=70)
            # This is the ACTUAL user's approved expressive chibi drawing
            # with teal spiky hair, cream vest and red scarf, not the older
            # painted/flat-rect placeholder. Compare real canvas pixels and
            # preserve gameplay state. PNG contains 4x20 80px pose cells.
            page.keyboard.press("F7")
            page.wait_for_function(
                "() => window.__beastPhysicsDebug && window.__beastPhysicsDebug.hero_art_approved_enabled === true",
                timeout=8000, polling=70)
            approved_state = snap(page)
            if (approved_state.get("map_id") != hero_before.get("map_id") or
                    approved_state.get("combat_hp") != hero_before.get("combat_hp") or
                    not approved_state.get("pixel_projection_mode") or
                    approved_state.get("hero_atlas_frame_size") != 80):
                raise AssertionError("Approved true 80px fighter source was not shown or changed real physical state: "
                                     + str(approved_state.get("hero_atlas_frame_size")))
            page.wait_for_timeout(180)
            approved_path = OUT / "moss-jade-approved-exact-art.png"
            canvas.screenshot(path=str(approved_path))
            with (Image.open(OUT / "moss-nes-style-2d-start.png").convert("RGB") as
                    baseline, Image.open(approved_path).convert("RGB") as approved_art):
                if baseline.size != approved_art.size:
                    raise AssertionError("F7 approved sprite modified Web viewport")
                approved_pixel_difference = sum(1 for old, new in zip(
                    baseline.getdata(), approved_art.getdata()) if old != new)
            if approved_pixel_difference < 700:
                raise AssertionError("Approved hand-drawn chibi art not visible in real WebGL: "
                                     + str(approved_pixel_difference))
            report["user_approved_jade_art_comparison"] = {
                "active": True, "atlas_cell_px": 80,
                "visible_changed_pixels": approved_pixel_difference,
                "physical_hp_unchanged": True, "physical_map_unchanged": True}
            # Isolate the original WJK art test on a REAL grounded stage.
            # Previous attempts sampled W after unrelated movement and
            # accumulated 0 grounded frames on the native motor. Never
            # replace real-contact proof with an input-only screenshot.
            page.keyboard.press("t")
            page.wait_for_function(
                "() => {const s=window.__beastPhysicsDebug; "
                "return s && s.hero_art_approved_enabled && s.player && "
                "s.player.grounded && "
                "Math.abs(s.human_physical_ground_clearance_m) < 0.25 && "
                "s.human_visual_gait === 'idle';}",
                timeout=11000, polling=70)
            # Explicit canvas focus survives Godot's map reload on T.
            # A focused keyboard input is a real WebGL input contract,
            # not a fake telemetry command or simulated game movement.
            canvas.evaluate("""element => {
                element.setAttribute('tabindex', '0');
                element.focus();
            }""")
            if not canvas.evaluate("element => document.activeElement === element"):
                raise AssertionError("Canvas lost keyboard focus after native T map reset")
            # Start sampling BEFORE pressing W, and collect actual Godot
            # frame telemetry in Chromium, not a delayed Python round-trip.
            page.evaluate("""() => {
                window.__beastWFootSamples = [];
                window.__beastWFootSampling = true;
                function sample() {
                    const s = window.__beastPhysicsDebug;
                    if (s && s.human_approved_motion_set) {
                        window.__beastWFootSamples.push({
                            phase: s.human_gait_phase,
                            row: Math.floor(s.human_sprite_frame / 4),
                            facing: s.human_sprite_frame % 4,
                            gait: s.human_visual_gait,
                            stride: s.human_ground_stride_m,
                            grounded: s.player.grounded,
                            clearance_m: s.human_physical_ground_clearance_m,
                            pad: s.human_sprite_foot_padding_px,
                            offset_y: s.human_sprite_offset_y
                        });
                    }
                    if (window.__beastWFootSampling &&
                        window.__beastWFootSamples.length < 240)
                        requestAnimationFrame(sample);
                }
                requestAnimationFrame(sample);
            }""")
            gait_started = snap(page)
            start_tick = gait_started["tick"]
            page.keyboard.down("w")
            try:
                page.wait_for_function(
                    "() => {const s=window.__beastPhysicsDebug; "
                    "return s && s.human_approved_motion_set && "
                    "s.player.grounded && s.player.vz < -0.25 && "
                    "s.human_sprite_frame % 4 === 3 && "
                    "['run','walk'].includes(s.human_visual_gait);}",
                    timeout=9000, polling=70)
            except Exception as exc:
                diagnose = snap(page)
                raise AssertionError(
                    "W did not move the grounded player after canvas focus: "
                    + str({"tick_advance": diagnose.get("tick", 0) - start_tick,
                           "player": diagnose.get("player"),
                           "gait": diagnose.get("human_visual_gait"),
                           "frame": diagnose.get("human_sprite_frame"),
                           "focus": canvas.evaluate(
                               "element => document.activeElement === element")})
                    ) from exc
            approved_rear = snap(page)
            if (approved_rear.get("human_sprite_frame", -1) % 4 != 3 or
                    approved_rear.get("human_visual_gait") not in ("walk", "run") or
                    approved_rear.get("hero_atlas_frame_size") != 80 or
                    not approved_rear.get("human_approved_motion_set")):
                raise AssertionError("W must use original full-body approved Jade: " + str(approved_rear))
            canvas.screenshot(path=str(OUT / "moss-jade-approved-rear-motion.png"))
            # Browser software-WebGL draws at lower FPS than the 60Hz
            # motor; a 480ms screenshot sampler missed the very brief
            # contact phase 0 while actual W travelled 3.29m grounded.
            # Observe >2 full 4-phase stride cycles with 1050ms extra
            # while player stays inside the 26m-deep Moss stage.
            page.wait_for_timeout(1050)
            gait_samples = page.evaluate("""() => {
                window.__beastWFootSampling = false;
                return window.__beastWFootSamples || [];
            }""")
            grounded_samples = [item for item in gait_samples
                                if item.get("gait") == "run" and item.get("grounded")]
            observed_phases = {item.get("phase") for item in grounded_samples}
            if any(item.get("facing") != 3 for item in grounded_samples):
                raise AssertionError("W lost rear facing while running")
            stride_begin = grounded_samples[0]["stride"] if grounded_samples else 0.0
            stride_end = grounded_samples[-1]["stride"] if grounded_samples else 0.0
            if len(observed_phases) != 4 or stride_end - stride_begin <= 0.9:
                raise AssertionError(
                    "W did not alternate four distance-driven foot phases: "
                    + str({"phases": sorted(observed_phases),
                           "grounded_samples": len(grounded_samples),
                           "distance": stride_end - stride_begin,
                           "sampled_foot_rows": [
                               (item["phase"], item["row"], round(item["stride"], 2),
                                round(item["clearance_m"], 3))
                               for item in grounded_samples[:60]],
                           "last_state": snap(page).get("player")}))
            bad_anchors = [x for x in grounded_samples
                           if abs(float(x.get("offset_y", 99))
                                  + float(x.get("pad", 99))) > 0.1
                           or abs(float(x.get("clearance_m", 99))) > 0.25]
            if bad_anchors:
                raise AssertionError(
                    "Jade W foot pivot is NOT on native physical ground: "
                    + str(bad_anchors[:5]))
            page.keyboard.up("w")
            page.wait_for_timeout(140)
            # While facing rear, J and K must render full illustrated bodies
            # on their physical attack clock. Godot ART-23 verifies alpha,
            # height and planted feet for all 4 directions.
            page.keyboard.press("j")
            page.wait_for_timeout(55)
            light_visual = snap(page)
            if (light_visual.get("human_visual_gait") != "attack" or
                    light_visual.get("human_sprite_frame", -1) // 4 not in (7, 8)):
                raise AssertionError("J failed to show complete rear light punch art: " + str(light_visual))
            canvas.screenshot(path=str(OUT / "moss-jade-approved-W-J.png"))
            page.wait_for_timeout(550)  # finish J recovery before K input
            page.keyboard.press("k")
            page.wait_for_timeout(55)
            heavy_visual = snap(page)
            if (heavy_visual.get("human_visual_gait") != "attack" or
                    heavy_visual.get("human_sprite_frame", -1) // 4 not in (9, 10)):
                raise AssertionError("K failed to show complete rear heavy punch art: " + str(heavy_visual))
            canvas.screenshot(path=str(OUT / "moss-jade-approved-W-K.png"))
            # A visual test, not only physics telemetry: the back half
            # of the playable XZ plane must display actual GRASS, not the
            # first 64px vertical retaining WALL painted as floor tiles.
            # Otherwise feet look like they float in front of a wall even
            # when is_on_floor() and PNG shoe pivot are both correct.
            j_grass = walkable_moss_green_fraction(
                OUT / "moss-jade-approved-W-J.png")
            k_grass = walkable_moss_green_fraction(
                OUT / "moss-jade-approved-W-K.png")
            if min(j_grass, k_grass) < 0.40:
                raise AssertionError(
                    "W/J/K rear depth still shows wall instead of real walkable grass: "
                    + str({"j_green_fraction": round(j_grass, 3),
                           "k_green_fraction": round(k_grass, 3)}))
            report["jade_wjk_physics_sprite_regression"] = {
                "walkable_grass_visible_j": round(j_grass, 3),
                "walkable_grass_visible_k": round(k_grass, 3),
                "w_unique_run_phases": sorted(observed_phases),
                "travel_stride_m": round(stride_end - stride_begin, 3),
                "grounded_samples": len(grounded_samples),
                "foot_anchor_max_error_px": round(max(
                    (abs(float(x["offset_y"]) + float(x["pad"]))
                     for x in grounded_samples), default=0.0), 3),
                "j_attack_row": light_visual["human_sprite_frame"] // 4,
                "k_attack_row": heavy_visual["human_sprite_frame"] // 4,
                "physical_hp_unchanged": heavy_visual.get("combat_hp") == hero_before.get("combat_hp")}
            # This fixture only verifies a TRUE moving rear-facing pose.
            # Do not require instant idle on W release: the real Godot
            # character can coast/slip with slope/gravity and remain
            # airborne for several frames. The pre-existing movement/
            # physical-stop tests remain independently strict below.
            page.wait_for_timeout(160)
            report["user_approved_jade_rear_motion"] = {
                "active": True,
                "direction": approved_rear["human_sprite_frame"] % 4,
                "pose_row": approved_rear["human_sprite_frame"] // 4,
                "gait": approved_rear["human_visual_gait"],
                "screenshot": "moss-jade-approved-rear-motion.png"}
            page.keyboard.press("F7")
            page.wait_for_function(
                "() => window.__beastPhysicsDebug && window.__beastPhysicsDebug.hero_art_approved_enabled === false",
                timeout=8000, polling=70)
            # Isolate the NEW W/rear-art fixture from all original 3D
            # movement tests. W changes actual world Z and can leave the
            # actor airborne/on a slope even after key release, which
            # invalidates the old D-only gait baseline. T is the game's
            # existing authoritative respawn to the same flat start.
            page.keyboard.press("t")
            page.wait_for_timeout(440)
            reset = snap(page)
            if (reset.get("map_id") != hero_before.get("map_id") or
                    reset.get("combat_hp") != hero_before.get("combat_hp") or
                    reset.get("hero_art_approved_enabled")):
                raise AssertionError("T did not isolate rear art fixture before physics regression tests")
            page.keyboard.press("F5")
            page.wait_for_timeout(180)
            if snap(page).get("pixel_projection_mode"):
                raise AssertionError("Moss F5 2D cannot return to 3D physics preview")
            report["moss_visible_floor_fraction"] = round(
                visible_floor_fraction(OUT / "moss-start.png"), 3)
            report["moss_tile_diversity"] = floor_tile_diversity(OUT / "moss-start.png")
            if (report["moss_tile_diversity"]["visible_color_groups"] < 3 or
                    report["moss_tile_diversity"]["dominant_color_fraction"] > 0.85):
                raise AssertionError("Moss pixel tile top surface is INVISIBLE "
                                     "despite valid material/mesh and collision: " +
                                     str(report["moss_tile_diversity"]))
            if report["moss_visible_floor_fraction"] < 0.14:
                raise AssertionError(
                    "Stage floor appears black/blank in WebGL2: "
                    + str(report["moss_visible_floor_fraction"]))

            page.keyboard.down("d")
            page.wait_for_timeout(700)
            running_visual = snap(page)
            report["physics_driven_run_art"] = {
                "gait": running_visual.get("human_visual_gait"),
                "frame": running_visual.get("human_sprite_frame"),
                "velocity_x": running_visual.get("player", {}).get("vx")}
            if (running_visual.get("human_visual_gait") != "run" or
                    running_visual.get("human_sprite_frame", -1) // 4 not in (3, 4) or
                    running_visual.get("player", {}).get("vx", 0.0) < 2.5):
                raise AssertionError("running sprite did not track real physical speed: " +
                                     str(report["physics_driven_run_art"]))
            canvas.screenshot(path=str(OUT / "moss-running-real-speed.png"))
            page.wait_for_timeout(250)
            page.keyboard.up("d")
            # The physical motor has inertia (especially at slope entry),
            # and CanvasItem's art can be a render frame behind the 60Hz
            # physics snapshot. Wait for BOTH a real stop and idle frame.
            page.wait_for_function(
                "() => {const s=window.__beastPhysicsDebug;"
                "if (!s || !s.player) return false;"
                "const speed=Math.hypot(s.player.vx, s.player.vz);"
                "return speed < 0.20 && s.human_visual_gait === 'idle';}",
                timeout=4000, polling=60)
            moved = snap(page)
            report["physics_driven_run_art_pass"] = True
            report["movement"] = moved
            report["player_dx"] = round(moved["player"]["x"]-first["player"]["x"], 3)
            if report["player_dx"] <= 0.8:
                raise AssertionError("3D motor did not respond to D: " + str(report["player_dx"]))
            if moved.get("human_sprite_frame", -1) % 4 != 2:
                raise AssertionError("Directional pixel sprite did not face right on D movement")
            if moved["player"]["vx"] > 5.0:
                raise AssertionError("3D horizontal motor exceeded configured speed")
            canvas.screenshot(path=str(OUT / "moss-moving.png"))
            page.keyboard.press("j")
            page.wait_for_timeout(180)
            attack_visual = snap(page)
            report["human_attack_visual"] = attack_visual
            # Combat owns the 60Hz strike timeline. The old
            # human_visual_action preview is intentionally not authoritative:
            # it can outlive a hitbox/recovery and was removed from genuine
            # attacks. Assert the PHYSICAL clock and the corresponding art.
            if (attack_visual.get("human_visual_gait") != "attack" or
                    not 1 <= attack_visual.get("human_attack_frame", -1) < 16):
                raise AssertionError(
                    "J did not begin the authoritative 60Hz light attack: "
                    + str({
                        "gait": attack_visual.get("human_visual_gait"),
                        "frame": attack_visual.get("human_attack_frame"),
                        "sprite": attack_visual.get("human_sprite_frame")}))
            if attack_visual.get("human_sprite_frame", -1) // 4 not in (7, 8):
                raise AssertionError("physical attack art not on original punch rows")
            canvas.screenshot(path=str(OUT / "moss-light-preview.png"))
            # The selected pose follows the physical attack clock; 3D
            # hit volume and damage are independently asserted by Godot.

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
            if not (30.0 <= docks.get("map_depth_m", 0.0) <= 32.0):
                raise AssertionError("Docks stage depth is outside compact 2.5D composition")
            if docks["actors"] != 4 or docks["obstacles"] < 5:
                raise AssertionError("3D actors / native colliders not created on switch")
            if docks.get("pixel_prop_skins") != 6:
                raise AssertionError("Night Docks missing original prop cladding")
            if docks.get("pixel_floor_sections") != 3 or docks.get("pixel_facade_panels", 0) < 10:
                raise AssertionError("Original pixel art layers missing in Docks scene")
            canvas.screenshot(path=str(OUT / "docks-high-platform.png"))
            page.keyboard.press("F5")
            page.wait_for_timeout(480)
            docks_pixel = snap(page)
            if (not docks_pixel.get("pixel_projection_mode") or
                    docks_pixel.get("map_id") != "night_docks" or
                    docks_pixel.get("pixel_view_fighters") != 4 or
                    docks_pixel.get("pixel_view_floor_tiles", 0) < 60 or
                    docks_pixel.get("pixel_floor_details", 0) < 15):
                raise AssertionError("Docks F5 2D scene missing original map/characters")
            canvas.screenshot(path=str(OUT / "docks-nes-style-2d-start.png"))
            report["docks_pixel_2d_start"] = {
                "tiles": docks_pixel["pixel_view_floor_tiles"],
                "floor_details": docks_pixel["pixel_floor_details"],
                "fighters": docks_pixel["pixel_view_fighters"],
                "colors": floor_tile_diversity(OUT / "docks-nes-style-2d-start.png")}
            page.keyboard.press("F5")
            page.wait_for_timeout(180)
            if snap(page).get("pixel_projection_mode"):
                raise AssertionError("Docks F5 could not return to original 3D view")
            if docks.get("ramp_visual_count", 0) < 25 or docks.get("ramp_angle_deg", 0) < 14:
                raise AssertionError("Docks downhill visual face and elevation labels missing")
            if docks["ramp_start_y"] - docks["ramp_end_y"] < 3.3:
                raise AssertionError("Docks downhill should descend by >= 3.3m")
            report["docks_visible_floor_fraction"] = round(
                visible_floor_fraction(OUT / "docks-high-platform.png"), 3)
            report["docks_tile_diversity"] = floor_tile_diversity(OUT / "docks-high-platform.png")
            if (report["docks_tile_diversity"]["visible_color_groups"] < 3 or
                    report["docks_tile_diversity"]["dominant_color_fraction"] > 0.85):
                raise AssertionError("Docks pixel tile top surface is INVISIBLE "
                                     "despite valid material/mesh and collision: " +
                                     str(report["docks_tile_diversity"]))
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
            # The real 3D player climbs/descends, but a fixed 2.5D stage
            # must not pan vertically in reaction to elevation changes.
            for stage, checkpoint in (
                ("moss ramp", moss_ramp_mid),
                ("docks ramp", docks_slope_mid),
                ("docks switch", docks),
            ):
                if abs(checkpoint["camera"]["y"] - first["camera"]["y"]) > 0.06:
                    raise AssertionError("stage camera vertically bobs during " + stage)
                if abs(checkpoint.get("horizontal_world_axis_screen_dy", 999.0)) > 0.15:
                    raise AssertionError("world X axis is visually tilted during " + stage)
                if checkpoint.get("visual_style_id") != first.get("visual_style_id"):
                    raise AssertionError("visual style changed across stages")
            report["visual_v0_horizontal_axis_locked"] = True
            report["visual_v0_stage_elevation_bob_m"] = round(
                max(abs(cp["camera"]["y"] - first["camera"]["y"])
                    for cp in (moss_ramp_mid, docks_slope_mid, docks)), 4)
            report["camera_projection_locked"] = True
            report["camera_rotation_deg"] = {
                k: first["camera"][k]
                for k in ("pitch_deg", "yaw_deg", "roll_deg")
            }
            # Opt-in human-only 2v2: leave the baseline slope/camera
            # traversal untouched. C starts AI and real damage resolution.
            page.keyboard.press("1")
            page.wait_for_timeout(350)
            restart = snap(page)
            if restart["map_id"] != "moss_temple" or restart.get("combat_completed_hits", -1) != 0:
                raise AssertionError("2v2 round did not reset for independent test")
            page.keyboard.press("c")
            page.wait_for_timeout(4800)
            battle = snap(page)
            report["human_2v2"] = battle
            if not battle.get("combat_ai_enabled", False):
                raise AssertionError("2v2 AI was not enabled by C")
            if battle.get("combat_completed_hits", 0) < 1:
                raise AssertionError("real 2v2 actors never landed a gameplay attack")
            # Each genuine physics damage/block event must emit exactly
            # one presentation-only original spark; art NEVER drives hits.
            if battle.get("pixel_hit_fx_total", -1) != battle.get("combat_completed_hits", -2):
                raise AssertionError("pixel hit flashes are not coupled one-to-one to real 3D hits")
            report["pixel_combat_fx_events_pass"] = True
            health = battle.get("combat_hp", {})
            if not health or sum(health.values()) >= 400:
                raise AssertionError("2v2 attack did not reduce any authoritative HP")
            bar_widths = battle.get("hud_hp_bar_px", {})
            for fighter, full_width in (("player", 206.0), ("ally", 206.0),
                                        ("enemy_a", 208.0), ("enemy_b", 211.0)):
                if fighter not in bar_widths or fighter not in health:
                    raise AssertionError("missing live HP bar or actor: " + fighter)
                expected_width = full_width * health[fighter] / 100.0
                if abs(bar_widths[fighter] - expected_width) > 3.5:
                    raise AssertionError("HUD HP bar does not track gameplay HP: " + fighter)
            report["human_2v2_hud_hp_synced"] = True
            canvas.screenshot(path=str(OUT / "moss-human-2v2.png"))
            report["human_2v2_pass"] = True
            report["round_status_during_battle"] = {
                "outcome": battle.get("round_outcome"),
                "time_ticks": battle.get("round_time_ticks"),
                "banner": battle.get("round_banner")}
            if battle.get("round_outcome") not in (1, 2, 3, 4):
                raise AssertionError("real 2v2 combat failed to enter a match outcome state")
            if not (0 <= battle.get("round_time_ticks", -1) < 5400):
                raise AssertionError("round clock did not advance with authoritative 60Hz gameplay")

            # New visual-first *comparison* view: still the same 3D physics,
            # but stage/fighters use an independent horizontal NES-like 2D
            # compositor, eliminating large oblique textured 3D planes.
            page.keyboard.press("F5")
            page.wait_for_timeout(680)
            pixel = snap(page)
            report["pixel_2d_preview"] = pixel
            if not pixel.get("pixel_projection_mode", False):
                raise AssertionError("F5 did not enable the 2D physics-backed visual adapter")
            if pixel.get("pixel_view_floor_tiles", 0) < 60:
                raise AssertionError("2D view did not render enough authored floor tiles")
            if pixel.get("pixel_view_fighters", 0) < 2:
                raise AssertionError("2D mode lost visible original human fighters")
            canvas.screenshot(path=str(OUT / "moss-nes-style-2d-preview.png"))
            report["pixel_2d_diversity"] = floor_tile_diversity(
                OUT / "moss-nes-style-2d-preview.png")
            if report["pixel_2d_diversity"]["visible_color_groups"] < 4:
                raise AssertionError("2D mode rendered a flat/blank stage")
            page.keyboard.press("F5")
            page.wait_for_timeout(200)
            if snap(page).get("pixel_projection_mode"):
                raise AssertionError("F5 cannot restore the legacy 3D visual comparison")
            report["pixel_2d_overlay_pass"] = True

            # T is a real 2v2 rematch: restore all fighter health, disable AI,
            # reset the timer and victory conditions, not merely the pixels.
            page.keyboard.press("t")
            page.wait_for_timeout(430)
            restarted = snap(page)
            report["round_restart"] = restarted
            if (restarted.get("round_outcome") != 0 or
                    restarted.get("round_time_ticks") != 5400 or
                    restarted.get("combat_ai_enabled") or
                    restarted.get("combat_completed_hits") != 0 or
                    sum(restarted.get("combat_hp", {}).values()) != 400):
                raise AssertionError("T restart failed to reset authoritative 2v2 HP/timer/AI")
            report["round_restart_pass"] = True

            # The authored jump row must be VISIBLE during a real Godot
            # jump in the fixed 2D pixel view. Pose art is never the source
            # of jump height/landing; screenshot is a separate QA gate.
            page.keyboard.press("F5")
            page.wait_for_timeout(180)
            page.keyboard.press("Space")
            page.wait_for_function(
                "() => {const s=window.__beastPhysicsDebug;"
                "return s && s.pixel_projection_mode === true"
                " && s.player && !s.player.grounded"
                " && Math.floor(s.human_sprite_frame / 4) === 5;}",
                timeout=2600, polling=45)
            original_jump = snap(page)
            report["original_human_jump_pose"] = {
                "visual_row": original_jump["human_sprite_frame"] // 4,
                "world_y": original_jump["player"]["y"],
                "physical_vy": original_jump["player"]["vy"]}
            canvas.screenshot(path=str(OUT / "moss-original-human-airborne-pose.png"))
            report["original_human_jump_pose_pass"] = True

            # A player can open the image-first version directly by URL
            # rather than discovering F5. It must boot the SAME tested PCK.
            direct_url = URL + "&pixel=1&capture_guard=1"
            direct_response = page.goto(direct_url, wait_until="domcontentloaded", timeout=50000)
            if direct_response is None or direct_response.status != 200:
                raise AssertionError("direct pixel preview URL unavailable")
            page.wait_for_function(
                "() => window.__beastPhysicsDebug && window.__beastPhysicsDebug.ready === true",
                timeout=180000, polling=750)
            page.wait_for_timeout(520)
            direct = snap(page)
            report["pixel_direct_url"] = {
                "url": direct_url, "source_sha": direct.get("source_sha"),
                "enabled": direct.get("pixel_projection_mode"),
                "drawn_tiles": direct.get("pixel_view_floor_tiles"),
                "drawn_fighters": direct.get("pixel_view_fighters")}
            if (direct.get("source_sha") != first.get("source_sha") or
                    not direct.get("pixel_guard_capture_debug") or
                    not direct.get("pixel_projection_mode") or
                    direct.get("pixel_view_floor_tiles", 0) < 60 or
                    direct.get("pixel_view_fighters") != 4):
                raise AssertionError("?pixel=1 did not directly boot the same real 3D brawler in 2D")
            canvas = page.locator("canvas#canvas").first
            if canvas.count() == 0:
                canvas = page.locator("canvas").first
            canvas.screenshot(path=str(OUT / "moss-direct-pixel-url.png"))
            report["pixel_direct_url_pass"] = True

            # Visual-first acceptance: capture the original FIXED-HORIZON
            # 2D gameplay while actual CharacterBody3D speed drives run
            # frames. Earlier moss-running-real-speed.png was recorded in
            # the deliberate 3D comparison mode and looked obliquely tilted.
            page.keyboard.down("d")
            try:
                page.wait_for_timeout(700)
                running_2d = snap(page)
                if (not running_2d.get("pixel_projection_mode") or
                        running_2d.get("human_visual_gait") != "run" or
                        running_2d.get("human_sprite_frame", -1) // 4 not in (3, 4)):
                    raise AssertionError("F5 original pixel art failed to animate true 2D running")
                canvas.screenshot(path=str(OUT / "moss-running-horizontal-pixel-2d.png"))
                report["original_2d_running_art_pass"] = True
            finally:
                page.keyboard.up("d")

            # Real defensive contact, not merely pressing G on an empty
            # arena. Keep the original 2D view ON, face the approaching
            # rivals, and capture a live CYAN spark while 3D HP resolves.
            page.keyboard.press("t")
            page.wait_for_timeout(350)
            page.keyboard.down("g")
            try:
                page.wait_for_function(
                    "() => window.__beastPhysicsDebug && window.__beastPhysicsDebug.player_guarding === true",
                    timeout=7000, polling=70)
                page.keyboard.press("c")
                page.wait_for_function(
                    "() => { const s = window.__beastPhysicsDebug; return s"
                    " && s.pixel_guard_fx_total > 0 && s.pixel_guard_fx_active > 0"
                    " && s.pixel_projection_mode === true; }",
                    timeout=20000, polling=45)
                guard_contact = snap(page)
                report["real_guard_contact"] = {
                    "blocks": guard_contact.get("player_blocks"),
                    "guard_fx_total": guard_contact.get("pixel_guard_fx_total"),
                    "total_fx": guard_contact.get("pixel_hit_fx_total"),
                    "real_contacts": guard_contact.get("combat_completed_hits"),
                    "active_fx": guard_contact.get("pixel_hit_fx_active"),
                    "active_cyan_guards": guard_contact.get("pixel_guard_fx_active"),
                    "player_hp": guard_contact.get("combat_hp", {}).get("player")}
                if (report["real_guard_contact"]["blocks"] < 1 or
                        report["real_guard_contact"]["guard_fx_total"] < 1 or
                        report["real_guard_contact"]["active_cyan_guards"] < 1):
                    raise AssertionError("G guard is not generating live 3D-block cyan FX")
                screenshot_path = OUT / "moss-cyan-guard-contact.png"
                canvas.screenshot(path=str(screenshot_path))
                cyan_pixels = visible_cyan_guard_pixels(screenshot_path)
                report["real_guard_contact"]["visible_cyan_pixels"] = cyan_pixels
                if cyan_pixels < 40:
                    raise AssertionError(
                        "Cyan shield missing from ACTUAL Chromium screenshot (%d matching pixels); "
                        "guard counter alone is not visual proof" % cyan_pixels)
                report["real_guard_contact_screenshot_pass"] = True
            finally:
                page.keyboard.up("g")

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
