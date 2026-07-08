import pytest
from pydantic import ValidationError

from agents.scenario.schemas import ScenarioInput, ScenarioOutput


def test_scenario_input_requires_logline() -> None:
    with pytest.raises(ValidationError):
        ScenarioInput()


def test_scenario_input_accepts_logline() -> None:
    result = ScenarioInput(logline="겁쟁이가 용을 잡아야 한다")
    assert result.logline == "겁쟁이가 용을 잡아야 한다"


def test_scenario_output_requires_scene_script() -> None:
    with pytest.raises(ValidationError):
        ScenarioOutput()
