# ADR 0002 — Heat-kernel graph residual for dependency violations

## Status
Accepted.

## Context
Marginal detectors cannot reliably identify situations where each metric is plausible but the relationship among metrics is abnormal.

## Decision
Learn a sparse dependency graph from baseline correlations, construct the normalized Laplacian, and use a heat-kernel low-pass operator. High-frequency residual energy becomes topology anomaly evidence.

## Consequences
The method is mathematically transparent but eigendecomposition is cubic in the number of features. Very large graphs should move to sparse Krylov/Chebyshev approximations.
