import math
from typing import Iterable, Sequence


def binomial_pmf(k: int, n: int, p: float) -> float:
    if n < 0 or k < 0 or k > n or not 0 <= p <= 1:
        raise ValueError("Invalid binomial parameters")
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def geometric_pmf(k: int, p: float) -> float:
    if k < 1 or not 0 < p <= 1:
        raise ValueError("Invalid geometric parameters")
    return p * (1 - p) ** (k - 1)


def negative_binomial_pmf(k: int, r: int, p: float) -> float:
    if k < 0 or r < 1 or not 0 < p <= 1:
        raise ValueError("Invalid negative binomial parameters")
    return math.comb(k + r - 1, r - 1) * p ** r * (1 - p) ** k


def fit_binomial(values: Sequence[int]) -> tuple:
    n = max(values)
    mean = sum(values) / len(values)
    p = mean / n if n else 0.0
    return n, p


def fit_geometric(values: Sequence[int]) -> float:
    mean = sum(values) / len(values)
    return 1.0 / mean if mean else 1.0


def fit_negative_binomial(values: Sequence[int]) -> tuple:
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    if variance <= mean:
        return 1, 1.0
    r = mean ** 2 / (variance - mean)
    p = r / (r + mean)
    return r, p


binomial_fit = fit_binomial
geometric_fit = fit_geometric
negative_binomial_fit = fit_negative_binomial
