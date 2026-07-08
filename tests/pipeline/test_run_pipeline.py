import pytest

from agents.scenario.schemas import ScenarioOutput
from pipeline.run_pipeline import run


def test_run_propagates_not_implemented_from_storyboard_stage(monkeypatch) -> None:
    monkeypatch.setattr(
        "pipeline.run_pipeline.generate_scenario",
        lambda logline: ScenarioOutput(scene_script="INT. 낡은 극장 - 밤\n\n지우가 대본을 꺼낸다."),
    )

    with pytest.raises(NotImplementedError):
        run("겁쟁이가 용을 잡아야 한다")
