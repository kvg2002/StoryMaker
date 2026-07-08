# StoryMaker Repo Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold the StoryMaker repository into the 3-stage agent pipeline structure (scenario/storyboard/animatic) defined in the design spec, migrate the four existing files into it, and push the result to the empty `kvg2002/StoryMaker` GitHub repo.

**Architecture:** Python single-stack, uv-managed, CLI-oriented. Each pipeline stage is an independent package under `agents/` with its own `schemas.py` (pydantic data contract), `prompts/training.md` (the existing methodology doc), and stub `agent.py`/support modules. `shared/` holds cross-stage API wrappers and IO helpers. `pipeline/run_pipeline.py` and `cli.py` wire the stages together. No real Claude/Gemini/ffmpeg logic is implemented in this plan — every function body is `raise NotImplementedError`, but every data contract (pydantic schema) is fully implemented and tested since it costs nothing to get right now and later tasks depend on the exact field names.

**Tech Stack:** Python >=3.11, uv, pydantic v2, anthropic SDK, google-genai SDK, python-docx, python-dotenv, pytest.

## Global Constraints

- Runtime: Python only (no Node/TS) — confirmed in design spec.
- Package manager: uv (`pyproject.toml` + `uv.lock`), not pip/poetry.
- Shot list JSON fields (storyboard → animatic contract) are exactly: `size`, `angle`, `movement`, `duration`, `description`, `dialogue`, `audio`, `sceneSlug` (spec §2.3, §4.6). Field names are case-sensitive and must match verbatim (`sceneSlug`, not `scene_slug`).
- Timeline JSON fields (animatic agent output) are exactly: `project`, `fps`, `resolution`, `cuts` — each cut is either a title-card object (`title_card`, `duration`) or a full cut object (`cut`, `image`, `duration`, `duration_rationale`, `motion`, `transition_out`, `overlays`, `flags`) (spec §5.5).
- Existing files must be moved (not copied/duplicated) into their new locations: `step1-scenario-training.md` → `agents/scenario/prompts/training.md`, `step2-storyboard-training.md` → `agents/storyboard/prompts/training.md`, `step3-animatic-training.md` → `agents/animatic/prompts/training.md`, `animatic_renderer.py` → `agents/animatic/renderer/animatic_renderer.py`.
- The original proposal PDF (`AI영상_프리프로덕션_파이프라인_기획서.pdf`) does not exist as a local file in this directory (confirmed via glob search) — it was only shared as a chat attachment. Do not fabricate its contents. `docs/README.md` should note where to place it if the user wants it archived.
- Remote is `https://github.com/kvg2002/StoryMaker.git`, currently empty (no refs) — plan ends with a push to `main`.
- Local git identity is already set (repo-local, not global): `user.name=kvg2002`, `user.email=edu079@wrtnedu.io`. Do not change global git config.

---

### Task 1: Project tooling scaffold (pyproject.toml, .gitignore, .env.example, README)

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `.env.example`
- Create: `README.md`
- Create: `docs/README.md`

**Interfaces:**
- Produces: a `uv sync`-able project named `storymaker`, Python `>=3.11`, with dependencies `anthropic`, `google-genai`, `pydantic`, `python-docx`, `python-dotenv`, dev dependency `pytest`. Later tasks' `import` statements (`anthropic`, `google.genai`, `pydantic`, `docx`, `dotenv`) rely on these being declared here.

- [ ] **Step 1: Write `pyproject.toml`**

```toml
[project]
name = "storymaker"
version = "0.1.0"
description = "AI 기반 영상 프리프로덕션 자동화 파이프라인 (시나리오-스토리보드-애니매틱)"
requires-python = ">=3.11"
dependencies = [
    "anthropic>=0.40.0",
    "google-genai>=0.3.0",
    "pydantic>=2.9.0",
    "python-docx>=1.1.0",
    "python-dotenv>=1.0.0",
]

[project.scripts]
storymaker = "cli:main"

[dependency-groups]
dev = [
    "pytest>=8.3.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 2: Write `.gitignore`**

```
.venv/
__pycache__/
*.pyc
outputs/
_clips/
.env
*.egg-info/
```

- [ ] **Step 3: Write `.env.example`**

```
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
```

- [ ] **Step 4: Write `README.md`**

```markdown
# StoryMaker

로그라인 한 줄에서 애니매틱 영상까지 — 시나리오 · 스토리보드 · 애니매틱 3단계 생성 에이전트 파이프라인.

