"""Statistical modeling and goodness-of-fit validation modules."""

from .continuous import ContinuousFit, fit_lognormal, fit_normal, fit_shifted_exponential
from .discrete import DiscreteFit, fit_binomial, fit_geometric, fit_negative_binomial
from .validation import ValidationReport, compute_aic_bic, ks_test, chi_square_test

__all__ = [
    "DiscreteFit",
    "fit_binomial",
    "fit_geometric",
    "fit_negative_binomial",
    "ContinuousFit",
    "fit_normal",
    "fit_shifted_exponential",
    "fit_lognormal",
    "ValidationReport",
    "compute_aic_bic",
    "ks_test",
    "chi_square_test",
]
