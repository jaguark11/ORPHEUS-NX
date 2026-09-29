from __future__ import annotations

import pandas as pd
from fastapi import FastAPI, HTTPException

from .engine import OrpheusEngine
from .schemas import FitRequest, ScoreRequest, ScoreResponse, NodeExplanation

app = FastAPI(
    title="ORPHEUS-NX",
    version="0.1.0",
    description="Probabilistic graph intelligence for multivariate operational telemetry.",
)
engine = OrpheusEngine()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "fitted": engine.fitted_}


@app.post("/fit")
def fit(req: FitRequest) -> dict:
    try:
        frame = pd.DataFrame(req.records)
        engine.fit(frame)
        return {"status": "fitted", "features": engine.names_, "threshold": engine.threshold_}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/score", response_model=ScoreResponse)
def score(req: ScoreRequest) -> ScoreResponse:
    if not engine.fitted_:
        raise HTTPException(status_code=409, detail="Model is not fitted")
    try:
        frame = pd.DataFrame(req.records)
        bundle = engine.score(frame)
        explanations = [
            NodeExplanation(**engine.explain_row(frame, int(i))) for i in bundle.anomaly_indices[:25]
        ]
        return ScoreResponse(
            threshold=bundle.threshold,
            anomaly_indices=bundle.anomaly_indices.tolist(),
            scores=bundle.fused.tolist(),
            explanations=explanations,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def run() -> None:
    import uvicorn
    uvicorn.run("orpheus_nx.api:app", host="0.0.0.0", port=8000, reload=False)
