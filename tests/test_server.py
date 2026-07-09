import json
import os

from fastapi.testclient import TestClient

import server
from agents.animatic.schemas import Timeline
from agents.scenario.schemas import ScenarioOutput
from agents.storyboard.schemas import Shot, StoryboardOutput
from pipeline.run_pipeline import PipelineResult

client = TestClient(server.app)

FAKE_SHOT_KWARGS = dict(
    size="WS",
    angle="eye-level",
    movement="static",
    duration=3,
    description="낡은 극장 무대 위, 지우가 소품 상자를 뒤진다",
    dialogue="",
    audio="",
    sceneSlug="S1",
)


def test_index_serves_frontend_html() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "StoryMaker" in response.text


def test_api_scenario_returns_scene_script_and_project_slug(tmp_path, monkeypatch) -> None:
    fake_scenario = ScenarioOutput(scene_script="INT. 낡은 극장 - 밤\n\n지우가 대본을 꺼낸다.")
    monkeypatch.setattr(server, "generate_scenario", lambda text: fake_scenario)
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)

    response = client.post(
        "/api/scenario", json={"logline": "겁쟁이가 용을 잡아야 한다", "title": "테스트"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["scene_script"] == fake_scenario.scene_script
    assert data["project_slug"]


def test_api_scenario_composes_all_form_fields_into_input(tmp_path, monkeypatch) -> None:
    captured = {}

    def fake_generate(text: str) -> ScenarioOutput:
        captured["text"] = text
        return ScenarioOutput(scene_script="...")

    monkeypatch.setattr(server, "generate_scenario", fake_generate)
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)

    client.post(
        "/api/scenario",
        json={
            "logline": "로그라인입니다",
            "title": "제목입니다",
            "genre": "성장기",
            "audience": ["청소년"],
            "tone": ["감성적"],
            "length": "10분내외 단편",
        },
    )

    text = captured["text"]
    assert "로그라인입니다" in text
    assert "제목입니다" in text
    assert "성장기" in text
    assert "청소년" in text
    assert "감성적" in text
    assert "10분내외 단편" in text


def test_api_storyboard_returns_image_url_when_image_exists(tmp_path, monkeypatch) -> None:
    fake_storyboard = StoryboardOutput(shots=[Shot(**FAKE_SHOT_KWARGS)])
    monkeypatch.setattr(server, "generate_storyboard", lambda text: fake_storyboard)
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)

    def fake_gcs(shots, output_dir):
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "cut1.png").write_bytes(b"fake-png")
        return []

    monkeypatch.setattr(server, "generate_contact_sheets", fake_gcs)

    response = client.post(
        "/api/storyboard", json={"scene_script": "...", "project_slug": "test-project"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["shots"]) == 1
    assert data["shots"][0]["image_url"] == "/outputs/test-project/images/cut1.png"
    assert data["shots"][0]["sceneSlug"] == "S1"
    assert data["image_failures"] == []


def test_api_storyboard_returns_null_image_url_when_generation_failed(tmp_path, monkeypatch) -> None:
    fake_storyboard = StoryboardOutput(shots=[Shot(**FAKE_SHOT_KWARGS)])
    monkeypatch.setattr(server, "generate_storyboard", lambda text: fake_storyboard)
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)
    monkeypatch.setattr(
        server,
        "generate_contact_sheets",
        lambda shots, output_dir: ["cut1.png 생성 실패: quota exceeded"],
    )

    response = client.post(
        "/api/storyboard", json={"scene_script": "...", "project_slug": "test-project"}
    )

    data = response.json()
    assert data["shots"][0]["image_url"] is None
    assert data["image_failures"] == ["cut1.png 생성 실패: quota exceeded"]


def test_api_storyboard_includes_team_notation_matching_docx_format(tmp_path, monkeypatch) -> None:
    shot_kwargs = dict(FAKE_SHOT_KWARGS)
    shot_kwargs.update(size="fs", angle="overhead", movement="zoom-in")
    fake_storyboard = StoryboardOutput(shots=[Shot(**shot_kwargs)])
    monkeypatch.setattr(server, "generate_storyboard", lambda text: fake_storyboard)
    monkeypatch.setattr(server, "generate_contact_sheets", lambda shots, output_dir: [])
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)

    response = client.post(
        "/api/storyboard", json={"scene_script": "...", "project_slug": "notation-test"}
    )

    data = response.json()
    assert data["shots"][0]["notation"] == "FS, Top Angle, Zoom In"


