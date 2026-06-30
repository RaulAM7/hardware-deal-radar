# Hardware Deal Radar — Codex / Agent Instructions

Read these files in order before starting any task:

1. `01_harness/RULES.md` — always-on constraints
2. `01_harness/STACK.md` — tech stack reference
3. `01_harness/TASKFLOW.md` — workflow phases

## Context

- `02_context/` contains BRIEF, FACTS, CONSTRAINTS, GLOSSARY, LINKS
- `docs/` contains migrated product and technical context
- `codex/` contains project-specific agent rules, goals, and definition of done
- Work from one active spec at a time in `03_specs/now/`
- Final deliverables go to `04_outputs/`
- Working debris goes to `05_scratch/`
- Skills in `shared/skills/` — load only when needed

## Product guardrails

- V1 is a Python CLI radar for ThinkPad deals on eBay Europe.
- Keep SQLite, YAML config, official eBay Browse API, Telegram/email alerts, and VPS/systemd deployment.
- Do not turn v1 into a frontend, SaaS, scraping system, multi-user product, or automatic purchasing tool.
- Do not block implementation on missing external credentials; use mock, dry-run, and noop modes.
