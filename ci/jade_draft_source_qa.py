#!/usr/bin/env python3
"""Trusted public CI driver. Private source stays on the ephemeral runner.
Print only fixed status labels, exit codes, aggregate pixel counts and sanitized
traceback coordinates. Never print private source, GIFs, screenshots or logs.
"""
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

def execute(label, args, timeout=180, env=None):
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, encoding="utf-8", errors="replace",
                       timeout=timeout, env=env)
    log = p.stdout
    print(f"{label}: exit={p.returncode}", flush=True)
    if p.returncode:
        for file, line in re.findall(r'File "[^"]*[/\\]([^"/\\]+)", line (\d+)', log):
            if re.fullmatch(r"[a-zA-Z0-9_.-]+", file):
                print(f"diagnostic location {file}:{line}")
        for kind in re.findall(r"(?m)^([A-Za-z]+(?:Error|Exception)):", log):
            print(f"diagnostic exception {kind}")
    return p.returncode, log

def verify(root):
    code, log = execute("Independent private verify.py", [
        sys.executable, str(root / "docs/reviews/issue-1/verify.py")])
    assert code == 0, "Independent Python verifier failed"
    assert "PASS: source ASE/PNG, frozen regions" in log
    assert "PASS: guard source landmarks and actual fist-core counts" in log
    assert "PASS: two-cycle GIF" in log
    print("PYTHON SOURCE VERIFIER PASS (native format, frozen regions, pivots, landmark and GIF contracts)")

def libresprite(root):
    from PIL import Image
    code, log = execute("Existing registered draft source smoke", [
        sys.executable, str(root / "tests/draft_animation_sources_smoke.py"),
        "--binary", "libresprite"], timeout=420)
    print("REGISTERED_DRAFTS_PASS=" + str(code == 0).lower())
    art = root / "experiments/physics_v2/art/drafts"
    errors = 0
    for side in ("right", "left"):
        stem = art / ("jade_run_eight_" + side)
        with tempfile.TemporaryDirectory(prefix="jade-private-export-") as tmp:
            png, data = Path(tmp)/"sheet.png", Path(tmp)/"sheet.json"
            cmd = ["libresprite", "-b", "--list-tags", "--sheet-type", "horizontal",
                   str(stem.with_suffix(".aseprite")), "--sheet", str(png),
                   "--data", str(data), "--format", "json-array"]
            status, _ = execute(f"LibreSprite {side} export", cmd, timeout=120,
                                env=dict(os.environ, SDL_VIDEODRIVER="dummy"))
            if status:
                errors += 1
                continue
            meta = json.loads(data.read_text())
            tags = meta["meta"]["frameTags"]
            assert len(tags) == 1 and tags[0]["name"] == f"run_{side}_guard"
            assert (tags[0]["from"], tags[0]["to"]) == (0, 7)
            frames = meta["frames"]
            assert len(frames) == 8
            for i, f in enumerate(frames):
                assert f["duration"] == 85
                assert f["sourceSize"] == {"w":80,"h":80}
                assert f["frame"] == {"x":80*i,"y":0,"w":80,"h":80}
            with Image.open(png) as out, Image.open(stem.with_suffix(".png")) as reference:
                a, b = out.convert("RGBA"), reference.convert("RGBA")
                assert a.size == b.size == (640,80)
                aa, bb = a.tobytes(), b.tobytes()
                # All four channels, including hidden RGB: ImageChops.getbbox
                # can ignore RGB-only differences on some Pillow versions.
                visible = hidden = 0
                for i in range(0,len(aa),4):
                    if aa[i:i+4] != bb[i:i+4]:
                        if aa[i+3] or bb[i+3]:
                            visible += 1
                        else:
                            hidden += 1
                print(f"STRICT_RGBA_{side.upper()} visible_diff={visible} transparent_rgb_diff={hidden}")
                if visible or hidden:
                    errors += 1
    assert not errors and code == 0, "LibreSprite strict source fidelity failed"
    print("PINNED LIBRESPRITE PASS: both native tagged eight-cel exports byte-exact RGBA")

