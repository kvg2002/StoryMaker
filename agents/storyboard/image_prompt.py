"""샷 명세(Shot) -> 이미지 생성 프롬프트 번역.

기획서 4.7절 템플릿([스타일]+[샷 사이즈]+[앵글]+[피사체·행동]+[비율])은 필드 조합만으로
결정되는 기계적 변환이라 LLM 호출 없이 문자열 포맷으로 처리한다.
"""
from agents.storyboard.schemas import Shot

STYLE_PREFIX = "black and white storyboard sketch, rough pencil style"
ASPECT_RATIO = "16:9"


def shot_to_image_prompt(shot: Shot) -> str:
    return (
        f"{STYLE_PREFIX}, {shot.size}, {shot.angle} angle, "
        f"{shot.description}, {ASPECT_RATIO}"
    )
