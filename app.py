"""CLI entrypoint for the LLM Hallucination Probability Benchmark."""

import argparse
from pathlib import Path
from typing import Any

import yaml

from src.db import init_db
from src.pipeline import BatchRunner, Evaluator, RunnerConfig
from src.providers import GeminiProvider, LLMProvider, OpenAIProvider


def load_config(config_path: Path) -> dict[str, Any]:
    """Load declarative experiment configuration from YAML."""
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_provider(provider_name: str, model_name: str) -> LLMProvider:
    """Instantiate an LLMProvider strategy by provider identifier."""
    registry = {
        "gemini": GeminiProvider,
        "openai": OpenAIProvider,
    }
    if provider_name not in registry:
        raise ValueError(f"Unsupported provider: {provider_name}")
    return registry[provider_name](model_name=model_name)


def cmd_init_db(config: dict[str, Any]) -> None:
    db_path = config["experiment"]["database_path"]
    init_db(db_path)
    print(f"Initialized database at {db_path}")


def cmd_run(config: dict[str, Any], limit: int | None) -> None:
    exp = config["experiment"]
    init_db(exp["database_path"])
    runner_cfg = RunnerConfig(
        experiment_name=exp["name"],
        db_path=exp["database_path"],
        batch_size=int(exp["batch_size"]),
        rate_limit_rpm=int(exp["rate_limit_rpm"]),
        max_retries=int(exp["max_retries"]),
        retry_backoff_seconds=float(exp["retry_backoff_seconds"]),
    )

    for model_cfg in config["models"]:
        provider_name = model_cfg["provider"]
        model_name = model_cfg["model_name"]
        provider = build_provider(provider_name, model_name)
        runner = BatchRunner(provider=provider, config=runner_cfg)
        for temperature in config["temperatures"]:
            run_id = runner.run(provider_name=provider_name, temperature=float(temperature), limit=limit)
            print(f"Completed run_id={run_id} ({provider_name}/{model_name}, T={temperature})")


def cmd_evaluate(config: dict[str, Any], run_id: int | None) -> None:
    evaluator = Evaluator(db_path=config["experiment"]["database_path"])
    grades = evaluator.auto_grade_pending(run_id=run_id)
    hallucinations = sum(1 for g in grades if g.is_hallucination)
    print(f"Graded {len(grades)} responses ({hallucinations} hallucinations detected)")


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM Hallucination Probability Benchmark")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/experiment.yaml"),
        help="Path to experiment YAML configuration.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init-db", help="Initialize the SQLite database schema.")

    run_parser = subparsers.add_parser("run", help="Run experiment batches against configured models.")
    run_parser.add_argument("--limit", type=int, default=None, help="Optional max number of questions.")

    eval_parser = subparsers.add_parser("evaluate", help="Auto-grade pending responses.")
    eval_parser.add_argument("--run-id", type=int, default=None, help="Optional run ID filter.")

    args = parser.parse_args()
    config = load_config(args.config)

    if args.command == "init-db":
        cmd_init_db(config)
    elif args.command == "run":
        cmd_run(config, limit=args.limit)
    elif args.command == "evaluate":
        cmd_evaluate(config, run_id=args.run_id)


if __name__ == "__main__":
    main()
