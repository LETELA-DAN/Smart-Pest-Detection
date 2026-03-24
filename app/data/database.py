import sqlite3
import datetime

def log_message(sender, message, diagnosis):
    conn = sqlite3.connect("smart_pest.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         sender TEXT, 
         message TEXT, 
         diagnosis TEXT, 
         timestamp DATETIME)
    """)
    cursor.execute("INSERT INTO logs (sender, message, diagnosis, timestamp) VALUES (?, ?, ?, ?)",
                   (sender, message, diagnosis, datetime.datetime.now()))
    conn.commit()
    conn.close()
