from orpheus_nx.data.synthetic import generate_critical_grid
from orpheus_nx.engine import OrpheusEngine

scenario = generate_critical_grid(n_steps=700, n_nodes=8, seed=7)
engine = OrpheusEngine().fit(scenario.frame.iloc[:300])
result = engine.score(scenario.frame)

print("threshold:", result.threshold)
print("alerts:", result.anomaly_indices[:10].tolist())
if len(result.anomaly_indices):
    print(engine.explain_row(scenario.frame, int(result.anomaly_indices[0])))
