"""OpenAI SDK provider implementation."""

import os
import time
from typing import Any

from .base import LLMProvider, ProviderResponse


class OpenAIProvider(LLMProvider):
    """LLMProvider implementation backed by the OpenAI Python SDK."""

    def __init__(self, model_name: str = "gpt-4o-mini", api_key: str | None = None) -> None:
        super().__init__(model_name)
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImportError(
                "openai is required for OpenAIProvider. Install it with: pip install openai"
            ) from exc

        resolved_key = api_key or os.getenv("OPENAI_API_KEY")
        self._client = OpenAI(api_key=resolved_key)

    def ask(self, prompt: str, temperature: float = 0.0, **kwargs: Any) -> ProviderResponse:
        """Query OpenAI chat completions and return a standardized ProviderResponse."""
        start = time.perf_counter()
        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            **kwargs,
        )
        latency_ms = (time.perf_counter() - start) * 1000.0

        choice = response.choices[0].message.content or ""
        usage = response.usage
        return ProviderResponse(
            text=choice.strip(),
            latency_ms=latency_ms,
            model_name=self.model_name,
            input_tokens=usage.prompt_tokens if usage else None,
            output_tokens=usage.completion_tokens if usage else None,
            raw=response,
        )
