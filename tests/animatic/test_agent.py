import pytest

from agents.animatic.agent import generate_timeline
from agents.animatic.validators import validate_timeline


def test_generate_timeline_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        generate_timeline([])


def test_validate_timeline_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        validate_timeline(None)
