# StoryMaker 리포지토리 스캐폴딩 설계

- **일자**: 2026-07-08
- **범위**: `AI영상_프리프로덕션_파이프라인_기획서.pdf`에 정의된 3단계 에이전트 파이프라인(시나리오·스토리보드·애니매틱)을 개발할 저장소의 폴더 구조/스켈레톤을 만들고 GitHub(`kvg2002/StoryMaker`, 현재 빈 리포)에 초기 커밋한다. 에이전트의 실제 로직(Claude/Gemini 호출)은 이번 범위에 포함하지 않는다.

## 결정 사항

| 항목 | 결정 | 근거 |
|---|---|---|
| 런타임 | Python 단일 스택 | 기존 `animatic_renderer.py`(ffmpeg)와 언어 통일, Claude/Gemini 모두 공식 Python SDK 제공 |
| 사용 형태 | CLI 도구 | 현재 규모에 가장 빠르게 개발 가능, 추후 웹/서버로 확장 가능 |
| 패키지 관리 | uv (`pyproject.toml` + `uv.lock`) | 가상환경 생성부터 실행까지 단일 명령으로 처리되는 최신 표준 |
| 기존 파일 배치 | 각 에이전트 폴더 하위로 이동 | `step1~3-*-training.md`는 각 단계 에이전트의 시스템 프롬프트 레퍼런스이므로 해당 에이전트 코드와 같은 위치에 두는 것이 탐색에 유리 |

## 아키텍처

기획서 2.2절의 핵심 원칙 — **판단은 에이전트(LLM), 생성·렌더링은 전용 엔진** — 을 폴더 경계로 강제한다. 각 파이프라인 단계는 독립 패키지(`agents/<stage>/`)로 분리되며, 다음 단계로 넘기는 데이터는 `schemas.py`의 pydantic 모델로 고정한다(기획서 2.3, 4.6, 5.5절의 필드 규격 반영).

```
StoryMaker/
├── agents/
│   ├── scenario/
│   │   ├── agent.py                       # Claude: 비트시트→씬리스트→씬대본
│   │   ├── schemas.py                     # 출력 JSON 스키마
│   │   └── prompts/training.md            # ← step1-scenario-training.md
│   ├── storyboard/
│   │   ├── agent.py                       # Claude: 씬 대본→샷 리스트 JSON
│   │   ├── image_prompt.py                # Claude: 샷 명세→이미지 프롬프트 번역
│   │   ├── image_gen.py                   # Gemini: 콘티 이미지 생성
│   │   ├── docx_export.py                 # 팀 표준 5컬럼 워드 출력
│   │   ├── schemas.py
│   │   └── prompts/training.md            # ← step2-storyboard-training.md
│   └── animatic/
│       ├── agent.py                       # Claude: 샷리스트→타임라인 JSON
│       ├── validators.py                  # 수치 검증(총 길이/자막 읽기 시간/연속 컷 등)
│       ├── renderer/animatic_renderer.py  # ← 기존 파일 그대로 이동
│       ├── schemas.py
│       └── prompts/training.md            # ← step3-animatic-training.md
├── pipeline/
│   └── run_pipeline.py                    # 3단계 오케스트레이션 (CLI 진입점)
├── shared/
│   ├── claude_client.py                   # Claude API 래퍼
│   ├── gemini_client.py                   # Gemini API 래퍼
│   └── io_utils.py                        # JSON 입출력, 경로 규칙
├── docs/
│   └── README.md                          # 원본 기획서 PDF 보관 안내(파일 자체는 로컬에 없어 이동 대상 아님)
├── tests/
│   ├── scenario/
│   ├── storyboard/
│   └── animatic/
├── outputs/                                # 실행 산출물, .gitignore 처리
├── .env.example                            # ANTHROPIC_API_KEY, GEMINI_API_KEY
├── .gitignore
├── pyproject.toml
├── cli.py                                  # storymaker scenario|storyboard|animatic|run
└── README.md
```

## 단계별 데이터 계약 (스켈레톤에 반영할 스키마 필드)

- **scenario → storyboard**: 씬 대본(텍스트). 슬러그라인·지문·대사 구조 유지.
- **storyboard → animatic**: 샷 리스트 JSON — `size`, `angle`, `movement`, `duration`, `description`, `dialogue`, `audio`, `sceneSlug` 필드 필수(기획서 4.6절).
- **animatic 출력**: 타임라인 JSON — `project`, `fps`, `resolution`, `cuts[]`(`cut`, `image`, `duration`, `duration_rationale`, `motion`, `transition_out`, `overlays`, `flags`)(기획서 5.5절).

`schemas.py` 스켈레톤에는 이 필드들을 pydantic 모델의 필드명/타입으로만 정의하고, 실제 검증 로직(발화시간 공식 등)은 다음 세션 구현 범위로 남긴다.

## 이번 범위에서 하지 않는 것

