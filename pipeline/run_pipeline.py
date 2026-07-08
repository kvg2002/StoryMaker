"""3단계 파이프라인 오케스트레이션: 시나리오 -> 스토리보드 -> 애니매틱 -> 렌더링."""
import re
from pathlib import Path

from pydantic import BaseModel

from agents.animatic.agent import generate_timeline
from agents.animatic.renderer.run_renderer import render_animatic
from agents.animatic.schemas import Timeline
from agents.animatic.validators import validate_timeline
from agents.scenario.agent import generate_scenario
from agents.scenario.schemas import ScenarioOutput
from agents.storyboard.agent import generate_storyboard
from agents.storyboard.docx_export import export_docx
from agents.storyboard.image_gen import generate_contact_sheets
from agents.storyboard.schemas import StoryboardOutput

OUTPUTS_ROOT = Path("outputs")


class PipelineResult(BaseModel):
    project_dir: Path
    scenario: ScenarioOutput
    storyboard: StoryboardOutput
    timeline: Timeline
    validation_flags: list[str]
    image_failures: list[str]
    docx_path: Path
    video_path: Path | None


def slugify_logline(logline: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z가-힣]+", "-", logline).strip("-")
    return slug[:40] or "storymaker"


def run_from_storyboard(
    scenario: ScenarioOutput, storyboard: StoryboardOutput, project_dir: Path
) -> PipelineResult:
    """스토리보드 이후 단계(이미지→타임라인→검증→docx→렌더링)만 실행한다.

    시나리오/스토리보드를 사람이 검토·수정한 뒤 이어서 진행하는 UI의 3단계 트리거가
    이 함수를 직접 호출한다 — `run()`처럼 scenario/storyboard를 새로 생성하지 않는다.
    """
    images_dir = project_dir / "images"

    image_failures = generate_contact_sheets(storyboard.shots, images_dir)

    timeline = generate_timeline(storyboard.shots)
    validation_flags = validate_timeline(timeline)

    docx_path = project_dir / "storyboard.docx"
    export_docx(storyboard, docx_path, images_dir=images_dir)

    timeline_path = images_dir / "timeline.json"
    timeline_path.parent.mkdir(parents=True, exist_ok=True)
    timeline_path.write_text(timeline.model_dump_json(indent=2), encoding="utf-8")

    video_path = project_dir / "animatic.mp4"
    try:
        render_animatic(timeline_path, video_path, cwd=images_dir)
    except Exception:
        video_path = None

    return PipelineResult(
        project_dir=project_dir,
        scenario=scenario,
        storyboard=storyboard,
        timeline=timeline,
        validation_flags=validation_flags,
        image_failures=image_failures,
        docx_path=docx_path,
        video_path=video_path,
    )


def run(logline: str, project_dir: Path | None = None) -> PipelineResult:
    if project_dir is None:
        project_dir = OUTPUTS_ROOT / slugify_logline(logline)

    scenario = generate_scenario(logline)
    storyboard = generate_storyboard(scenario.scene_script)
    return run_from_storyboard(scenario, storyboard, project_dir)
