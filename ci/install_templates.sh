#!/usr/bin/env bash
set -euo pipefail
FOLDER="$RUNNER_TEMP/beast-godot-templates"
TARGET="$HOME/.local/share/godot/export_templates/4.7.2.stable"
mkdir -p "$FOLDER" "$TARGET"
curl -fsSL --retry 4 --retry-delay 3 \
  "https://github.com/godotengine/godot/releases/download/4.7.2-stable/Godot_v4.7.2-stable_export_templates.tpz" \
  -o "$FOLDER/templates.tpz"
unzip -q "$FOLDER/templates.tpz" -d "$FOLDER/unpacked"
test -f "$FOLDER/unpacked/templates/web_release.zip"
cp -a "$FOLDER/unpacked/templates/." "$TARGET/"
echo "Installed Godot 4.7.2 export templates."
