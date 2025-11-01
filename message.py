# message.py
from database import get_conn, init_db
from datetime import datetime

def send_message(sender, receiver, content):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (username, receiver, content) VALUES (?, ?, ?);",
        (sender, receiver, content)
    )
    conn.commit()
    conn.close()
    print("Message sent successfully!")

def get_unread_count(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) AS c FROM messages WHERE receiver = ? AND read = 0;",
        (username,)
    )
    row = cur.fetchone()
    conn.close()
    return row["c"] if row else 0

def fetch_unread_messages(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, username AS sender, receiver, content, read, timestamp
        FROM messages
        WHERE receiver = ? AND read = 0
        ORDER BY timestamp ASC;
        """,
        (username,)
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def mark_unread_as_read(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE messages SET read = 1 WHERE receiver = ? AND read = 0;",
        (username,)
    )
    conn.commit()
    conn.close()

def view_conversation(user_a, user_b, *, mark_read_for=None):
    """
    Return all messages between user_a and user_b (both directions),
    sorted by time. If mark_read_for is set (e.g., the viewer username),
    mark any incoming messages to that viewer as read.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, username AS sender, receiver, content, read, timestamp
        FROM messages
        WHERE (username = ? AND receiver = ?)
           OR (username = ? AND receiver = ?)
        ORDER BY datetime(timestamp) ASC;
        """,
        (user_a, user_b, user_b, user_a)
    )
    rows = cur.fetchall()

    if mark_read_for:
        cur.execute(
            """
            UPDATE messages
               SET read = 1
             WHERE receiver = ? AND read = 0
               AND username = ?;
            """,
            (mark_read_for, user_b)
        )
        conn.commit()

    conn.close()
    return [dict(r) for r in rows]