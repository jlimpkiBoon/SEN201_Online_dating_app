import sqlite3
from database import get_conn, init_db
from datetime import datetime

def send_message(sender, receiver, content):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute
    (
        "INSERT INTO messages (username, receiver, content) VALUES (?, ?, ?);",
        (sender, receiver, content)
    )
    conn.commit()
    conn.close()
    print("Message sent successfully!")

def view_messages(sender, receiver):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute
    (
        "SELECT * FROM messages WHERE (username = ? AND receiver = ?) ORDER BY timestamp;",
        (sender, receiver)
    )
    messages = cur.fetchall()
    conn.close()
    return messages  