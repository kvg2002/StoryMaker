"""1단계 시나리오 생성 에이전트: 로그라인 -> 비트 시트 -> 씬 리스트 -> 씬 대본.

방법론 레퍼런스: agents/scenario/prompts/training.md
언어 모델: Gemini (gemini-2.5-pro)
"""
from agents.scenario.schemas import ScenarioOutput


def generate_scenario(logline: str) -> ScenarioOutput:
    raise NotImplementedError
