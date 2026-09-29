from pathlib import Path
import typer
from orpheus_nx.data.synthetic import generate_critical_grid


def main(output: Path = Path("synthetic_grid.csv"), steps: int = 1500, nodes: int = 12, seed: int = 42):
    scenario = generate_critical_grid(steps, nodes, seed=seed)
    scenario.frame.to_csv(output, index=False)
    typer.echo(f"wrote {len(scenario.frame)} rows to {output}")
    typer.echo(f"planted event starts: {scenario.anomaly_indices}")


if __name__ == "__main__":
    typer.run(main)
