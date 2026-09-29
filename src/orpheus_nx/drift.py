from __future__ import annotations

import numpy as np

EPS = 1e-9


def population_stability_index(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    """Population Stability Index averaged across features.

    PSI is a pragmatic operational drift statistic, not a hypothesis test.
    """
    ref = np.asarray(reference, dtype=float)
    cur = np.asarray(current, dtype=float)
    if ref.ndim == 1:
        ref = ref[:, None]
        cur = cur[:, None]
    values = []
    for j in range(ref.shape[1]):
        edges = np.unique(np.quantile(ref[:, j], np.linspace(0, 1, bins + 1)))
        if len(edges) < 3:
            values.append(0.0)
            continue
        edges[0], edges[-1] = -np.inf, np.inf
        rp = np.histogram(ref[:, j], bins=edges)[0].astype(float)
        cp = np.histogram(cur[:, j], bins=edges)[0].astype(float)
        rp = np.maximum(rp / max(rp.sum(), 1.0), EPS)
        cp = np.maximum(cp / max(cp.sum(), 1.0), EPS)
        values.append(float(np.sum((cp - rp) * np.log(cp / rp))))
    return float(np.mean(values))


def symmetric_gaussian_kl(reference: np.ndarray, current: np.ndarray) -> float:
    """Symmetric KL approximation between diagonal Gaussian feature marginals."""
    ref = np.asarray(reference, dtype=float)
    cur = np.asarray(current, dtype=float)
    mr, mc = ref.mean(axis=0), cur.mean(axis=0)
    vr, vc = ref.var(axis=0) + EPS, cur.var(axis=0) + EPS
    kl_rc = 0.5 * np.sum(np.log(vc / vr) + (vr + (mr - mc) ** 2) / vc - 1)
    kl_cr = 0.5 * np.sum(np.log(vr / vc) + (vc + (mc - mr) ** 2) / vr - 1)
    return float(0.5 * (kl_rc + kl_cr) / ref.shape[1])
