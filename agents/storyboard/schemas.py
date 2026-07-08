"""스토리보드 에이전트 출력 스키마 — 애니매틱 에이전트의 입력 계약(기획서 4.6절)."""
from pydantic import BaseModel


class Shot(BaseModel):
    size: str
    angle: str
    movement: str
    duration: int
    description: str
    dialogue: str
    audio: str
    sceneSlug: str


class StoryboardOutput(BaseModel):
    shots: list[Shot]
