#!/usr/bin/env python3
"""LibreSprite v1.3 integration smoke, using ORIGINAL *test-only* 80px pixels.

Writes a small spec-conformant layered 4-frame .ase file into a temporary
directory, then invokes actual LibreSprite, exports PNG + json-array frameTags
and verifies frame pixels, sizes and duration. NEVER contains or publishes
PRIVATE fighter art. The test is intentionally NOT a 10-clip visual signoff.
"""
from __future__ import annotations
import argparse
import json
import os
import struct
import subprocess
import tempfile
import zlib
from pathlib import Path

from PIL import Image


def word_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    return struct.pack("<H", len(encoded)) + encoded


def chunk(kind: int, data: bytes) -> bytes:
    return struct.pack("<IH", len(data) + 6, kind) + data


def make_editable(path: Path, frame_count: int = 4,
                  tags: list[tuple[str, int, int]] | None = None) -> None:
    # Test-only original pixels. Can exercise a complete ten-tag source
    # contract without publishing it as actual Jade animation art.
    tags = tags if tags is not None else [("smoke_four", 0, 3)]
    frames = []
    for frame in range(frame_count):
        parts = []
        if frame == 0:
            layer = struct.pack("<6HB3s", 1, 0, 0, 0, 0, 0, 255, b"\0"*3)
            parts.append(chunk(0x2004, layer + word_string("original-test-only-cel")))
            tags_bytes = [struct.pack("<H", len(tags)) + b"\0"*8]
            for name, first, last in tags:
                tags_bytes.append(
                    struct.pack("<HHBH", first, last, 0, 0) + b"\0"*6 +
                    bytes((25, 158, 150, 0)) + word_string(name))
            parts.append(chunk(0x2018, b"".join(tags_bytes)))
        color = (20 + 25 * (frame % 4), 90 + 20 * (frame % 4), 170 - 19 * (frame % 4), 255)
        rgba = bytearray(80 * 80 * 4)
        for y in range(80):
            for x in range(80):
                # A distinct full pixel cell per frame, not any Jade source.
                if 8 + (frame % 9) <= x < 68 + (frame % 9) and 8 <= y < 72:
                    rgba[(y * 80 + x) * 4:(y * 80 + x + 1) * 4] = bytes(color)
        cel = (struct.pack("<HhhBHh", 0, 0, 0, 255, 2, 0) +
               b"\0"*5 + struct.pack("<HH", 80, 80) +
               zlib.compress(bytes(rgba)))
        parts.append(chunk(0x2005, cel))
        body = b"".join(parts)
        # Frame header 16 bytes.
        frames.append(struct.pack("<IHHHHI", len(body) + 16, 0xF1FA,
                                  len(parts), 100, 0, 0) + body)
    header = bytearray(128)
    struct.pack_into("<IHHHHH", header, 0, 128 + sum(map(len, frames)),
                     0xA5E0, frame_count, 80, 80, 32)
    struct.pack_into("<I", header, 14, 1)
    struct.pack_into("<H", header, 18, 100)
    header[30] = 0
    header[32] = 1
    header[33] = 1
    path.write_bytes(header + b"".join(frames))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", default=os.environ.get("LIBRESPRITE_BIN", "libresprite"))
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="beast-ls-smoke-") as tmp:
        directory = Path(tmp)
        source, sheet, meta = (directory / x for x in
                                ("smoke.ase", "smoke.png", "smoke.json"))
        make_editable(source)
        env = dict(os.environ, SDL_VIDEODRIVER="dummy")
        cmd = [args.binary, "-b", "--list-tags", "--sheet-type", "horizontal",
               str(source), "--sheet", str(sheet), "--data", str(meta),
               "--format", "json-array"]
        process = subprocess.run(cmd, env=env, capture_output=True, text=True,
                                 encoding="utf-8", errors="replace",
                                 timeout=100, check=False)
        if process.returncode != 0:
            raise RuntimeError("LibreSprite round-trip CLI failed: " +
                               (process.stderr or process.stdout)[-1800:])
        if not sheet.is_file() or not meta.is_file():
            raise RuntimeError("LibreSprite did not produce expected sheet/metadata")
        metadata = json.loads(meta.read_text(encoding="utf-8"))
        frames = metadata.get("frames", [])
        tags = metadata.get("meta", {}).get("frameTags", [])
        if len(frames) != 4:
            raise AssertionError(f"Expected exactly four actual frames, got {len(frames)}")
        if not any(t.get("name") == "smoke_four" and
                   t.get("from") == 0 and t.get("to") == 3 for t in tags):
            raise AssertionError(f"Actual LibreSprite tag missing: {tags}")
        with Image.open(sheet) as im:
            if im.size != (320, 80):
                raise AssertionError(f"Untrimmed 4x80 sheet incorrect: {im.size}")
            rgba = im.convert("RGBA")
            for index in range(4):
                rectangle = frames[index].get("frame", {})
                if rectangle.get("w") != 80 or rectangle.get("h") != 80:
                    raise AssertionError(f"Frame {index} was trimmed/scaled: {rectangle}")
                if frames[index].get("duration") != 100:
                    raise AssertionError(f"LibreSprite lost frame duration: {frames[index]}")
                x = rectangle["x"] + 40
                y = rectangle["y"] + 40
                color = rgba.getpixel((x, y))
                expected = (20 + 25 * index, 90 + 20 * index,
                            170 - 19 * index, 255)
                if color != expected:
                    raise AssertionError(f"Frame {index} pixel corrupt: {color} vs {expected}")
        print("LIBRESPRITE REAL BINARY ROUNDTRIP PASS: editable .ase layer+4 cels,"
              " --batch, original RGBA8 80px sheet, 4 PNG frames, tags/durations")
        print("THIS IS TEST-ONLY, NOT A JADE SPRITE OR ART ACCEPTANCE")


if __name__ == "__main__":
    main()
