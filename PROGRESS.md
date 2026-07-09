# StoryMaker 진행 상황 (2026-07-09 갱신)

최신 커밋: `837206c` (GitHub `kvg2002/StoryMaker` main 브랜치에 반영 완료) + 이후 시나리오 모델을
`gemini-2.5-pro`로 상향한 로컬 변경(아직 커밋 전일 수 있음 — `git log` 확인).

## 한 줄 요약

로그라인 → 시나리오 → 스토리보드 → 애니매틱 3단계 파이프라인이 전부 동작하고,
Streamlit 웹 UI에서 **단계마다 사람이 검토·수정한 뒤 직접 진행**하는 위자드 형태로 완성됨.
55/55 테스트 통과. **2026-07-09: Gemini 계정에 결제 등록 완료, 이미지 생성·`gemini-2.5-pro` 할당량 문제 해결됨.**

## 지금 당장 다시 시작하는 법

```bash
cd "C:\Users\kvg20\OneDrive\바탕 화면\Vibcoding\StoryMaker"
uv sync
uv run pytest                       # 55 passed 나오면 정상
uv run streamlit run app.py         # 웹 UI (권장) — http://localhost:8501
# 또는
uv run python cli.py run "로그라인"   # CLI로 한 번에 실행
```

`.env`에 `GEMINI_API_KEY`가 이미 들어있음(git에는 안 올라감, 로컬에만 존재). 새 컴퓨터에서 열면
`.env.example`을 `.env`로 복사하고 키를 채워야 함.

## 완성된 것

### 백엔드 (agents/)
- **`agents/scenario/agent.py`** — `generate_scenario(logline)`: Gemini(`gemini-2.5-pro`)로 Save the Cat 구조 기반 씬 대본 생성. 학습 문서(`prompts/training.md`)를 system_instruction으로 주입. (스토리보드·애니매틱은 `gemini-2.5-flash` 유지 — 근거는 설계 문서의 2026-07-09 결정 참고.)
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
- `run_from_storyboard(scenario, storyboard, project_dir) -> PipelineResult` — **시나리오/스토리보드를 사람이 수정한 뒤** 그 지점부터 이어서 실행(이미지→타임라인→검증→docx→렌더링). UI의 3단계 진행 버튼이 이 함수를 호출함.
- `PipelineResult`: `project_dir`, `scenario`, `storyboard`, `timeline`, `validation_flags`, `image_failures`, `docx_path`, `video_path`(렌더링 실패 시 `None`).
- 산출물은 `outputs/<로그라인 슬러그>/`에 저장: `images/cut{n}.png`, `images/timeline.json`, `storyboard.docx`, `animatic.mp4`.

### CLI (cli.py)
- `storymaker scenario <로그라인>` — 1단계만.
- `storymaker storyboard <로그라인>` — 1~2단계.
- `storymaker run <로그라인>` — 전체 파이프라인, 결과 요약 출력.

### 웹 UI (app.py) — Streamlit, 단계별 위자드
- **0단계**: 로그라인 입력 → "1단계: 시나리오 생성"
- **1단계**: 씬 대본이 `st.text_area`로 표시되고 **직접 수정 가능**. "🔄 다시 생성" 또는 "2단계로 진행" 선택.
- **2단계**: 샷마다 펼침 패널로 size/angle/movement/duration/description/dialogue/audio/sceneSlug **직접 수정 가능**. "🔄 다시 생성" 또는 "3단계로 진행" 선택 — **수정된 값이 3단계 입력으로 들어감**(재생성 안 됨).
- **3단계**: 이미지 생성 실패 목록, docx 다운로드 버튼, 검증 플래그, mp4(있으면 재생).
- Streamlit `AppTest` 하네스로 실제 Gemini 호출을 포함한 전체 클릭 스루(입력→시나리오→13개 샷 스토리보드→완료)를 검증 완료, 예외 0건.

### 인프라
- Gemini 단일 백엔드(Claude 제거함, 커밋 `4c73e00` 참고).
- ffmpeg 설치됨(`winget install Gyan.FFmpeg`, 8.1.2).
- uv 패키지 관리, pytest 55개 전부 통과.

## 알려진 제약 / 미해결 이슈

1. ~~이미지 생성 API 할당량 0~~ — **2026-07-09 결제 등록으로 해결됨.** `gemini-2.5-flash-image` 실제 이미지 생성 성공, `gemini-2.5-pro`도 정상 호출 확인.
2. docx의 "강조 컷"(이미지가 칸을 넘어가는 대형 배치) 기능 미구현 — 현재는 샷 1개=행 1개만.
3. UI에 "1단계로 돌아가기"(뒤로가기) 버튼 없음 — "처음부터 다시"만 있음.
4. 목표 러닝타임(`target_runtime_seconds`)을 UI에서 입력받는 기능 없음 — `validate_timeline`은 지원하지만 UI가 안 넘겨줌.
5. Gemini 무료 티어 자체가 가끔 503(서버 과부하)을 반환함 — 재시도 로직 없음, 실패하면 그냥 에러 표시.

## 다음에 이어서 할 만한 것 (우선순위 순 추천)

1. 결제 등록도 됐으니 **실제 이미지·mp4까지 나오는 전체 파이프라인 한 번 정식으로 돌려보기**.
2. UI에 "1단계로 돌아가기" 버튼 추가 (뒤로 가기 네비게이션).
3. UI에 목표 러닝타임 입력 필드 추가 → `validate_timeline(timeline, target_runtime_seconds=...)`에 연결.
4. Gemini 호출에 재시도/백오프 로직 추가(503 대응).
5. docx 강조 컷(칸 병합) 기능.

## 참고 문서

- 설계 결정 전체 이력: `docs/superpowers/specs/2026-07-08-storymaker-repo-scaffold-design.md` (스캐폴딩 → Gemini 전환 → 전 기능 구현까지 모든 결정과 근거 기록됨)
- 최초 구현 계획: `docs/superpowers/plans/2026-07-08-storymaker-repo-scaffold.md`
- 각 단계 방법론 원본: `agents/<stage>/prompts/training.md`
