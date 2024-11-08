"""Utilitary functions."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any, TypeGuard

if TYPE_CHECKING:
    from numpy.typing import NDArray

    try:
        from dask.typing import DaskCollection
    except ImportError:
        DaskCollection: Any = NDArray  # type: ignore


def is_dask_collection(x: object) -> TypeGuard[DaskCollection]:
    """Check if argument is a dask collection without importing if not necessary.

    Code mostly lifted from xarray.core.is_dask_collection.
    """
    if importlib.util.find_spec("dask"):
        from dask.base import is_dask_collection

        return is_dask_collection(x)
    return False
