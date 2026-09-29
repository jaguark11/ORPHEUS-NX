from __future__ import annotations

import numpy as np
from sklearn.covariance import LedoitWolf


EPS = 1e-9


def robust_location_scale(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Median/MAD estimator, resilient to sparse contamination."""
    median = np.median(x, axis=0)
    mad = np.median(np.abs(x - median), axis=0)
    scale = 1.4826 * mad
    fallback = np.std(x, axis=0, ddof=1)
    scale = np.where(scale < EPS, np.where(fallback < EPS, 1.0, fallback), scale)
    return median, scale


def robust_zscore(x: np.ndarray, center: np.ndarray, scale: np.ndarray) -> np.ndarray:
    return np.abs((x - center) / (scale + EPS))


class ShrunkMahalanobis:
    """Stable multivariate distance using Ledoit-Wolf covariance shrinkage."""

    def fit(self, x: np.ndarray) -> "ShrunkMahalanobis":
        self.center_ = np.median(x, axis=0)
        cov = LedoitWolf().fit(x)
        self.precision_ = cov.precision_
        return self

    def score_samples(self, x: np.ndarray) -> np.ndarray:
        delta = x - self.center_
        d2 = np.einsum("ij,jk,ik->i", delta, self.precision_, delta)
        return np.sqrt(np.maximum(d2, 0.0))
