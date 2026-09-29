import numpy as np
from orpheus_nx.math.graph import GraphSpectralResidual


def test_graph_residual_reacts_to_topology_break():
    rng = np.random.default_rng(0)
    latent = rng.normal(size=300)
    x = np.column_stack([
        latent + rng.normal(0, 0.05, 300),
        0.9 * latent + rng.normal(0, 0.05, 300),
        -0.7 * latent + rng.normal(0, 0.08, 300),
        0.5 * latent + rng.normal(0, 0.08, 300),
    ])
    detector = GraphSpectralResidual(tau=0.8, k=2).fit(x, ["a", "b", "c", "d"])
    normal = detector.score_samples(x[:20]).mean()
    broken = x[:20].copy()
    broken[:, 0] += 6.0
    broken[:, 1] -= 6.0
    assert detector.score_samples(broken).mean() > normal * 2.0
