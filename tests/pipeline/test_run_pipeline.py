from agents.animatic.schemas import Cut, Motion, Overlays, Timeline
from agents.scenario.schemas import ScenarioOutput
from agents.storyboard.schemas import Shot, StoryboardOutput
from pipeline.run_pipeline import (
    PipelineResult,
    finalize_from_storyboard,
    run,
    run_from_storyboard,
)

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


def _patch_all_stages(monkeypatch, *, image_failures=None, validation_flags=None, render_error=None):
    monkeypatch.setattr("pipeline.run_pipeline.generate_scenario", lambda logline: FAKE_SCENARIO)
    monkeypatch.setattr(
        "pipeline.run_pipeline.generate_storyboard", lambda scene_script: FAKE_STORYBOARD
    )
    monkeypatch.setattr(
        "pipeline.run_pipeline.generate_contact_sheets",
        lambda shots, output_dir: image_failures or [],
    )
    monkeypatch.setattr("pipeline.run_pipeline.generate_timeline", lambda shots: FAKE_TIMELINE)
    monkeypatch.setattr(
        "pipeline.run_pipeline.validate_timeline", lambda timeline: validation_flags or []
    )
    monkeypatch.setattr("pipeline.run_pipeline.export_docx", lambda storyboard, path, images_dir: None)

    def fake_render(timeline_path, output_path, cwd):
        if render_error:
            raise render_error

    monkeypatch.setattr("pipeline.run_pipeline.render_animatic", fake_render)


def test_run_returns_pipeline_result_with_all_stage_outputs(tmp_path, monkeypatch) -> None:
    _patch_all_stages(monkeypatch)

    result = run("겁쟁이가 용을 잡아야 한다", project_dir=tmp_path)

    assert isinstance(result, PipelineResult)
    assert result.scenario == FAKE_SCENARIO
    assert result.storyboard == FAKE_STORYBOARD
    assert result.timeline == FAKE_TIMELINE
    assert result.validation_flags == []
    assert result.image_failures == []
    assert result.project_dir == tmp_path
    assert result.docx_path == tmp_path / "storyboard.docx"
    assert result.video_path == tmp_path / "animatic.mp4"


def test_run_collects_image_failures_and_validation_flags(tmp_path, monkeypatch) -> None:
    _patch_all_stages(
        monkeypatch,
        image_failures=["cut1.png 생성 실패: quota exceeded"],
        validation_flags=["컷 1: 대사 길이 부족"],
    )

    result = run("겁쟁이가 용을 잡아야 한다", project_dir=tmp_path)

    assert result.image_failures == ["cut1.png 생성 실패: quota exceeded"]
    assert result.validation_flags == ["컷 1: 대사 길이 부족"]


def test_run_sets_video_path_to_none_when_rendering_fails(tmp_path, monkeypatch) -> None:
    _patch_all_stages(monkeypatch, render_error=RuntimeError("ffmpeg not found"))

    result = run("겁쟁이가 용을 잡아야 한다", project_dir=tmp_path)

    assert result.video_path is None
    # 렌더링 실패해도 나머지 산출물은 정상 반환
    assert result.docx_path == tmp_path / "storyboard.docx"


def test_run_derives_project_dir_from_logline_when_not_given(monkeypatch) -> None:
    _patch_all_stages(monkeypatch)

    result = run("겁쟁이가 용을 잡아야 한다")

    assert result.project_dir.parent.name == "outputs"


def test_run_from_storyboard_does_not_regenerate_scenario_or_storyboard(tmp_path, monkeypatch) -> None:
    _patch_all_stages(monkeypatch)
    monkeypatch.setattr(
        "pipeline.run_pipeline.generate_scenario",
        lambda logline: (_ for _ in ()).throw(AssertionError("should not regenerate scenario")),
    )
    monkeypatch.setattr(
        "pipeline.run_pipeline.generate_storyboard",
        lambda scene_script: (_ for _ in ()).throw(AssertionError("should not regenerate storyboard")),
    )

    edited_scenario = ScenarioOutput(scene_script="사용자가 직접 수정한 씬 대본")
    edited_storyboard = StoryboardOutput(
        shots=[
            Shot(
                size="CU",
                angle="high",
                movement="static",
                duration=2,
                description="사용자가 수정한 샷 설명",
                dialogue="",
                audio="",
                sceneSlug="S1",
            )
        ]
    )

    result = run_from_storyboard(edited_scenario, edited_storyboard, tmp_path)

    assert result.scenario == edited_scenario
    assert result.storyboard == edited_storyboard
    assert result.project_dir == tmp_path
    assert result.docx_path == tmp_path / "storyboard.docx"


def test_finalize_from_storyboard_does_not_regenerate_images(tmp_path, monkeypatch) -> None:
    _patch_all_stages(monkeypatch)
    monkeypatch.setattr(
        "pipeline.run_pipeline.generate_contact_sheets",
        lambda shots, output_dir: (_ for _ in ()).throw(AssertionError("should not regenerate images")),
    )

    result = finalize_from_storyboard(
        FAKE_SCENARIO, FAKE_STORYBOARD, tmp_path, image_failures=["이미 기록된 실패"]
    )

    assert result.image_failures == ["이미 기록된 실패"]
    assert result.timeline == FAKE_TIMELINE
    assert result.docx_path == tmp_path / "storyboard.docx"


def test_finalize_from_storyboard_defaults_image_failures_to_empty_list(tmp_path, monkeypatch) -> None:
    _patch_all_stages(monkeypatch)
    monkeypatch.setattr(
        "pipeline.run_pipeline.generate_contact_sheets",
        lambda shots, output_dir: (_ for _ in ()).throw(AssertionError("should not regenerate images")),
    )

    result = finalize_from_storyboard(FAKE_SCENARIO, FAKE_STORYBOARD, tmp_path)

    assert result.image_failures == []
