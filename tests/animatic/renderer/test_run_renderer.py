from pathlib import Path
from unittest.mock import MagicMock

import pytest

from agents.animatic.renderer.run_renderer import render_animatic


def test_render_animatic_invokes_renderer_script_with_absolute_paths(tmp_path, monkeypatch) -> None:
    timeline_path = tmp_path / "images" / "timeline.json"
    output_path = tmp_path / "animatic.mp4"
    cwd = tmp_path / "images"

    fake_run = MagicMock(return_value=MagicMock(returncode=0, stderr=""))
    monkeypatch.setattr("agents.animatic.renderer.run_renderer.subprocess.run", fake_run)

    render_animatic(timeline_path, output_path, cwd)

    fake_run.assert_called_once()
    args, kwargs = fake_run.call_args
    command = args[0]
    assert str(timeline_path.resolve()) in command
    assert str(output_path.resolve()) in command
    assert kwargs["cwd"] == str(cwd)


def test_render_animatic_raises_when_ffmpeg_fails(tmp_path, monkeypatch) -> None:
    timeline_path = tmp_path / "images" / "timeline.json"
    output_path = tmp_path / "animatic.mp4"
    cwd = tmp_path / "images"

    fake_run = MagicMock(return_value=MagicMock(returncode=1, stderr="ffmpeg error: no such file"))
    monkeypatch.setattr("agents.animatic.renderer.run_renderer.subprocess.run", fake_run)

    with pytest.raises(RuntimeError, match="ffmpeg error"):
        render_animatic(timeline_path, output_path, cwd)


def test_render_animatic_creates_cwd_if_missing(tmp_path, monkeypatch) -> None:
    timeline_path = tmp_path / "images" / "timeline.json"
    output_path = tmp_path / "animatic.mp4"
    cwd = tmp_path / "images"
    assert not cwd.exists()

    fake_run = MagicMock(return_value=MagicMock(returncode=0, stderr=""))
    monkeypatch.setattr("agents.animatic.renderer.run_renderer.subprocess.run", fake_run)

    render_animatic(timeline_path, output_path, cwd)

    assert cwd.exists()
