import pytest

from shared.claude_client import get_claude_client


def test_get_claude_client_raises_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(KeyError):
        get_claude_client()


def test_get_claude_client_returns_client_with_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    client = get_claude_client()
    assert client is not None
