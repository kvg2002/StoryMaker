"""콘티 이미지 실제 생성 (Gemini 담당)."""
from pathlib import Path

from agents.storyboard.image_prompt import shot_to_image_prompt
from agents.storyboard.schemas import Shot
from shared.gemini_client import get_gemini_client

IMAGE_MODEL = "gemini-2.5-flash-image"


def generate_contact_sheet_image(prompt: str) -> bytes:
    client = get_gemini_client()
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=prompt,
    )
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            return part.inline_data.data
    raise RuntimeError("Gemini 응답에 이미지 데이터가 없습니다.")


def generate_contact_sheets(shots: list[Shot], output_dir: Path) -> list[str]:
    """샷마다 콘티 이미지를 생성해 output_dir/cut{n}.png로 저장한다.

    개별 샷의 이미지 생성이 실패해도(예: API 할당량 소진) 나머지 샷은 계속 진행하고,
    실패한 샷은 경고 메시지로 모아 반환한다 — 이미지 없이도 docx/타임라인/렌더링은 진행 가능해야 한다.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    failures = []
    for i, shot in enumerate(shots, start=1):
        filename = f"cut{i}.png"
        try:
            image_bytes = generate_contact_sheet_image(shot_to_image_prompt(shot))
        except Exception as e:
            failures.append(f"{filename} 생성 실패: {e}")
            continue
        (output_dir / filename).write_bytes(image_bytes)
    return failures
