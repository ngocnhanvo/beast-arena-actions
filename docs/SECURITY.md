# Security boundaries

- All Godot compute in public standard GitHub-hosted runner; private source repo has no workflows.
- `BEAST_ARENA_READ_TOKEN`: fine-grained, Contents read-only, scoped to the one private repository.
- `BEAST_ARENA_RELEASE_TOKEN`: optional distinct Contents read/write token scoped to one private repo, exposed only to the private release step. Treat code allowed onto the private main branch as trusted.
- Checkout disables persisted Git credentials. Tokens must never be printed in logs.
- Never attach raw checked-out source tree, `.godot/`, project PCK or unreviewed workspace files to public artifacts.
- No PR or `pull_request_target` event checks out private source with secrets.
- Public binaries may permit decompilation of script/asset data. Public artifact upload disabled by default and requires explicit input.
- Upgrade to full SHA pinning for external Actions after CI baseline is validated.
