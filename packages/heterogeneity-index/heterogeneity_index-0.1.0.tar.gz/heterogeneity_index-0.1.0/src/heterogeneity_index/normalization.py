"""Function to determine normalization coefficients.

This module provides functions to determine the normalization coefficients for
each components.

See :ref:`normalization-coefficients` for details.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, cast

import numpy as np

from .components import COMPONENTS_NAMES

try:
    import xarray as xr

    _has_xarray = True
except ImportError:
    _has_xarray = False

try:
    import dask.array as da

    _has_dask = True
except ImportError:
    _has_dask = False


def compute_coefficients_components(
    components: xr.Dataset | Sequence[np.ndarray | da.Array | xr.DataArray],
) -> dict[str, float]:
    """Find normalization coefficients for all components.

    Coefficients are defined such that components contribute equally to the
    final HI variance.
    This function does not modify components, only returns the coefficients.

    Coefficients are computed over the full range of data contained in input
    parameter ``components``.

    Parameters
    ----------
    components:
        Either a :class:`xarray.Dataset` containing the three components, such as
        returned from :func:`~.components.compute_components_xarray`, or three arrays
        (from Numpy, Dask, or Xarray) in the order defined by
        :data:`~.components.COMPONENTS_NAMES` (by default, ``stdev``, ``skew``,
        ``bimod``).

    Returns
    -------
    coefficients:
        Dictionnary containing coefficients for each component.
    """
    if _has_xarray and isinstance(components, xr.Dataset):
        components = tuple(components[name] for name in COMPONENTS_NAMES)
    components = cast(Sequence[np.ndarray | da.Array | xr.DataArray], components)

    coefficients = {}
    for name, comp in zip(COMPONENTS_NAMES, components, strict=True):
        std: Any  # silence mypy about std being an array
        # There is no standard array API for nanstd, we have to check the type
        if name == "skew":
            comp = np.fabs(comp)
        if _has_xarray and isinstance(comp, xr.DataArray):
            std = comp.std()
        elif _has_dask and isinstance(comp, da.Array):
            std = da.nanstd(comp)
        elif isinstance(comp, np.ndarray):
            std = np.nanstd(comp)
        else:
            raise TypeError(f"Unrecognized array type: {type(comp)}")
        std = float(std)
        if std < 1e-6:
            raise ValueError(f"Found standard deviation near 0 for {name}.")

        coefficients[name] = 1.0 / std

    return coefficients


def compute_coefficient_hi(
    components: xr.Dataset | Sequence[np.ndarray | da.Array | xr.DataArray],
    coefficients: dict[str, float],
    quantile_target: float = 0.95,
    hi_limit: float = 9.5,
    **kwargs: Any,
) -> float:
    """Compute final normalization coefficient for the HI.

    Returns a coefficient to normalize the HI (the sum of the three normalized
    components) such that 95% of its values are below a limit value of *9.5*.
    (These are the default values but can be changed with the parameters
    ``quantile_target`` and ``hi_limit``).

    Parameters
    ----------
    components:
        Either a :class:`xarray.Dataset` containing the three components, such as
        returned from :func:`~.components.compute_components_xarray`, or three arrays
        (from Numpy, Dask, or Xarray) in the order defined by
        :data:`~.components.COMPONENTS_NAMES` (by default, ``stdev``, ``skew``,
        ``bimod``).
    coefficients:
        Dictionnary of the components normalization coefficients.
    quantile_target:
        Fraction of the quantity of HI values that should be below ``hi_limit``
        once normalized. Should be between 0 and 1.
    hi_limit:
        See ``quantile_target``.
    kwargs:
        Arguments passed to :func:`xhistogram.core.histogram`.

    Returns
    -------
    Coefficient to normalize the HI with.
    """
    from scipy import stats
    from xhistogram.core import histogram

    if _has_xarray and isinstance(components, xr.Dataset):
        components = tuple(components[name] for name in COMPONENTS_NAMES)
    components = cast(Sequence[np.ndarray | da.Array | xr.DataArray], components)

    # un-normalized HI
    hi = apply_coefficients(components, coefficients)

    kwargs_defaults = dict(bins=np.linspace(0.0, 80.0, 800 + 1), density=False)
    kwargs = kwargs_defaults | kwargs
    bins = kwargs.pop("bins")
    hist, *_ = histogram(hi, bins=[bins], **kwargs)

    rhist = stats.rv_histogram((hist, bins), density=kwargs["density"])
    # current HI value at quantile target
    current_hi = rhist.ppf(quantile_target)
    coef = hi_limit / current_hi

    return coef


def apply_coefficients(
    components: xr.Dataset | Sequence[np.ndarray | da.Array | xr.DataArray],
    coefficients: Mapping[str, float],
) -> xr.DataArray | np.ndarray | da.Array:
    """Return Heterogeneity Index computed from un-normalized components.

    Parameters
    ----------
    components:
        Either a :class:`xarray.Dataset` containing the three components, such as
        returned from :func:`~.components.compute_components_xarray`, or three arrays
        (from Numpy, Dask, or Xarray) in the order defined by
        :data:`~.components.COMPONENTS_NAMES` (by default, ``stdev``, ``skew``,
        ``bimod``).
    coefficients:
        Dictionnary of the components normalization coefficients.
        If the coefficient for the HI is present, it will be applied, otherwise it will
        be taken equal to 1.

    Returns
    -------
    Normalized HI (single variable).
    """
    if _has_xarray and isinstance(components, xr.Dataset):
        components = tuple(components[name] for name in COMPONENTS_NAMES)
    components = cast(Sequence[np.ndarray | da.Array | xr.DataArray], components)
    components = [c.copy() for c in components]

    comps = dict(zip(COMPONENTS_NAMES, components, strict=True))
    comps["skew"] = np.fabs(comps["skew"])

    for name in comps.keys():
        comps[name] *= coefficients[name]

    hi = comps["stdev"] + comps["skew"] + comps["bimod"]

    if "HI" in coefficients:
        hi *= coefficients["HI"]

    if _has_xarray and isinstance(hi, xr.DataArray):
        hi = hi.rename("HI")

    return hi
