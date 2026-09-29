# Architecture

```text
                 +-------------------------+
telemetry -----> | validation / imputation | ----+
                 +-------------------------+     |
                                                   v
                          +----------------- feature matrix ----------------+
                          |                      |                           |
                          v                      v                           v
                Robust Geometry        Isolation Forest           Graph Spectral
                MAD + Mahalanobis       temporal context          heat residual
                          |                      |                           |
                          +-----------+----------+---------------------------+
                                      |
                                      v
                               Change-Point Bank
                                      |
                                      v
                            Empirical Tail Calibration
                                      |
                                      v
                               Weighted Fusion
                                      |
                         +------------+-------------+
                         |                          |
                         v                          v
                    anomaly rank               explanations
                                                contributors +
                                                topology residuals
```

## Runtime modes

- **Library**: embed `OrpheusEngine` inside a Python service or notebook.
- **CLI**: synthetic benchmark and CSV scoring.
- **REST**: FastAPI `/fit`, `/score`, `/health`.
- **Container**: Docker image and Compose health check.

## Production extension points

A real deployment would normally add Kafka/Redpanda ingestion, OpenTelemetry collectors, a durable time-series store (ClickHouse/Timescale/InfluxDB), model registry, authn/authz, a scheduler for drift-aware retraining, and a dashboard. Those are intentionally adapters rather than hard requirements so the repository remains runnable on a laptop.
