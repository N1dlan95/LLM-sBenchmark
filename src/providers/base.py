"""Abstract base class for LLM providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ProviderResponse:
    """Standardized response returned by any LLMProvider."""

    text: str
    latency_ms: float
    model_name: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    raw: Any = None


class LLMProvider(ABC):
    """Strategy interface for querying different LLM APIs uniformly."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    @abstractmethod
    def ask(self, prompt: str, temperature: float = 0.0, **kwargs: Any) -> ProviderResponse:
        """Send a prompt to the LLM and return a standardized ProviderResponse."""
