"""Continuous probability models: Normal, Shifted Exponential, and Log-Normal."""

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from scipy import stats


@dataclass(slots=True)
class ContinuousFit:
    """Fitted parameters and log-likelihood for a continuous distribution."""

    distribution: str
    params: tuple[float, ...]
    log_likelihood: float
    num_params: int


def fit_normal(observations: Sequence[float]) -> ContinuousFit:
    """Fit Normal(loc, scale) by maximum likelihood."""
    data = np.asarray(observations, dtype=float)
    loc, scale = stats.norm.fit(data)
    ll = float(np.sum(stats.norm.logpdf(data, loc=loc, scale=scale)))
    return ContinuousFit(
        distribution="norm",
        params=(float(loc), float(scale)),
        log_likelihood=ll,
        num_params=2,
    )


def fit_shifted_exponential(observations: Sequence[float]) -> ContinuousFit:
    """Fit shifted Exponential(loc, scale) to positive metrics such as latency."""
    data = np.asarray(observations, dtype=float)
    loc, scale = stats.expon.fit(data)
    ll = float(np.sum(stats.expon.logpdf(data, loc=loc, scale=scale)))
    return ContinuousFit(
        distribution="expon",
        params=(float(loc), float(scale)),
        log_likelihood=ll,
        num_params=2,
    )


def fit_lognormal(observations: Sequence[float]) -> ContinuousFit:
    """Fit Log-Normal(s, loc=0, scale) to strictly positive observations."""
    data = np.asarray(observations, dtype=float)
    s, loc, scale = stats.lognorm.fit(data, floc=0)
    ll = float(np.sum(stats.lognorm.logpdf(data, s, loc=loc, scale=scale)))
    return ContinuousFit(
        distribution="lognorm",
        params=(float(s), float(loc), float(scale)),
        log_likelihood=ll,
        num_params=2,
    )
