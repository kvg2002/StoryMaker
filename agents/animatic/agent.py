"""3단계 애니매틱 생성 에이전트: 샷 리스트 -> 타임라인 JSON.

방법론 레퍼런스: agents/animatic/prompts/training.md
렌더링은 이 에이전트가 아니라 agents/animatic/renderer/animatic_renderer.py가 담당한다.
"""
from agents.animatic.schemas import Timeline
from agents.storyboard.schemas import Shot


def generate_timeline(shots: list[Shot]) -> Timeline:
    raise NotImplementedError
