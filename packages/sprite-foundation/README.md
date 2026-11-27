# Sprite Foundation — portable validation core (v0.1)

A **project-independent** open-source (MIT) Python 3.10+ library. Uses Pillow only.
No Godot, Aseprite, Beast Arena, Canvas, AI model or paid API dependency.

## What it does

- Accepts variable-size RGBA frame sources (`canvas`), any `frame_count`, any named body parts,
  project-declared topology, arbitrary bottom-to-top draw order, optional blank gear slots.
- Reads actual per-part PNG pixels. Confirms no missing/blank/clipped parts, checks real
  overlap/touch between edges, image connectivity and reconstructed final PNG equality.
- Measures optional **project-specific** body proportions; these are triage warnings,
  not universal human anatomy laws. Generates per-frame JSON evidence with hashes.
- Separates `structure_status`, `visual_review_status`, `release_status`.
  No approved external reference/signature, rejected owner review or unverified foot contact
  forces **BLOCKED**, even when source/LibreSprite/Godot tests PASS.
- Prevents an AI agent silently creating its own approved baseline: trusted approval
  fingerprint is signed using an out-of-repo human-managed secret and includes exact
  pixels of each frame. Unsigned JSON flags are *not* sufficient.

## Install and run

```sh
python -m pip install -e packages/sprite-foundation
sprite-foundation audit --manifest /workspace/sprite_manifest.json \
  --root /workspace/sprite-source --out /tmp/anatomy_report.json
# exit 2 = structural FAIL; exit 3 = art/motion/review BLOCKED; exit 0 = candidate only.
python -m unittest discover -s packages/sprite-foundation/tests -v
```

Use `--technical-only` **only** in a validator test that asserts `release_status=BLOCKED`
from the JSON. This does not authorize art or gameplay.

## Manifest data contract (example)

```json
{
  "schema": "sprite-foundation/1",
  "project_id": "another-independent-game",
  "asset_id": "hero-bare-body-run-right",
  "canvas": [96, 96],
  "frame_count": 8,
  "parts": ["head", "neck", "torso"],
  "layer_order": ["torso", "neck", "head"],
  "part_template": "source/body/{part}/run_{frame:02d}.png",
  "render_template": "render/neutral/run_{frame:02d}.png",
  "topology": [
    {"a": "head", "b": "neck", "contact_gap_px": 1, "min_overlap_pixels": 4},
    {"a": "neck", "b": "torso", "contact_gap_px": 1, "min_overlap_pixels": 4}
  ],
  "authoring": {"source_kind": "procedural", "owner_review": "REJECTED"},
  "motion": {"ground_contact_verified": false, "loop_review_verified": false}
}
```

Templates are sandboxed under `--root`. Do not include absolute paths or traversal.
Project adapters own part definitions and style thresholds; this library owns validation.

## One-way ownership and release gates

1. Artist/agent authors PNGs and pose annotations without touching project validators.
2. Independent structure validator checks real raster, topology, anchors, composition.
3. Artist sees per-frame visual evidence and separately reviews the animated seam.
4. **Owner**, *not the agent*, approves final source via externally signed pixel hashes.
5. Actual game build/Pages/Chromium must be separately proven against pinned SHAs.

Owner operation after full visual signoff, using a private out-of-repo key:

```sh
SPRITE_FOUNDATION_REVIEW_KEY=... sprite-foundation owner-sign \
  --report /tmp/anatomy_report.json --out /private/approved-art.json
SPRITE_FOUNDATION_REVIEW_KEY=... sprite-foundation audit \
  --manifest /workspace/sprite_manifest.json --root /workspace \
  --approval /private/approved-art.json --out /tmp/approved-report.json
```

**Do not** run `owner-sign` in automatic CI or in any AI agent. A valid signature
confirms exact owner-approved bytes, **not** the correctness of gait physics or all game animations.

## Limits

The analyzer cannot recognize beautiful art, true human anatomy, plausible 3D occlusion,
hand gestures or physical planted-foot behavior from 2D masks alone. It explicitly
refuses to certify those claims. Never treat a green file roundtrip as aesthetic
acceptance, and never use an existing rejected source as an automatically accepted golden.

## Optional independent landmark drift checks

Project adapters may supply `anchors_by_frame`, a list of dictionaries from
**part names to [x,y]** for each frame, and `anchor_tolerance_px` (0–20).
These anchors detect layers moved by small agents without re-validating
appearance against a generator's own guesses. For true art acceptance,
landmarks must come from a separately approved pose bible.

Use `--review-sheet /private/out/review.png` to export an annotated local
contact sheet; never upload original or derived private game art into PUBLIC
CI logs or workflow artifacts. The package does not publish its input images.