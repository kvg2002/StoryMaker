# StoryMaker

로그라인 한 줄에서 애니매틱 영상까지 — 시나리오 · 스토리보드 · 애니매틱 3단계 생성 에이전트 파이프라인.

## 파이프라인

1. **시나리오 에이전트** (`agents/scenario/`) — 로그라인 → 비트 시트 → 씬 리스트 → 씬 대본
2. **스토리보드 에이전트** (`agents/storyboard/`) — 씬 대본 → 샷 리스트(JSON) → 콘티 이미지 → 팀 표준 워드(.docx)
3. **애니매틱 에이전트** (`agents/animatic/`) — 샷 리스트 → 타임라인 JSON → 애니매틱 mp4 + 타임코드 시트

각 단계의 방법론 레퍼런스는 `agents/<stage>/prompts/training.md`에 있다. 전체 설계는
`docs/superpowers/specs/2026-07-08-storymaker-repo-scaffold-design.md` 참고.

## 기술 스택

Gemini 단일 백엔드로 동작한다 — 언어·구조 판단(시나리오/샷 리스트/타임라인)은 `gemini-2.5-flash`,
콘티 이미지 생성은 `gemini-2.5-flash-image`. 두 역할 모두 `shared/gemini_client.py`의 클라이언트를 사용한다.
(`gemini-2.5-pro`는 무료 티어 할당량이 0인 계정이 있어 기본값을 flash로 잡았다. pro를 쓰려면 각 `agent.py`의
`MODEL` 상수를 바꾸면 된다.)

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

### 웹 UI (Streamlit)

```bash
uv run streamlit run app.py
```

로컬에서 브라우저가 자동으로 열린다(기본 `http://localhost:8501`). 로그라인을 입력하고
"생성 시작"을 누르면 시나리오·샷 리스트·콘티 이미지·docx 다운로드·애니매틱 mp4를 한 화면에서 확인할 수 있다.
