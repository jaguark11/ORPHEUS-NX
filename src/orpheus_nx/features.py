from __future__ import annotations

import numpy as np


def temporal_feature_matrix(x: np.ndarray, window: int = 24) -> np.ndarray:
    """Causal rolling features for each timestamp.

    Features: current standardized level, first difference, rolling mean deviation,
    rolling volatility ratio. Kept compact enough for real-time use.
    """
    n, d = x.shape
    out = np.zeros((n, d * 4), dtype=float)
    diff = np.vstack([np.zeros((1, d)), np.diff(x, axis=0)])
    for i in range(n):
        s = max(0, i - window + 1)
        hist = x[s : i + 1]
        mu = hist.mean(axis=0)
        sd = hist.std(axis=0) + 1e-9
        out[i, 0:d] = x[i]
        out[i, d : 2 * d] = diff[i]
        out[i, 2 * d : 3 * d] = (x[i] - mu) / sd
        out[i, 3 * d : 4 * d] = sd / (np.mean(sd) + 1e-9)
    return out
