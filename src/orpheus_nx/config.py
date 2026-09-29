from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(slots=True)
class EngineConfig:
    window_size: int = 48
    contamination: float = 0.03
    graph_tau: float = 0.7
    graph_neighbors: int = 4
    robust_weight: float = 0.28
    isolation_weight: float = 0.27
    graph_weight: float = 0.30
    change_weight: float = 0.15
    alert_quantile: float = 0.985
    random_state: int = 42

    def normalized_weights(self) -> tuple[float, float, float, float]:
        values = [self.robust_weight, self.isolation_weight, self.graph_weight, self.change_weight]
        total = sum(values)
        if total <= 0:
            raise ValueError("At least one fusion weight must be positive")
        return tuple(v / total for v in values)  # type: ignore[return-value]

    @classmethod
    def from_json(cls, path: str | Path) -> "EngineConfig":
        with open(path, "r", encoding="utf-8") as f:
            return cls(**json.load(f))

    def to_dict(self) -> dict:
        return asdict(self)
