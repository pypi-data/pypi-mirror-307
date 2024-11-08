from __future__ import annotations

from ._array_object import Array
from ._dtypes import _integer_dtypes

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

import numpy as np

def take(x: Array, indices: Array, /, *, axis: Optional[int] = None) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.take <numpy.take>`.

    See its docstring for more information.
    """
    if axis is None and x.ndim != 1:
        raise ValueError("axis must be specified when ndim > 1")
    if indices.dtype not in _integer_dtypes:
        raise TypeError("Only integer dtypes are allowed in indexing")
    if indices.ndim != 1:
        raise ValueError("Only 1-dim indices array is supported")
    if x.device != indices.device:
        raise ValueError(f"Arrays from two different devices ({x.device} and {indices.device}) can not be combined.")
    return Array._new(np.take(x._array, indices._array, axis=axis), device=x.device)
