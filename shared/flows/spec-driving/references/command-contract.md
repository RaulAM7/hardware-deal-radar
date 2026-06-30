# Spec-Drive Command Contract

These commands are implemented as repository-local prompt files for Claude and
Codex. They are command specifications, not a deterministic CLI.

All commands must load:

- `shared/flows/spec-driving/README.md`
- `shared/flows/spec-driving/references/orchestrator-contract.md`
- the relevant stage, review, or command contract

## `spec-drive-init <case_id>`

Scaffold a run at `04_outputs/spec-driving/<case_id>/`.

Create the approved run layout, default `run_config.yaml`, empty `raw/README.md`,
initial `state/run_state.json`, and initial `state/artifact_manifest.json`.

Do not generate business artifacts.

## `spec-drive-run <case_id>`

Run the orchestrator from the current state until:

- a required stage returns `BLOCKED`
- a stage returns `FAIL` and needs revision work in a later turn
- Stage 04 passes and Stage 06 is disabled
- Stage 06 passes

Never skip a review gate.

## `spec-drive-stage <case_id> <stage_id>`

Run exactly one stage and its review gate. Do not continue to the next stage.

## `spec-drive-review <case_id> <stage_id>`

Run only the reviewer for an existing stage artifact and update state from the
review verdict.

## `spec-drive-status <case_id>`

Read state and manifest, then report:

- run status
- active stage
- stage statuses
- artifact paths
- latest review verdicts
- blocked questions
- next action

Do not edit artifacts.

## `spec-drive-override <case_id> <stage_id>`

Record an explicit human override for a failed or blocked review. Require
operator, reason, accepted risk, and next action. Do not delete review evidence.

## `spec-drive-skip <case_id> <stage_id>`

Only Stage 06 may be skipped. Record the skip review with verdict `SKIPPED` and
the reason. Reject skip attempts for Stages 00-04.

## `spec-drive-export <case_id>`

Create or update `handoffs/export_index.md` with approved artifacts, review
evidence, unresolved risks, skips, and overrides. Do not duplicate artifacts.

## `spec-drive-doctor <case_id>`

Inspect the run for contract drift:

- missing expected folders or state files
- invalid stage statuses
- missing artifact paths
- missing review files for passed stages
- forbidden business artifacts
- Stage 06 output while disabled

Report findings and shortest fix paths. Do not rewrite business artifacts.
