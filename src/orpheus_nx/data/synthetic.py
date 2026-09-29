from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass(slots=True)
class SyntheticScenario:
    frame: pd.DataFrame
    anomaly_indices: list[int]


def generate_critical_grid(
    n_steps: int = 900,
    n_nodes: int = 10,
    anomaly_fraction: float = 0.025,
    seed: int = 42,
) -> SyntheticScenario:
    """Synthetic correlated infrastructure telemetry with planted anomalies.

    Signals are generated from latent demand, weather, periodicity and local noise.
    Injected incidents include spikes, collective drifts and topology-breaking events.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(n_steps)
    daily = np.sin(2 * np.pi * t / 96)
    harmonic = 0.45 * np.sin(2 * np.pi * t / 31 + 0.7)
    random_walk = np.cumsum(rng.normal(0, 0.018, n_steps))
    latent = 2.0 * daily + harmonic + random_walk

    loadings = rng.uniform(0.7, 1.4, size=n_nodes)
    offsets = rng.normal(10.0, 1.4, size=n_nodes)
    data = np.column_stack([
        offsets[j] + loadings[j] * latent + rng.normal(0, 0.22 + j * 0.01, n_steps)
        for j in range(n_nodes)
    ])

    n_anom = max(8, int(n_steps * anomaly_fraction))
    candidates = np.arange(max(80, int(n_steps * 0.50)), n_steps - 20)
    chosen = sorted(rng.choice(candidates, size=n_anom, replace=False).tolist())
    truth: set[int] = set()
    for idx_pos, i in enumerate(chosen):
        mode = idx_pos % 3
        if mode == 0:
            node = int(rng.integers(0, n_nodes))
            data[i, node] += rng.choice([-1, 1]) * rng.uniform(4.5, 7.0)
            truth.add(i)
        elif mode == 1:
            width = int(rng.integers(4, 10))
            nodes = rng.choice(n_nodes, size=max(2, n_nodes // 3), replace=False)
            drift = rng.choice([-1, 1]) * rng.uniform(1.2, 2.0)
            end = min(i + width, n_steps)
            data[i:end, nodes] += drift
            truth.update(range(i, end))
        else:
            a, b = rng.choice(n_nodes, size=2, replace=False)
            # break normal graph smoothness: two related signals diverge sharply
            data[i, a] += 3.8
            data[i, b] -= 3.8
            truth.add(i)

    columns = [f"node_{i:02d}" for i in range(n_nodes)]
    frame = pd.DataFrame(data, columns=columns)
    frame.insert(0, "timestamp", pd.date_range("2026-01-01", periods=n_steps, freq="15min"))
    return SyntheticScenario(frame=frame, anomaly_indices=sorted(truth))
