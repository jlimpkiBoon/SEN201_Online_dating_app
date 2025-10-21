
from database import get_conn
from typing import Dict
import sqlite3


def create_note(username, about_user, content):
    """Create a new note about another user."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO notes (username, about_user, content)
        VALUES (?, ?, ?);
        """,
        (username, about_user, content),
    )
    conn.commit()
    conn.close()

    return

def get_notes(username):
    """Get all notes written by the current account."""

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, about_user, content, timestamp
        FROM notes
        WHERE username = ?
        ORDER BY timestamp DESC;
        """,
        (username,),
    )
    rows = cur.fetchall()
    conn.close()

    notes = [dict(row) for row in rows]

    print("\n")

    if not notes:
        print("There is no note.")
    else:
        for n in notes:
            print(f"Account: {n['about_user']}")
            print(f"Note: {n['content']}")
            print(f"Date: {n['timestamp']}")
            print("\n")

    return notes

def get_notes_by_user(username, about_user):
    """Get notes wriiten about a specific user."""

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, about_user, content, timestamp
        FROM notes
        WHERE username = ? AND about_user = ?
        ORDER BY timestamp DESC;
        """,
        (username, about_user),
    )
    rows = cur.fetchall()
    conn.close()

    notes = [dict(row) for row in rows]

    print("\n")

    if not notes:
        print("There is no note.")
    else:
        for n in notes:
            print(f"Account: {n['about_user']}")
            print(f"Note: {n['content']}")
            print(f"Date: {n['timestamp']}")
            print("\n")

    return notes