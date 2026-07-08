"""3단계 파이프라인 오케스트레이션: 시나리오 -> 스토리보드 -> 애니매틱."""
from agents.animatic.agent import generate_timeline
from agents.animatic.schemas import Timeline
from agents.scenario.agent import generate_scenario
from agents.storyboard.agent import generate_storyboard


def run(logline: str) -> Timeline:
    scenario = generate_scenario(logline)
    storyboard = generate_storyboard(scenario.scene_script)
    return generate_timeline(storyboard.shots)
