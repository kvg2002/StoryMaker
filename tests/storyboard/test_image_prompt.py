from agents.storyboard.image_prompt import shot_to_image_prompt
from agents.storyboard.schemas import Shot


def test_shot_to_image_prompt_includes_size_angle_and_description() -> None:
    shot = Shot(
        size="MCU",
        angle="low",
        movement="static",
        duration=3,
        description="지우가 낡은 대본을 손에 쥐고 표지를 쓸어본다",
        dialogue="",
        audio="",
        sceneSlug="S1",
    )

    prompt = shot_to_image_prompt(shot)

    assert "MCU" in prompt
    assert "low" in prompt
    assert "지우가 낡은 대본을 손에 쥐고 표지를 쓸어본다" in prompt


def test_shot_to_image_prompt_uses_sketch_style_and_16_9_ratio() -> None:
    shot = Shot(
        size="WS",
        angle="eye-level",
        movement="static",
        duration=4,
        description="낡은 극장 무대 전경",
        dialogue="",
        audio="",
        sceneSlug="S1",
    )

    prompt = shot_to_image_prompt(shot)

    assert "pencil" in prompt
    assert "16:9" in prompt
