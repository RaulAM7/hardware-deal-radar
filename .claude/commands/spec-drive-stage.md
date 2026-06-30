---
description: Run one spec-driving stage and its review gate.
argument-hint: <case_id> <stage_id>
---

Use `spec-driving-orchestrator`.

Arguments: `$ARGUMENTS`

Load `shared/flows/spec-driving/references/command-contract.md` and execute
`spec-drive-stage <case_id> <stage_id>`. Stop after the stage review verdict.