## 파이프라인

1. **시나리오 에이전트** (`agents/scenario/`) — 로그라인 → 비트 시트 → 씬 리스트 → 씬 대본
2. **스토리보드 에이전트** (`agents/storyboard/`) — 씬 대본 → 샷 리스트(JSON) → 콘티 이미지 → 팀 표준 워드(.docx)
3. **애니매틱 에이전트** (`agents/animatic/`) — 샷 리스트 → 타임라인 JSON → 애니매틱 mp4 + 타임코드 시트

각 단계의 방법론 레퍼런스는 `agents/<stage>/prompts/training.md`에 있다. 전체 설계는
`docs/superpowers/specs/2026-07-08-storymaker-repo-scaffold-design.md` 참고.

## 개발 환경

```bash
uv sync
cp .env.example .env  # ANTHROPIC_API_KEY, GEMINI_API_KEY 채우기
uv run pytest
```

## 실행

```bash
uv run storymaker run "겁쟁이가 용을 잡아야 한다"
```

애니매틱 렌더링에는 시스템에 `ffmpeg`가 설치되어 있어야 한다.
```

- [ ] **Step 5: Write `docs/README.md`**

```markdown
# docs/

- `superpowers/specs/`, `superpowers/plans/` — 이 저장소 구조를 만든 설계/구현 계획 문서.
- 원본 기획서 `AI영상_프리프로덕션_파이프라인_기획서.pdf`는 로컬 파일로 존재하지 않아 이 저장소에 포함되지 않았다.
  보관하려면 이 폴더에 직접 넣을 것.
```

- [ ] **Step 6: Verify uv can resolve the project**

Run: `uv sync`
Expected: creates `.venv/` and `uv.lock`, exits 0 with no errors.

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml .gitignore .env.example README.md docs/README.md uv.lock
git commit -m "chore: scaffold project tooling (uv, gitignore, readme)"
```

---

### Task 2: `shared/io_utils.py` — JSON read/write helpers

**Files:**
- Create: `shared/__init__.py`
- Create: `shared/io_utils.py`
- Test: `tests/shared/test_io_utils.py`

**Interfaces:**
- Produces: `write_json(data: dict, path: Path) -> None`, `read_json(path: Path) -> dict`. Later tasks (agents, pipeline) will use these for persisting intermediate JSON artifacts.

- [ ] **Step 1: Write the failing test**

Create `tests/__init__.py` (empty) and `tests/shared/__init__.py` (empty) first, then:

```python
# tests/shared/test_io_utils.py
import json
from pathlib import Path

from shared.io_utils import read_json, write_json


def test_write_json_creates_parent_dirs_and_file(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "out.json"

    write_json({"a": 1}, target)

    assert target.exists()
    assert json.loads(target.read_text(encoding="utf-8")) == {"a": 1}


def test_read_json_round_trips_unicode(tmp_path: Path) -> None:
    target = tmp_path / "out.json"
    write_json({"caption": "이순신이 절뚝거리며 걸음"}, target)

    result = read_json(target)

    assert result["caption"] == "이순신이 절뚝거리며 걸음"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/shared/test_io_utils.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'shared'` (or `shared.io_utils`)

- [ ] **Step 3: Write minimal implementation**

```python
# shared/__init__.py
```

```python
# shared/io_utils.py
"""JSON 입출력 및 산출물 경로 규칙."""
import json
from pathlib import Path

OUTPUTS_DIR = Path("outputs")


def write_json(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/shared/test_io_utils.py -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add shared/__init__.py shared/io_utils.py tests/__init__.py tests/shared/__init__.py tests/shared/test_io_utils.py
git commit -m "feat: add shared JSON io_utils with tests"
```

---

### Task 3: `agents/scenario/` package — schema + agent stub + migrated training doc

**Files:**
- Create: `agents/__init__.py`
- Create: `agents/scenario/__init__.py`
- Create: `agents/scenario/schemas.py`
- Create: `agents/scenario/agent.py`
- Move: `step1-scenario-training.md` → `agents/scenario/prompts/training.md`
- Test: `tests/scenario/__init__.py`
- Test: `tests/scenario/test_schemas.py`
- Test: `tests/scenario/test_agent.py`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `ScenarioInput(logline: str)`, `ScenarioOutput(scene_script: str)` pydantic models; `generate_scenario(logline: str) -> str` (raises `NotImplementedError` for now). `pipeline/run_pipeline.py` (Task 7) imports `generate_scenario` from `agents.scenario.agent`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/scenario/test_schemas.py
import pytest
from pydantic import ValidationError

