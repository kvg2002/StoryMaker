"""샷 명세(Shot) -> 이미지 생성 프롬프트 번역 (Claude 담당)."""
from agents.storyboard.schemas import Shot


def shot_to_image_prompt(shot: Shot) -> str:
    raise NotImplementedError
