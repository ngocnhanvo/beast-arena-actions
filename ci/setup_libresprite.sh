#!/usr/bin/env bash
# LibreSprite 1.3 OFFICIAL upstream AppImage. Installed transiently on public
# Linux runner; binary is never stored in the user's repositories or artifacts.
set -euo pipefail

VERSION="v1.3"
ARCHIVE="libresprite-v1.3-linux-x86_64.AppImage"
DOWNLOAD="https://github.com/LibreSprite/LibreSprite/releases/download/${VERSION}/${ARCHIVE}"
SHA256="fd90bddda8135fe00f4a9a9c8c9ebd48f9b07e8782ab269be5c9efb1a851af30"
ROOT="${RUNNER_TEMP:-/tmp}/beast-libresprite-${VERSION}"
mkdir -p "$ROOT"
cd "$ROOT"

if [[ ! -x "$ROOT/squashfs-root/AppRun" ]]; then
  curl --fail --location --show-error --silent --retry 4 --retry-all-errors \
    --connect-timeout 20 --max-time 180 --output "$ARCHIVE" "$DOWNLOAD"
  printf '%s  %s\n' "$SHA256" "$ARCHIVE" | sha256sum --check --status
  chmod +x "$ARCHIVE"
  # No FUSE / root privileges required on GitHub-hosted Ubuntu.
  "./$ARCHIVE" --appimage-extract >/dev/null
fi

# AppRun is the real upstream program; no gh cli auth or image files leave
# the private checkout. SDL dummy driver supports non-GUI batch mode.
cat > "$ROOT/libresprite" <<EOF
#!/usr/bin/env bash
export SDL_VIDEODRIVER=dummy
exec "$ROOT/squashfs-root/AppRun" "\$@"
EOF
chmod +x "$ROOT/libresprite"
"$ROOT/libresprite" --version
if [[ -n "${GITHUB_PATH:-}" ]]; then
  echo "$ROOT" >> "$GITHUB_PATH"
fi
if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
  echo "LibreSprite ${VERSION}: official Linux AppImage SHA-256 verified; batch CLI installed; visual art is NOT automatically approved." >> "$GITHUB_STEP_SUMMARY"
fi
printf 'LIBRESPRITE_READY=%s\n' "$ROOT/libresprite"
