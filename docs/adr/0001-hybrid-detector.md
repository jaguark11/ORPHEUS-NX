# ADR 0001 — Use a hybrid detector instead of a single deep model

## Status
Accepted.

## Context
Operational datasets often have few labels and multiple anomaly geometries. A large neural model would create training, explainability and dependency costs without guaranteeing better behavior on sparse tabular telemetry.

## Decision
Use four heterogeneous detectors and calibrate them into a shared empirical tail coordinate. This separates geometry from fusion and lets teams replace individual detectors without rewriting the system.

## Consequences
The engine is interpretable and works without GPUs. It can also fail when the baseline is not representative; production deployments need regime segmentation and drift monitoring.
