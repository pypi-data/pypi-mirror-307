"""Utility functions for distance calculations in qubit measurement analysis."""

from typing import Any, Iterable
import numpy as np


def sspd_to(
    source: Iterable,
    other: Iterable,
    xp: Any,
    method: str = "cross_product",
) -> np.ndarray:
    """
    Compute SSPD from source to target.

    Args:
        self_values: The values of the source.
        other: The target to compute SSPD to.
        xp: The ArrayModule instance for computation.
        method: The method to use for SSPD computation. Either 'cross_product' (default) or 'pairwise'.
    """
    if method not in ["cross_product", "pairwise"]:
        raise ValueError("Method must be either 'cross_product' or 'pairwise'")

    return _compute_sspd(source, other, xp=xp, method=method)


def _compute_sspd(source, target, xp, method):
    """
    Args:
        source: array of shape (N1, ch, L1) or (ch, L1)
        target: array of shape (N2, ch, L2) or (ch, L2)
        xp: array module instance
        method: 'pairwise' or 'cross_product'
    """
    N1, ch, _ = source.shape if source.ndim == 3 else (1, *source.shape)
    N2, ch, _ = target.shape if target.ndim == 3 else (1, *target.shape)
    source_indexing = lambda idx: (slice(None), idx) if source.ndim == 3 else idx
    target_indexing = lambda idx: (slice(None), idx) if target.ndim == 3 else idx

    if method == "cross_product":
        result = np.empty((ch, N1, N2))
        for idx in range(ch):
            result[idx] = xp.sspd_cross_product(
                source[source_indexing(idx)], target[target_indexing(idx)]
            )
    else:  # pairwise
        result = np.empty((ch, N1))
        for idx in range(ch):
            result[idx] = xp.sspd_pairwise(
                source[source_indexing(idx)], target[target_indexing(idx)]
            )
    return result
