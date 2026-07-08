from agents.animatic.schemas import Cut, Motion, Overlays, TitleCard, Timeline
from agents.animatic.validators import validate_timeline


def _cut(**overrides) -> Cut:
    defaults = dict(
        cut=1,
        image="cut1.png",
        duration=4.0,
        duration_rationale="",
        motion=Motion(type="static"),
        transition_out="cut",
        overlays=Overlays(info="", caption="", audio_note=""),
        flags=[],
    )
    defaults.update(overrides)
    return Cut(**defaults)


def _timeline(cuts) -> Timeline:
    return Timeline(project="테스트", fps=24, resolution="1280x720", cuts=cuts)


def test_total_length_within_target_produces_no_flag() -> None:
    timeline = _timeline([_cut(duration=10.0)])

    flags = validate_timeline(timeline, target_runtime_seconds=10.0)

    assert flags == []


def test_total_length_outside_target_is_flagged() -> None:
    timeline = _timeline([_cut(duration=100.0)])

    flags = validate_timeline(timeline, target_runtime_seconds=10.0)

    assert any("총 길이" in f for f in flags)


def test_no_target_runtime_skips_total_length_check() -> None:
    timeline = _timeline([_cut(duration=1000.0)])

    flags = validate_timeline(timeline)

    assert not any("총 길이" in f for f in flags)


def test_dialogue_cut_too_short_is_auto_raised_and_flagged() -> None:
    # "아직 여기 있었네" = 7 음절 -> 7/5.5 + 0.8 ≈ 2.07초 필요
    cut = _cut(duration=1.0, overlays=Overlays(info="", caption='"아직 여기 있었네"', audio_note=""))
    timeline = _timeline([cut])

    flags = validate_timeline(timeline)

    assert timeline.cuts[0].duration > 2.0
    assert any("대사" in f for f in flags)


def test_dialogue_cut_already_long_enough_is_untouched() -> None:
    cut = _cut(duration=5.0, overlays=Overlays(info="", caption='"아직 여기 있었네"', audio_note=""))
    timeline = _timeline([cut])

    flags = validate_timeline(timeline)

    assert timeline.cuts[0].duration == 5.0
    assert not any("대사" in f for f in flags)


def test_caption_too_long_for_duration_is_flagged() -> None:
    long_caption = "이것은 아주 길고 자세한 상황 설명 자막으로 화면 안에서 다 읽기 어려울 수 있다"
    cut = _cut(duration=1.0, overlays=Overlays(info="", caption=long_caption, audio_note=""))
    timeline = _timeline([cut])

    flags = validate_timeline(timeline)

    assert any("자막" in f for f in flags)


def test_three_consecutive_equal_durations_is_flagged() -> None:
    timeline = _timeline([_cut(duration=2.0), _cut(duration=2.0), _cut(duration=2.0)])

    flags = validate_timeline(timeline)

    assert any("동일 길이" in f for f in flags)


def test_two_consecutive_equal_durations_is_not_flagged() -> None:
    timeline = _timeline([_cut(duration=2.0), _cut(duration=2.0), _cut(duration=3.0)])

    flags = validate_timeline(timeline)

    assert not any("동일 길이" in f for f in flags)


def test_dissolve_inside_scene_is_forced_to_cut_and_flagged() -> None:
    timeline = _timeline([_cut(transition_out="dissolve"), _cut()])

    flags = validate_timeline(timeline)

    assert timeline.cuts[0].transition_out == "cut"
    assert any("전환" in f for f in flags)


def test_dissolve_at_scene_boundary_before_title_card_is_allowed() -> None:
    timeline = _timeline(
        [_cut(transition_out="dissolve"), TitleCard(title_card="S#2", duration=1.5), _cut()]
    )

    flags = validate_timeline(timeline)

    assert timeline.cuts[0].transition_out == "dissolve"
    assert not any("전환" in f for f in flags)
