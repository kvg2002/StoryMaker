import pytest

from agents.storyboard.agent import generate_storyboard
from agents.storyboard.docx_export import export_docx
from agents.storyboard.image_gen import generate_contact_sheet_image
from agents.storyboard.image_prompt import shot_to_image_prompt


def test_generate_storyboard_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        generate_storyboard("INT. 낡은 극장 - 밤\n\n지우가 소품 상자를 뒤진다.")


def test_shot_to_image_prompt_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        shot_to_image_prompt(None)


def test_generate_contact_sheet_image_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        generate_contact_sheet_image("a prompt")


def test_export_docx_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        export_docx(None, None)
