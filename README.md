# ORPHEUS-NX

**Probabilistic Graph Intelligence for Critical Infrastructure Telemetry**

> A hybrid anomaly-intelligence engine that fuses robust multivariate statistics, graph signal processing, temporal Isolation Forests and online change-point evidence into explainable incident scores.

ORPHEUS-NX is designed as a serious portfolio-grade engineering project rather than a notebook demo. It can serve as the analytical core for observability, industrial telemetry, operations integrity, supply-chain monitoring or public-infrastructure anomaly detection.

## Why this exists

Real operational incidents have different geometries. A single sensor can spike, a whole process can drift, a multivariate covariance regime can fail, or several individually normal metrics can violate their dependency topology. One model rarely handles all of these well.

ORPHEUS-NX runs four complementary detectors:

1. **Robust geometry** — MAD z-scores + Ledoit-Wolf Mahalanobis distance.
2. **Temporal isolation** — Isolation Forest over causal rolling features.
3. **Graph spectral residual** — heat-kernel graph smoothing over a learned dependency graph.
4. **Change-point evidence** — Page-Hinkley bank for persistent shifts.

Detector outputs are mapped into empirical tail coordinates and fused into a normalized incident score with per-alert explanations.

## Architecture

```text
Telemetry
   |
   v
Validation & causal features
   |
   +--> Robust MAD / shrinkage Mahalanobis ----+
   +--> Temporal Isolation Forest -------------+--> empirical calibration --> fusion --> alerts
   +--> Graph spectral heat residual ----------+                              |
   +--> Page-Hinkley change evidence ----------+                              +--> explanations
```

See `docs/mathematics.md` for the graph Laplacian / heat-kernel formulation and `docs/architecture.md` for the system view.

## Quick start

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -e ".[dev]"
pytest
orpheus demo --steps 900 --nodes 10
```

Example programmatic use:

```python
from orpheus_nx.data.synthetic import generate_critical_grid
from orpheus_nx.engine import OrpheusEngine

scenario = generate_critical_grid(n_steps=900, n_nodes=10)
engine = OrpheusEngine().fit(scenario.frame.iloc[:400])
result = engine.score(scenario.frame)

print(result.anomaly_indices[:10])
print(engine.explain_row(scenario.frame, int(result.anomaly_indices[0])))
```

## REST API

```bash
uvicorn orpheus_nx.api:app --host 0.0.0.0 --port 8000
```

Endpoints:

- `GET /health`
- `POST /fit`
- `POST /score`
- interactive OpenAPI docs at `/docs`

## Synthetic benchmark

The repository includes a generator for correlated infrastructure-like telemetry. It plants three incident families: isolated spikes, collective drifts, and graph-topology breaks. This gives the repository a reproducible test path without shipping sensitive or proprietary datasets.

```bash
orpheus demo --steps 1200 --nodes 12 --output benchmark.json
```

The CLI returns ROC-AUC, precision, recall, F1, alert count and top-scoring observations.

## Repository layout

```text
src/orpheus_nx/
  api.py                 FastAPI service
  benchmark.py           evaluation utilities
  cli.py                 Typer CLI
  engine.py              orchestration + fusion
  features.py            causal time-series feature generation
  storage.py             SQLite anomaly event store
  data/synthetic.py      reproducible telemetry simulator
  math/robust.py         robust statistics + shrinkage covariance
  math/graph.py          graph Laplacian and heat-kernel residual
  math/changepoint.py    online persistent-shift detector
  models/fusion.py       empirical tail calibration

docs/                    architecture, math, deployment, threat model
examples/                 runnable Python example
tests/                    unit + API tests
.github/workflows/        CI on Python 3.11 and 3.12
Dockerfile                deployable service image
docker-compose.yml        local container orchestration
```

## Engineering properties

- no external data is required for the demo;
- deterministic synthetic scenarios via seeded RNG;
- interpretable detector decomposition;
- correlation graph learned from baseline data;
- graph spectral filtering with normalized Laplacian eigendecomposition;
- robust covariance shrinkage for high-dimensional stability;
- online drift evidence;
- CLI, Python API, HTTP API, tests, container and CI;
- safe by design: telemetry analytics only, no exploitation or surveillance acquisition.

## Where this fits in a real company

A production implementation can sit after OpenTelemetry/Kafka ingestion and before SIEM/ITSM or an operations dashboard. The engine is intentionally independent of the transport layer so teams can integrate Kafka, Redpanda, ClickHouse, TimescaleDB, InfluxDB or cloud-native services without rewriting the mathematical core.

## Roadmap

- streaming adapter for Kafka / Redpanda;
- regime-conditioned baselines and concept-drift monitor;
- low-rank randomized graph filtering for thousands of nodes;
- conformal alert calibration;
- model registry integration;
- OpenTelemetry metrics exporter;
- optional autoencoder detector behind the same fusion interface;
- graph-aware incident clustering across time.

## Safety and operational boundaries

ORPHEUS-NX consumes telemetry provided by authorized systems. It does not compromise endpoints, collect credentials, evade security tools, scrape private devices, or autonomously take enforcement action. See `docs/threat_model.md`.

## License

MIT.

## Verified reference run

The packaged reference run (`benchmark.json`) was executed with seed `42`, 900 timestamps and 10 telemetry signals. The verified run produced ROC-AUC ≈ **0.96445** on the synthetic planted-anomaly scenario. See `VERIFICATION.md` for the exact commands. Metrics are scenario-specific and should not be generalized to real infrastructure without domain validation.
