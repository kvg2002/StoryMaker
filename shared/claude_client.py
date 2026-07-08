"""Claude API 래퍼 — 언어·구조 판단(시나리오/샷 리스트/타임라인 생성) 담당."""
import os

import anthropic


def get_claude_client() -> anthropic.Anthropic:
    api_key = os.environ["ANTHROPIC_API_KEY"]
    return anthropic.Anthropic(api_key=api_key)