from agents.scenario.schemas import ScenarioInput, ScenarioOutput


def test_scenario_input_requires_logline() -> None:
    with pytest.raises(ValidationError):
        ScenarioInput()


def test_scenario_input_accepts_logline() -> None:
    result = ScenarioInput(logline="겁쟁이가 용을 잡아야 한다")
    assert result.logline == "겁쟁이가 용을 잡아야 한다"


def test_scenario_output_requires_scene_script() -> None:
    with pytest.raises(ValidationError):
        ScenarioOutput()
```

```python
# tests/scenario/test_agent.py
import pytest

from agents.scenario.agent import generate_scenario


def test_generate_scenario_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        generate_scenario("겁쟁이가 용을 잡아야 한다")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/scenario/ -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'agents'`

- [ ] **Step 3: Write minimal implementation**

```python
# agents/__init__.py
```

```python
# agents/scenario/__init__.py
```

```python
# agents/scenario/schemas.py
"""시나리오 에이전트 입출력 스키마."""
from pydantic import BaseModel


class ScenarioInput(BaseModel):
    logline: str


class ScenarioOutput(BaseModel):
    scene_script: str
```

```python
# agents/scenario/agent.py
"""1단계 시나리오 생성 에이전트: 로그라인 -> 비트 시트 -> 씬 리스트 -> 씬 대본.

방법론 레퍼런스: agents/scenario/prompts/training.md
"""
from agents.scenario.schemas import ScenarioOutput


def generate_scenario(logline: str) -> ScenarioOutput:
    raise NotImplementedError
```

Note: `test_agent.py` calls `generate_scenario("...")` and expects `NotImplementedError` — the stub raises unconditionally, so the return type annotation being `ScenarioOutput` is fine even though it never returns.

- [ ] **Step 4: Move the training doc**

```bash
mkdir -p agents/scenario/prompts
mv step1-scenario-training.md agents/scenario/prompts/training.md
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/scenario/ -v`
Expected: PASS (4 passed)

- [ ] **Step 6: Commit**

```bash
git add agents/__init__.py agents/scenario/ tests/scenario/
git commit -m "feat: scaffold scenario agent package, migrate training doc"
```

---

### Task 4: `agents/storyboard/` package — schema (shot list contract) + stubs + migrated training doc

**Files:**
- Create: `agents/storyboard/__init__.py`
- Create: `agents/storyboard/schemas.py`
- Create: `agents/storyboard/agent.py`
- Create: `agents/storyboard/image_prompt.py`
- Create: `agents/storyboard/image_gen.py`
- Create: `agents/storyboard/docx_export.py`
- Move: `step2-storyboard-training.md` → `agents/storyboard/prompts/training.md`
- Test: `tests/storyboard/__init__.py`
- Test: `tests/storyboard/test_schemas.py`
- Test: `tests/storyboard/test_agent.py`

**Interfaces:**
- Consumes: nothing from earlier tasks directly (takes a scene script `str`, matching `ScenarioOutput.scene_script` from Task 3).
- Produces: `Shot(size, angle, movement, duration, description, dialogue, audio, sceneSlug)` and `StoryboardOutput(shots: list[Shot])` pydantic models — this is the exact JSON contract Task 5's animatic agent consumes. Also `generate_storyboard(scene_script: str) -> StoryboardOutput`, `shot_to_image_prompt(shot: Shot) -> str`, `generate_contact_sheet_image(prompt: str) -> bytes`, `export_docx(storyboard: StoryboardOutput, path: Path) -> None` — all stubs raising `NotImplementedError`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/storyboard/test_schemas.py
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
```

```python
# tests/storyboard/test_agent.py
import pytest

from agents.storyboard.agent import generate_storyboard
from agents.storyboard.docx_export import export_docx
from agents.storyboard.image_gen import generate_contact_sheet_image
from agents.storyboard.image_prompt import shot_to_image_prompt


def test_generate_storyboard_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        generate_storyboard("INT. 낡은 극장 - 밤\n\n지우가 소품 상자를 뒤진다.")


def test_shot_to_image_prompt_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        shot_to_image_prompt(None)


def test_generate_contact_sheet_image_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        generate_contact_sheet_image("a prompt")


def test_export_docx_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        export_docx(None, None)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/storyboard/ -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'agents.storyboard'`

