from __future__ import annotations

import json
from pathlib import Path
import typer
import pandas as pd

from .benchmark import evaluate
from .config import EngineConfig
from .data.synthetic import generate_critical_grid
from .engine import OrpheusEngine

app = typer.Typer(help="ORPHEUS-NX command-line interface")


@app.command()
def demo(
    steps: int = typer.Option(900, min=200),
    nodes: int = typer.Option(10, min=3),
    seed: int = 42,
    output: Path | None = typer.Option(None),
) -> None:
    """Run a complete synthetic incident-detection benchmark."""
    scenario = generate_critical_grid(steps, nodes, seed=seed)
    baseline_n = max(120, int(steps * 0.45))
    baseline = scenario.frame.iloc[:baseline_n]
    engine = OrpheusEngine().fit(baseline)
    bundle = engine.score(scenario.frame)
    metrics = evaluate(bundle.fused, bundle.anomaly_indices, scenario.anomaly_indices, len(scenario.frame))
    result = {
        "project": "ORPHEUS-NX",
        "baseline_samples": baseline_n,
        "threshold": bundle.threshold,
        "metrics": metrics,
        "top_alerts": sorted(
            [
                {"index": int(i), "score": float(bundle.fused[i])}
                for i in range(len(bundle.fused))
            ],
            key=lambda x: x["score"],
            reverse=True,
        )[:12],
    }
    text = json.dumps(result, indent=2)
    typer.echo(text)
    if output:
        output.write_text(text, encoding="utf-8")


@app.command()
def score_csv(
    baseline_csv: Path,
    target_csv: Path,
    config: Path | None = None,
) -> None:
    cfg = EngineConfig.from_json(config) if config else EngineConfig()
    baseline = pd.read_csv(baseline_csv)
    target = pd.read_csv(target_csv)
    engine = OrpheusEngine(cfg).fit(baseline)
    bundle = engine.score(target)
    for i in bundle.anomaly_indices:
        typer.echo(json.dumps(engine.explain_row(target, int(i))))

if __name__ == "__main__":
    app()
