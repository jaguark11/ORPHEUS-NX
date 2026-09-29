from __future__ import annotations

from typing import Dict, List
from pydantic import BaseModel, Field


class FitRequest(BaseModel):
    records: List[Dict[str, float]] = Field(min_length=20)


class ScoreRequest(BaseModel):
    records: List[Dict[str, float]] = Field(min_length=1)


class NodeExplanation(BaseModel):
    node: str
    fused_score: float
    robust_score: float
    isolation_score: float
    graph_score: float
    change_score: float
    top_features: List[str]
    neighbor_disagreement: Dict[str, float]


class ScoreResponse(BaseModel):
    threshold: float
    anomaly_indices: List[int]
    scores: List[float]
    explanations: List[NodeExplanation]
