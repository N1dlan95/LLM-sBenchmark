import os
from typing import Optional

from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI Chat Completions provider."""

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.0,
        api_key: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(model, temperature, **kwargs)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def ask(self, prompt: str, temperature: Optional[float] = None, **kwargs) -> str:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImportError("Install the OpenAI SDK ('openai')") from exc

        client = OpenAI(api_key=self.api_key)
        completion = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature if temperature is not None else self.temperature,
            **kwargs,
        )
        return completion.choices[0].message.content or ""


OpenAI = OpenAIProvider
