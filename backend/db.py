from __future__ import annotations
from pathlib import Path
import sqlite3
from datetime import datetime, timezone
from uuid import uuid4

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "analytics.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS analyses (
    analysis_id TEXT PRIMARY KEY,
    score INTEGER NOT NULL,
    classification TEXT NOT NULL,
    password_length INTEGER NOT NULL,
    unique_character_ratio REAL NOT NULL,
    weakness_count INTEGER NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS findings (
    finding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id TEXT NOT NULL,
    finding_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY(analysis_id) REFERENCES analyses(analysis_id)
);
"""


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(SCHEMA)


def record_analysis(result: dict) -> str:
    init_db()
    analysis_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO analyses (analysis_id, score, classification, password_length, unique_character_ratio, weakness_count, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                analysis_id,
                result["score"],
                result["classification"],
                result["metrics"]["length"],
                result["metrics"]["unique_character_ratio"],
                len(result["findings"]),
                created_at,
            ),
        )
        for finding in result["findings"]:
            conn.execute(
                "INSERT INTO findings (analysis_id, finding_type, severity, description) VALUES (?, ?, ?, ?)",
                (analysis_id, finding["type"], finding["severity"], finding["description"]),
            )
    return analysis_id


def dashboard_stats() -> dict:
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
        avg_score = conn.execute("SELECT COALESCE(AVG(score), 0) FROM analyses").fetchone()[0]
        classifications = conn.execute("SELECT classification, COUNT(*) FROM analyses GROUP BY classification").fetchall()
        weaknesses = conn.execute("SELECT finding_type, COUNT(*) FROM findings GROUP BY finding_type ORDER BY COUNT(*) DESC").fetchall()
        length_distribution = conn.execute("SELECT password_length, COUNT(*) FROM analyses GROUP BY password_length ORDER BY password_length").fetchall()
        recent = conn.execute("SELECT analysis_id, score, classification, password_length, weakness_count, created_at FROM analyses ORDER BY created_at DESC LIMIT 20").fetchall()

    cls = {k: 0 for k in ["VERY WEAK", "WEAK", "MODERATE", "STRONG", "VERY STRONG"]}
    cls.update({row[0]: row[1] for row in classifications})
    return {
        "total_analyses": total,
        "average_score": round(avg_score, 2),
        "strength_distribution": cls,
        "weakness_frequency": [{"type": k, "count": v} for k, v in weaknesses],
        "length_distribution": [{"length": k, "count": v} for k, v in length_distribution],
        "recent_history": [
            {"analysis_id": r[0], "score": r[1], "classification": r[2], "password_length": r[3], "weakness_count": r[4], "created_at": r[5]}
            for r in recent
        ],
    }
