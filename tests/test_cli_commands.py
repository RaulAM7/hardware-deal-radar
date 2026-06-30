from __future__ import annotations

from hardware_deal_radar.cli import app


def test_validate_show_and_doctor(runner, isolated_project) -> None:
    result = runner.invoke(app, ["validate-config", "--config-dir", "config"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["show-config", "--config-dir", "config"])
    assert result.exit_code == 0
    assert "searches:" in result.output
    result = runner.invoke(app, ["doctor", "--config-dir", "config"])
    assert result.exit_code == 0
    assert "config" in result.output


def test_mock_dry_run_flow(runner, isolated_project) -> None:
    db_path = str((isolated_project / "data" / "radar.sqlite").resolve())
    result = runner.invoke(
        app,
        ["run-once", "--config-dir", "config", "--mock", "--dry-run", "--db-path", db_path],
    )
    assert result.exit_code == 0
    assert '"raw_results_count"' in result.output

    result = runner.invoke(app, ["list-recent", "--db-path", db_path])
    assert result.exit_code == 0
    assert "ThinkPad" in result.output

    result = runner.invoke(app, ["explain-score", "1", "--db-path", db_path])
    assert result.exit_code == 0
    assert "Positive reasons" in result.output

    result = runner.invoke(
        app, ["digest", "--config-dir", "config", "--dry-run", "--db-path", db_path]
    )
    assert result.exit_code == 0
    assert "Hardware Deal Radar digest" in result.output

    result = runner.invoke(app, ["test-alert", "--config-dir", "config", "--dry-run"])
    assert result.exit_code == 0
    assert "simulated" in result.output
