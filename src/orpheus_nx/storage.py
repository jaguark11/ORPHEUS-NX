from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable


SCHEMA = """
CREATE TABLE IF NOT EXISTS anomaly_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts DATETIME DEFAULT CURRENT_TIMESTAMP,
  source TEXT NOT NULL,
  score REAL NOT NULL,
  payload TEXT NOT NULL
);
"""


class EventStore:
    def __init__(self, path: str | Path = "orpheus_events.db"):
        self.path = str(path)
        with sqlite3.connect(self.path) as con:
            con.execute(SCHEMA)

    def append(self, source: str, score: float, payload: dict) -> int:
        with sqlite3.connect(self.path) as con:
            cur = con.execute(
                "INSERT INTO anomaly_events(source, score, payload) VALUES (?, ?, ?)",
                (source, float(score), json.dumps(payload, sort_keys=True)),
            )
            return int(cur.lastrowid)

    def latest(self, limit: int = 20) -> list[dict]:
        with sqlite3.connect(self.path) as con:
            rows = con.execute(
                "SELECT id, ts, source, score, payload FROM anomaly_events ORDER BY id DESC LIMIT ?",
                (int(limit),),
            ).fetchall()
        return [
            {"id": r[0], "ts": r[1], "source": r[2], "score": r[3], "payload": json.loads(r[4])}
            for r in rows
        ]
