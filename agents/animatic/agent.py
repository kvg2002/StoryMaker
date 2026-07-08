"""3단계 애니매틱 생성 에이전트: 샷 리스트 -> 타임라인 JSON.

방법론 레퍼런스: agents/animatic/prompts/training.md
언어 모델: Gemini (gemini-2.5-flash)
렌더링은 이 에이전트가 아니라 agents/animatic/renderer/animatic_renderer.py가 담당한다.
"""
from pathlib import Path

from google.genai import types

from agents.animatic.schemas import Timeline
from agents.storyboard.schemas import Shot, StoryboardOutput
from shared.gemini_client import get_gemini_client

MODEL = "gemini-2.5-flash"
TRAINING_DOC_PATH = Path(__file__).parent / "prompts" / "training.md"


def _build_system_instruction() -> str:
    training_doc = TRAINING_DOC_PATH.read_text(encoding="utf-8")
    return (
        "당신은 영상 프리프로덕션 파이프라인의 3단계 애니매틱 생성 에이전트다. "
        "아래 방법론을 따라 입력된 샷 리스트로부터 타임라인 JSON을 작성하라. "
        "각 컷의 image 필드에는 사용할 콘티 이미지 파일명을 자유롭게 지정하라(예: cut1.png).\n\n"
        f"{training_doc}"
    )


def generate_timeline(shots: list[Shot]) -> Timeline:
    client = get_gemini_client()
    shot_list_json = StoryboardOutput(shots=shots).model_dump_json()
    response = client.models.generate_content(
        model=MODEL,
        contents=shot_list_json,
        config=types.GenerateContentConfig(
            system_instruction=_build_system_instruction(),
            response_mime_type="application/json",
            response_schema=Timeline,
        ),
    )
    return response.parsed
