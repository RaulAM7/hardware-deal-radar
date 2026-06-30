# Assumptions

- The context pack in `CONTENEDOR CONTEXT PACK/` supersedes the earlier scaffold/npm direction.
- The next work phase is planning/spec generation, not direct implementation.
- The implementation will use `uv` for dependency management and a normal `.venv` for runtime.
- SQLite table creation at app startup is acceptable for v1 unless the planning spec chooses migrations.
- Score can initially live on the listing record if that keeps v1 simpler; a separate score table is optional.
- `price_history` is useful but optional if it threatens implementation focus.
- Exact eBay Browse API request/response details must be verified during the API integration spec.
- Real credentials may be absent during implementation; mock, dry-run, and noop flows are required.
- Root `.env.example` naming is canonical for now.

## Still Unknown

- Exact purchase budget ceiling by model and generation.
- Exact scoring weights for CPU, model generation, seller, keyboard, marketplace, and risk signals.
- Final SMTP provider and VPS host details.
- Final production VPS path and Linux user are still unknown.
