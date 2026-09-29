# Deployment Guide

## Local

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
pytest
orpheus demo
uvicorn orpheus_nx.api:app --host 0.0.0.0 --port 8000
```

Swagger UI is available at `/docs`.

## Docker

```bash
docker compose up --build
```

## Suggested production topology

1. OpenTelemetry / industrial gateway produces metrics.
2. Kafka or Redpanda partitions streams by site or asset domain.
3. Feature service creates aligned windows.
4. ORPHEUS-NX scores windows and writes ranked incidents.
5. Alert router sends high-confidence events to SIEM/ITSM.
6. Analysts inspect the graph explanation before action.

For large fleets, shard by logical dependency graph and maintain separate baselines by operating regime.
