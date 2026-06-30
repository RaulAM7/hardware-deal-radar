# DECISIONS

Short decision log.

- 2026-03-01: Decision template initialized. Status: pending
- 2026-06-16: Package the repo as a `create-*` npm CLI that copies a vetted scaffold snapshot instead of publishing it as a runtime library. Status: accepted
- [inferred] 2026-06-30: Supersede the npm scaffold direction with Hardware Deal Radar as the active product direction. Status: accepted
- [inferred] 2026-06-30: Use Python 3.12+ for v1. Status: accepted
- [inferred] 2026-06-30: Use SQLite for persistence and YAML for configuration. Status: accepted
- [inferred] 2026-06-30: Use CLI as the primary interface; no frontend web app in v1. Status: accepted
- [inferred] 2026-06-30: Use official eBay Browse API as the only v1 marketplace source; no HTML scraping in v1. Status: accepted
- [inferred] 2026-06-30: Limit v1 scope to ThinkPad models across eBay ES, DE, IT, and GB. Status: accepted
- [inferred] 2026-06-30: Treat 32 GB RAM as minimum and 64 GB RAM as ideal. Status: accepted
- [inferred] 2026-06-30: Use deterministic explainable scoring; no generative-AI scoring in v1. Status: accepted
- [inferred] 2026-06-30: Use Telegram for strong alerts and SMTP email for digest. Status: accepted
- [inferred] 2026-06-30: Use VPS deployment with venv and systemd timer every 6 hours. Status: accepted
- [inferred] 2026-06-30: Implement real, mock, dry-run, and noop modes so credentials do not block implementation. Status: accepted
- [inferred] 2026-06-30: Use scoring thresholds `80` strong alert, `60` digest, and `50` ignore-below as initial defaults. Status: accepted
