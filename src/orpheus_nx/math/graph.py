from __future__ import annotations

import numpy as np
import networkx as nx


EPS = 1e-12


def correlation_graph(x: np.ndarray, names: list[str], k: int = 4) -> nx.Graph:
    """Build a sparse undirected graph from absolute feature correlation."""
    if x.shape[1] != len(names):
        raise ValueError("Feature names must match matrix width")
    corr = np.nan_to_num(np.corrcoef(x, rowvar=False), nan=0.0)
    np.fill_diagonal(corr, 0.0)
    g = nx.Graph()
    g.add_nodes_from(names)
    k = max(1, min(k, max(1, len(names) - 1)))
    for i, src in enumerate(names):
        order = np.argsort(np.abs(corr[i]))[::-1][:k]
        for j in order:
            if i == j:
                continue
            weight = float(abs(corr[i, j]))
            if weight > 0:
                g.add_edge(src, names[j], weight=weight)
    return g


def normalized_laplacian(g: nx.Graph, names: list[str]) -> np.ndarray:
    a = nx.to_numpy_array(g, nodelist=names, weight="weight", dtype=float)
    degree = a.sum(axis=1)
    invsqrt = np.diag(1.0 / np.sqrt(np.maximum(degree, EPS)))
    return np.eye(len(names)) - invsqrt @ a @ invsqrt


class GraphSpectralResidual:
    """Graph-signal high-frequency energy detector.

    A healthy observation is assumed to be smooth over the learned feature graph.
    The detector computes the residual after heat-kernel low-pass filtering:
        H_tau = U exp(-tau Lambda) U^T
        r = x - H_tau x
    """

    def __init__(self, tau: float = 0.7, k: int = 4):
        self.tau = tau
        self.k = k

    def fit(self, x: np.ndarray, names: list[str]) -> "GraphSpectralResidual":
        self.names_ = list(names)
        self.center_ = np.median(x, axis=0)
        scale = np.median(np.abs(x - self.center_), axis=0) * 1.4826
        self.scale_ = np.where(scale < 1e-9, np.std(x, axis=0) + 1e-9, scale)
        self.graph_ = correlation_graph(x, self.names_, self.k)
        lap = normalized_laplacian(self.graph_, self.names_)
        vals, vecs = np.linalg.eigh(lap)
        filt = np.exp(-self.tau * vals)
        self.heat_kernel_ = (vecs * filt) @ vecs.T
        return self

    def residual_matrix(self, x: np.ndarray) -> np.ndarray:
        z = (x - self.center_) / self.scale_
        smooth = z @ self.heat_kernel_.T
        return z - smooth

    def score_samples(self, x: np.ndarray) -> np.ndarray:
        r = self.residual_matrix(x)
        return np.sqrt(np.mean(r * r, axis=1))

    def node_disagreement(self, row: np.ndarray) -> dict[str, float]:
        r = self.residual_matrix(row.reshape(1, -1))[0]
        return {name: float(abs(v)) for name, v in zip(self.names_, r)}
