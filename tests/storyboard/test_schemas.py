import pytest
from pydantic import ValidationError

from agents.storyboard.schemas import Shot, StoryboardOutput

VALID_SHOT_KWARGS = dict(
    size="MS",
    angle="eye-level",
    movement="static",
    duration=4,
    description="지우가 대본을 꺼내 표지를 쓸어본다",
    dialogue="아직 여기 있었네.",
    audio="",
    sceneSlug="S1",
)


def test_shot_accepts_all_required_fields() -> None:
    shot = Shot(**VALID_SHOT_KWARGS)
    assert shot.sceneSlug == "S1"
    assert shot.duration == 4


def test_shot_missing_scene_slug_fails() -> None:
    kwargs = {k: v for k, v in VALID_SHOT_KWARGS.items() if k != "sceneSlug"}
    with pytest.raises(ValidationError):
        Shot(**kwargs)


def test_storyboard_output_holds_list_of_shots() -> None:
    output = StoryboardOutput(shots=[Shot(**VALID_SHOT_KWARGS)])
    assert len(output.shots) == 1
