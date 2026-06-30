# Initial Context Report - 2026-06-30

## What was built

- `02_context/BRIEF.md`: consolidated product brief, v1 outcome, success definition, current state, and immediate next step.
- `02_context/FACTS.md`: verifiable project, scope, stack, scoring, and repo-state facts with source references.
- `02_context/CONSTRAINTS.md`: budget/time unknowns, tooling limits, non-negotiables, operational constraints, and product constraints.
- `02_context/GLOSSARY.md`: concise definitions for radar, listing, scoring, dry-run, mock/noop modes, digest, source client, and source normalizer.
- `02_context/LINKS.md`: source URLs actually present in the provided material.
- `docs/`: migrated structured product and technical context from `CONTENEDOR CONTEXT PACK/docs/`, plus assumptions and technical decisions.
- `codex/`: migrated project agent rules, definition of done, and goal prompts from `CONTENEDOR CONTEXT PACK/codex/`.
- `config/`: created executable example YAML files for searches, scoring, and marketplaces.
- `03_specs/backlog.md`: seeded inferred planning and implementation backlog items.
- `03_specs/decisions.md`: seeded inferred decisions that supersede the old scaffold direction.
- `03_specs/now/001_planning-and-specs.md`: replaced the old active spec with a planning/spec-generation spec.
- `03_specs/archive/2026-06-16_npm-scaffold_superseded.md`: archived the previous npm scaffold spec as superseded.
- `README.md`, `AGENTS.md`, `CLAUDE.md`, `01_harness/STACK.md`: reoriented repo entrypoints around Hardware Deal Radar.
- `.env.example` and `.gitignore`: normalized environment placeholders and ensured `.env` is ignored.

## Gaps and unknowns

- Exact purchase budget by model/generation is still unknown; this blocks final price threshold tuning.
- Exact scoring weights are still unknown; this blocks final scoring implementation details but not planning.
- Final SMTP provider and VPS host details are unknown; this blocks production deployment configuration only.
- Final dependency workflow is undecided between `uv` and `pip-tools`; this should be resolved in project foundation spec.
- Final persistence library is undecided between SQLModel and lightweight SQLAlchemy; this should be resolved in storage spec.
- Official eBay Browse API endpoint/request details were not present as source links; the API integration spec should verify official docs.

## Conflicts found

- `README.md`, `01_harness/STACK.md`, and `03_specs/now/001_now.md` described an npm scaffold CLI; `CONTENEDOR CONTEXT PACK/` describes Hardware Deal Radar. Handled by superseding the scaffold direction and archiving the old spec.
- `00_inbox/hardware-deal-radar-project-contex.md` proposed digest threshold `65-79`; `CONTENEDOR CONTEXT PACK/docs/05-alerting-strategy.md`, `docs/08-scoring-model.md`, and `config/scoring.example.yaml.md` use digest threshold `60`. Handled by using `60` as the current canonical default.
- `.env.example` and `CONTENEDOR CONTEXT PACK/.env.example` used different SMTP/email variable names. Handled by preserving the more complete root naming and adding `EBAY_MARKETPLACE_DEFAULT`.
- `00_inbox/` included a more granular snapshot-oriented data model; `CONTENEDOR CONTEXT PACK/docs/07-data-model.md` allows a simpler v1 listing-centric model. Handled by leaving the simpler model as current planning default while preserving optional history in specs.

## Suggested next action

Run the active planning spec in `03_specs/now/001_planning-and-specs.md` to generate implementation-ready specs and `codex/implementation-plan.md`.
