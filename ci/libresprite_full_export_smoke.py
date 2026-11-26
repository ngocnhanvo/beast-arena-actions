#!/usr/bin/env python3
"""End-to-end smoke: PRIVATE Beast Arena exporter + real LibreSprite CLI.

Generates a disposable, fully editable, 58-frame test-only .ase timeline
with all 10 guard tags and a manually authored fixture foot coordinate for
each frame; runs the actual PRIVATE tools/libresprite_export.py; verifies the
real, full-size 4640×80 exported PNG/metadata. Does not publish test art.
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image
from libresprite_roundtrip_smoke import make_editable


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", default="game")
    parser.add_argument("--binary", default="libresprite")
    args = parser.parse_args()
    game = Path(args.game).resolve()
    config = json.loads((game / "experiments/physics_v2/art/fighters/animation_profiles.json")
                        .read_text(encoding="utf-8"))
    tags = config["contract"]["clip_tags"]
    counts = config["contract"]["minimum_frames"]
    ranges = []
    first = 0
    for action, name in tags.items():
        count = counts[action]
        ranges.append((name, first, first + count - 1))
        first += count
    assert first >= 50 and len(ranges) == 10
    with tempfile.TemporaryDirectory(prefix="beast-guard-export-smoke-") as temp:
        root = Path(temp)
        source = root / "guard-test.ase"
        pivots = root / "guard-test.foot.json"
        output = root / "final-export"
        make_editable(source, frame_count=first, tags=ranges)
        pivots.write_text(json.dumps({
            "schema_version": 1,
            "source_frame_count": first,
            "foot_pivots": [
                {"frame": i, "x": 40, "y": 76} for i in range(first)
            ],
        }), encoding="utf-8")
        cmd = [sys.executable, str(game / "tools/libresprite_export.py"),
               "--fighter", "jade_human",
               "--source", str(source),
               "--foot", str(pivots),
               "--binary", args.binary,
               "--output-dir", str(output)]
        result = subprocess.run(
            cmd, env=dict(os.environ, SDL_VIDEODRIVER="dummy"),
            capture_output=True, text=True, timeout=160, check=False,
        )
        if result.returncode != 0:
            raise AssertionError("REAL private LibreSprite importer failed: " +
                                 result.stdout[-1500:] + result.stderr[-1600:])
        export_png = output / "jade_human.png"
        export_json = output / "jade_human.json"
        if not export_png.is_file() or not export_json.is_file():
            raise AssertionError("Full original metadata export missing")
        metadata = json.loads(export_json.read_text(encoding="utf-8"))
        exported_tags = {t["name"] for t in metadata["meta"]["frameTags"]}
        if exported_tags != set(tags.values()):
            raise AssertionError("Ten required original clip tags not retained")
        slices = metadata["meta"].get("slices", [])
        if (len(slices) != 1 or slices[0]["name"] != "foot_anchor"
                or len(slices[0].get("keys", [])) != first):
            raise AssertionError("Artist foot sidecar was not merged as full frame slice")
        with Image.open(export_png) as sheet:
            if sheet.size != (first * 80, 80) or sheet.mode != "RGBA":
                raise AssertionError(f"Not an untrimmed native RGBA8 80px sheet: {sheet.size} {sheet.mode}")
        if len(metadata["frames"]) != first:
            raise AssertionError("LibreSprite lost source frame count")
        print(f"LIBRESPRITE FULL GUARD EXPORT PASS: {first} TEST-ONLY frames, "
              "10 tags, 80px native RGBA8, per-frame foot pivots, REAL private exporter.")
        print("Original fighter art remains PENDING_ART; no test pixels shipped.")


if __name__ == "__main__":
    main()
