#!/usr/bin/env bash
set -euo pipefail
test -f .github/workflows/build.yml
test -f ci/setup_godot.sh
test -f ci/install_templates.sh
test -f docs/SETUP.md
bash -n ci/validate.sh ci/setup_godot.sh ci/install_templates.sh
# Fail fast on Playwright syntax errors before costly private Godot import.
python3 -m py_compile ci/playwright_smoke.py ci/playwright_base_only.py
if grep -R -nE '(ghp_|github_pat_|ghs_)[A-Za-z0-9_]{20,}' ci .github docs README.md; then
  echo "::error::Possible hardcoded GitHub credential."
  exit 1
fi
echo "Public CI configuration preflight OK."