- [ ] **Step 3: Write minimal implementation**

```python
# agents/storyboard/__init__.py
```

```python
# agents/storyboard/schemas.py
"""스토리보드 에이전트 출력 스키마 — 애니매틱 에이전트의 입력 계약(기획서 4.6절)."""
from pydantic import BaseModel


class Shot(BaseModel):
    size: str
    angle: str
    movement: str
    duration: int
    description: str
    dialogue: str
    audio: str
    sceneSlug: str


class StoryboardOutput(BaseModel):
    shots: list[Shot]
```

```python
# agents/storyboard/agent.py
"""2단계 스토리보드 생성 에이전트: 씬 대본 -> 샷 리스트(JSON).

방법론 레퍼런스: agents/storyboard/prompts/training.md
"""
from agents.storyboard.schemas import StoryboardOutput


def generate_storyboard(scene_script: str) -> StoryboardOutput:
    raise NotImplementedError
```

```python
# agents/storyboard/image_prompt.py
"""샷 명세(Shot) -> 이미지 생성 프롬프트 번역 (Claude 담당)."""
from agents.storyboard.schemas import Shot


def shot_to_image_prompt(shot: Shot) -> str:
    raise NotImplementedError
```

```python
# agents/storyboard/image_gen.py
"""콘티 이미지 실제 생성 (Gemini 담당)."""


def generate_contact_sheet_image(prompt: str) -> bytes:
    raise NotImplementedError
```

```python
# agents/storyboard/docx_export.py
"""팀 표준 5컬럼 워드 출력 (기획서 4.8절)."""
from pathlib import Path

from agents.storyboard.schemas import StoryboardOutput


def export_docx(storyboard: StoryboardOutput, path: Path) -> None:
    raise NotImplementedError
```

- [ ] **Step 4: Move the training doc**

```bash
mkdir -p agents/storyboard/prompts
mv step2-storyboard-training.md agents/storyboard/prompts/training.md
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/storyboard/ -v`
Expected: PASS (7 passed)

- [ ] **Step 6: Commit**

```bash
git add agents/storyboard/ tests/storyboard/
git commit -m "feat: scaffold storyboard agent package with shot list schema, migrate training doc"
```

---

### Task 5: `agents/animatic/` package — schema (timeline contract) + stubs + migrated training doc + renderer

**Files:**
- Create: `agents/animatic/__init__.py`
- Create: `agents/animatic/schemas.py`
- Create: `agents/animatic/agent.py`
- Create: `agents/animatic/validators.py`
- Move: `step3-animatic-training.md` → `agents/animatic/prompts/training.md`
- Move: `animatic_renderer.py` → `agents/animatic/renderer/animatic_renderer.py`
- Test: `tests/animatic/__init__.py`
- Test: `tests/animatic/test_schemas.py`
- Test: `tests/animatic/test_agent.py`

**Interfaces:**
- Consumes: `Shot` list from Task 4 (`agents.storyboard.schemas.Shot`) as input type for `generate_timeline`.
- Produces: `Motion(type: str)`, `Overlays(info, caption, audio_note)`, `Cut(cut, image, duration, duration_rationale, motion, transition_out, overlays, flags)`, `TitleCard(title_card, duration)`, `Timeline(project, fps, resolution, cuts: list[Cut | TitleCard])` pydantic models (fields per spec §5.5). `generate_timeline(shots: list[Shot]) -> Timeline` and `validate_timeline(timeline: Timeline) -> list[str]` stubs. `agents/animatic/renderer/animatic_renderer.py` is moved unmodified — it is invoked as a subprocess/script by a later (out-of-scope) task, not imported.

- [ ] **Step 1: Write the failing tests**

```python
# tests/animatic/test_schemas.py
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
```

```python
# tests/animatic/test_agent.py
import pytest

from agents.animatic.agent import generate_timeline
from agents.animatic.validators import validate_timeline


def test_generate_timeline_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        generate_timeline([])


def test_validate_timeline_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        validate_timeline(None)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/animatic/ -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'agents.animatic'`

- [ ] **Step 3: Write minimal implementation**

```python
# agents/animatic/__init__.py
```

