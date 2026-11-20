"""Google GenAI SDK provider implementation."""

import os
import time
from typing import Any

from .base import LLMProvider, ProviderResponse


class GeminiProvider(LLMProvider):
    """LLMProvider implementation backed by the Google GenAI SDK."""

    def __init__(self, model_name: str = "gemini-2.5-flash", api_key: str | None = None) -> None:
        super().__init__(model_name)
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise ImportError(
                "google-genai is required for GeminiProvider. Install it with: pip install google-genai"
            ) from exc

        resolved_key = api_key or os.getenv("GEMINI_API_KEY")
        self._client = genai.Client(api_key=resolved_key)
        self._types = types

    def ask(self, prompt: str, temperature: float = 0.0, **kwargs: Any) -> ProviderResponse:
        """Query Gemini and return a standardized ProviderResponse."""
        config = self._types.GenerateContentConfig(temperature=temperature, **kwargs)
        start = time.perf_counter()
        response = self._client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config,
        )
        latency_ms = (time.perf_counter() - start) * 1000.0

        usage = getattr(response, "usage_metadata", None)
        return ProviderResponse(
            text=(response.text or "").strip(),
            latency_ms=latency_ms,
            model_name=self.model_name,
            input_tokens=getattr(usage, "prompt_token_count", None),
            output_tokens=getattr(usage, "candidates_token_count", None),
            raw=response,
        )
