from fastapi.testclient import TestClient
from orpheus_nx.api import app
from orpheus_nx.data.synthetic import generate_critical_grid


def test_health_and_fit_score_api():
    c = TestClient(app)
    assert c.get("/health").status_code == 200
    s = generate_critical_grid(n_steps=250, n_nodes=4, seed=5)
    train = s.frame.iloc[:130].drop(columns=["timestamp"]).to_dict(orient="records")
    target = s.frame.iloc[130:160].drop(columns=["timestamp"]).to_dict(orient="records")
    assert c.post("/fit", json={"records": train}).status_code == 200
    resp = c.post("/score", json={"records": target})
    assert resp.status_code == 200
    assert "scores" in resp.json()
