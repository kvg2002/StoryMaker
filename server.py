"""StoryMaker FastAPI 백엔드: 팀원이 만든 정적 프론트(index.html/style.css/script.js)를
서빙하고, 3단계 파이프라인을 REST API로 노출한다.

실행: uv run uvicorn server:app --reload
"""
from dotenv import load_dotenv

load_dotenv()

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agents.scenario.agent import generate_scenario
from agents.scenario.schemas import ScenarioOutput
from agents.storyboard.agent import generate_storyboard
from agents.storyboard.docx_export import shot_notation
from agents.storyboard.image_gen import generate_contact_sheets
from agents.storyboard.schemas import Shot, StoryboardOutput
from pipeline.run_pipeline import OUTPUTS_ROOT, finalize_from_storyboard, slugify_logline

OUTPUTS_ROOT.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="StoryMaker API")


# ── 프론트 정적 파일 서빙 ──────────────────────────────────────────────
@app.get("/")
def serve_index() -> FileResponse:
    return FileResponse("index.html")


@app.get("/style.css")
def serve_style() -> FileResponse:
    return FileResponse("style.css")


@app.get("/script.js")
def serve_script() -> FileResponse:
    return FileResponse("script.js")


app.mount("/outputs", StaticFiles(directory=str(OUTPUTS_ROOT)), name="outputs")


# ── 프로젝트 아카이브 (새로고침해도 토큰 낭비 없이 이전 결과를 다시 불러오기) ──
def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ── 1단계: 시나리오 ──────────────────────────────────────────────────
class ScenarioRequest(BaseModel):
    title: str = ""
    length: str = ""
    genre: str = ""
    audience: list[str] = []
    tone: list[str] = []
    logline: str


class ScenarioResponse(BaseModel):
    scene_script: str
    project_slug: str


def _compose_scenario_input(req: ScenarioRequest) -> str:
    lines = ["[기획 정보]"]
    if req.title:
        lines.append(f"제목: {req.title}")
    if req.length:
        lines.append(f"길이: {req.length}")
    if req.genre:
        lines.append(f"장르: {req.genre}")
    if req.audience:
        lines.append(f"타겟 관객: {', '.join(req.audience)}")
    if req.tone:
        lines.append(f"이야기 톤: {', '.join(req.tone)}")
    lines.append("")
    lines.append("[로그라인]")
    lines.append(req.logline)
    return "\n".join(lines)


@app.post("/api/scenario", response_model=ScenarioResponse)
def api_scenario(req: ScenarioRequest) -> ScenarioResponse:
    scenario = generate_scenario(_compose_scenario_input(req))
    project_slug = slugify_logline(req.title or req.logline)

    _write_json(
        OUTPUTS_ROOT / project_slug / "scenario.json",
        {"title": req.title, "logline": req.logline, "scene_script": scenario.scene_script},
    )

    return ScenarioResponse(scene_script=scenario.scene_script, project_slug=project_slug)


# ── 2단계: 스토리보드 ────────────────────────────────────────────────
class StoryboardRequest(BaseModel):
    scene_script: str
    project_slug: str
    shot_count: str = ""
    camera_style: str = ""


class ShotOut(Shot):
    image_url: str | None = None
    notation: str = ""


class StoryboardResponse(BaseModel):
    shots: list[ShotOut]
    image_failures: list[str]


def _compose_storyboard_input(req: StoryboardRequest) -> str:
    lines = [req.scene_script, "", "[스토리보드 제작 노트]"]
    if req.shot_count:
        lines.append(f"샷 개수: {req.shot_count}")
    if req.camera_style:
        lines.append(f"카메라 스타일: {req.camera_style}")
    return "\n".join(lines)


@app.post("/api/storyboard", response_model=StoryboardResponse)
def api_storyboard(req: StoryboardRequest) -> StoryboardResponse:
    storyboard = generate_storyboard(_compose_storyboard_input(req))
    images_dir = OUTPUTS_ROOT / req.project_slug / "images"
    image_failures = generate_contact_sheets(storyboard.shots, images_dir)

    shots_out = []
    for i, shot in enumerate(storyboard.shots, start=1):
        image_path = images_dir / f"cut{i}.png"
        image_url = (
            f"/outputs/{req.project_slug}/images/cut{i}.png" if image_path.exists() else None
        )
        shots_out.append(
            ShotOut(**shot.model_dump(), image_url=image_url, notation=shot_notation(shot))
        )

    _write_json(
        OUTPUTS_ROOT / req.project_slug / "storyboard.json",
        {
            "shots": [s.model_dump() for s in shots_out],
            "image_failures": image_failures,
        },
    )

    return StoryboardResponse(shots=shots_out, image_failures=image_failures)


