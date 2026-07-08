from unittest.mock import MagicMock

import pytest

from agents.animatic.agent import generate_timeline
from agents.animatic.schemas import Cut, Motion, Overlays, Timeline
from agents.animatic.validators import validate_timeline
from agents.storyboard.schemas import Shot

FAKE_SHOTS = [
    Shot(
        size="WS",
        angle="eye-level",
        movement="static",
        duration=3,
        description="낡은 극장 무대 위, 지우가 소품 상자를 뒤진다",
        dialogue="",
        audio="",
        sceneSlug="S1",
    )
]

FAKE_TIMELINE = Timeline(
    project="테스트 프로젝트",
    fps=24,
    resolution="1280x720",
    cuts=[
        Cut(
            cut=1,
            image="cut1.png",
            duration=4.0,
            duration_rationale="WS(+1.5)+기본(1.0)",
            motion=Motion(type="static"),
            transition_out="cut",
            overlays=Overlays(info="CUT 1 | WS", caption="지우가 상자를 뒤진다", audio_note=""),
            flags=[],
        )
    ],
)


def test_generate_timeline_returns_timeline_from_gemini_response(monkeypatch) -> None:
    fake_response = MagicMock(parsed=FAKE_TIMELINE)
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response
    monkeypatch.setattr("agents.animatic.agent.get_gemini_client", lambda: fake_client)

    result = generate_timeline(FAKE_SHOTS)

    assert result == FAKE_TIMELINE


def test_generate_timeline_calls_gemini_with_shot_list_and_json_schema(monkeypatch) -> None:
    fake_response = MagicMock(parsed=FAKE_TIMELINE)
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response
    monkeypatch.setattr("agents.animatic.agent.get_gemini_client", lambda: fake_client)

    generate_timeline(FAKE_SHOTS)

    fake_client.models.generate_content.assert_called_once()
    call_kwargs = fake_client.models.generate_content.call_args.kwargs
    assert call_kwargs["model"] == "gemini-2.5-flash"
    assert "sceneSlug" in call_kwargs["contents"]
    assert call_kwargs["config"].response_mime_type == "application/json"
    assert call_kwargs["config"].response_schema is Timeline
    assert "월터 머치" in call_kwargs["config"].system_instruction


def test_validate_timeline_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        validate_timeline(None)
