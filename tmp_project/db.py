import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "equipment_log.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

def insert_log(name: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO logs (name) VALUES (?)", (name,))

def get_all_logs():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT name, recorded_at FROM logs ORDER BY id DESC")
        return cursor.fetchall()