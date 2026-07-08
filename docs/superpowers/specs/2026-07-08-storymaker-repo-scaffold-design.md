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
│   └── AI영상_프리프로덕션_파이프라인_기획서.pdf
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