def test_api_storyboard_composes_shot_count_and_camera_style_into_input(tmp_path, monkeypatch) -> None:
    captured = {}

    def fake_generate(text: str) -> StoryboardOutput:
        captured["text"] = text
        return StoryboardOutput(shots=[])

    monkeypatch.setattr(server, "generate_storyboard", fake_generate)
    monkeypatch.setattr(server, "generate_contact_sheets", lambda shots, output_dir: [])
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)

    client.post(
        "/api/storyboard",
        json={
            "scene_script": "씬 대본 원문",
            "project_slug": "test-project",
            "shot_count": "12컷",
            "camera_style": "액션",
        },
    )

    text = captured["text"]
    assert "씬 대본 원문" in text
    assert "12컷" in text
    assert "액션" in text


def test_api_animatic_returns_docx_and_video_urls(tmp_path, monkeypatch) -> None:
    project_dir = tmp_path / "test-project"
    docx_path = project_dir / "storyboard.docx"
    video_path = project_dir / "animatic.mp4"
    project_dir.mkdir(parents=True)
    docx_path.write_bytes(b"fake docx")
    video_path.write_bytes(b"fake mp4")

    fake_timeline = Timeline(project="t", fps=24, resolution="1280x720", cuts=[])
    fake_result = PipelineResult(
        project_dir=project_dir,
        scenario=ScenarioOutput(scene_script="s"),
        storyboard=StoryboardOutput(shots=[]),
        timeline=fake_timeline,
        validation_flags=["flag1"],
        image_failures=[],
        docx_path=docx_path,
        video_path=video_path,
    )
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)
    monkeypatch.setattr(
        server,
        "finalize_from_storyboard",
        lambda scenario, storyboard, project_dir: fake_result,
    )

    response = client.post(
        "/api/animatic",
        json={"scene_script": "s", "project_slug": "test-project", "shots": []},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["docx_url"] == "/outputs/test-project/storyboard.docx"
    assert data["video_url"] == "/outputs/test-project/animatic.mp4"
    assert data["validation_flags"] == ["flag1"]
    assert data["image_failures"] == []


def test_api_animatic_returns_null_video_url_when_rendering_failed(tmp_path, monkeypatch) -> None:
    project_dir = tmp_path / "test-project"
    docx_path = project_dir / "storyboard.docx"
    project_dir.mkdir(parents=True)
    docx_path.write_bytes(b"fake docx")

    fake_timeline = Timeline(project="t", fps=24, resolution="1280x720", cuts=[])
    fake_result = PipelineResult(
        project_dir=project_dir,
        scenario=ScenarioOutput(scene_script="s"),
        storyboard=StoryboardOutput(shots=[]),
        timeline=fake_timeline,
        validation_flags=[],
        image_failures=[],
        docx_path=docx_path,
        video_path=None,
    )
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)
    monkeypatch.setattr(
        server,
        "finalize_from_storyboard",
        lambda scenario, storyboard, project_dir: fake_result,
    )

    response = client.post(
        "/api/animatic",
        json={"scene_script": "s", "project_slug": "test-project", "shots": []},
    )

    data = response.json()
    assert data["video_url"] is None


def test_api_scenario_persists_scenario_json(tmp_path, monkeypatch) -> None:
    fake_scenario = ScenarioOutput(scene_script="INT. 낡은 극장 - 밤")
    monkeypatch.setattr(server, "generate_scenario", lambda text: fake_scenario)
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)

    response = client.post(
        "/api/scenario", json={"logline": "겁쟁이가 용을 잡아야 한다", "title": "겁쟁이 용사"}
    )
    project_slug = response.json()["project_slug"]

    saved = json.loads((tmp_path / project_slug / "scenario.json").read_text(encoding="utf-8"))
    assert saved["title"] == "겁쟁이 용사"
    assert saved["logline"] == "겁쟁이가 용을 잡아야 한다"
    assert saved["scene_script"] == fake_scenario.scene_script


