# 2026-06-16 npm scaffold spec - superseded

Status: superseded by Hardware Deal Radar context pack migration on 2026-06-30.

## Original Outcome

- The repo can be published and executed as an npm scaffold CLI.

## Original Scope

- Add npm package metadata.
- Add a CLI entrypoint that copies the scaffold into a target directory.
- Add focused tests.
- Update docs and stack metadata.

## Original Acceptance Criteria

- [x] A valid `package.json` exists for npm publication.
- [x] A CLI command can scaffold this workspace into a target directory.
- [x] Package internals are not copied into generated workspaces.
- [x] Focused automated tests exist for scaffold behavior.
- [x] README documents usage and version behavior.
- [x] Stack metadata reflects the introduced Node.js package.
- [x] A deliverable note is written under `04_outputs/`.
- [x] Packaging is validated with npm tooling.

## Supersession Note

- The current repository is now oriented around `hardware-deal-radar`, a Python CLI product for ThinkPad deal detection.
- This archived spec must not drive future implementation work.
