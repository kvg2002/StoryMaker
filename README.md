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
