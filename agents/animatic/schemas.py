"""애니매틱 에이전트 출력 스키마 — 렌더러의 입력 계약(기획서 5.5절)."""
from typing import Union

from pydantic import BaseModel


class Motion(BaseModel):
    type: str


class Overlays(BaseModel):
    info: str
    caption: str
    audio_note: str


class Cut(BaseModel):
    cut: int
    image: str
    duration: float
    duration_rationale: str
    motion: Motion
    transition_out: str
    overlays: Overlays
    flags: list[str] = []


class TitleCard(BaseModel):
    title_card: str
    duration: float


class Timeline(BaseModel):
    project: str
    fps: int
    resolution: str
    cuts: list[Union[Cut, TitleCard]]
