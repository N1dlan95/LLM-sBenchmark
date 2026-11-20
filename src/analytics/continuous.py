import math
from typing import Sequence


def fit_normal(values: Sequence[float]) -> tuple:
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return mean, math.sqrt(variance)


def normal_pdf(value: float, mean: float, std: float) -> float:
    if std <= 0:
        raise ValueError("Standard deviation must be positive")
    return math.exp(-0.5 * ((value - mean) / std) ** 2) / (std * math.sqrt(2 * math.pi))


def fit_exponential_shifted(values: Sequence[float]) -> tuple:
    location = min(values)
    shifted = [value - location for value in values]
    mean = sum(shifted) / len(shifted)
    rate = 1.0 / mean if mean else float("inf")
    return location, rate


def shifted_exponential_pdf(value: float, location: float, rate: float) -> float:
    if value < location:
        return 0.0
    if rate <= 0:
        raise ValueError("Rate must be positive")
    return rate * math.exp(-rate * (value - location))


def fit_log_normal(values: Sequence[float]) -> tuple:
    positive = [value for value in values if value > 0]
    if not positive:
        raise ValueError("Log-normal fitting requires positive values")
    logs = [math.log(value) for value in positive]
    mu = sum(logs) / len(logs)
    variance = sum((value - mu) ** 2 for value in logs) / len(logs)
    return mu, math.sqrt(variance)


fit_normal_distribution = fit_normal
fit_shifted_exponential = fit_exponential_shifted
fit_lognormal = fit_log_normal
