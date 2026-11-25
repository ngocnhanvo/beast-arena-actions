#!/usr/bin/env bash
set -euo pipefail
FOLDER="$RUNNER_TEMP/beast-godot"
mkdir -p "$FOLDER"
curl -fsSL --retry 4 --retry-delay 3 \
  "https://github.com/godotengine/godot/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip" \
  -o "$FOLDER/godot.zip"
unzip -q "$FOLDER/godot.zip" -d "$FOLDER"
sudo install -m 0755 "$FOLDER/Godot_v4.7.2-stable_linux.x86_64" /usr/local/bin/godot
godot --headless --version
