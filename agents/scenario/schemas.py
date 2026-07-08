"""시나리오 에이전트 입출력 스키마."""
from pydantic import BaseModel


class ScenarioInput(BaseModel):
    logline: str


class ScenarioOutput(BaseModel):
    scene_script: str