- Claude/Gemini API 실제 호출 로직
- docx 생성/ffmpeg 렌더링 실행 로직 검증(코드는 이동만, 동작 재확인은 다음 세션)
- CLI 명령어의 실제 동작 구현(스텁만 생성)

## Git/GitHub 연동

- 로컬 디렉토리를 git 저장소로 초기화, `origin`을 `https://github.com/kvg2002/StoryMaker.git`으로 연결(리포는 현재 비어 있음, 확인 완료).
- 초기 커밋에 스캐폴딩 전체를 포함해 `main` 브랜치로 푸시.

## 결정 변경: Gemini 단일 백엔드 (2026-07-08)

초기 스캐폴딩(Task 1~8)은 기획서 원안대로 "텍스트=Claude, 이미지=Gemini" 이원 구조로 구현했으나, 이후 **Gemini API 키만 사용하는 단일 백엔드로 전환**하기로 결정했다.

- **근거**: Gemini는 이미지 생성뿐 아니라 텍스트 생성도 지원하므로, 별도 Claude API 키 없이 하나의 공급자로 파이프라인 전체를 운용할 수 있다. API 키 하나·SDK 하나로 구조가 단순해진다.
- **변경 내용**:
  - `shared/claude_client.py` 및 관련 테스트 삭제. `shared/gemini_client.py`가 텍스트 판단(시나리오/샷 리스트/타임라인 JSON)과 콘티 이미지 생성을 모두 담당.
  - `pyproject.toml`에서 `anthropic` 의존성 제거.
  - `.env.example`에서 `ANTHROPIC_API_KEY` 제거, `GEMINI_API_KEY`만 유지.
  - 각 에이전트(`agents/scenario/agent.py`, `agents/storyboard/agent.py`, `agents/storyboard/image_prompt.py`, `agents/animatic/agent.py`)의 docstring에서 "Claude 담당" 표기를 Gemini로 수정.
  - 언어 판단 모델은 애초 `gemini-2.5-pro`로 정했으나, 실제 키로 스모크테스트한 결과 이 계정은 pro 모델 무료 할당량이 0(`RESOURCE_EXHAUSTED`, limit: 0)이라 **`gemini-2.5-flash`로 하향 조정**했다(2026-07-08, 시나리오 에이전트 실구현 시 확인). 콘티 이미지는 여전히 `gemini-2.5-flash-image`.
- **범위에서 제외**: `agents/<stage>/prompts/training.md`(원본 기획서 방법론 레퍼런스)는 촬영 문법·편집 이론 등 API 공급자와 무관한 내용이 대부분이라 이번 전환에서 수정하지 않았다. 다만 각 문서의 "콘티 이미지 생성 파이프라인 (Claude + Gemini)" 절 등 특정 공급자를 못박은 부분은 실제 구현과 다를 수 있으니, 프롬프트를 다시 작성하는 시점에 참고용으로만 취급할 것.
- **위 "아키텍처" 트리와 표는 스캐폴딩 당시 상태를 기록한 것으로 그대로 둔다.** 현재 실제 구조는 `shared/claude_client.py`가 없고 `shared/gemini_client.py` 단독이라는 점이 다르다.

## 결정 변경: 전 기능 구현 + Streamlit UI (2026-07-08)

3단계 뼈대(생성 로직)까지 완성한 뒤, 나머지 스텁(콘티 이미지 생성, docx 출력, 타임라인 검증, 실제 mp4 렌더링)을 모두 구현하고 웹 UI를 추가했다.

