"""2단계 스토리보드 생성 에이전트: 씬 대본 -> 샷 리스트(JSON).

방법론 레퍼런스: agents/storyboard/prompts/training.md
언어 모델: Gemini (gemini-2.5-flash), 콘티 이미지: Gemini (gemini-2.5-flash-image)
"""
from pathlib import Path

from google.genai import types

from agents.storyboard.schemas import StoryboardOutput
from shared.gemini_client import get_gemini_client

MODEL = "gemini-2.5-flash"
TRAINING_DOC_PATH = Path(__file__).parent / "prompts" / "training.md"


def _build_system_instruction() -> str:
    training_doc = TRAINING_DOC_PATH.read_text(encoding="utf-8")
    return (
        "당신은 영상 프리프로덕션 파이프라인의 2단계 스토리보드 생성 에이전트다. "
        "아래 방법론을 따라 씬 대본을 샷 단위로 분해해 샷 리스트를 작성하라. "
        "sceneSlug에는 해당 씬의 슬러그라인을 그대로 사용하라.\n\n"
        f"{training_doc}"
    )


def generate_storyboard(scene_script: str) -> StoryboardOutput:
    client = get_gemini_client()
    response = client.models.generate_content(
        model=MODEL,
        contents=scene_script,
        config=types.GenerateContentConfig(
            system_instruction=_build_system_instruction(),
            response_mime_type="application/json",
            response_schema=StoryboardOutput,
        ),
    )
    return response.parsed
