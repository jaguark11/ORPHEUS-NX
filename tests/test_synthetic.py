from orpheus_nx.data.synthetic import generate_critical_grid


def test_synthetic_shape_and_anomalies():
    s = generate_critical_grid(n_steps=400, n_nodes=6, seed=10)
    assert s.frame.shape == (400, 7)  # timestamp + six nodes
    assert len(s.anomaly_indices) >= 8
    assert min(s.anomaly_indices) >= 50
