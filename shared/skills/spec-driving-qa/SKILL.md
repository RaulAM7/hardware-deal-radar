---
name: spec-driving-qa
description: Strict QA gate for the spec-driving workflow. Use whenever reviewing a Stage 00, 01, 02, 03, 04, or optional Stage 06 artifact, interpreting PASS/FAIL/BLOCKED/SKIPPED verdicts, or checking whether a spec-driving run may advance.
---

# Goal

Prevent false progress in the spec-driving workflow.

# Required References

- Flow overview: `../../flows/spec-driving/README.md`
- Review contract: `../../flows/spec-driving/references/review-contract.md`
- Stage contract: `../../flows/spec-driving/references/stage-contract.md`
- Review template: `../../flows/spec-driving/templates/stage_review.md`

# Inputs

- The stage artifact being reviewed
- `run_config.yaml`
- `state/run_state.json`
- `state/artifact_manifest.json`
- Approved prior-stage artifacts
- Stage 00 source map

# Output

One review file:

```text
reviews/stage_<stage_id>_review_iter_<nn>.md
```

Use YAML front matter and the required review sections from the review contract.

# Verdict Rules

- `PASS`: only when every criterion has explicit evidence.
- `FAIL`: artifact can be fixed from available material.
- `BLOCKED`: truthful completion needs missing operator input.
- `SKIPPED`: only for Stage 06 when execution planning is disabled or explicitly
  skipped.

# Mandatory Checks

Check:

- expected path and filename
- required headings
- source traceability for important claims
- no invented facts
- unresolved blockers are not hidden as assumptions
- no scope creep
- no forbidden business artifacts
- Stage 04 does not invent scope beyond Stage 03
- Stage 06 is gated by `execution_plan_enabled`
- artifact ends with a handoff, except skipped Stage 06

# Anti-Patterns

- Passing based on tone or completeness impression.
- Writing a decorative review with no criterion-by-criterion evidence.
- Treating missing source support as a harmless assumption.
- Allowing a proposal to sell unapproved technical scope.
