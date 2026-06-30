# Spec-Driving Stage Contract

Stage agents produce one artifact at the expected path and nothing else unless
the orchestrator explicitly asks for a handoff note or revision archive.

All artifacts default to Spanish. Use another language only when `run_config.yaml`
sets `artifact_language` differently.

## Global Stage Rules

- Do not invent facts.
- Mark missing information as `Unknown`.
- Cite source ids from Stage 00 for important claims and decisions.
- Do not hide blockers as assumptions.
- Do not create business artifacts outside the expected stage path.
- End every artifact with `Handoff to Next Stage`.
- Preserve the buyer priority model generically:
  primary functional or strategic buyer first, operational pain owner second,
  economic buyer only for cost, ROI, and value framing.

The flow is abstract. Do not hardcode any first-run or client-specific details.

## Stage 00 - Intake Context Pack

Artifact:

```text
context/00_intake_context_pack.md
```

Purpose: normalize chaotic material into a traceable context pack without
solving the project.

Required extraction:

- project summary
- actors and stakeholders
- raw facts
- business goals
- operational pains
- technical constraints
- open questions
- assumptions
- contradictions
- source map
- candidate scope areas
- non-goals
- missing information

Assign stable source ids such as `SRC-001` and use them downstream.

## Stage 01 - Problem Audit

Artifact:

```text
artifacts/01_problem_audit_v1.md
```

Purpose: distinguish actual problems from wishes, vague ideas, implementation
fantasies, and unsupported assumptions.

Each problem must cover:

- who feels it
- cause
- operational or business impact
- whether system, process, or automation could resolve it
- MVP relevance
- supporting evidence
- unknowns

## Stage 02 - MVP Scope Decision

Artifact:

```text
artifacts/02_mvp_scope_decision_v1.md
```

Purpose: make an opinionated Phase 1/MVP scope decision.

Required decision sections:

- Phase 1 / MVP scope
- Phase 2 candidates
- explicitly out of scope
- rationale
- dependency notes
- risk notes
- unresolved questions
- do-not-sell-this-yet warnings when needed

This stage must decide. It must not only list options.

## Stage 03 - Technical Pre-Sales Blueprint

Artifact:

```text
artifacts/03_technical_presales_blueprint_v1.md
```

Purpose: produce the pre-sales technical and functional blueprint that grounds
the commercial proposal.

Include only the depth needed to price and sell with confidence. Do not include
atomic implementation tasks, exhaustive issue lists, or a repository file tree.

## Stage 04 - Commercial Proposal

Artifact:

```text
artifacts/04_commercial_proposal_v1.md
```

Purpose: translate the approved blueprint into buyer-friendly commercial
narrative.

ROI, cost, saved-hours, and value material must be sections inside this
artifact. Do not create an independent ROI artifact.

Pricing uses placeholders unless explicit pricing input exists in sources or
run config.

The proposal must not invent technical scope beyond Stage 03.

## Stage 06 - Execution Plan

Artifact:

```text
artifacts/06_execution_plan_v1.md
```

Purpose: produce a deeper implementation plan only when
`execution_plan_enabled: true`.

Backlog, milestones, repository or system structure, QA, deployment, and
handoff planning may appear only as sections inside this artifact.

If Stage 06 is not enabled, it must be reviewed as `SKIPPED` with the skip
reason recorded.
