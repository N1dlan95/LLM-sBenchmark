import argparse
import json
from pathlib import Path

from src.pipeline.runner import ExperimentRunner


def load_config(path: str = "config/experiment.yaml") -> dict:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(path)
    try:
        import yaml

        with config_path.open("r", encoding="utf-8") as stream:
            return yaml.safe_load(stream) or {}
    except ImportError:
        result = {}
        with config_path.open("r", encoding="utf-8") as stream:
            for line in stream:
                if ":" in line and not line.lstrip().startswith("#"):
                    key, value = line.split(":", 1)
                    result[key.strip()] = value.strip().strip("'\"")
        return result


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM benchmark runner")
    parser.add_argument("--config", default="config/experiment.yaml")
    parser.add_argument("--init-db", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    db_path = config.get("database", "data/experiment.db")
    runner = ExperimentRunner(db_path=db_path)
    if args.init_db:
        print(json.dumps({"database": runner.db_path, "status": "initialized"}))


if __name__ == "__main__":
    main()
