from database import get_conn, init_db
from datetime import datetime
from notification import create_notification


def send_message(sender, receiver, content):
    init_db()
    conn = get_conn()
    cur = conn.cursor()

    # insert the message
    cur.execute(
        """
        INSERT INTO messages (username, receiver, content)
        VALUES (?, ?, ?);
        """,
        (sender, receiver, content)
    )
    conn.commit()
    conn.close()

    # create notification for receiver
    create_notification(
        username=receiver,
        notif_type="new_message",
        from_user=sender,
        content_preview=content[:50]  # only first 50 chars
    )

    print("Message sent successfully!")


def get_unread_count(username):
    """
    Return how many unread messages this user has in total.
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*) AS c
        FROM messages
        WHERE receiver = ?
          AND read = 0;
        """,
        (username,)
    )
    row = cur.fetchone()
    conn.close()

    return row["c"] if row else 0


def fetch_unread_messages(username):
    """
    Return a list of unread messages for this user,
    oldest first. Each row becomes a dict.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            id,
            username AS sender,
            receiver,
            content,
            read,
            timestamp
        FROM messages
        WHERE receiver = ?
          AND read = 0
        ORDER BY timestamp ASC;
        """,
        (username,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_unread_as_read(username):
    """
    Mark ALL unread messages for this user as read.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE messages
        SET read = 1
        WHERE receiver = ?
          AND read = 0;
        """,
        (username,),
    )
    conn.commit()
    conn.close()


def view_conversation(user_a, user_b, *, mark_read_for=None):
    """
    Return all messages between user_a and user_b (both directions),
    sorted by time.

    If mark_read_for is provided (ex: the viewer username),
    we will ALSO mark any incoming messages to that viewer as read.
    """
    conn = get_conn()
    cur = conn.cursor()

    # get the full conversation both ways
    cur.execute(
        """
        SELECT
            id,
            username AS sender,
            receiver,
            content,
            read,
            timestamp
        FROM messages
        WHERE (username = ? AND receiver = ?)
           OR (username = ? AND receiver = ?)
        ORDER BY datetime(timestamp) ASC;
        """,
        (user_a, user_b, user_b, user_a)
    )
    rows = cur.fetchall()

    # if we know who is viewing, mark messages they RECEIVED as read
    if mark_read_for:
        cur.execute(
            """
            UPDATE messages
            SET read = 1
            WHERE receiver = ?
              AND read = 0
              AND username = ?;
            """,
            (mark_read_for, user_b)
        )
        conn.commit()

    conn.close()

    return [dict(r) for r in rows]
