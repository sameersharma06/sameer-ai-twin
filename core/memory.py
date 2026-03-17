import sqlite3
import datetime
import os

DB_PATH = "data/sameer_ai.db"

def _connect():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_logs (
            date       TEXT PRIMARY KEY,
            summary    TEXT,
            work_hours REAL DEFAULT 0
        )
    """)
    conn.commit()
    return conn

def save_log(summary: str, work_hours: float = 0):
    conn = _connect()
    today = datetime.date.today().isoformat()
    conn.execute(
        "INSERT OR REPLACE INTO daily_logs (date, summary, work_hours) VALUES (?,?,?)",
        (today, summary, work_hours)
    )
    conn.commit()
    conn.close()

def get_recent_logs(days: int = 7):
    conn = _connect()
    rows = conn.execute(
        "SELECT date, summary, work_hours FROM daily_logs "
        "ORDER BY date DESC LIMIT ?", (days,)
    ).fetchall()
    conn.close()
    return rows