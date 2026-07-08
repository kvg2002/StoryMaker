"""타임라인 JSON 수치 검증 규칙 (기획서 5.6절: 총 길이, 자막 읽기 시간, 연속 컷 등)."""
from agents.animatic.schemas import Timeline


def validate_timeline(timeline: Timeline) -> list[str]:
    raise NotImplementedError
