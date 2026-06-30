# FACTS

## Product

- Fact: v1 is an internal radar for used/refurbished professional ThinkPad opportunities on European eBay marketplaces.
  Source: `00_inbox/hardware-deal-radar-project-contex.md`; `CONTENEDOR CONTEXT PACK/README.md`; `CONTENEDOR CONTEXT PACK/docs/00-product-vision.md`
  Confidence: high

- Fact: The primary user is Raul, and the purchase goal is a clear upgrade for development, AI-assisted coding, multitasking, automation, documentation, CRM, and business operations.
  Source: `00_inbox/hardware-deal-radar-project-contex.md`; `CONTENEDOR CONTEXT PACK/docs/03-buying-criteria.md`
  Confidence: high

- Fact: The project has two goals: build a useful radar and validate a B-shot agentic workflow with planning first and implementation second.
  Source: `CONTENEDOR CONTEXT PACK/README.md`; `CONTENEDOR CONTEXT PACK/docs/00-product-vision.md`; `00_inbox/hardware-deal-radar-project-contex.md`
  Confidence: high

## Scope

- Fact: v1 is ThinkPad-only, prioritizing P14s, T14, T16, P1, and X1 Extreme.
  Source: `00_inbox/hardware-deal-radar-project-contex.md`; `CONTENEDOR CONTEXT PACK/docs/03-buying-criteria.md`
  Confidence: high

- Fact: Minimum purchase floor is 32 GB RAM; ideal RAM is 64 GB.
  Source: `CONTENEDOR CONTEXT PACK/docs/03-buying-criteria.md`; `00_inbox/hardware-deal-radar-project-contex.md`
  Confidence: high

- Fact: Target marketplaces are eBay Spain, Germany, Italy, and United Kingdom.
  Source: `CONTENEDOR CONTEXT PACK/docs/04-marketplaces-and-sources.md`; `00_inbox/hardware-deal-radar-project-contex.md`
  Confidence: high

- Fact: UK listings are allowed but penalized for import, customs, returns, timing, and uncertain total cost.
  Source: `CONTENEDOR CONTEXT PACK/docs/03-buying-criteria.md`; `CONTENEDOR CONTEXT PACK/docs/04-marketplaces-and-sources.md`
  Confidence: high

## Technical Decisions

- Fact: Closed stack is Python 3.12+, SQLite, YAML config, CLI, official eBay Browse API, Telegram alerts, email digest, venv on VPS, and systemd timer every 6 hours.
  Source: `CONTENEDOR CONTEXT PACK/docs/06-cto-architecture.md`; `00_inbox/hardware-deal-radar-project-contex.md`
  Confidence: high

- Fact: Docker is optional/documented and not required for v1 operation.
  Source: `CONTENEDOR CONTEXT PACK/README.md`; `CONTENEDOR CONTEXT PACK/docs/06-cto-architecture.md`
  Confidence: high

- Fact: Scoring must be deterministic, explainable, configurable, and must not use generative AI in v1.
  Source: `CONTENEDOR CONTEXT PACK/docs/08-scoring-model.md`; `CONTENEDOR CONTEXT PACK/codex/agent-rules.md`
  Confidence: high

- Fact: Initial scoring thresholds are strong alert `80`, digest `60`, and ignore below `50`.
  Source: `CONTENEDOR CONTEXT PACK/docs/05-alerting-strategy.md`; `CONTENEDOR CONTEXT PACK/docs/08-scoring-model.md`; `CONTENEDOR CONTEXT PACK/config/scoring.example.yaml.md`
  Confidence: high

- Fact: The system must support real, mock, dry-run, and noop modes.
  Source: `00_inbox/hardware-deal-radar-project-contex.md`; `CONTENEDOR CONTEXT PACK/codex/agent-rules.md`
  Confidence: high

- Fact: Missing eBay, Telegram, SMTP, network, or systemd dependencies must not block implementation.
  Source: `00_inbox/hardware-deal-radar-project-contex.md`; `CONTENEDOR CONTEXT PACK/codex/goal-02-implementation.md`
  Confidence: high

## Current Repo State

- Fact: The repo previously contained scaffold/npm-oriented README, stack metadata, and active spec text.
  Source: `README.md` before migration; `01_harness/STACK.md` before migration; `03_specs/now/001_now.md`
  Confidence: high

- Fact: The previous scaffold/npm direction is superseded by the Hardware Deal Radar context pack.
  Source: `CONTENEDOR CONTEXT PACK/README.md`; `CONTENEDOR CONTEXT PACK/codex/goal-01-planning.md`; migrated repo files
  Confidence: high

## Unknowns and Assumptions

- Unknown: exact purchase budget ceiling by model tier.
- Unknown: final scoring weights by CPU generation, model generation, seller signals, keyboard layout, and country-specific risks.
- Unknown: final SMTP provider and VPS host details.
- Unknown: whether implementation will choose `uv` or `pip-tools`, and whether persistence uses SQLModel or SQLAlchemy.
- Assumption: use root `.env.example` naming as canonical and document any pack naming differences as historical conflict.
