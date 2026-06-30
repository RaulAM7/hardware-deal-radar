# BRIEF

## What

- Hardware Deal Radar is an internal VPS-hosted CLI radar for finding real buying opportunities in used or refurbished professional ThinkPad laptops on eBay Europe.
- It is not an eBay saved-search clone. Its value is normalization, risk-aware total cost estimation, deterministic scoring, deduplication, history, and actionable alerts.

## Who

- Primary user: Raul.
- Use case: wait for an objective hardware upgrade opportunity instead of buying from anxiety.

## Why

- Raul's current 16 GB laptop can become limiting for browser-heavy work, multiple Codex/Claude Code sessions, worktrees, local services, automation, documentation, CRM, and business operations.
- The desired purchase should be a clear improvement, especially around RAM and professional reliability.
- The project also validates a B-shot agentic workflow: one planning/spec goal, then one implementation goal.

## v1 Outcome

- A Python 3.12+ CLI system that:
  - reads YAML search/scoring/marketplace config;
  - queries the official eBay Browse API for ES, DE, IT, and GB;
  - normalizes listings;
  - extracts or infers model, RAM, SSD, CPU, keyboard, seller, condition, and risk signals;
  - estimates total cost in EUR;
  - deduplicates and persists history in SQLite;
  - calculates deterministic explainable score;
  - sends strong Telegram alerts;
  - generates email digest for medium candidates;
  - runs manually and every 6 hours via systemd timer;
  - supports real, mock, dry-run, and noop modes.

## Success

- Alert little, but alert well.
- Every alert acts as a decision card: title, inferred specs, seller, marketplace, total cost, score, positives, risks, and link.
- Missing credentials or external service failures do not block implementation or local validation.

## Current State

- Context has been migrated from `00_inbox/` and `CONTENEDOR CONTEXT PACK/`.
- `docs/`, `codex/`, and `config/` now contain planning-ready project material.
- The previous npm scaffold direction is superseded.
- No functional Python implementation exists yet.

## Immediate Next Step

- Execute the active planning spec in `03_specs/now/` to produce implementation-ready specs and an ordered implementation plan.
