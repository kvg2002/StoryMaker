"""Gemini API 래퍼 — 언어·구조 판단(시나리오/샷 리스트/타임라인 생성)과 콘티 이미지 생성을 모두 담당."""
import os

from google import genai


def get_gemini_client() -> genai.Client:
    api_key = os.environ["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key)
