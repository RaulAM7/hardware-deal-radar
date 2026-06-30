# SPEC-002 - Config System

## Objective

Implement YAML configuration loading, validation, and inspection for searches, scoring, and marketplaces.

## Scope

- Convert example configs into runtime configs.
- Define Pydantic schemas for `searches.yaml`, `scoring.yaml`, and `marketplaces.yaml`.
- Validate cross-file references.
- Add `radar validate-config` and `radar show-config`.
- Support explicit config directory selection.

## Out of Scope

- eBay API calls.
- Scoring calculation beyond schema validation.
- Alert sending.
- Web or interactive config UI.

## Expected Files and Modules

- `config/searches.yaml`
- `config/scoring.yaml`
- `config/marketplaces.yaml`
- `src/hardware_deal_radar/config/loader.py`
- `src/hardware_deal_radar/config/schemas.py`
- `tests/test_config_loader.py`
- `tests/fixtures/config/`

## Tasks

- Copy example YAML files into runtime YAML files if they do not exist.
- Define schemas for marketplace, search, scoring thresholds, scoring weights, keywords, and risk penalties.
- Validate that each enabled search references known marketplaces.
- Validate thresholds are ordered: strong alert greater than digest, digest greater than ignore-below.
- Validate minimum RAM and preferred RAM are positive and preferred is at least minimum.
- Add clear errors for missing files, invalid YAML, missing keys, or bad cross-references.
- Implement `radar validate-config --config-dir config`.
- Implement `radar show-config --config-dir config` with sanitized output and no secrets.

## Acceptance Criteria

- [ ] Runtime config files exist under `config/`.
- [ ] Valid provided config passes validation.
- [ ] Invalid marketplace references fail with a clear message.
- [ ] Invalid threshold ordering fails with a clear message.
- [ ] `radar validate-config` exits `0` on valid config.
- [ ] `radar show-config` prints the loaded config without secrets.
- [ ] Config loader can be imported and used by later pipeline specs.

## Tests and Checks

- Test valid config load.
- Test missing file errors.
- Test invalid YAML errors.
- Test cross-reference validation.
- Test threshold ordering.
- Run `uv run pytest tests/test_config_loader.py`.

## Risks

- Overly strict schemas can block useful future changes; allow optional fields where source data may be incomplete.
- Under-specified schemas can push errors later into runtime; validate core fields now.

## Assumptions

- Config file names are canonical: `searches.yaml`, `scoring.yaml`, `marketplaces.yaml`.
- Example files remain as documentation and may be copied manually or by setup instructions.
