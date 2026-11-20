import math
from typing import Callable, Sequence


def ks_statistic(values: Sequence[float], cdf: Callable[[float], float]) -> float:
    ordered = sorted(values)
    n = len(ordered)
    if n == 0:
        raise ValueError("Cannot compute KS statistic for empty data")
    maximum = 0.0
    for i, value in enumerate(ordered, start=1):
        d_plus = i / n - cdf(value)
        d_minus = cdf(value) - (i - 1) / n
        maximum = max(maximum, d_plus, d_minus)
    return maximum


def chi_square(observed: Sequence[int], expected: Sequence[float]) -> float:
    if len(observed) != len(expected):
        raise ValueError("Observed and expected values must have the same length")
    return sum(
        (observed_i - expected_i) ** 2 / expected_i
        for observed_i, expected_i in zip(observed, expected)
        if expected_i > 0
    )


def qq_coordinates(values: Sequence[float], quantile: Callable[[float], float]) -> tuple:
    ordered = sorted(values)
    n = len(ordered)
    theoretical = [quantile((i + 0.5) / n) for i in range(n)]
    return theoretical, ordered


def qq_plot(values: Sequence[float], quantile: Callable[[float], float], path: str) -> str:
    theoretical, sample = qq_coordinates(values, quantile)
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError("Install matplotlib to generate QQ plots") from exc
    plt.figure()
    plt.scatter(theoretical, sample)
    plt.xlabel("Theoretical quantiles")
    plt.ylabel("Sample quantiles")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def aic(log_likelihood: float, parameter_count: int) -> float:
    return 2 * parameter_count - 2 * log_likelihood


def bic(log_likelihood: float, parameter_count: int, sample_count: int) -> float:
    return parameter_count * math.log(sample_count) - 2 * log_likelihood


ks_test = ks_statistic
chi_square_test = chi_square
qqplot = qq_plot
