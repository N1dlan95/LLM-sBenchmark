import sqlite3
import time
from pathlib import Path
from typing import Iterable, List, Optional

from src.providers.base import LLMProvider


class ExperimentRunner:
    """Runs benchmark batches, persists data, and retries transient failures."""

    def __init__(
        self,
        db_path: str = "data/experiment.db",
        batch_size: int = 20,
        requests_per_minute: int = 60,
        retries: int = 3,
        retry_delay: float = 1.0,
    ):
        self.db_path = str(db_path)
        self.batch_size = batch_size
        self.requests_per_minute = requests_per_minute
        self.retries = retries
        self.retry_delay = retry_delay
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_db(self) -> None:
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    provider TEXT NOT NULL,
                    model TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    reference_answer TEXT,
                    metadata TEXT
                );
                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    answer TEXT,
                    error TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(run_id) REFERENCES runs(id),
                    FOREIGN KEY(question_id) REFERENCES questions(id)
                );
                CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    response_id INTEGER UNIQUE,
                    score REAL,
                    rationale TEXT,
                    manual INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY(response_id) REFERENCES responses(id)
                );
                """
            )

    def add_questions(self, prompts: Iterable[str]) -> None:
        with self._connect() as db:
            db.executemany(
                "INSERT INTO questions(prompt) VALUES (?)",
                [(prompt,) for prompt in prompts],
            )

    def run(
        self,
        provider: LLMProvider,
        prompts: Optional[Iterable[str]] = None,
        temperature: Optional[float] = None,
    ) -> int:
        with self._connect() as db:
            cursor = db.execute(
                "INSERT INTO runs(provider, model, temperature, status) VALUES (?, ?, ?, 'running')",
                (
                    provider.__class__.__name__,
                    provider.model,
                    provider.temperature if temperature is None else temperature,
                ),
            )
            run_id = cursor.lastrowid
            if prompts is None:
                questions = db.execute("SELECT id, prompt FROM questions").fetchall()
            else:
                questions = []
                for prompt in prompts:
                    cursor = db.execute("INSERT INTO questions(prompt) VALUES (?)", (prompt,))
                    questions.append({"id": cursor.lastrowid, "prompt": prompt})

        interval = 60.0 / max(1, self.requests_per_minute)
        for start in range(0, len(questions), self.batch_size):
            batch = questions[start:start + self.batch_size]
            for index, question in enumerate(batch):
                answer = None
                error = None
                for attempt in range(self.retries + 1):
                    try:
                        answer = provider.ask(
                            question["prompt"],
                            temperature=temperature,
                        )
                        break
                    except Exception as exc:
                        error = str(exc)
                        if attempt < self.retries:
                            time.sleep(self.retry_delay * (2 ** attempt))
                with self._connect() as db:
                    db.execute(
                        "INSERT INTO responses(run_id, question_id, answer, error) VALUES (?, ?, ?, ?)",
                        (run_id, question["id"], answer, error),
                    )
                if (start + index + 1) % max(1, self.batch_size) != 0:
                    time.sleep(interval)

        with self._connect() as db:
            db.execute("UPDATE runs SET status = 'completed' WHERE id = ?", (run_id,))
        return int(run_id)

    run_batch = run
