# StoryMaker

로그라인 한 줄에서 애니매틱 영상까지 — 시나리오 · 스토리보드 · 애니매틱 3단계 생성 에이전트 파이프라인.

## 파이프라인

1. **시나리오 에이전트** (`agents/scenario/`) — 로그라인 → 비트 시트 → 씬 리스트 → 씬 대본
2. **스토리보드 에이전트** (`agents/storyboard/`) — 씬 대본 → 샷 리스트(JSON) → 콘티 이미지 → 팀 표준 워드(.docx)
3. **애니매틱 에이전트** (`agents/animatic/`) — 샷 리스트 → 타임라인 JSON → 애니매틱 mp4 + 타임코드 시트

각 단계의 방법론 레퍼런스는 `agents/<stage>/prompts/training.md`에 있다. 전체 설계는
`docs/superpowers/specs/2026-07-08-storymaker-repo-scaffold-design.md` 참고.

## 기술 스택

Gemini 단일 백엔드로 동작한다. `shared/gemini_client.py`의 클라이언트를 모든 단계가 공유하고,
단계별로 모델만 다르게 쓴다:

| 단계 | 모델 | 근거 |
|---|---|---|
| 시나리오 (`agents/scenario/agent.py`) | `gemini-3.1-pro-preview` | 창작 완성도가 가장 중요한 단계. 같은 로그라인으로 `gemini-2.5-pro`와 비교했을 때 완결된 4씬 구조·액션 클라이맥스·자가 체크리스트까지 수행해 이 모델이 우위였음(토큰은 약 19% 더 씀, 2026-07-09 확인) |
| 스토리보드 (`agents/storyboard/agent.py`) | `gemini-2.5-flash` | 샷 문법 규칙 적용 위주 구조화 작업이라 flash로 충분 |
| 애니매틱 (`agents/animatic/agent.py`) | `gemini-2.5-flash` | `validators.py`가 수치를 사후 검증·자동 보정해 안전망 역할을 함 |
| 콘티 이미지 (`agents/storyboard/image_gen.py`) | `gemini-2.5-flash-image` | 콘티는 완성 일러스트가 아닌 구도 전달용 스케치가 목적이고, 샷 개수만큼 반복 호출돼 비용에 민감 |

모델을 바꾸려면 각 `agent.py`(또는 `image_gen.py`)의 `MODEL` 상수를 수정하면 된다.

## 개발 환경

```bash
uv sync
cp .env.example .env  # GEMINI_API_KEY 채우기
uv run pytest
```

## 실행

### CLI

```bash
uv run python cli.py scenario "겁쟁이가 용을 잡아야 한다"    # 1단계만
uv run python cli.py storyboard "겁쟁이가 용을 잡아야 한다"  # 1~2단계
uv run python cli.py run "겁쟁이가 용을 잡아야 한다"          # 전체 파이프라인
```

`run`은 산출물을 `outputs/<로그라인 슬러그>/`에 저장한다: 콘티 이미지(`images/cut{n}.png`),
타임라인 JSON, 스토리보드 워드(`storyboard.docx`), 애니매틱 mp4(`animatic.mp4`).

애니매틱 렌더링에는 시스템에 `ffmpeg`가 설치되어 있어야 한다(`winget install Gyan.FFmpeg`).
콘티 이미지 생성이 실패해도(예: API 할당량 소진) 나머지 단계는 계속 진행되며, 렌더링은
실제 이미지 파일이 있을 때만 성공한다.

### 웹 UI (FastAPI + 정적 프론트, 권장)

```bash
uv run uvicorn server:app --reload
```

`http://127.0.0.1:8000`에서 실제 서비스 UI가 뜬다. 1단계(프로젝트 정보/장르/타겟관객/톤/로그라인)
입력 후 생성하면 씬 대본을 검토·수정할 수 있고, 2단계에서 스토리보드+콘티 이미지, 3단계에서
애니매틱(mp4·docx·검증 경고)까지 단계별로 사람이 확인하며 진행한다. 프론트엔드
(`index.html`/`style.css`/`script.js`)는 팀원이 제작, 백엔드 연동(`server.py`)은 이후 추가함.

`server.py`가 제공하는 API:

| 엔드포인트 | 역할 |
|---|---|
| `POST /api/scenario` | 1단계 폼 필드를 합성해 시나리오 생성 |
| `POST /api/storyboard` | 씬 대본 → 샷 리스트 + 콘티 이미지 생성 |
| `POST /api/animatic` | 샷 리스트 → 타임라인 검증 + docx + mp4 렌더링(이미지는 재생성하지 않음) |

생성물은 `/outputs/<project_slug>/`로 정적 서빙된다.

### 웹 UI (Streamlit, 더 이상 사용 안 함)

```bash
uv run streamlit run app.py
```

과거에 쓰던 위자드형 UI로, `app.py`에 코드가 남아있지만 신규 기능은 여기에 추가하지 않는다.
현재는 위 FastAPI + 정적 프론트 조합이 주력 UI다.