- **`shot_to_image_prompt`는 Gemini 호출 없이 결정적 템플릿 함수로 구현**했다. 기획서 4.7절 템플릿이 필드 조합만으로 정해지는 기계적 변환이라 LLM이 불필요하고, 무료 티어 할당량 리스크도 줄어든다.
- **콘티 이미지 생성(`gemini-2.5-flash-image`)은 이 계정에서 무료 할당량이 0**(`RESOURCE_EXHAUSTED`, limit: 0)으로 확인됐다. `generate_contact_sheets`는 샷별 생성 실패를 개별적으로 흡수하고 나머지 샷은 계속 진행하도록 설계했다 — 이미지 없이도 docx·타임라인·검증은 끝까지 동작해야 한다는 원칙.
- **`export_docx`**: python-docx로 기획서 4.8절의 5컬럼(Cut/Video/Content/Audio/Time) 표를 실제로 생성. 팀 표기 관례(OTS→OSS, overhead→Top Angle 등) 반영. 강조 컷(Video+Content 칸 병합)은 이번 범위에서 생략 — 필요시 후속 작업.
- **`validate_timeline`**: 학습 문서 PART 10 규칙 중 대사 컷 최소 길이 자동 상향, 자막 읽기 시간 부족 플래그, 동일 길이 3연속 플래그, 씬 내부 전환 강제 교정(cut)을 구현. 총 길이 검증은 `target_runtime_seconds`를 선택적으로 받아 있을 때만 체크. 실제 생성 데이터로 라이브 테스트한 결과 11건의 실제 문제를 정확히 잡아냄(자막 읽기 시간 부족 10건, 대사 길이 자동 상향 1건).
- **ffmpeg를 `winget install Gyan.FFmpeg`로 설치**해 실제 mp4 렌더링 경로를 열었다. `agents/animatic/renderer/run_renderer.py`가 검증된 `animatic_renderer.py` 스크립트를 서브프로세스로 호출한다(스크립트 내용은 수정하지 않음 — 기획서 원칙 준수). 콘티 이미지가 없으면 렌더링은 실패하고 `PipelineResult.video_path`가 `None`이 된다 — 파이프라인 전체가 죽지 않고 나머지 산출물(docx, timeline.json)은 정상 반환.
- **`pipeline/run_pipeline.py`가 `PipelineResult`(pydantic 모델)를 반환**하도록 변경 — 이전에는 `Timeline`만 반환했으나, 프로젝트 폴더 경로·docx 경로·비디오 경로·검증 플래그·이미지 실패 목록을 UI/CLI가 모두 참조해야 해서 확장했다.
- **`app.py` (Streamlit 웹 UI)** 추가: `uv run streamlit run app.py`로 로컬 브라우저에서 실행. 로그라인 입력 → 생성 버튼 → 시나리오/샷별 이미지·설명/docx 다운로드/검증 플래그/mp4 순서로 표시. UI 자체는 이미 테스트된 파이프라인 함수를 호출만 하는 얇은 레이어라 별도 자동화 테스트 없이 실제 기동 확인(HTTP 200)으로 검증했다.

## 결정 변경: 결제 등록 완료 + 단계별 모델 재조정 (2026-07-09)

Gemini 계정에 결제를 등록해 `gemini-2.5-pro`, `gemini-2.5-flash-image` 모두 무료 티어 할당량 0 제약이 풀렸다(실제 이미지 생성 성공으로 확인). 이에 따라 단계별로 모델을 재조정했다.

- **시나리오만 `gemini-2.5-pro`로 상향**했다. 근거: 창작 판단이 가장 중요한 단계인데 사람이 직접 검증하는 것 외에 사후 보정 코드가 없고(2·3단계는 `validators.py`가 있음), 파이프라인당 1회만 호출돼 상위 모델 비용 부담이 작다.
- **스토리보드·애니매틱은 `gemini-2.5-flash` 유지**. 둘 다 규칙 적용 위주의 구조화 출력 작업이고, 애니매틱은 검증 코드가 안전망 역할을 하므로 상위 모델이 굳이 필요하지 않다.
- **콘티 이미지는 `gemini-2.5-flash-image`("나노바나나") 유지**. 콘티는 완성 일러스트가 아닌 구도 전달용 스케치가 목적(기획서 원칙)이고, 샷 개수만큼 반복 호출되는 유일한 단계라 비용에 가장 민감하다. `gemini-3-pro-image`("나노바나나 프로")나 `imagen-4.0` 같은 상위 이미지 모델로 바꿀 수도 있지만 현재는 불필요하다고 판단.
- 이 변경은 `agents/scenario/agent.py`의 `MODEL` 상수만 수정하는 최소 변경이었고, 사용자 요청에 따라 실제 API를 호출하는 라이브 테스트는 생략했다(기존 mock 단위 테스트로만 확인).

## 결정 변경: 시나리오 모델을 gemini-3.1-pro-preview로 재상향 (2026-07-09)

같은 로그라인("가야인·문신·성장기·청소년" 소재)으로 `gemini-2.5-pro`와 `gemini-3.1-pro-preview`를 직접 비교했다.

- **`gemini-2.5-pro`**: 기폭제 씬 1개만 정교하게 작성. 문장 완성도는 높지만 "완성된 씬 대본" 기준으로는 미완결(주인공이 결심하는 데서 종료).
- **`gemini-3.1-pro-preview`**: 4개 씬으로 기승전결을 완주(성인식 실패 → 갈등 → 금지된 동굴에서의 액션 클라이맥스 → 마을로 돌아와 인정받는 엔딩). 오프닝/엔딩 대비, 목표-결핍 충돌 등 학습 문서 원칙을 스스로 체크리스트로 검증까지 수행.
- **토큰 비교** (`count_tokens`로 실측, 입력은 두 모델 동일하게 5,610토큰): 2.5-pro 출력 1,475토큰(총 7,085) vs 3.1-pro-preview 출력 2,808토큰(총 8,418) — **약 19% 더 사용**하지만 완결성 차이가 그 이상이라고 판단.
- **결론**: 시나리오 단계를 `gemini-3.1-pro-preview`로 변경. 스토리보드·애니매틱·이미지 생성은 위 절의 결정을 그대로 유지.
