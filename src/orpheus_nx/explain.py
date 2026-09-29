from __future__ import annotations

import numpy as np


def top_contributors(row: np.ndarray, center: np.ndarray, scale: np.ndarray, names: list[str], k: int = 3) -> list[str]:
    z = np.abs((row - center) / (scale + 1e-9))
    order = np.argsort(z)[::-1][:k]
    return [names[i] for i in order]
