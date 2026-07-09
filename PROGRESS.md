# StoryMaker 진행 상황 (2026-07-09 갱신)

최신 커밋: `5da1749` (GitHub `kvg2002/StoryMaker` main 브랜치, 팀원의 정적 프론트엔드 프로토타입
`index.html`/`style.css`/`script.js` 추가) + 이후 FastAPI 백엔드 연동 작업(이 문서 갱신 시점 기준 로컬
변경, 아직 커밋 전 — `git log` 확인). 시나리오 모델은 `gemini-2.5-pro` → `gemini-3.1-pro-preview`로
상향(같은 로그라인 비교 결과 완결성이 더 높아 최종 선택).

## 한 줄 요약

로그라인 → 시나리오 → 스토리보드 → 애니매틱 3단계 파이프라인이 전부 동작하고, **팀원이 만든
HTML/CSS 프론트엔드 + FastAPI 백엔드(`server.py`)** 조합으로 실제 서비스형 UI가 완성됨.
**Streamlit(`app.py`)은 더 이상 사용하지 않음** — 팀원 프론트로 완전히 대체됨(코드는 참고용으로
레포에 남아있음). 65/65 테스트 통과. **2026-07-09: Gemini 계정에 결제 등록 완료, 이미지 생성·
`gemini-2.5-pro` 할당량 문제 해결됨.**

## 지금 당장 다시 시작하는 법

```bash
cd "C:\Users\kvg20\OneDrive\바탕 화면\Vibcoding\StoryMaker"
uv sync
uv run pytest                          # 65 passed 나오면 정상
uv run uvicorn server:app --reload     # 실제 서비스 UI (권장) — http://127.0.0.1:8000
# 또는
uv run python cli.py run "로그라인"      # CLI로 한 번에 실행
```

`.env`에 `GEMINI_API_KEY`가 이미 들어있음(git에는 안 올라감, 로컬에만 존재). 새 컴퓨터에서 열면
`.env.example`을 `.env`로 복사하고 키를 채워야 함.

## 완성된 것

### 백엔드 (agents/)
- **`agents/scenario/agent.py`** — `generate_scenario(logline)`: Gemini(`gemini-3.1-pro-preview`)로 Save the Cat 구조 기반 씬 대본 생성. 학습 문서(`prompts/training.md`)를 system_instruction으로 주입. (스토리보드·애니매틱은 `gemini-2.5-flash` 유지 — 근거는 설계 문서의 2026-07-09 결정 참고.)
- **`agents/storyboard/agent.py`** — `generate_storyboard(scene_script)`: Gemini 구조화 출력(`response_schema=StoryboardOutput`)으로 샷 리스트 JSON 생성.
- **`agents/storyboard/image_prompt.py`** — `shot_to_image_prompt(shot)`: **LLM 호출 없이** 결정적 템플릿으로 이미지 프롬프트 생성(기획서 4.7절 공식이 기계적 변환이라 API 불필요).
- **`agents/storyboard/image_gen.py`** — `generate_contact_sheet_image(prompt)`: 실제 `gemini-2.5-flash-image` 호출. `generate_contact_sheets(shots, output_dir)`: 샷별로 반복 호출해 `cut{n}.png` 저장, 개별 실패는 흡수하고 계속 진행.
- **`agents/storyboard/docx_export.py`** — `export_docx(storyboard, path, images_dir=None)`: python-docx로 팀 표준 5컬럼(Cut/Video/Content/Audio/Time) 워드 파일 생성. 강조 컷(칸 병합)은 미구현.
- **`agents/animatic/agent.py`** — `generate_timeline(shots)`: Gemini 구조화 출력(`response_schema=Timeline`, `Union[Cut, TitleCard]` 포함)으로 타임라인 JSON 생성.
- **`agents/animatic/validators.py`** — `validate_timeline(timeline, target_runtime_seconds=None)`: 대사 컷 최소 길이 자동 상향, 자막 읽기 시간 부족 플래그, 동일 길이 3연속 플래그, 씬 내부 전환 강제 교정(cut). **실제 생성 데이터로 라이브 검증 시 진짜 문제 7~11건을 정확히 잡아냄.**
- **`agents/animatic/renderer/animatic_renderer.py`** — 원본 검증된 ffmpeg 스크립트(수정 안 함).
- **`agents/animatic/renderer/run_renderer.py`** — 위 스크립트를 서브프로세스로 안전하게 호출하는 래퍼(cwd를 이미지 폴더로 지정).

### 파이프라인 (pipeline/run_pipeline.py)
- `run(logline, project_dir=None) -> PipelineResult` — 시나리오부터 끝까지 한 번에.
- `run_from_storyboard(scenario, storyboard, project_dir) -> PipelineResult` — **시나리오/스토리보드를 사람이 수정한 뒤** 그 지점부터 이어서 실행(이미지→타임라인→검증→docx→렌더링).
- `finalize_from_storyboard(scenario, storyboard, project_dir, image_failures=None) -> PipelineResult` — **이미지는 이미 생성돼 있다고 가정**하고 타임라인→검증→docx→렌더링만 실행. `server.py`의 `/api/animatic`이 호출(2단계에서 만든 이미지를 다시 만들지 않기 위함).
- `PipelineResult`: `project_dir`, `scenario`, `storyboard`, `timeline`, `validation_flags`, `image_failures`, `docx_path`, `video_path`(렌더링 실패 시 `None`).
- 산출물은 `outputs/<프로젝트 슬러그>/`에 저장: `images/cut{n}.png`, `images/timeline.json`, `storyboard.docx`, `animatic.mp4`.

### CLI (cli.py)
- `storymaker scenario <로그라인>` — 1단계만.
- `storymaker storyboard <로그라인>` — 1~2단계.
- `storymaker run <로그라인>` — 전체 파이프라인, 결과 요약 출력.

