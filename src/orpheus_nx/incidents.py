from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class Incident:
    start: int
    end: int
    peak_index: int
    peak_score: float
    mean_score: float
    duration: int


def group_alerts(scores: np.ndarray, threshold: float, max_gap: int = 2) -> list[Incident]:
    """Collapse point alerts into operator-friendly incident intervals."""
    scores = np.asarray(scores, dtype=float)
    idx = np.flatnonzero(scores >= threshold)
    if len(idx) == 0:
        return []
    groups: list[list[int]] = [[int(idx[0])]]
    for i in idx[1:]:
        if int(i) - groups[-1][-1] <= max_gap + 1:
            groups[-1].append(int(i))
        else:
            groups.append([int(i)])
    out = []
    for g in groups:
        segment = scores[g[0] : g[-1] + 1]
        peak_local = int(np.argmax(segment))
        out.append(
            Incident(
                start=g[0],
                end=g[-1],
                peak_index=g[0] + peak_local,
                peak_score=float(segment[peak_local]),
                mean_score=float(segment.mean()),
                duration=g[-1] - g[0] + 1,
            )
        )
    return out
