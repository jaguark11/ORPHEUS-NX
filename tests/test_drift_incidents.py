import numpy as np
from orpheus_nx.drift import population_stability_index, symmetric_gaussian_kl
from orpheus_nx.incidents import group_alerts


def test_drift_statistics_increase_on_shift():
    rng = np.random.default_rng(5)
    a = rng.normal(0, 1, size=(500, 3))
    b = rng.normal(0, 1, size=(500, 3))
    c = rng.normal(1.8, 1.5, size=(500, 3))
    assert population_stability_index(a, c) > population_stability_index(a, b)
    assert symmetric_gaussian_kl(a, c) > symmetric_gaussian_kl(a, b)


def test_incident_grouping():
    s = np.array([0.1, .95, .96, .2, .91, .1, .1, .99])
    incidents = group_alerts(s, .9, max_gap=1)
    assert len(incidents) == 2
    assert incidents[0].start == 1 and incidents[0].end == 4
    assert incidents[1].peak_index == 7
