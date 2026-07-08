import subprocess
import sys


def test_cli_help_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "cli.py", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "run" in result.stdout


def test_cli_run_without_logline_exits_nonzero() -> None:
    result = subprocess.run(
        [sys.executable, "cli.py", "run"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_cli_help_lists_scenario_subcommand() -> None:
    result = subprocess.run(
        [sys.executable, "cli.py", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "scenario" in result.stdout


def test_cli_scenario_without_logline_exits_nonzero() -> None:
    result = subprocess.run(
        [sys.executable, "cli.py", "scenario"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
