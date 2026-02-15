from __future__ import annotations

import os

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel


_RECOMMENDED_MODELS: list[str] = [
    "claude-haiku-3.5-20241022",
    "claude-sonnet-4-20250514",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gpt-4o",
    "gpt-4o-mini",
]


_PROVIDER_PREFIXES: dict[str, str] = {
    "gpt-": "openai",
    "o1": "openai",
    "o3": "openai",
    "o4": "openai",
    "claude-": "anthropic",
    "gemini-": "google",
}


_PROVIDER_ENV_KEYS: dict[str, str] = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
}


def list_models() -> list[str]:
    """추천 LLM 모델 이름 리스트를 반환."""
    return sorted(_RECOMMENDED_MODELS)


def _get_model_name(value: str | int) -> str:
    """str | int → model_name 문자열. 리스트에 없으면 에러."""
    models = list_models()

    if isinstance(value, int):
        if not (0 <= value < len(models)):
            raise IndexError(f"Model 인덱스 {value}가 범위를 벗어났습니다.")
        return models[value]

    for m in models:
        if m == value:
            return m

    raise ValueError(f"알 수 없는 Model: {value}")


def create_llm(value: str | int) -> BaseChatModel:
    """str | int → BaseChatModel 객체. 리스트에 없으면 에러."""
    model_name = _get_model_name(value)

    provider = _resolve_provider(model_name)
    env_key = _PROVIDER_ENV_KEYS[provider]
    api_key = os.environ.get(env_key)
    if not api_key:
        raise ValueError(f"Environment variable '{env_key}' is not set")

    if provider == "openai":
        return ChatOpenAI(model=model_name, openai_api_key=api_key)  # type: ignore[call-arg]
    elif provider == "anthropic":
        return ChatAnthropic(model_name=model_name, anthropic_api_key=api_key, timeout=None, stop=None)  # type: ignore[call-arg]
    elif provider == "google":
        return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)  # type: ignore[call-arg]
    else:
        raise ValueError(f"Unsupported model: {model_name}")


def _resolve_provider(model_name: str) -> str:
    for prefix, provider in _PROVIDER_PREFIXES.items():
        if model_name.startswith(prefix):
            return provider

    # model not found
    raise ValueError(
        f"Cannot determine provider for model '{model_name}'. "
        f"Known prefixes: {list(_PROVIDER_PREFIXES.keys())}"
    )
