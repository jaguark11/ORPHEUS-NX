# Threat Model and Safety Boundaries

## Assets
- telemetry confidentiality and integrity;
- model thresholds and baseline statistics;
- alert/event history;
- API availability.

## Primary risks
- poisoned baseline data;
- replayed or forged telemetry;
- schema drift;
- unauthorized scoring or event access;
- alert flooding;
- model staleness under seasonal regime changes.

## Mitigations for production
- mTLS between collectors and scoring service;
- signed ingestion envelopes and monotonic sequence IDs;
- RBAC around model fit operations;
- immutable model artifact hashes;
- baseline provenance and quarantine windows;
- rate limiting plus circuit breakers;
- out-of-band operator review for high-impact actions.

ORPHEUS-NX is a detection component. It deliberately excludes offensive security capabilities and does not execute remediation against third-party systems.
