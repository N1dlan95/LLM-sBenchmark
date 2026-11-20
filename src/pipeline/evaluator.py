from typing import Iterable, Optional


class Evaluator:
    """Automatic evaluation and support for manual audit scores."""

    def score(
        self,
        answer: str,
        reference_answer: Optional[str] = None,
        *,
        manual: bool = False,
    ) -> float:
        if manual:
            raise ValueError("Manual scores must be supplied through audit_score")
        if reference_answer is None:
            return 0.0
        answer_tokens = set(answer.lower().split())
        reference_tokens = set(reference_answer.lower().split())
        if not reference_tokens:
            return 1.0 if not answer_tokens else 0.0
        return len(answer_tokens & reference_tokens) / len(reference_tokens)

    def audit_score(self, response_id: int, score: float, rationale: str = "") -> dict:
        if not 0 <= score <= 1:
            raise ValueError("Score must be between 0 and 1")
        return {
            "response_id": response_id,
            "score": score,
            "rationale": rationale,
            "manual": True,
        }

    automatic_grade = score
