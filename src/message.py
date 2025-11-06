# file: message.py
# purpose: Manage user-to-user messaging, including sending, reading, and viewing message history
# author: Pepper & Thiri
# date: 2025-09-29

from database import get_conn, init_db
from datetime import datetime

def send_message(sender, receiver, content):
    """
    Send a message from one user to another and store it in the database.

    Args:
        sender (str): Username of the message sender.
        receiver (str): Username of the message receiver.
        content (str): The message text to be sent.

    Returns: None
    """
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
    """
    Retrieve the count of unread messages for a given user.

    Args:
        username (str): Username of the message receiver.

    Returns:
        int: The number of unread messages for the user.
    """
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
    """
    Fetch all unread messages for a specific user, sorted by timestamp.

    Args:
        username (str): Username of the message receiver.

    Returns:
        list[dict]: A list of unread messages with sender, content, and timestamp.
    """
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
    """
    Mark all unread messages for a given user as read.

    Args:
        username (str): Username of the message receiver.

    Returns: None
    """
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
    Retrieve all messages exchanged between two users, sorted by time.
    Optionally, mark incoming messages as read for one of the users.

    Args:
        user_a (str): First user in the conversation.
        user_b (str): Second user in the conversation.
        mark_read_for (str, optional): Username for whom incoming messages will be marked as read.

    Returns:
        list[dict]: A list of messages (both directions) including sender, receiver, content, and timestamp.
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

def get_contacted_users(username):
    """
    Retrieve a list of all unique users that the given user has either
    sent messages to or received messages from.

    Args:
        username (str): The username of the current user.

    Returns:
        list[str]: A list of distinct usernames that have interacted with the user.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT DISTINCT other_user FROM (
            SELECT receiver AS other_user
            FROM messages
            WHERE username = ?
            UNION
            SELECT username AS other_user
            FROM messages
            WHERE receiver = ?
        )
        ORDER BY other_user COLLATE NOCASE;
        """,
        (username, username)
    )
    rows = cur.fetchall()
    conn.close()
    return [r["other_user"] for r in rows]
