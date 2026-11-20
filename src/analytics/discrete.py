"""Discrete probability models: Binomial, Geometric, and Negative Binomial."""

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from scipy import stats


@dataclass(slots=True)
class DiscreteFit:
    """Fitted parameters and log-likelihood for a discrete distribution."""

    distribution: str
    params: dict[str, float]
    log_likelihood: float
    num_params: int


def fit_binomial(hallucination_counts: Sequence[int], n_trials: int) -> DiscreteFit:
    """Fit Binomial(n=n_trials, p) to hallucination counts per batch."""
    data = np.asarray(hallucination_counts, dtype=int)
    p_hat = float(np.clip(data.mean() / n_trials, 1e-9, 1.0 - 1e-9))
    ll = float(np.sum(stats.binom.logpmf(data, n=n_trials, p=p_hat)))
    return DiscreteFit(
        distribution="binomial",
        params={"n": float(n_trials), "p": p_hat},
        log_likelihood=ll,
        num_params=1,
    )


def fit_geometric(trials_until_hallucination: Sequence[int]) -> DiscreteFit:
    """Fit Geometric(p) to 1-indexed trial counts until the first hallucination."""
    data = np.asarray(trials_until_hallucination, dtype=int)
    p_hat = float(np.clip(1.0 / data.mean(), 1e-9, 1.0 - 1e-9))
    ll = float(np.sum(stats.geom.logpmf(data, p=p_hat)))
    return DiscreteFit(
        distribution="geometric",
        params={"p": p_hat},
        log_likelihood=ll,
        num_params=1,
    )


def fit_negative_binomial(failures_before_r_hallucinations: Sequence[int], r: int) -> DiscreteFit:
    """Fit Negative Binomial(r, p) using method of moments for p."""
    data = np.asarray(failures_before_r_hallucinations, dtype=int)
    mean_val = float(data.mean())
    p_hat = float(np.clip(r / (r + mean_val), 1e-9, 1.0 - 1e-9))
    ll = float(np.sum(stats.nbinom.logpmf(data, n=r, p=p_hat)))
    return DiscreteFit(
        distribution="negative_binomial",
        params={"r": float(r), "p": p_hat},
        log_likelihood=ll,
        num_params=1,
    )
