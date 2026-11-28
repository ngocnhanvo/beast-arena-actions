"""Guard animation source quality gate for the PRIVATE checkout in PUBLIC CI.

The profile JSON and actual Aseprite assets live only in the PRIVATE repo.
This script checks structure and exported-Web inclusion, logs no raw art.
Technical readiness is never the same thing as owner visual approval.
"""
import configparser
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("game")
GAME = ROOT / "experiments" / "physics_v2"
REQUIRED_FIGHTERS = {"jade_human", "ally_human", "rival_a_human", "rival_b_human"}
ACTIONS = {
    "idle", "walk_up", "walk_down", "walk_left", "walk_right",
    "run_left", "run_right", "punch", "kick", "jump"
}
GUARD_ACTIONS = {
    "idle", "walk_up", "walk_down", "walk_left", "walk_right",
    "run_left", "run_right"
}
MIN_FRAMES = {
    "idle": 4, "walk_up": 6, "walk_down": 6,
    "walk_left": 6, "walk_right": 6,
    "run_left": 8, "run_right": 8,
    "punch": 4, "kick": 5, "jump": 5
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    source = GAME / "art" / "fighters" / "animation_profiles.json"
    manifest = json.loads(source.read_text(encoding="utf-8"))
    require(manifest.get("schema_version") == 1, "unsupported guard schema")
    contract = manifest.get("contract", {})
    require(contract.get("stance") == "guard", "guard stance is required")
    require(contract.get("pixel_size") == [80, 80], "native 80px required")
    tags = contract.get("clip_tags", {})
    nums = contract.get("minimum_frames", {})
    require(set(tags) == ACTIONS and set(nums) == ACTIONS,
            "ten standardized fighter actions required")
    require(len(set(tags.values())) == 10, "clip tags must be unique")
    for action, tag in tags.items():
        require(isinstance(tag, str) and bool(tag), "empty tag: " + action)
        require(isinstance(nums[action], int) and
                nums[action] >= MIN_FRAMES[action],
                "insufficient keyframes for " + action)
        if action in GUARD_ACTIONS:
            require("guard" in tag, "unguarded locomotion clip " + action)
        if action in ("walk_up", "walk_down"):
            require(tag.endswith("front"),
                    "both W/S must show front: " + action)
    require(tags["walk_up"] != tags["walk_down"],
            "W/S require independently authored clips")

    fighters = manifest.get("fighters", {})
    require(REQUIRED_FIGHTERS.issubset(fighters),
            "one or more of four existing fighter profiles missing")
    pending = []
    for fighter_id, actor in fighters.items():
        for key in ("png", "json", "reference_png"):
            require(isinstance(actor.get(key), str)
                    and actor[key].startswith("res://"),
                    "invalid res:// path: " + fighter_id + " / " + key)
        ref = GAME / actor["reference_png"].removeprefix("res://")
        require(ref.is_file(), "original fighter reference missing: " +
                fighter_id)
        path = actor.get("source")
        if not path:
            require(str(actor.get("status", "")).startswith("PENDING_ART"),
                    "missing source not labelled PENDING_ART: " + fighter_id)
            pending.append(fighter_id)
        else:
            require(isinstance(path, str) and
                    path.lower().endswith((".ase", ".aseprite")),
                    "editable source must be Aseprite: " + fighter_id)

    config = configparser.ConfigParser()
    config.read(GAME / "export_presets.cfg", encoding="utf-8")
    exported = config.get("preset.0", "include_filter", fallback="")
    require("art/fighters/*.json" in exported,
            "Web export must bundle guard fighter profiles JSON")
    require("art/export/*.json" in exported,
            "Web export must bundle authored Aseprite JSON frames")
    require("art/base/character_scale_contract.json" in exported,
            "Web export must include pose-invariant JSON read by FileAccess")
    print(f"GUARD PROFILE STATIC PASS: {len(fighters)} fighters, "
          f"{len(tags)} combat-stance clips; {len(pending)} PENDING_ART")
    print("ART VISUAL REVIEW: NOT PASSED; static contract cannot inspect hands")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"GUARD PROFILE STATIC FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