def test_api_storyboard_persists_storyboard_json(tmp_path, monkeypatch) -> None:
    fake_storyboard = StoryboardOutput(shots=[Shot(**FAKE_SHOT_KWARGS)])
    monkeypatch.setattr(server, "generate_storyboard", lambda text: fake_storyboard)
    monkeypatch.setattr(server, "generate_contact_sheets", lambda shots, output_dir: [])
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)

    client.post("/api/storyboard", json={"scene_script": "...", "project_slug": "persist-test"})

    saved = json.loads((tmp_path / "persist-test" / "storyboard.json").read_text(encoding="utf-8"))
    assert len(saved["shots"]) == 1
    assert saved["shots"][0]["sceneSlug"] == "S1"
    assert saved["image_failures"] == []


def test_api_animatic_persists_animatic_json(tmp_path, monkeypatch) -> None:
    project_dir = tmp_path / "persist-test"
    project_dir.mkdir(parents=True)
    fake_timeline = Timeline(project="t", fps=24, resolution="1280x720", cuts=[])
    fake_result = PipelineResult(
        project_dir=project_dir,
        scenario=ScenarioOutput(scene_script="s"),
        storyboard=StoryboardOutput(shots=[]),
        timeline=fake_timeline,
        validation_flags=["flag1"],
        image_failures=["fail1"],
        docx_path=project_dir / "storyboard.docx",
        video_path=None,
    )
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)
    monkeypatch.setattr(
        server,
        "finalize_from_storyboard",
        lambda scenario, storyboard, project_dir: fake_result,
    )

    client.post(
        "/api/animatic",
        json={"scene_script": "s", "project_slug": "persist-test", "shots": []},
    )

    saved = json.loads((project_dir / "animatic.json").read_text(encoding="utf-8"))
    assert saved["validation_flags"] == ["flag1"]
    assert saved["image_failures"] == ["fail1"]


def test_list_projects_returns_saved_projects_sorted_by_recency(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)

    older = tmp_path / "older-project"
    older.mkdir()
    (older / "scenario.json").write_text(
        json.dumps({"title": "오래된 프로젝트", "logline": "l1", "scene_script": "s1"}),
        encoding="utf-8",
    )

    newer = tmp_path / "newer-project"
    newer.mkdir()
    (newer / "scenario.json").write_text(
        json.dumps({"title": "새 프로젝트", "logline": "l2", "scene_script": "s2"}),
        encoding="utf-8",
    )
    (newer / "storyboard.json").write_text(json.dumps({"shots": [], "image_failures": []}))
    os.utime(older / "scenario.json", (1000, 1000))
    os.utime(newer / "scenario.json", (2000, 2000))

    response = client.get("/api/projects")

    assert response.status_code == 200
    data = response.json()
    assert [p["slug"] for p in data] == ["newer-project", "older-project"]
    assert data[0]["title"] == "새 프로젝트"
    assert data[0]["has_storyboard"] is True
    assert data[1]["has_storyboard"] is False


def test_list_projects_excludes_dirs_without_scenario_json(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)
    (tmp_path / "incomplete-project").mkdir()

    response = client.get("/api/projects")

    assert response.json() == []


def test_get_project_returns_full_saved_state(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)
    project_dir = tmp_path / "full-project"
    project_dir.mkdir()
    (project_dir / "scenario.json").write_text(
        json.dumps({"title": "완성 프로젝트", "logline": "l", "scene_script": "씬 대본"}),
        encoding="utf-8",
    )
    (project_dir / "storyboard.json").write_text(
        json.dumps({"shots": [{**FAKE_SHOT_KWARGS, "image_url": None, "notation": "WS"}], "image_failures": []})
    )
    (project_dir / "animatic.json").write_text(
        json.dumps({"validation_flags": ["경고1"], "image_failures": []})
    )
    (project_dir / "storyboard.docx").write_bytes(b"fake docx")
    (project_dir / "animatic.mp4").write_bytes(b"fake mp4")

    response = client.get("/api/projects/full-project")

    assert response.status_code == 200
    data = response.json()
    assert data["scene_script"] == "씬 대본"
    assert len(data["shots"]) == 1
    assert data["validation_flags"] == ["경고1"]
    assert data["docx_url"] == "/outputs/full-project/storyboard.docx"
    assert data["video_url"] == "/outputs/full-project/animatic.mp4"


def test_get_project_404_for_unknown_slug(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(server, "OUTPUTS_ROOT", tmp_path)

    response = client.get("/api/projects/does-not-exist")

    assert response.status_code == 404
