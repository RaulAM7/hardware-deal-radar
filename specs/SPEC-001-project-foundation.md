# SPEC-001 - Project Foundation

## Objective

Create the Python project foundation for Hardware Deal Radar without implementing business logic beyond safe command stubs.

## Scope

- Add Python packaging and dependency metadata.
- Establish source, test, config, scripts, data, docs, and package layout.
- Add console script entrypoint `radar`.
- Add baseline settings loading from `.env` without printing secrets.
- Keep `.env.example` public and `.env` ignored.
- Add initial developer commands for install, lint, and test.

## Out of Scope

- Real eBay API calls.
- Real Telegram or SMTP delivery.
- Full pipeline implementation.
- systemd installation.
- Docker as required runtime.

## Expected Files and Modules

- `pyproject.toml`
- `uv.lock`
- `src/hardware_deal_radar/__init__.py`
- `src/hardware_deal_radar/main.py`
- `src/hardware_deal_radar/cli.py`
- `src/hardware_deal_radar/settings.py`
- `tests/test_cli_foundation.py`
- `README.md`
- `.env.example`
- `.gitignore`

## Tasks

- Configure project name `hardware-deal-radar`, Python `>=3.12`, package module `hardware_deal_radar`, and console script `radar`.
- Use `uv` as dependency workflow with a normal `.venv`.
- Add dependencies: Typer, Pydantic, pydantic-settings, PyYAML, httpx, SQLModel, Rich.
- Add dev dependencies: pytest, ruff.
- Create Typer app with placeholder commands for required CLI surface.
- Implement settings class that reads `.env` via pydantic-settings and masks secret fields in display.
- Keep `.env.example` with empty secret values only.
- Ensure `.gitignore` excludes `.env`, `.venv/`, caches, and SQLite runtime files.
- Update README with setup commands and statement that implementation is spec-driven.

## Acceptance Criteria

- [ ] `uv sync` creates a working environment.
- [ ] `uv run radar --help` exits successfully.
- [ ] `uv run radar doctor` exists, even if only foundation checks are implemented.
- [ ] `uv run pytest` passes.
- [ ] `uv run ruff check .` passes.
- [ ] Importing `hardware_deal_radar` works.
- [ ] Secret fields are masked in settings/debug output.
- [ ] `.env` is ignored by git and not needed for mock/help commands.

## Tests and Checks

- Test CLI help.
- Test package import.
- Test settings load from environment with empty optional values.
- Test secret masking for eBay, Telegram, and SMTP password fields.
- Run `uv run pytest`.
- Run `uv run ruff check .`.

## Risks

- Dependency choices can grow too quickly; keep only the selected baseline.
- Settings output can accidentally expose secrets; masking must be tested early.

## Assumptions

- `uv` is available or can be installed on the development machine and VPS.
- SQLModel is chosen over raw SQLAlchemy to keep schema definitions close to Pydantic-style models.