```python
# agents/animatic/schemas.py
"""애니매틱 에이전트 출력 스키마 — 렌더러의 입력 계약(기획서 5.5절)."""
from typing import Union

from pydantic import BaseModel


class Motion(BaseModel):
    type: str


class Overlays(BaseModel):
    info: str
    caption: str
    audio_note: str


class Cut(BaseModel):
    cut: int
    image: str
    duration: float
    duration_rationale: str
    motion: Motion
    transition_out: str
    overlays: Overlays
    flags: list[str] = []


class TitleCard(BaseModel):
    title_card: str
    duration: float


class Timeline(BaseModel):
    project: str
    fps: int
    resolution: str
    cuts: list[Union[Cut, TitleCard]]
```

```python
# agents/animatic/agent.py
"""3단계 애니매틱 생성 에이전트: 샷 리스트 -> 타임라인 JSON.

방법론 레퍼런스: agents/animatic/prompts/training.md
렌더링은 이 에이전트가 아니라 agents/animatic/renderer/animatic_renderer.py가 담당한다.
"""
from agents.animatic.schemas import Timeline
from agents.storyboard.schemas import Shot


def generate_timeline(shots: list[Shot]) -> Timeline:
    raise NotImplementedError
```

```python
# agents/animatic/validators.py
"""타임라인 JSON 수치 검증 규칙 (기획서 5.6절: 총 길이, 자막 읽기 시간, 연속 컷 등)."""
from agents.animatic.schemas import Timeline


def validate_timeline(timeline: Timeline) -> list[str]:
    raise NotImplementedError
```

- [ ] **Step 4: Move the training doc and renderer**

```bash
mkdir -p agents/animatic/prompts agents/animatic/renderer
mv step3-animatic-training.md agents/animatic/prompts/training.md
mv animatic_renderer.py agents/animatic/renderer/animatic_renderer.py
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/animatic/ -v`
Expected: PASS (6 passed)

- [ ] **Step 6: Commit**

```bash
git add agents/animatic/ tests/animatic/
git commit -m "feat: scaffold animatic agent package with timeline schema, migrate training doc and renderer"
```

---

### Task 6: `shared/claude_client.py` and `shared/gemini_client.py` — API client wrappers

**Files:**
- Create: `shared/claude_client.py`
- Create: `shared/gemini_client.py`
- Test: `tests/shared/test_claude_client.py`
- Test: `tests/shared/test_gemini_client.py`

**Interfaces:**
- Consumes: `ANTHROPIC_API_KEY` / `GEMINI_API_KEY` environment variables.
- Produces: `get_claude_client() -> anthropic.Anthropic`, `get_gemini_client() -> genai.Client`. Future agent implementations (out of scope here) will call these instead of constructing SDK clients directly.

- [ ] **Step 1: Write the failing tests**

```python
# tests/shared/test_claude_client.py
import pytest

from shared.claude_client import get_claude_client


def test_get_claude_client_raises_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(KeyError):
        get_claude_client()


def test_get_claude_client_returns_client_with_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    client = get_claude_client()
    assert client is not None
```

```python
# tests/shared/test_gemini_client.py
import pytest

from shared.gemini_client import get_gemini_client


def test_get_gemini_client_raises_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(KeyError):
        get_gemini_client()


def test_get_gemini_client_returns_client_with_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    client = get_gemini_client()
    assert client is not None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/shared/test_claude_client.py tests/shared/test_gemini_client.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'shared.claude_client'`

- [ ] **Step 3: Write minimal implementation**

```python
# shared/claude_client.py
"""Claude API 래퍼 — 언어·구조 판단(시나리오/샷 리스트/타임라인 생성) 담당."""
import os

import anthropic


def get_claude_client() -> anthropic.Anthropic:
    api_key = os.environ["ANTHROPIC_API_KEY"]
    return anthropic.Anthropic(api_key=api_key)
```

```python
# shared/gemini_client.py
"""Gemini API 래퍼 — 콘티 이미지 생성 담당 (Anthropic API는 이미지 생성 미지원)."""
import os

from google import genai


def get_gemini_client() -> genai.Client:
    api_key = os.environ["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/shared/test_claude_client.py tests/shared/test_gemini_client.py -v`
Expected: PASS (4 passed)

- [ ] **Step 5: Commit**

```bash
git add shared/claude_client.py shared/gemini_client.py tests/shared/test_claude_client.py tests/shared/test_gemini_client.py
git commit -m "feat: add Claude and Gemini API client wrappers"
```

