"""Actual WebGL canvas motion diagnostic: *not* Sprite3D telemetry-only acceptance.

Captures live canonical-page sprite frames, a real browser video, browser rAF
pose history, abrupt visual jumps and Godot drawn-history, without modifying
game state. This is a diagnostic: it cannot approve visual artwork.
"""
import json
import os
import time
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

URL = "https://ngocnhanvo.github.io/beast-arena-actions/physics-v2/"
OUT = Path("playwright-report/jade-motion-diagnostic")
OUT.mkdir(parents=True, exist_ok=True)


def snap(page):
    return page.evaluate("window.__beastPhysicsDebug || null")


def capture_sprint(page, canvas, key, direction):
    # Game's existing reset 'R'; never set actor position or motor directly.
    page.wait_for_timeout(380)
    canvas.click(force=True)
    page.keyboard.press("r")
    page.wait_for_function(
        "() => {let s=window.__beastPhysicsDebug; return s && s.player"
        " && s.player.grounded && !s.sprint_requested"
        " && Math.abs(s.player.vx)<0.3 && Math.abs(s.player.vz)<0.3;}",
        timeout=15000, polling=70)
    page.evaluate("""() => {
      window.__motionRafTrace = [];
      window.__motionCapturing = true;
      const started = performance.now();
      function tick() {
        if (!window.__motionCapturing) return;
        const s=window.__beastPhysicsDebug;
        if (s && s.review_run_active) {
          window.__motionRafTrace.push({
            dt: Math.round(performance.now() - started),
            phase: s.review_preview_frame,
            frame: s.human_sprite_frame,
            vx: s.player?.vx,
            grounded: s.player?.grounded,
            foot_pad: s.human_sprite_foot_padding_px,
            body_height: s.review_effective_body_height_px,
            phys_y: s.player?.y
          });
        }
        requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    }""")
    page.keyboard.press(key, delay=60)
    page.wait_for_timeout(60)
    page.keyboard.down(key)
    frames = []
    start = time.monotonic()
    try:
        page.wait_for_function(
            "() => window.__beastPhysicsDebug?.review_run_active === true",
            timeout=10000, polling=30)
        # Capture on the actual canvas while real gameplay is running.
        # No freezing sprites or injecting animation frame values.
        seen = set()
        last = None
        if os.getenv("DIAG_STRESS_SCREENSHOTS", "0") != "1":
            # IMPORTANT: synchronous canvas.screenshot() freezes expensive
            # WebGL/SwiftShader draws by up to seconds, creating artificial
            # skipped phases. Record honest uninterrupted browser video/rAF.
            page.wait_for_timeout(3700)
            trace_only = page.evaluate("window.__motionRafTrace || []")
            seen.update(int(x["phase"]) for x in trace_only
                        if x.get("phase") in range(8))
        while (os.getenv("DIAG_STRESS_SCREENSHOTS", "0") == "1"
               and time.monotonic() - start < 5.0):
            state = snap(page)
            if not state or not state.get("review_run_active"):
                page.wait_for_timeout(16)
                continue
            phase = int(state.get("review_preview_frame", -1))
            if phase in range(8) and (phase not in seen or
                                      (last == 7 and phase == 0)):
                name = f"{direction}-phase-{phase:02d}-{len(frames):02d}.png"
                canvas.screenshot(path=str(OUT / name), timeout=15000)
                frames.append({
                    "phase": phase, "file": name,
                    "source_frame": state.get("review_run_source_frame"),
                    "sprint_vx": state.get("player", {}).get("vx"),
                    "body_height": state.get("review_effective_body_height_px"),
                    "foot_pad": state.get("human_sprite_foot_padding_px"),
                    "elapsed": round(time.monotonic() - start, 3)
                })
                seen.add(phase)
            last = phase
            page.wait_for_timeout(8)
            if len(seen) == 8 and len(frames) >= 9:
                break
    finally:
        page.keyboard.up(key)
        page.evaluate("() => { window.__motionCapturing = false; }")
    current = snap(page)
    trace = page.evaluate("window.__motionRafTrace || []")
    phase_sequence = [x["phase"] for x in trace
                      if x["phase"] in range(8)]
    collapsed = [p for i,p in enumerate(phase_sequence)
                 if i == 0 or p != phase_sequence[i-1]]
    intervals = []
    for a,b in zip(trace,trace[1:]):
        if a["phase"] != b["phase"]:
            intervals.append(b["dt"] - a["dt"])
    return {
        "direction": direction,
        "canvas_captures": frames,
        "captured_phases": sorted(seen),
        "raf_trace_samples": len(trace),
        "raf_phase_sequence": collapsed,
        "screenshot_mode": os.getenv("DIAG_STRESS_SCREENSHOTS", "0") == "1",
        "raf_frame_intervals_ms": [
            trace[i]["dt"] - trace[i - 1]["dt"]
            for i in range(1, len(trace))
        ],
        "raf_full_cycle_detected": any(
            collapsed[i:i+8] == list(range(8))
            for i in range(max(0, len(collapsed)-7))),
        "raf_wrap_detected": any(
            collapsed[i:i+2] == [7,0]
            for i in range(max(0, len(collapsed)-1))),
        "raf_history_duration_ms": (trace[-1]["dt"]-trace[0]["dt"]
                                   if len(trace)>1 else 0),
        "drawn_phase_history": current.get("review_run_drawn_phase_history"),
        "drawn_phase_mask": current.get("review_run_drawn_phase_mask"),
        "phys_vx_final": current.get("player", {}).get("vx"),
        "body_height_range": sorted({
            x["body_height"] for x in frames if x["body_height"] is not None
        }),
        "foot_pad_range": sorted({
            x["foot_pad"] for x in frames if x["foot_pad"] is not None
        }),
        "raf_trace": trace
    }