# ── 3단계: 애니매틱 ──────────────────────────────────────────────────
class AnimaticRequest(BaseModel):
    scene_script: str
    project_slug: str
    shots: list[Shot]


class AnimaticResponse(BaseModel):
    docx_url: str | None
    video_url: str | None
    validation_flags: list[str]
    image_failures: list[str]


@app.post("/api/animatic", response_model=AnimaticResponse)
def api_animatic(req: AnimaticRequest) -> AnimaticResponse:
    scenario = ScenarioOutput(scene_script=req.scene_script)
    storyboard = StoryboardOutput(shots=req.shots)
    project_dir = OUTPUTS_ROOT / req.project_slug
    result = finalize_from_storyboard(scenario, storyboard, project_dir)

    docx_url = (
        f"/outputs/{req.project_slug}/storyboard.docx" if result.docx_path.exists() else None
    )
    video_url = (
        f"/outputs/{req.project_slug}/animatic.mp4" if result.video_path is not None else None
    )

    _write_json(
        project_dir / "animatic.json",
        {"validation_flags": result.validation_flags, "image_failures": result.image_failures},
    )

    return AnimaticResponse(
        docx_url=docx_url,
        video_url=video_url,
        validation_flags=result.validation_flags,
        image_failures=result.image_failures,
    )


# ── 프로젝트 목록/불러오기 ───────────────────────────────────────────
class ProjectSummary(BaseModel):
    slug: str
    title: str
    updated_at: float
    has_storyboard: bool
    has_animatic: bool


class ProjectDetail(BaseModel):
    slug: str
    title: str
    scene_script: str = ""
    shots: list[ShotOut] = []
    image_failures: list[str] = []
    validation_flags: list[str] = []
    docx_url: str | None = None
    video_url: str | None = None


def _project_title(meta: dict, slug: str) -> str:
    return meta.get("title") or meta.get("logline", "")[:24] or slug


@app.get("/api/projects", response_model=list[ProjectSummary])
def api_list_projects() -> list[ProjectSummary]:
    projects = []
    for project_dir in OUTPUTS_ROOT.iterdir():
        scenario_path = project_dir / "scenario.json"
        if not project_dir.is_dir() or not scenario_path.exists():
            continue
        meta = _read_json(scenario_path)
        projects.append(
            ProjectSummary(
                slug=project_dir.name,
                title=_project_title(meta, project_dir.name),
                updated_at=scenario_path.stat().st_mtime,
                has_storyboard=(project_dir / "storyboard.json").exists(),
                has_animatic=(project_dir / "animatic.mp4").exists(),
            )
        )
    projects.sort(key=lambda p: p.updated_at, reverse=True)
    return projects


@app.get("/api/projects/{slug}", response_model=ProjectDetail)
def api_get_project(slug: str) -> ProjectDetail:
    project_dir = OUTPUTS_ROOT / slug
    scenario_path = project_dir / "scenario.json"
    if not scenario_path.exists():
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다.")

    scenario_meta = _read_json(scenario_path)
    detail = ProjectDetail(
        slug=slug,
        title=_project_title(scenario_meta, slug),
        scene_script=scenario_meta.get("scene_script", ""),
    )

    storyboard_path = project_dir / "storyboard.json"
    if storyboard_path.exists():
        storyboard_meta = _read_json(storyboard_path)
        detail.shots = [ShotOut(**s) for s in storyboard_meta.get("shots", [])]
        detail.image_failures = storyboard_meta.get("image_failures", [])

    if (project_dir / "storyboard.docx").exists():
        detail.docx_url = f"/outputs/{slug}/storyboard.docx"

    if (project_dir / "animatic.mp4").exists():
        detail.video_url = f"/outputs/{slug}/animatic.mp4"

    animatic_path = project_dir / "animatic.json"
    if animatic_path.exists():
        detail.validation_flags = _read_json(animatic_path).get("validation_flags", [])

    return detail