---

### Task 7: `pipeline/run_pipeline.py` + `cli.py` — orchestration entrypoint

**Files:**
- Create: `pipeline/__init__.py`
- Create: `pipeline/run_pipeline.py`
- Create: `cli.py`
- Test: `tests/pipeline/__init__.py`
- Test: `tests/pipeline/test_run_pipeline.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Consumes: `generate_scenario` (Task 3), `generate_storyboard` (Task 4), `generate_timeline` (Task 5).
- Produces: `run(logline: str) -> Timeline` in `pipeline.run_pipeline`; `main() -> None` CLI entrypoint in `cli.py` registered as the `storymaker` console script (Task 1's `pyproject.toml`).

- [ ] **Step 1: Write the failing tests**

```python
# tests/pipeline/test_run_pipeline.py
import pytest

from pipeline.run_pipeline import run


def test_run_propagates_not_implemented_from_scenario_stage() -> None:
    with pytest.raises(NotImplementedError):
        run("겁쟁이가 용을 잡아야 한다")
```

```python
# tests/test_cli.py
import subprocess
import sys


def test_cli_help_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "cli.py", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "run" in result.stdout


def test_cli_run_without_logline_exits_nonzero() -> None:
    result = subprocess.run(
        [sys.executable, "cli.py", "run"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/pipeline/ tests/test_cli.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'pipeline'` (and `cli.py` not found for the subprocess tests)

- [ ] **Step 3: Write minimal implementation**

```python
# pipeline/__init__.py
```

```python
# pipeline/run_pipeline.py
"""3단계 파이프라인 오케스트레이션: 시나리오 -> 스토리보드 -> 애니매틱."""
from agents.animatic.agent import generate_timeline
from agents.animatic.schemas import Timeline
from agents.scenario.agent import generate_scenario
from agents.storyboard.agent import generate_storyboard


def run(logline: str) -> Timeline:
    scenario = generate_scenario(logline)
    storyboard = generate_storyboard(scenario.scene_script)
    return generate_timeline(storyboard.shots)
```

```python
# cli.py
"""StoryMaker CLI 진입점: storymaker run <logline>"""
import argparse

from pipeline.run_pipeline import run


def main() -> None:
    parser = argparse.ArgumentParser(prog="storymaker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="전체 파이프라인 실행")
    run_parser.add_argument("logline", help="로그라인 또는 기획 아이디어")

    args = parser.parse_args()

    if args.command == "run":
        run(args.logline)


if __name__ == "__main__":
    main()
```

Note: `pipeline/run_pipeline.py`'s `run()` calls `generate_scenario(logline)` which raises `NotImplementedError` immediately (Task 3's stub), so `test_run_propagates_not_implemented_from_scenario_stage` passes without needing storyboard/animatic to do anything. `test_cli_run_without_logline_exits_nonzero` passes because `argparse` exits with status 2 when the required `logline` positional is missing — it never reaches `run()`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/pipeline/ tests/test_cli.py -v`
Expected: PASS (3 passed)

- [ ] **Step 5: Commit**

```bash
git add pipeline/ cli.py tests/pipeline/ tests/test_cli.py
git commit -m "feat: wire pipeline orchestration and CLI entrypoint"
```

---

### Task 8: Full test suite sanity check and push to GitHub

**Files:** none created; verification and push only.

**Interfaces:** none.

- [ ] **Step 1: Confirm no leftover top-level training/renderer files**

Run: `ls step1-scenario-training.md step2-storyboard-training.md step3-animatic-training.md animatic_renderer.py 2>&1`
Expected: four "No such file or directory" errors — confirms all four were moved out of the top level.

- [ ] **Step 2: Run the full test suite**

Run: `uv run pytest -v`
Expected: all tests from Tasks 2–7 pass (26 passed), 0 failed

- [ ] **Step 3: Confirm git status is clean**

Run: `git status`
Expected: `nothing to commit, working tree clean`

- [ ] **Step 4: Push to GitHub**

```bash
git branch -M main
git push -u origin main
```

Expected: push succeeds, `main` branch created on `https://github.com/kvg2002/StoryMaker`.

- [ ] **Step 5: Verify on GitHub**

Run: `git ls-remote https://github.com/kvg2002/StoryMaker.git`
Expected: shows a `refs/heads/main` ref matching the local `main` HEAD commit hash (`git rev-parse HEAD`).
