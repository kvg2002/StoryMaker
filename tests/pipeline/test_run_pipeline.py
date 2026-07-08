from agents.animatic.schemas import Cut, Motion, Overlays, Timeline
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
            overlays=Overlays(info="CUT 1 | WS", caption="지우가 대본을 꺼낸다", audio_note=""),
            flags=[],
        )
    ],
)


def test_run_chains_all_three_stages_and_returns_the_timeline(monkeypatch) -> None:
    monkeypatch.setattr(
        "pipeline.run_pipeline.generate_scenario", lambda logline: FAKE_SCENARIO
    )
    monkeypatch.setattr(
        "pipeline.run_pipeline.generate_storyboard",
        lambda scene_script: FAKE_STORYBOARD,
    )
    monkeypatch.setattr(
        "pipeline.run_pipeline.generate_timeline", lambda shots: FAKE_TIMELINE
    )

    result = run("겁쟁이가 용을 잡아야 한다")

    assert result == FAKE_TIMELINE
