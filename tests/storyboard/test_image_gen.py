from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from agents.storyboard.image_gen import generate_contact_sheet_image, generate_contact_sheets
from agents.storyboard.schemas import Shot

FAKE_IMAGE_BYTES = b"\x89PNG\r\n\x1a\nfake-png-bytes"


def _fake_response_with_image(image_bytes: bytes):
    part = SimpleNamespace(inline_data=SimpleNamespace(data=image_bytes, mime_type="image/png"))
    content = SimpleNamespace(parts=[part])
    candidate = SimpleNamespace(content=content)
    return SimpleNamespace(candidates=[candidate])


def test_generate_contact_sheet_image_returns_inline_image_bytes(monkeypatch) -> None:
    fake_response = _fake_response_with_image(FAKE_IMAGE_BYTES)
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response
    monkeypatch.setattr("agents.storyboard.image_gen.get_gemini_client", lambda: fake_client)

    result = generate_contact_sheet_image("a black and white storyboard sketch")

    assert result == FAKE_IMAGE_BYTES


def test_generate_contact_sheet_image_calls_gemini_image_model(monkeypatch) -> None:
    fake_response = _fake_response_with_image(FAKE_IMAGE_BYTES)
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response
    monkeypatch.setattr("agents.storyboard.image_gen.get_gemini_client", lambda: fake_client)

    generate_contact_sheet_image("a black and white storyboard sketch")

    fake_client.models.generate_content.assert_called_once()
    call_kwargs = fake_client.models.generate_content.call_args.kwargs
    assert call_kwargs["model"] == "gemini-2.5-flash-image"
    assert call_kwargs["contents"] == "a black and white storyboard sketch"


def test_generate_contact_sheet_image_raises_when_no_image_part(monkeypatch) -> None:
    part = SimpleNamespace(inline_data=None)
    content = SimpleNamespace(parts=[part])
    candidate = SimpleNamespace(content=content)
    fake_response = SimpleNamespace(candidates=[candidate])
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response
    monkeypatch.setattr("agents.storyboard.image_gen.get_gemini_client", lambda: fake_client)

    with pytest.raises(RuntimeError):
        generate_contact_sheet_image("a black and white storyboard sketch")


SHOTS = [
    Shot(size="WS", angle="eye-level", movement="static", duration=3,
         description="낡은 극장 무대", dialogue="", audio="", sceneSlug="S1"),
    Shot(size="MCU", angle="low", movement="static", duration=2,
         description="지우의 얼굴", dialogue="", audio="", sceneSlug="S1"),
]


def test_generate_contact_sheets_writes_one_png_per_shot(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        "agents.storyboard.image_gen.generate_contact_sheet_image",
        lambda prompt: FAKE_IMAGE_BYTES,
    )

    failures = generate_contact_sheets(SHOTS, tmp_path)

    assert failures == []
    assert (tmp_path / "cut1.png").read_bytes() == FAKE_IMAGE_BYTES
    assert (tmp_path / "cut2.png").read_bytes() == FAKE_IMAGE_BYTES


def test_generate_contact_sheets_continues_past_individual_failures(tmp_path, monkeypatch) -> None:
    def flaky_generate(prompt: str) -> bytes:
        if "얼굴" in prompt:
            raise RuntimeError("quota exceeded")
        return FAKE_IMAGE_BYTES

    monkeypatch.setattr(
        "agents.storyboard.image_gen.generate_contact_sheet_image", flaky_generate
    )

    failures = generate_contact_sheets(SHOTS, tmp_path)

    assert len(failures) == 1
    assert "cut2" in failures[0]
    assert (tmp_path / "cut1.png").exists()
    assert not (tmp_path / "cut2.png").exists()
