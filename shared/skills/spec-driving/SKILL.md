---
name: spec-driving
description: Run the reusable spec-driving workflow for chaotic client or project material. Use for spec-drive init, run, stage, status, export, skip, override, or doctor operations, and for producing Stage 00, 01, 02, 03, 04, or optional Stage 06 artifacts inside isolated run containers.
---

# Goal

Operate the reusable spec-driving flow without hardcoding any specific client
case.

# Required References

Read only the references needed for the current command:

- Flow overview: `../../flows/spec-driving/README.md`
- Orchestrator rules: `../../flows/spec-driving/references/orchestrator-contract.md`
- Stage rules: `../../flows/spec-driving/references/stage-contract.md`
- Command rules: `../../flows/spec-driving/references/command-contract.md`
- Templates: `../../flows/spec-driving/templates/`
- Schemas: `../../flows/spec-driving/schemas/`

# Inputs

- Run root: `04_outputs/spec-driving/<case_id>/`
- `run_config.yaml`
- `raw/`
- `context/00_intake_context_pack.md` after Stage 00
- Previously approved artifacts and reviews
- Internal state in `state/`

# Outputs

Write only the expected file for the current action:

- Stage 00: `context/00_intake_context_pack.md`
- Stage 01: `artifacts/01_problem_audit_v1.md`
- Stage 02: `artifacts/02_mvp_scope_decision_v1.md`
- Stage 03: `artifacts/03_technical_presales_blueprint_v1.md`
- Stage 04: `artifacts/04_commercial_proposal_v1.md`
- Stage 06: `artifacts/06_execution_plan_v1.md`
- Export: `handoffs/export_index.md`
- State: `state/run_state.json` and `state/artifact_manifest.json`

# Procedure

1. Load the flow overview and the relevant contract.
2. Read run config and state before acting.
3. Confirm the target stage is allowed.
4. Read only the sources needed for the current stage.
5. Produce the canonical artifact using the matching template headings.
6. Cite Stage 00 source ids for important claims and decisions.
7. Mark unknowns as `Unknown` rather than guessing.
8. End stage artifacts with `Handoff to Next Stage`.
9. Do not advance state past a stage until a review verdict exists.

# Stage 06 Rule

Do not create `06_execution_plan_v1.md` unless `execution_plan_enabled: true`.
If execution planning is disabled, Stage 06 can only be recorded as skipped
through the reviewer gate.

# Buyer Priority Rule

Keep the role model generic:

1. Primary functional or strategic buyer has highest priority.
2. Operational pain owner defines the day-to-day problems to solve.
3. Economic buyer appears mainly in cost, ROI, and value justification.

Use named people only when the source material names them.

# Anti-Patterns

- Creating a real run for a future case unless requested.
- Using `00_inbox/` as the run container.
- Creating independent ROI, backlog, milestone, repository structure, or final
  manifest business artifacts.
- Letting Stage 04 invent scope not approved in Stage 03.
- Letting assumptions hide unresolved blockers.
- Passing or advancing a stage without review evidence.
