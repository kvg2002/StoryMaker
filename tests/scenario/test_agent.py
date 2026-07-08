import pytest

from agents.scenario.agent import generate_scenario


def test_generate_scenario_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        generate_scenario("겁쟁이가 용을 잡아야 한다")
