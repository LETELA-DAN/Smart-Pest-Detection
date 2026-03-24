import sqlite3
from datetime import datetime

DB_PATH = "smart_pest.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Table for storing every SMS exchange
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT,
            diagnosis TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def log_message(sender, message, diagnosis):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (sender, message, diagnosis, timestamp) VALUES (?, ?, ?, ?)",
        (sender, message, diagnosis, datetime.now())
    )
    conn.commit()
    conn.close()