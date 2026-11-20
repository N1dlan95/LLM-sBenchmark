import os
from typing import Optional

from .base import LLMProvider


class GeminiProvider(LLMProvider):
    """Google Gemini provider using the Google GenAI SDK."""

    def __init__(
        self,
        model: str = "gemini-2.0-flash",
        temperature: float = 0.0,
        api_key: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(model, temperature, **kwargs)
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

    def ask(self, prompt: str, temperature: Optional[float] = None, **kwargs) -> str:
        try:
            from google import genai

            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={"temperature": temperature if temperature is not None else self.temperature},
            )
            return response.text
        except ImportError:
            try:
                import google.generativeai as genai

                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel(self.model)
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": temperature if temperature is not None else self.temperature
                    },
                )
                return response.text
            except ImportError as exc:
                raise ImportError("Install the Google GenAI SDK ('google-genai')") from exc


Gemini = GeminiProvider
