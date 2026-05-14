import sqlite3
import os

def init_db(db_path: str):
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

def insert_log(name: str, db_path: str = None):
    db_path = db_path or os.environ.get('DB_PATH', 'equipment_log.db')
    with sqlite3.connect(db_path) as conn:
        conn.execute("INSERT INTO logs (name) VALUES (?)", (name,))

def get_all_logs(db_path: str = None):
    db_path = db_path or os.environ.get('DB_PATH', 'equipment_log.db')
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT name, recorded_at FROM logs ORDER BY id DESC")
        return cursor.fetchall()