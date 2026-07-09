"""1단계 시나리오 생성 에이전트: 로그라인 -> 비트 시트 -> 씬 리스트 -> 씬 대본.

방법론 레퍼런스: agents/scenario/prompts/training.md
언어 모델: Gemini (gemini-3.1-pro-preview — 같은 로그라인으로 gemini-2.5-pro와 비교 시
완결된 4씬 구조·액션 클라이맥스·자가 체크리스트까지 수행해 창작 완성도가 더 높았음, 2026-07-09 확인.
토큰은 약 19% 더 쓰지만(출력이 길어져서) 완결성 대비 부담은 작다고 판단)
"""
from pathlib import Path

from google.genai import types

from agents.scenario.schemas import ScenarioOutput
from shared.gemini_client import get_gemini_client

MODEL = "gemini-3.1-pro-preview"
TRAINING_DOC_PATH = Path(__file__).parent / "prompts" / "training.md"


def _build_system_instruction() -> str:
    training_doc = TRAINING_DOC_PATH.read_text(encoding="utf-8")
    return (
        "당신은 영상 프리프로덕션 파이프라인의 1단계 시나리오 생성 에이전트다. "
        "아래 방법론을 따라 사용자가 준 로그라인으로부터 완성된 씬 대본(슬러그라인, 지문, 대사 포함)을 작성하라.\n\n"
        f"{training_doc}"
    )


def generate_scenario(logline: str) -> ScenarioOutput:
    client = get_gemini_client()
    response = client.models.generate_content(
        model=MODEL,
        contents=logline,
        config=types.GenerateContentConfig(
            system_instruction=_build_system_instruction(),
        ),
    )
    return ScenarioOutput(scene_script=response.text)
