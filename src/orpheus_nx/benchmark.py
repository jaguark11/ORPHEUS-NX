from __future__ import annotations

import numpy as np
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score


def evaluate(scores: np.ndarray, predicted_indices: np.ndarray, truth_indices: list[int], n: int) -> dict:
    truth = np.zeros(n, dtype=int)
    truth[np.asarray(truth_indices, dtype=int)] = 1
    pred = np.zeros(n, dtype=int)
    pred[np.asarray(predicted_indices, dtype=int)] = 1
    precision, recall, f1, _ = precision_recall_fscore_support(
        truth, pred, average="binary", zero_division=0
    )
    try:
        auc = roc_auc_score(truth, scores)
    except ValueError:
        auc = float("nan")
    return {
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "roc_auc": float(auc),
        "alerts": int(pred.sum()),
        "truth_events": int(truth.sum()),
    }
