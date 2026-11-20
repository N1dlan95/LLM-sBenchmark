"""SQLite database management for experiment runs, questions, responses, and grades."""

import sqlite3
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_name TEXT NOT NULL,
    provider TEXT NOT NULL,
    model_name TEXT NOT NULL,
    temperature REAL NOT NULL,
    batch_size INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    prompt TEXT NOT NULL,
    expected_answer TEXT NOT NULL,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    raw_response TEXT NOT NULL,
    latency_ms REAL NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES runs(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    response_id INTEGER NOT NULL UNIQUE,
    is_hallucination INTEGER NOT NULL CHECK (is_hallucination IN (0, 1)),
    evaluation_method TEXT NOT NULL CHECK (evaluation_method IN ('auto', 'manual')),
    notes TEXT,
    graded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (response_id) REFERENCES responses(id)
);
"""


def get_connection(db_path: str | Path) -> sqlite3.Connection:
    """Open a SQLite connection with foreign keys enabled."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: str | Path) -> None:
    """Create the database tables if they do not exist."""
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
