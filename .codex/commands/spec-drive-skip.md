---
description: Skip optional Stage 06 in a spec-driving run.
argument-hint: <case_id> 06
---

Use `spec-driving-orchestrator`.

Arguments: `$ARGUMENTS`

Load `shared/flows/spec-driving/references/command-contract.md` and execute
`spec-drive-skip <case_id> <stage_id>`. Reject skip attempts for Stages 00-04.
