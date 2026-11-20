"""Batch runner with rate limiting, retries, and SQLite persistence."""

from dataclasses import dataclass
from pathlib import Path
import time
from typing import Iterable, Sequence

from src.db import get_connection
from src.providers.base import LLMProvider, ProviderResponse


@dataclass(slots=True)
class RunnerConfig:
    """Execution parameters for batch runs."""

    experiment_name: str
    db_path: str | Path = "data/experiment.db"
    batch_size: int = 20
    rate_limit_rpm: int = 30
    max_retries: int = 3
    retry_backoff_seconds: float = 2.0


def _chunked(items: Sequence[dict], size: int) -> Iterable[Sequence[dict]]:
    """Yield slices of items with length up to `size`."""
    for start in range(0, len(items), size):
        yield items[start : start + size]


class BatchRunner:
    """Orchestrates question batches of 20 with rate limiting and retry."""

    def __init__(self, provider: LLMProvider, config: RunnerConfig) -> None:
        self.provider = provider
        self.config = config
        self._min_interval = 60.0 / max(config.rate_limit_rpm, 1)
        self._last_request_at = 0.0

    def _respect_rate_limit(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request_at = time.monotonic()

    def _ask_with_retry(self, prompt: str, temperature: float) -> ProviderResponse:
        last_error: Exception | None = None
        for attempt in range(self.config.max_retries + 1):
            self._respect_rate_limit()
            try:
                return self.provider.ask(prompt=prompt, temperature=temperature)
            except Exception as exc:  # noqa: BLE001 - retry transient SDK/network failures
                last_error = exc
                if attempt < self.config.max_retries:
                    delay = self.config.retry_backoff_seconds * (2**attempt)
                    time.sleep(delay)
        raise RuntimeError(f"Provider call failed after {self.config.max_retries + 1} attempts") from last_error

    def run(self, provider_name: str, temperature: float, limit: int | None = None) -> int:
        """Execute questions in batches and persist the run and responses to SQLite."""
        with get_connection(self.config.db_path) as conn:
            query = "SELECT id, prompt FROM questions ORDER BY id"
            if limit is not None:
                query += f" LIMIT {int(limit)}"
            questions = [dict(row) for row in conn.execute(query).fetchall()]

            cursor = conn.execute(
                """
                INSERT INTO runs (experiment_name, provider, model_name, temperature, batch_size)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.config.experiment_name,
                    provider_name,
                    self.provider.model_name,
                    temperature,
                    self.config.batch_size,
                ),
            )
            run_id = int(cursor.lastrowid)

            for batch in _chunked(questions, self.config.batch_size):
                for question in batch:
                    result = self._ask_with_retry(question["prompt"], temperature)
                    conn.execute(
                        """
                        INSERT INTO responses (
                            run_id, question_id, raw_response, latency_ms, input_tokens, output_tokens
                        )
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            run_id,
                            question["id"],
                            result.text,
                            result.latency_ms,
                            result.input_tokens,
                            result.output_tokens,
                        ),
                    )
                conn.commit()

        return run_id
