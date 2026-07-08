import pytest
from pydantic import ValidationError

from agents.animatic.schemas import Cut, Motion, Overlays, TitleCard, Timeline

VALID_CUT_KWARGS = dict(
    cut=1,
    image="cut1.png",
    duration=4.0,
    duration_rationale="FS(+1.0)+기본(1.0)+자막판독, 대사없음",
    motion=Motion(type="static"),
    transition_out="cut",
    overlays=Overlays(
        info="CUT 1 | FS, Top Angle",
        caption="이순신이 절뚝거리며 걸음",
        audio_note="새소리, 저벅저벅",
    ),
    flags=[],
)


def test_cut_accepts_all_required_fields() -> None:
    cut = Cut(**VALID_CUT_KWARGS)
    assert cut.motion.type == "static"
    assert cut.overlays.caption == "이순신이 절뚝거리며 걸음"


def test_cut_missing_duration_rationale_fails() -> None:
    kwargs = {k: v for k, v in VALID_CUT_KWARGS.items() if k != "duration_rationale"}
    with pytest.raises(ValidationError):
        Cut(**kwargs)


def test_title_card_holds_text_and_duration() -> None:
    card = TitleCard(title_card="S#3. EXT. 활터 - 낮", duration=1.5)
    assert card.duration == 1.5


def test_timeline_holds_mixed_cuts_and_title_cards() -> None:
    timeline = Timeline(
        project="테스트 프로젝트",
        fps=24,
        resolution="1280x720",
        cuts=[
            TitleCard(title_card="S#3. EXT. 활터 - 낮", duration=1.5),
            Cut(**VALID_CUT_KWARGS),
        ],
    )
    assert len(timeline.cuts) == 2
