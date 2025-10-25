from database import get_conn, init_db

def create_notification(username: str, notif_type: str, from_user: str, content_preview: str):
    """
    Add a new notification for 'username'.
    notif_type could be 'new_message', 'match', etc.
    """
    init_db()
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO notifications (username, type, from_user, content_preview, seen)
        VALUES (?, ?, ?, ?, 0);
        """,
        (username, notif_type, from_user, content_preview)
    )
    conn.commit()
    conn.close()


def get_notifications(username: str):
    """
    Return all notifications for this user, newest first.
    Each notification is turned into a dict for easy printing.
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, type, from_user, content_preview, created_at, seen
        FROM notifications
        WHERE username = ?
        ORDER BY created_at DESC;
        """,
        (username,)
    )
    rows = cursor.fetchall()
    conn.close()

    notifications = []
    for row in rows:
        notifications.append({
            "id": row["id"],
            "type": row["type"],
            "from_user": row["from_user"],
            "preview": row["content_preview"],
            "time": row["created_at"],
            "seen": bool(row["seen"]),
        })
    return notifications


def mark_all_seen(username: str):
    """
    Mark ALL notifications for this user as seen.
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE notifications
        SET seen = 1
        WHERE username = ?;
        """,
        (username,)
    )
    conn.commit()
    conn.close()
