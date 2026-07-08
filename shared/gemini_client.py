"""Gemini API 래퍼 — 콘티 이미지 생성 담당 (Anthropic API는 이미지 생성 미지원)."""
import os

from google import genai


def get_gemini_client() -> genai.Client:
    api_key = os.environ["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key)
