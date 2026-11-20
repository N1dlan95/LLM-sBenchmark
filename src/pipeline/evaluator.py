"""Automatic grading and manual audit support for LLM responses."""

from dataclasses import dataclass
from pathlib import Path
import re

from src.db import get_connection


@dataclass(slots=True)
class GradeResult:
    """Evaluation outcome for a single response."""

    response_id: int
    is_hallucination: bool
    evaluation_method: str
    notes: str | None = None


def normalize_text(value: str) -> str:
    """Normalize whitespace and casing for deterministic comparison."""
    return re.sub(r"\s+", " ", value.strip().lower())


class Evaluator:
    """Evaluates responses automatically and supports manual audit overrides."""

    def __init__(self, db_path: str | Path = "data/experiment.db") -> None:
        self.db_path = db_path

    def auto_grade_pending(self, run_id: int | None = None) -> list[GradeResult]:
        """Automatically grade ungraded responses by checking if expected_answer appears."""
        sql = """
            SELECT r.id AS response_id, r.raw_response, q.expected_answer
            FROM responses r
            JOIN questions q ON q.id = r.question_id
            LEFT JOIN grades g ON g.response_id = r.id
            WHERE g.id IS NULL
        """
        params: tuple = ()
        if run_id is not None:
            sql += " AND r.run_id = ?"
            params = (run_id,)

        results: list[GradeResult] = []
        with get_connection(self.db_path) as conn:
            rows = conn.execute(sql, params).fetchall()
            for row in rows:
                expected = normalize_text(row["expected_answer"])
                actual = normalize_text(row["raw_response"])
                is_hallucination = expected not in actual
                grade = GradeResult(
                    response_id=int(row["response_id"]),
                    is_hallucination=is_hallucination,
                    evaluation_method="auto",
                    notes="Expected answer matched" if not is_hallucination else "Expected answer missing",
                )
                conn.execute(
                    """
                    INSERT INTO grades (response_id, is_hallucination, evaluation_method, notes)
                    VALUES (?, ?, ?, ?)
                    """,
                    (grade.response_id, int(grade.is_hallucination), grade.evaluation_method, grade.notes),
                )
                results.append(grade)
            conn.commit()
        return results

    def record_manual_audit(
        self, response_id: int, is_hallucination: bool, notes: str | None = None
    ) -> None:
        """Insert or update a manual audit grade for a response."""
        with get_connection(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO grades (response_id, is_hallucination, evaluation_method, notes)
                VALUES (?, ?, 'manual', ?)
                ON CONFLICT(response_id) DO UPDATE SET
                    is_hallucination = excluded.is_hallucination,
                    evaluation_method = 'manual',
                    notes = excluded.notes,
                    graded_at = CURRENT_TIMESTAMP
                """,
                (response_id, int(is_hallucination), notes),
            )
            conn.commit()
