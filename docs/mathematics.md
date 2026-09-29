# Mathematical Core

ORPHEUS-NX intentionally avoids betting on a single anomaly detector. Operational anomalies can be marginal, multivariate, temporal, or topological; each failure mode has different geometry.

## 1. Robust marginal geometry

For feature `j`, the location is the median and scale is the median absolute deviation (MAD):

`MAD_j = 1.4826 * median(|x_j - median(x_j)|)`

A row-level robust energy is the RMS of absolute robust z-scores. In parallel, a Ledoit-Wolf covariance estimator gives a shrinkage precision matrix `P`. The global distance is

`d_M(x) = sqrt((x - mu)^T P (x - mu))`.

The robust component combines marginal deviation and multivariate covariance violation.

## 2. Graph-spectral topology residual

Features become vertices of a weighted graph. Edges are learned from absolute baseline correlation. Let `L = U Lambda U^T` be the normalized graph Laplacian. A heat kernel

`H_tau = U exp(-tau Lambda) U^T`

acts as a graph low-pass filter. Healthy telemetry tends to remain smooth over the dependency graph. ORPHEUS-NX computes

`r = z - H_tau z`

and the graph anomaly score is the RMS high-frequency energy `||r||_2 / sqrt(d)`. This catches topology-breaking incidents where individually plausible measurements violate relationships between subsystems.

## 3. Temporal isolation geometry

For each timestamp, ORPHEUS-NX constructs a causal feature vector containing current level, first difference, rolling standardized deviation, and volatility ratio. An Isolation Forest estimates how quickly the observation is isolated by random partitions.

## 4. Change-point evidence

A bank of Page-Hinkley recursions tracks persistent upward deviation. This provides a continuous shift severity that reacts differently from point anomaly detectors.

## 5. Empirical tail calibration and fusion

Raw detectors have incompatible scales. Each baseline detector distribution is converted to an empirical CDF rank in `[0,1]`. Four calibrated channels are fused through normalized weights plus an agreement term. This allows one detector to flag a violent local break while giving extra confidence when independent geometries agree.

This is not a probabilistic guarantee; the calibrated scores are empirical tail coordinates over the baseline regime, designed for operational ranking and thresholding.
