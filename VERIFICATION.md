# Verification Record

Verified locally on 2026-09-29.

## Commands

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m orpheus_nx.cli demo --steps 900 --nodes 10 --output benchmark.json
python -m compileall -q src
```

## Result

- Test suite: **7 passed**.
- Synthetic benchmark seed: `42`.
- Samples: `900`.
- Signals: `10`.
- Baseline samples: `405`.
- ROC-AUC: approximately **0.96445**.
- Default alert threshold is derived only from baseline scores using the configured empirical quantile.

Precision/recall depend on the alert quantile and incident cost model; the repository intentionally exposes this as configuration rather than presenting a universal threshold.
