from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    """Abstract interface shared by all model providers."""

    def __init__(self, model: str, temperature: float = 0.0, **kwargs):
        self.model = model
        self.temperature = temperature
        self.options = kwargs

    @abstractmethod
    def ask(self, prompt: str, temperature: Optional[float] = None, **kwargs) -> str:
        """Send *prompt* and return the provider's text response."""
        raise NotImplementedError
