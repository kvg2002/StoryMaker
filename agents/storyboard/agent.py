"""2단계 스토리보드 생성 에이전트: 씬 대본 -> 샷 리스트(JSON).

방법론 레퍼런스: agents/storyboard/prompts/training.md
언어 모델: Gemini (gemini-2.5-pro), 콘티 이미지: Gemini (gemini-2.5-flash-image)
"""
from agents.storyboard.schemas import StoryboardOutput


def generate_storyboard(scene_script: str) -> StoryboardOutput:
    raise NotImplementedError
