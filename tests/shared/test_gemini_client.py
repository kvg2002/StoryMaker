import pytest

from shared.gemini_client import get_gemini_client


def test_get_gemini_client_raises_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(KeyError):
        get_gemini_client()


def test_get_gemini_client_returns_client_with_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    client = get_gemini_client()
    assert client is not None
