---
description: Record an explicit human override for a failed or blocked gate.
argument-hint: <case_id> <stage_id>
---

Use `spec-driving-orchestrator`.

Arguments: `$ARGUMENTS`

Load `shared/flows/spec-driving/references/command-contract.md` and execute
`spec-drive-override <case_id> <stage_id>`. Require operator, reason, accepted
risk, and next action.
