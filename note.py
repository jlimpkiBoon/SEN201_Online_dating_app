# file: notes.py
# purpose: Manage user-created notes in the database — including creation, retrieval, and user-specific queries.
# author: Ryuki
# date: 2025-09-29

from database import get_conn
from typing import Dict
import sqlite3

def create_note(username, about_user, content):
    """
    Create a new note about another user.

    Args:
        username (str): The username of the person creating the note.
        about_user (str): The username of the person the note is about.
        content (str): The note content.

    Returns: None
    """
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
    """
    Retrieve all notes written by a specific user.

    Args:
        username (str): The username whose notes to retrieve.

    Returns:
        List[Dict]: A list of dictionaries, each representing a note.
    """
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
    """
    Retrieve all notes written by a specific user about another specific user.

    Args:
        username (str): The username who wrote the notes.
        about_user (str): The username about whom the notes were written.

    Returns:
        List[Dict]: A list of dictionaries, each representing a note.
    """
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