from __future__ import annotations

import numpy as np


class PageHinkleyBank:
    """Online mean-shift detector applied independently to each signal.

    The output is a continuous severity rather than only a boolean alarm.
    """

    def __init__(self, delta: float = 0.01, threshold: float = 8.0, alpha: float = 0.995):
        self.delta = delta
        self.threshold = threshold
        self.alpha = alpha

    def fit(self, x: np.ndarray) -> "PageHinkleyBank":
        self.mean_ = np.mean(x, axis=0)
        self.scale_ = np.std(x, axis=0) + 1e-9
        return self

    def score_sequence(self, x: np.ndarray) -> np.ndarray:
        m = np.zeros(x.shape[1], dtype=float)
        running = self.mean_.copy()
        scores = []
        for row in x:
            running = self.alpha * running + (1.0 - self.alpha) * row
            standardized = (row - running) / self.scale_
            m = np.maximum(0.0, m + standardized - self.delta)
            scores.append(float(np.max(m / self.threshold)))
        return np.asarray(scores)
