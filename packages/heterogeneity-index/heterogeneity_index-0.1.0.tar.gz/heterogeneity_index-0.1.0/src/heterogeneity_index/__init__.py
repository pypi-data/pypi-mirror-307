"""Heterogeneity Index computation."""

from .components import (
    compute_components_dask,
    compute_components_numpy,
    compute_components_xarray,
)
from .normalization import (
    apply_coefficients,
    compute_coefficient_hi,
    compute_coefficients_components,
)

__version__ = "0.1.0"


__all__ = [
    "compute_components_dask",
    "compute_components_numpy",
    "compute_components_xarray",
    "apply_coefficients",
    "compute_coefficient_hi",
    "compute_coefficients_components",
]