def make_montage(direction, data):
    # A diagnostic contact sheet of 8 actual screenshot canvas captures.
    captures = data["canvas_captures"]
    chosen = [next((x for x in captures if x["phase"]==i), None)
              for i in range(8)]
    if not any(chosen):
        return
    tile_size=(360,240)
    out=Image.new("RGB",(tile_size[0]*4,tile_size[1]*2),(23,23,28))
    draw=ImageDraw.Draw(out)
    for i,x in enumerate(chosen):
        col,row=i%4,i//4
        if not x:continue
        screenshot=Image.open(OUT / x["file"]).convert("RGB")
        # Canvas has actor near screen center, camera follows player.
        w,h=screenshot.size
        region=screenshot.crop((
            max(0,int(w*.22)),max(0,int(h*.37)),
            min(w,int(w*.75)),min(h,int(h*.70))))
        region.thumbnail((tile_size[0]-10,tile_size[1]-35))
        out.paste(region,(col*tile_size[0]+5,row*tile_size[1]+21))
        draw.text((col*tile_size[0]+8,row*tile_size[1]+2),
                  f"{direction.upper()} pose {i}: actual canvas",fill="white")
    out.save(OUT / f"{direction}-all-eight-real-canvas-poses.png")


def main():
    result={"canonical_url":URL,"status":"IN_PROGRESS"}
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=[
            "--enable-webgl","--use-gl=angle","--use-angle=swiftshader",
            "--enable-unsafe-swiftshader","--disable-dev-shm-usage"])
        context=browser.new_context(
            viewport={"width":1200,"height":800},
            record_video_dir=str(OUT/"video"),record_video_size={"width":1200,"height":800})
        page=context.new_page()
        try:
            response=page.goto(URL+"?e2e=1&review=1",
                               wait_until="domcontentloaded",timeout=60000)
            if not response or response.status!=200:
                raise AssertionError("Canonical game Pages is not HTTP 200")
            page.wait_for_function(
                "() => window.__beastPhysicsDebug?.ready === true",
                timeout=180000,polling=200)
            s=snap(page)
            result["source_sha"]=s.get("source_sha")
            result["pipeline_sha"]=s.get("pipeline_sha")
            result["build_run_id"]=s.get("build_run_id")
            if os.environ.get("EXPECTED_GAME_SOURCE_SHA") and (
                s.get("source_sha") != os.environ["EXPECTED_GAME_SOURCE_SHA"]):
                raise AssertionError("Wrong game SHA, no diagnostic of stale sprites")
            if os.environ.get("EXPECTED_BUILD_RUN_ID") and (
                str(s.get("build_run_id")) != os.environ["EXPECTED_BUILD_RUN_ID"]):
                raise AssertionError("Wrong Pages deploy, no diagnostic of stale sprites")
            if s.get("review_run_source_pose_count",0) not in (0,8):
                raise AssertionError("Unexpected Jade pose count")
            canvas=page.locator("canvas#canvas").first
            if canvas.count()==0:canvas=page.locator("canvas").first
            canvas.wait_for(state="visible",timeout=20000)
            canvas.screenshot(path=str(OUT/"before-sprint.png"))
            result["runs"]=[]
            for key,name in [("d","right"),("a","left")]:
                d=capture_sprint(page,canvas,key,name)
                result["runs"].append(d)
                make_montage(name,d)
                print("JADE ACTUAL CANVAS DIAGNOSTIC",name,
                      "captured=",d["captured_phases"],
                      "rAF=",d["raf_phase_sequence"],
                      "GPU=",d["drawn_phase_history"],
                      "height=",d["body_height_range"])
            # Source/renderer correctness != art quality.
            result["status"]="DIAGNOSTICS_CAPTURED_NO_ART_APPROVAL"
            if not all(d["captured_phases"] for d in result["runs"]):
                raise AssertionError("No live rAF source phases captured")
        except Exception as exc:
            result["status"]="FAIL"
            result["error"]=str(exc)
            raise
        finally:
            for key in ("a","d","w","s"):page.keyboard.up(key)
            (OUT/"report.json").write_text(
                json.dumps(result,ensure_ascii=False,indent=2))
            context.close()
            browser.close()


if __name__=="__main__":
    main()
