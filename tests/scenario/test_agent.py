from unittest.mock import MagicMock

from agents.scenario.agent import generate_scenario
from agents.scenario.schemas import ScenarioOutput


def test_generate_scenario_returns_scene_script_from_gemini_response(monkeypatch) -> None:
    fake_response = MagicMock(text="INT. 낡은 극장 - 밤\n\n지우가 소품 상자를 뒤진다.")
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response
    monkeypatch.setattr("agents.scenario.agent.get_gemini_client", lambda: fake_client)

    result = generate_scenario("겁쟁이가 용을 잡아야 한다")

    assert isinstance(result, ScenarioOutput)
    assert result.scene_script == fake_response.text


def test_generate_scenario_calls_gemini_with_logline_and_training_doc(monkeypatch) -> None:
    fake_response = MagicMock(text="INT. 낡은 극장 - 밤\n\n지우가 소품 상자를 뒤진다.")
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response
    monkeypatch.setattr("agents.scenario.agent.get_gemini_client", lambda: fake_client)

    generate_scenario("겁쟁이가 용을 잡아야 한다")

    fake_client.models.generate_content.assert_called_once()
    call_kwargs = fake_client.models.generate_content.call_args.kwargs
    assert call_kwargs["model"] == "gemini-2.5-flash"
    assert call_kwargs["contents"] == "겁쟁이가 용을 잡아야 한다"
    system_instruction = call_kwargs["config"].system_instruction
    assert "Save the Cat" in system_instruction
