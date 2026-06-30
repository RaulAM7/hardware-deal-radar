# Spec-Driving Orchestrator Contract

The orchestrator coordinates a run. It does not write all stage artifacts by
itself. It delegates artifact production to stage agents and delegates gate
evaluation to `spec-driving-reviewer`.

All paths below are relative to the run root:

```text
04_outputs/spec-driving/<case_id>/
```

## Required Inputs

- `run_config.yaml`
- `raw/` containing the operator-provided source material
- `state/run_state.json`
- `state/artifact_manifest.json`

## Run Config Defaults

```yaml
case_id: ""
run_id: ""
artifact_language: "es"
execution_plan_enabled: false
operator: ""
created_at: ""
notes: ""
```

`execution_plan_enabled` is the only setting that allows Stage 06. Do not infer
implementation readiness from enthusiasm, buyer interest, or commercial value.

## Run State

Maintain `state/run_state.json` with:

- `case_id`
- `run_id`
- `mode`, default `standard`
- `run_status`
- `active_stage`
- `stage_statuses`
- `artifact_paths`
- `review_paths`
- `iteration_counts`
- `max_iterations`, default `null`
- `blocked_questions`
- `assumptions`
- `overrides`
- `last_action`
- `next_action`
- `updated_at`

Allowed stage statuses:

- `PENDING`
- `READY`
- `RUNNING`
- `IN_REVIEW`
- `REVISION_REQUIRED`
- `PASSED`
- `FAILED`
- `BLOCKED`
- `SKIPPED`

Allowed run statuses:

- `INITIALIZED`
- `IN_PROGRESS`
- `BLOCKED`
- `PRE_SALES_COMPLETE`
- `IMPLEMENTATION_READY`
- `COMPLETED`
- `FAILED`

## Artifact Manifest

Maintain `state/artifact_manifest.json` with one record per stage:

- expected artifact path
- current artifact path
- latest review path
- approved review path
- latest verdict
- iteration count
- source requirements
- status

This manifest is internal metadata. It is not a business deliverable.

## Initialization

`spec-drive-init <case_id>` scaffolds the run only. It creates the directory
layout, an empty `raw/README.md`, default `run_config.yaml`, initial state, and
artifact manifest. It does not import raw files, generate business artifacts, or
run Stage 00.

Use the initial files in `templates/` as the starting shape for `run_config.yaml`,
`raw/README.md`, `state/run_state.json`, and `state/artifact_manifest.json`.

## Stage Execution

For a stage run:

1. Read `run_config.yaml`, `state/run_state.json`, and
   `state/artifact_manifest.json`.
2. Confirm prior required stages are `PASSED`, unless the current stage is 00.
3. Confirm Stage 06 is enabled before running Stage 06.
4. Mark the stage `RUNNING`.
5. Prepare a compact input packet for the stage agent.
6. Invoke the correct stage agent.
7. Verify the expected artifact path exists.
8. Mark the stage `IN_REVIEW`.
9. Invoke `spec-driving-reviewer`.
10. Read the review verdict and update state.

The orchestrator must never advance a stage without a review file and explicit
verdict.

## Iteration Rules

Failed drafts are preserved under:

```text
artifacts/_iterations/stage_<stage_id>_iter_<nn>_<artifact_name>
```

The canonical artifact path remains fixed. Before rewriting a failed canonical
artifact, archive the old version to `_iterations/`.

There is no fixed iteration limit by default. Use `max_iterations: null` in
state. If repeated review feedback shows the same blocker and no progress is
possible without operator input, mark the stage and run `BLOCKED`.

## Verdict Handling

- `PASS`: mark stage `PASSED`, record approved review, advance.
- `FAIL`: mark stage `REVISION_REQUIRED`, preserve review feedback, rerun the
  same stage on the next action.
- `BLOCKED`: mark stage and run `BLOCKED`, record blocking questions, stop.
- `SKIPPED`: allowed only for Stage 06; record skip reason and mark Stage 06
  `SKIPPED`.

## Completion

If Stage 04 passes and `execution_plan_enabled` is false, set run status to
`PRE_SALES_COMPLETE`.

If Stage 06 passes, set run status to `IMPLEMENTATION_READY`.

## Override

An override can advance past a failed or blocked gate only when an operator uses
the override command. Record:

- operator
- timestamp
- stage id
- review path
- original verdict
- reason
- accepted risk
- next action

Do not edit or remove the original review evidence.

## Export

`spec-drive-export` creates or updates `handoffs/export_index.md`. It lists
approved artifacts, review verdicts, unresolved risks, skip decisions, and
overrides. It does not duplicate artifact files.
