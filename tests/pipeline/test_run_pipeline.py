import pytest

from agents.scenario.schemas import ScenarioOutput
from agents.storyboard.schemas import Shot, StoryboardOutput
from pipeline.run_pipeline import run

FAKE_SCENARIO = ScenarioOutput(scene_script="INT. 낡은 극장 - 밤\n\n지우가 대본을 꺼낸다.")
FAKE_STORYBOARD = StoryboardOutput(
    shots=[
        Shot(
            size="WS",
            angle="eye-level",
            movement="static",
            duration=3,
            description="낡은 극장 무대 위, 지우가 대본을 꺼낸다",
            dialogue="",
            audio="",
            sceneSlug="S1",
        )
    ]
)


def test_run_propagates_not_implemented_from_animatic_stage(monkeypatch) -> None:
    monkeypatch.setattr(
        "pipeline.run_pipeline.generate_scenario", lambda logline: FAKE_SCENARIO
    )
    monkeypatch.setattr(
        "pipeline.run_pipeline.generate_storyboard",
        lambda scene_script: FAKE_STORYBOARD,
    )

    with pytest.raises(NotImplementedError):
        run("겁쟁이가 용을 잡아야 한다")
