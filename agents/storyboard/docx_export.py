"""팀 표준 5컬럼 워드 출력 (기획서 4.8절)."""
from pathlib import Path

from agents.storyboard.schemas import StoryboardOutput


def export_docx(storyboard: StoryboardOutput, path: Path) -> None:
    raise NotImplementedError
