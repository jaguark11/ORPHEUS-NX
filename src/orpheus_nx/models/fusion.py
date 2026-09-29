from __future__ import annotations

import numpy as np


EPS = 1e-12


class EmpiricalCalibrator:
    """Maps heterogeneous detector scores to empirical [0,1] tail probabilities."""

    def fit(self, scores: np.ndarray) -> "EmpiricalCalibrator":
        self.sorted_ = np.sort(np.asarray(scores, dtype=float))
        return self

    def transform(self, scores: np.ndarray) -> np.ndarray:
        s = np.asarray(scores, dtype=float)
        ranks = np.searchsorted(self.sorted_, s, side="right")
        return ranks / max(len(self.sorted_), 1)


class WeightedTailFusion:
    def __init__(self, weights: tuple[float, float, float, float]):
        self.weights = np.asarray(weights, dtype=float)
        self.calibrators = [EmpiricalCalibrator() for _ in range(4)]

    def fit(self, components: list[np.ndarray]) -> "WeightedTailFusion":
        for cal, score in zip(self.calibrators, components):
            cal.fit(score)
        return self

    def transform(self, components: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
        calibrated = np.column_stack([
            cal.transform(score) for cal, score in zip(self.calibrators, components)
        ])
        # emphasize consensus among detectors while preserving single-detector spikes
        linear = calibrated @ self.weights
        agreement = np.sqrt(np.mean(calibrated * calibrated, axis=1))
        fused = 0.78 * linear + 0.22 * agreement
        return np.clip(fused, 0.0, 1.0), calibrated
