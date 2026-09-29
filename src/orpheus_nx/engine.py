from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from .config import EngineConfig
from .features import temporal_feature_matrix
from .math.robust import robust_location_scale, robust_zscore, ShrunkMahalanobis
from .math.graph import GraphSpectralResidual
from .math.changepoint import PageHinkleyBank
from .models.fusion import WeightedTailFusion
from .explain import top_contributors


@dataclass(slots=True)
class ScoreBundle:
    fused: np.ndarray
    calibrated: np.ndarray
    threshold: float
    anomaly_indices: np.ndarray


class OrpheusEngine:
    """Hybrid unsupervised detector designed for multivariate operational telemetry."""

    def __init__(self, config: EngineConfig | None = None):
        self.config = config or EngineConfig()
        self.fitted_ = False

    @staticmethod
    def _clean_frame(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
        numeric = frame.select_dtypes(include=[np.number]).copy()
        if numeric.empty:
            raise ValueError("At least one numeric telemetry column is required")
        numeric = numeric.interpolate(limit_direction="both").ffill().bfill()
        return numeric, list(numeric.columns)

    def fit(self, frame: pd.DataFrame) -> "OrpheusEngine":
        numeric, names = self._clean_frame(frame)
        x = numeric.to_numpy(dtype=float)
        if len(x) < max(20, self.config.window_size):
            raise ValueError("Insufficient baseline samples for fit")

        self.names_ = names
        self.center_, self.scale_ = robust_location_scale(x)
        self.mahal_ = ShrunkMahalanobis().fit(x)
        robust = self._robust_component(x)

        features = temporal_feature_matrix(x, self.config.window_size)
        self.isolation_ = IsolationForest(
            n_estimators=240,
            contamination=self.config.contamination,
            random_state=self.config.random_state,
            n_jobs=-1,
        ).fit(features)
        isolation = -self.isolation_.score_samples(features)

        self.graph_ = GraphSpectralResidual(
            tau=self.config.graph_tau, k=self.config.graph_neighbors
        ).fit(x, names)
        graph = self.graph_.score_samples(x)

        self.change_ = PageHinkleyBank().fit(x)
        change = self.change_.score_sequence(x)

        self.fusion_ = WeightedTailFusion(self.config.normalized_weights()).fit(
            [robust, isolation, graph, change]
        )
        fused, _ = self.fusion_.transform([robust, isolation, graph, change])
        self.threshold_ = float(np.quantile(fused, self.config.alert_quantile))
        self.fitted_ = True
        return self

    def _robust_component(self, x: np.ndarray) -> np.ndarray:
        z = robust_zscore(x, self.center_, self.scale_)
        local = np.sqrt(np.mean(z * z, axis=1))
        global_d = self.mahal_.score_samples(x)
        # normalize global distance by dimension for scale stability
        global_d = global_d / np.sqrt(max(x.shape[1], 1))
        return 0.55 * local + 0.45 * global_d

    def score(self, frame: pd.DataFrame) -> ScoreBundle:
        if not self.fitted_:
            raise RuntimeError("Engine must be fitted before scoring")
        numeric = frame[self.names_].copy().interpolate(limit_direction="both").ffill().bfill()
        x = numeric.to_numpy(dtype=float)
        robust = self._robust_component(x)
        features = temporal_feature_matrix(x, self.config.window_size)
        isolation = -self.isolation_.score_samples(features)
        graph = self.graph_.score_samples(x)
        change = self.change_.score_sequence(x)
        fused, calibrated = self.fusion_.transform([robust, isolation, graph, change])
        idx = np.flatnonzero(fused >= self.threshold_)
        return ScoreBundle(fused=fused, calibrated=calibrated, threshold=self.threshold_, anomaly_indices=idx)

    def explain_row(self, frame: pd.DataFrame, index: int) -> dict:
        if not self.fitted_:
            raise RuntimeError("Engine must be fitted before explaining")
        numeric = frame[self.names_].copy().interpolate(limit_direction="both").ffill().bfill()
        x = numeric.to_numpy(dtype=float)
        if index < 0 or index >= len(x):
            raise IndexError(index)
        bundle = self.score(numeric)
        row = x[index]
        c = bundle.calibrated[index]
        return {
            "node": f"observation_{index}",
            "fused_score": float(bundle.fused[index]),
            "robust_score": float(c[0]),
            "isolation_score": float(c[1]),
            "graph_score": float(c[2]),
            "change_score": float(c[3]),
            "top_features": top_contributors(row, self.center_, self.scale_, self.names_),
            "neighbor_disagreement": self.graph_.node_disagreement(row),
        }