### 웹 UI (server.py + index.html/style.css/script.js) — FastAPI + 팀원 제작 프론트, 단계별 위자드 ⭐ 현재 주력 UI
- `server.py`가 정적 프론트(`/`, `/style.css`, `/script.js`)를 서빙하고 `/outputs`에 생성물을 마운트, 3개 API 엔드포인트를 제공:
  - `POST /api/scenario` — 1단계 폼(제목/길이/장르/타겟관객/톤/로그라인)을 전부 텍스트로 합쳐 `generate_scenario`에 전달. 응답: `scene_script`, `project_slug`.
  - `POST /api/storyboard` — 씬 대본 + 샷개수/카메라스타일을 합쳐 `generate_storyboard` → `generate_contact_sheets`까지 실행. 응답: `shots`(+ `image_url`), `image_failures`.
  - `POST /api/animatic` — 씬 대본 + 샷 목록으로 `finalize_from_storyboard` 실행(이미지 재생성 없음). 응답: `docx_url`, `video_url`(렌더링 실패 시 `None`), `validation_flags`, `image_failures`.
  - 폼 필드 합성은 API 계층(`_compose_scenario_input`/`_compose_storyboard_input`)에서만 처리 — `generate_scenario`/`generate_storyboard`의 시그니처(문자열 1개 입력)는 그대로 유지해 CLI에서도 계속 동작함.
- `index.html`에 시나리오 검토용 `<textarea>`(수정 가능) + "🔄 다시 생성"/"2단계로 진행" 버튼, 스토리보드 결과 그리드(실제 콘티 이미지로 교체), 애니매틱 결과(영상 `<video>`, docx 다운로드 링크, 검증/실패 경고 목록)를 추가.
- `script.js`가 각 "생성하기" 버튼에서 실제 `fetch()`로 위 3개 API를 호출, 로딩 스피너 오버레이를 띄우고 완료 시 결과를 반영. AI 응답 텍스트는 전부 `textContent`로 렌더링(HTML 삽입 없음, XSS 방지).
- 색감(색조) 선택 chip은 UI에는 있지만 **이미지 생성에 반영하지 않음** — 콘티는 원래부터 흑백 스케치가 목적이므로(사용자 확인됨).
- **Streamlit(`app.py`)은 이제 사용 안 함** — 코드는 참고용으로만 남아있고 신규 기능은 여기 안 들어감.

### 인프라
- Gemini 단일 백엔드(Claude 제거함, 커밋 `4c73e00` 참고).
- ffmpeg 설치됨(`winget install Gyan.FFmpeg`, 8.1.2).
- FastAPI + uvicorn 추가(`fastapi`, `uvicorn[standard]`, `python-multipart`, `httpx`).
- uv 패키지 관리, pytest 65개 전부 통과.

## 알려진 제약 / 미해결 이슈

1. ~~이미지 생성 API 할당량 0~~ — **2026-07-09 결제 등록으로 해결됨.** `gemini-2.5-flash-image` 실제 이미지 생성 성공, `gemini-2.5-pro`도 정상 호출 확인.
2. docx의 "강조 컷"(이미지가 칸을 넘어가는 대형 배치) 기능 미구현 — 현재는 샷 1개=행 1개만.
3. UI에 "1단계로 돌아가기"(뒤로가기) 버튼 없음 — 사이드바/상단 파이프라인 카드를 눌러 임의 단계로 이동은 가능하지만, 데이터가 아직 없는 단계로 가면 "먼저 n단계를 진행해주세요" 토스트만 뜨고 자동으로 이전 단계로 보내주진 않음.
4. 목표 러닝타임(`target_runtime_seconds`)을 UI에서 입력받는 기능 없음 — `validate_timeline`은 지원하지만 UI가 안 넘겨줌.
5. Gemini 무료 티어 자체가 가끔 503(서버 과부하)을 반환함 — 재시도 로직 없음, 실패하면 그냥 에러 토스트 표시.
6. 스토리보드 화면비율(`aspect_ratio`) 선택 chip이 UI에는 있지만 `/api/storyboard`로 전달되지 않음(샷개수/카메라스타일만 반영) — 이번 연동 작업 범위 밖으로 일부러 제외함.
7. 실제 Gemini API를 호출하는 전체 브라우저 end-to-end 테스트는 아직 안 해봄(2026-07-09 기준) — 백엔드는 65개 mocked 테스트로만 검증됨. 사용자가 직접 `http://127.0.0.1:8000`에서 확인 예정.

## 다음에 이어서 할 만한 것 (우선순위 순 추천)

1. **브라우저에서 실제로 한 번 끝까지 눌러보기**(시나리오→스토리보드→애니매틱) — 아직 실제 Gemini 호출로 전체 흐름을 검증한 적 없음.
2. UI에 "1단계로 돌아가기" 버튼 추가 (뒤로 가기 네비게이션).
3. `aspect_ratio`를 `/api/storyboard`에 반영할지 결정 (이미지 생성 시 화면비율 지정).
4. UI에 목표 러닝타임 입력 필드 추가 → `validate_timeline(timeline, target_runtime_seconds=...)`에 연결.
5. Gemini 호출에 재시도/백오프 로직 추가(503 대응).
6. docx 강조 컷(칸 병합) 기능.

## 참고 문서

- 설계 결정 전체 이력: `docs/superpowers/specs/2026-07-08-storymaker-repo-scaffold-design.md` (스캐폴딩 → Gemini 전환 → 전 기능 구현까지 모든 결정과 근거 기록됨)
- 최초 구현 계획: `docs/superpowers/plans/2026-07-08-storymaker-repo-scaffold.md`
- 각 단계 방법론 원본: `agents/<stage>/prompts/training.md`
