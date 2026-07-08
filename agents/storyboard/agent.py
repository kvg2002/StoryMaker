"""2단계 스토리보드 생성 에이전트: 씬 대본 -> 샷 리스트(JSON).

방법론 레퍼런스: agents/storyboard/prompts/training.md
"""
from agents.storyboard.schemas import StoryboardOutput


def generate_storyboard(scene_script: str) -> StoryboardOutput:
    raise NotImplementedError
