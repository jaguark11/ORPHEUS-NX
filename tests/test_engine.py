import numpy as np
from orpheus_nx.data.synthetic import generate_critical_grid
from orpheus_nx.engine import OrpheusEngine


def test_engine_scores_planted_events_above_background():
    s = generate_critical_grid(n_steps=700, n_nodes=8, seed=22)
    engine = OrpheusEngine().fit(s.frame.iloc[:280])
    bundle = engine.score(s.frame)
    truth = np.asarray(s.anomaly_indices)
    normal = np.setdiff1d(np.arange(len(s.frame)), truth)
    assert bundle.fused[truth].mean() > bundle.fused[normal].mean()
    assert bundle.fused.max() <= 1.0
    assert bundle.fused.min() >= 0.0


def test_explanation_has_components():
    s = generate_critical_grid(n_steps=500, n_nodes=6, seed=3)
    engine = OrpheusEngine().fit(s.frame.iloc[:220])
    exp = engine.explain_row(s.frame, s.anomaly_indices[0])
    assert 0.0 <= exp["fused_score"] <= 1.0
    assert len(exp["top_features"]) == 3
    assert len(exp["neighbor_disagreement"]) == 6
