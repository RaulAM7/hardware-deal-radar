# Spec-Driving Review Contract

The reviewer is a real stage gate. It is not decorative.

Every review must produce one Markdown file with YAML front matter under:

```text
reviews/stage_<stage_id>_review_iter_<nn>.md
```

## Front Matter

```yaml
---
stage_id: "00"
reviewer_id: "spec-driving-reviewer"
artifact_path: "context/00_intake_context_pack.md"
verdict: "PASS"
iteration: 1
reviewed_at: ""
---
```

Allowed verdicts:

- `PASS`
- `FAIL`
- `BLOCKED`
- `SKIPPED`

## Required Review Sections

```markdown
# Review - Stage <stage_id>

## Verdict

## Reviewed Artifact

## Checklist Evidence

## Missing Items

## Contradictions

## Scope Creep

## Unsupported Assumptions

## Required Fixes

## Shortest Fix Path

## Blocking Questions
```

`Checklist Evidence` must include criteria-by-criteria evidence. A generic
"looks good" approval is invalid.

## Mandatory Fail Conditions

Return `FAIL` when any of these are true:

- artifact path is wrong
- artifact name is wrong
- required sections are missing
- source traceability is missing for important claims
- facts are invented
- unresolved blockers are disguised as assumptions
- scope creep appears
- output is too generic to use
- Stage 02 ignores primary buyer priority
- Stage 04 overfocuses on economic-buyer analysis
- Stage 04 invents scope not present in Stage 03
- independent ROI artifact is created or requested
- forbidden Stage 07/08/09/final manifest business artifacts are created
- Stage 06 is produced when `execution_plan_enabled` is false
- stage output bypasses previous stage decisions
- stage output contradicts previous approved artifact
- handoff summary is missing

Return `BLOCKED` when required source information is missing and the artifact
cannot be made truthful by marking it Unknown.

Return `SKIPPED` only for Stage 06 when execution planning is disabled or an
operator explicitly skips it.

Return `PASS` only when all required criteria have explicit evidence.
