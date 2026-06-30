# Hardware Deal Radar — Claude Code Instructions

Read these files in order before starting any task:

1. `01_harness/RULES.md` — always-on constraints
2. `01_harness/STACK.md` — tech stack reference
3. `01_harness/TASKFLOW.md` — workflow phases

## Quick reference

- **Context**: `02_context/` (BRIEF, FACTS, CONSTRAINTS, GLOSSARY, LINKS)
- **Docs**: `docs/` — product and technical context
- **Codex goals**: `codex/`
- **Active spec**: `03_specs/now/` — work from one spec at a time
- **Deliverables**: `04_outputs/`
- **Scratch/WIP**: `05_scratch/`
- **Skills**: `shared/skills/` — load only when needed
- **Agents**: `shared/agents/` — delegate via subagent definitions

## Product guardrails

- V1 is a Python CLI radar for ThinkPad deals on eBay Europe.
- Keep SQLite, YAML config, official eBay Browse API, Telegram/email alerts, and VPS/systemd deployment.
- Do not turn v1 into a frontend, SaaS, scraping system, multi-user product, or automatic purchasing tool.
- Do not block implementation on missing external credentials; use mock, dry-run, and noop modes.
