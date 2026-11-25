# Checkpoint — 2026-11-25

- Public Actions `beast-arena-actions/main`: CI code and workflow.
- Private Game `beast-arena/main`: Godot 4.7.2 scaffold.
- Public push = preflight; manual workflow_dispatch = immediate private checkout/build; hourly public schedule = SHA change-detection + build (no private minutes).
- Mandatory read-only PAT secret: `BEAST_ARENA_READ_TOKEN`.
- Optional private release token: `BEAST_ARENA_RELEASE_TOKEN`.
- Public artifacts are OFF by default.
- Status: preflight to be verified; full build depends on PAT secret configuration.

## Verification

- CI run #45645624827: successful Godot import, combat/smoke tests, Windows/Web exports.
- No private release was produced in that run because the release credential was absent at the time.
- Rerun requested to verify current secret configuration and private-release upload on a public runner.
