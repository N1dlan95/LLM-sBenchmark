"""Goodness-of-fit validation: KS test, Chi-square test, QQ-plot, and AIC/BIC."""

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy import stats


@dataclass(slots=True)
class ValidationReport:
    """Summary of goodness-of-fit and information criteria metrics."""

    test_name: str
    statistic: float
    p_value: float
    aic: float
    bic: float


def compute_aic_bic(log_likelihood: float, num_params: int, sample_size: int) -> tuple[float, float]:
    """Compute Akaike (AIC) and Bayesian (BIC) information criteria."""
    aic = 2.0 * num_params - 2.0 * log_likelihood
    bic = num_params * float(np.log(max(sample_size, 1))) - 2.0 * log_likelihood
    return aic, bic


def ks_test(
    observations: Sequence[float],
    cdf_name: str,
    params: tuple[float, ...],
    log_likelihood: float,
    num_params: int,
) -> ValidationReport:
    """Run one-sample Kolmogorov-Smirnov goodness-of-fit test."""
    data = np.asarray(observations, dtype=float)
    result = stats.kstest(data, cdf_name, args=params)
    aic, bic = compute_aic_bic(log_likelihood, num_params, len(data))
    return ValidationReport(
        test_name=f"ks:{cdf_name}",
        statistic=float(result.statistic),
        p_value=float(result.pvalue),
        aic=aic,
        bic=bic,
    )


def chi_square_test(
    observed_counts: Sequence[float],
    expected_counts: Sequence[float],
    log_likelihood: float,
    num_params: int,
) -> ValidationReport:
    """Run Pearson's Chi-square goodness-of-fit test."""
    obs = np.asarray(observed_counts, dtype=float)
    exp = np.asarray(expected_counts, dtype=float)
    result = stats.chisquare(f_obs=obs, f_exp=exp, ddof=num_params)
    aic, bic = compute_aic_bic(log_likelihood, num_params, int(obs.sum()))
    return ValidationReport(
        test_name="chi_square",
        statistic=float(result.statistic),
        p_value=float(result.pvalue),
        aic=aic,
        bic=bic,
    )


def save_qq_plot(
    observations: Sequence[float],
    dist_name: str,
    params: tuple[float, ...],
    output_path: str | Path,
) -> Path:
    """Generate and save a QQ-plot comparing observations against a theoretical distribution."""
    import matplotlib.pyplot as plt

    data = np.asarray(observations, dtype=float)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 6))
    stats.probplot(data, dist=dist_name, sparams=params, plot=ax)
    ax.set_title(f"QQ-Plot ({dist_name})")
    fig.tight_layout()
    fig.savefig(target, dpi=150)
    plt.close(fig)
    return target
