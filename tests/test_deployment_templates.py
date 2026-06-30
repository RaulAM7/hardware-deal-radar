from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_systemd_templates_and_scripts_exist() -> None:
    service = REPO_ROOT / "scripts/systemd/hardware-deal-radar.service"
    timer = REPO_ROOT / "scripts/systemd/hardware-deal-radar.timer"
    install_script = REPO_ROOT / "scripts/install-vps.sh"
    setup_script = REPO_ROOT / "scripts/setup-systemd.sh"
    run_once_script = REPO_ROOT / "scripts/run-once.sh"

    for path in (service, timer, install_script, setup_script, run_once_script):
        assert path.exists(), f"missing deployment artifact: {path}"

    service_text = service.read_text(encoding="utf-8")
    timer_text = timer.read_text(encoding="utf-8")

    assert "__RADAR_APP_DIR__" in service_text
    assert ".venv/bin/radar run-once" in service_text
    assert "OnCalendar=*-*-* 00/6:00:00" in timer_text


def test_shell_scripts_have_valid_bash_syntax() -> None:
    scripts = [
        REPO_ROOT / "scripts/install-vps.sh",
        REPO_ROOT / "scripts/run-once.sh",
        REPO_ROOT / "scripts/setup-systemd.sh",
    ]
    for script in scripts:
        subprocess.run(["bash", "-n", str(script)], check=True)
