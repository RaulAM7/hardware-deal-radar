# Technical Decisions

- [inferred] Use Python 3.12+ for v1 implementation.
- [inferred] Use SQLite for v1 persistence.
- [inferred] Use YAML files for search, scoring, and marketplace configuration.
- [inferred] Use a CLI as the primary interface.
- [inferred] Use official eBay Browse API as the only v1 source.
- [inferred] Separate source client, source normalizer, pipeline, scoring, storage, alerts, reports, and config modules.
- [inferred] Use deterministic scoring with explicit reasons, risk flags, unknown fields, and recommendations.
- [inferred] Use Telegram for strong alerts and SMTP email for digest.
- [inferred] Use systemd timer every 6 hours on a VPS.
- [inferred] Keep Docker optional/documented only.
- [inferred] Support real, mock, dry-run, and noop modes from the start.
- [inferred] Do not block implementation on missing external credentials.
- [inferred] Do not introduce frontend, SaaS, scraping, generative-AI scoring, Postgres/Supabase, Kubernetes, or automatic purchasing in v1.
- [inferred] Treat the previous scaffold/npm direction as superseded.
