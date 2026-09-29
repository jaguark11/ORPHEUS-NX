# Productization Notes

ORPHEUS-NX can be positioned as a telemetry intelligence component rather than a monolithic observability product.

## Commercially useful applications

- anomaly detection in industrial sensors and utility operations;
- SRE / cloud telemetry triage across correlated service metrics;
- fraud or process-integrity monitoring where entities form dependency graphs;
- supply-chain and logistics exception detection;
- public-sector infrastructure monitoring using non-classified operational data.

## Why the graph layer matters

Many commercial detectors independently score metrics. That misses relational failures: two values can both look statistically normal while their relationship becomes physically or operationally impossible. The graph spectral residual is designed to expose that class of event.

## Responsible scope

The project analyzes telemetry supplied to it. It does not perform intrusion, credential collection, malware delivery, surveillance acquisition, exploitation, or autonomous enforcement. Decisions should stay with authorized operators.