def godot(root):
    project = root / "experiments/physics_v2"
    code, log = execute("Godot headless Physics V2 import", [
        "godot","--headless","--editor","--path",str(project),"--import","--quit"], timeout=480)
    errors = len(re.findall(r"SCRIPT ERROR:|ERROR: Failed to load script", log))
    print(f"IMPORT_SCRIPT_ERRORS={errors}")
    assert code == 0 and errors == 0, "Godot import failed"
    results = []
    for name in ("guard_animation_profiles_smoke.gd","three_quarter_preview_smoke.gd"):
        code, log = execute(name, ["godot","--headless","--path",str(project),
                                   "--script","res://tests/"+name], timeout=180)
        errors = len(re.findall(r"SCRIPT ERROR:|ERROR: Failed to load script", log))
        jade_codes = sorted(set(re.findall(r"JADE-34-(\d+)", log)))
        print(f"GODOT_SMOKE {name} script_errors={errors} jade_codes={','.join(jade_codes)}")
        passed = code == 0 and errors == 0
        if name.startswith("three_quarter"):
            passed = passed and "JADE RUN GUARD ARM COUNTERSWING SOURCE PASS" in log and "JADE THREE-QUARTER PREVIEW PASS" in log
        print(f"GODOT_SMOKE {name} {'PASS' if passed else 'FAIL'}")
        results.append(passed)
    assert all(results), "Godot source smoke failed"
    print("GODOT NATIVE SOURCE PASS (no export, no deploy)")

def playback(root):
    from PIL import Image, ImageSequence
    from playwright.sync_api import sync_playwright
    source = root / "docs/reviews/issue-1"
    for name, required_count in (("jade-run-loop.gif", 8),("jade-run-to-idle.gif",9)):
        path = source/name
        with Image.open(path) as img:
            w,h = img.size
            expected = [hashlib.sha256(f.convert("RGB").tobytes()).digest()
                        for f in ImageSequence.Iterator(img)]
        canonical = {}
        for i,k in enumerate(expected):
            canonical.setdefault(k, i if i < 8 else (8 if i >= 16 else i%8))
        assert len(canonical) == required_count
        uri = base64.b64encode(path.read_bytes()).decode("ascii")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(viewport={"width":w,"height":h},
                                              device_scale_factor=1)
                context.route("**/*", lambda route: route.abort())
                page = context.new_page()
                page.set_content("<style>html,body{margin:0;background:#3a434e}</style>"
                                 "<img id='motion' src='data:image/gif;base64,"+uri+"'>")
                page.locator("#motion").evaluate("i => i.decode()")
                seen, sequence, unrecognized = set(), [], 0
                deadline = time.monotonic()+8
                while time.monotonic()<deadline:
                    png = page.screenshot(animations="allow")
                    with Image.open(io.BytesIO(png)) as frame:
                        key = hashlib.sha256(frame.convert("RGB").tobytes()).digest()
                    idx = canonical.get(key)
                    if idx is None:
                        unrecognized += 1
                    else:
                        seen.add(idx)
                        if not sequence or sequence[-1]!=idx:
                            sequence.append(idx)
                    if len(seen)==required_count and any(a==7 and b==0 for a,b in zip(sequence,sequence[1:])):
                        break
                browser.close()
        except Exception as e:
            # Playwright exceptions can contain the private data URI. Never echo.
            print("PLAYBACK exception type="+type(e).__name__)
            raise SystemExit(1)
        seam = any(a==7 and b==0 for a,b in zip(sequence,sequence[1:]))
        print(f"CHROMIUM_GIF {name} unique_frames={len(seen)}/{required_count} seam_7_to_0={seam} unmatched_samples={unrecognized}")
        assert len(seen)==required_count and seam, "Playback did not observe every distinct frame and seam"
    print("CHROMIUM GIF PLAYBACK PASS; not live game or artistic approval")

if __name__ == "__main__":
    try:
        mode, directory = sys.argv[1:]
        root = Path(directory).resolve()
        {"verify":verify,"libresprite":libresprite,"godot":godot,"playback":playback}[mode](root)
    except (AssertionError, KeyError, ValueError, OSError, subprocess.TimeoutExpired) as e:
        # Fixed exception type only; never print private values or source.
        print("GATE FAILED: "+type(e).__name__)
        raise SystemExit(1)
