from unittest.mock import MagicMock

from agents.storyboard.agent import generate_storyboard
from agents.storyboard.schemas import Shot, StoryboardOutput

FAKE_STORYBOARD = StoryboardOutput(
    shots=[
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
)


def test_generate_storyboard_returns_shots_from_gemini_response(monkeypatch) -> None:
    fake_response = MagicMock(parsed=FAKE_STORYBOARD)
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response
    monkeypatch.setattr("agents.storyboard.agent.get_gemini_client", lambda: fake_client)

    result = generate_storyboard("INT. 낡은 극장 - 밤\n\n지우가 소품 상자를 뒤진다.")

    assert result == FAKE_STORYBOARD


def test_generate_storyboard_calls_gemini_with_scene_script_and_json_schema(monkeypatch) -> None:
    fake_response = MagicMock(parsed=FAKE_STORYBOARD)
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response
    monkeypatch.setattr("agents.storyboard.agent.get_gemini_client", lambda: fake_client)

    generate_storyboard("INT. 낡은 극장 - 밤\n\n지우가 소품 상자를 뒤진다.")

    fake_client.models.generate_content.assert_called_once()
    call_kwargs = fake_client.models.generate_content.call_args.kwargs
    assert call_kwargs["model"] == "gemini-2.5-flash"
    assert call_kwargs["contents"] == "INT. 낡은 극장 - 밤\n\n지우가 소품 상자를 뒤진다."
    assert call_kwargs["config"].response_mime_type == "application/json"
    assert call_kwargs["config"].response_schema is StoryboardOutput
    assert "샷 사이즈" in call_kwargs["config"].system_instruction
